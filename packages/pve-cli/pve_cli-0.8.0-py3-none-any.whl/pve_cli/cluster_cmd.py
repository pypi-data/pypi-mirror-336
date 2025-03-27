import json
import tempfile
import time
from datetime import timedelta
from typing import Annotated

import typer
from rich import print as rprint
from rich.console import Console
from rich.progress import Progress, TaskID, TimeElapsedColumn
from rich.table import Table

from .helper.check import check_vm_migrate
from .helper.conversion import b2gb
from .helper.ui import migration_task, spinner_col, text_col, usage_bar
from .proxmox import Proxmox
from .util.exceptions import PVECLIError, PVECLIMigrationCheckError

cluster_cli = typer.Typer()
vm_mapping_cli = typer.Typer()
cluster_cli.add_typer(vm_mapping_cli, name='vm-mapping')


@cluster_cli.callback()
def cluster_callback(
    ctx: typer.Context,
    parallel: Annotated[
        int, typer.Option('--parallel', '-p', show_default=True, help='Sets how many migrations should be run in parallel')
    ] = 4,
):
    proxmox_api: Proxmox = ctx.obj['proxmox_api']
    ctx.obj['nodes'] = proxmox_api.node.list_()
    ctx.obj['cluster'] = proxmox_api.cluster.info()
    ctx.obj['parallel_migrations'] = parallel


@cluster_cli.command()
def reboot(
    ctx: typer.Context,
):
    proxmox_api: Proxmox = ctx.obj['proxmox_api']
    nodes = ctx.obj['nodes']
    parallel_migrations = ctx.obj['parallel_migrations']
    vms_all = proxmox_api.vm.list_()
    vms_running = [vm for vm in vms_all if vm['status'] == 'running']

    node_migration_map = {nodes[i]['node']: nodes[i - 1]['node'] for i in range(len(nodes))}
    migration_blockers = []
    with_local_disks = False
    for vm in vms_running:
        try:
            migration_check_result = check_vm_migrate(proxmox_api=proxmox_api, vm=vm, dest_node=node_migration_map[vm['node']])
            if migration_check_result['local_disks']:
                with_local_disks = True
        except PVECLIMigrationCheckError as err:
            migration_blockers.append(err)

    if migration_blockers:
        raise PVECLIError(
            'Can not automatically reboot cluster because running VM(s) are not online-migration ready:\n'
            + '\n'.join([blocker.message for blocker in migration_blockers])
        )

    for node_data in nodes:
        node = node_data['node']
        tmp_node = node_migration_map[node]
        node_running_vms = [vm['vmid'] for vm in vms_running if vm['node'] == node]

        migration_failed = migrate_vms(
            api=proxmox_api,
            dest_node=tmp_node,
            vmid_list=node_running_vms,
            parallel_migrations=parallel_migrations,
            with_local_disks=with_local_disks,
        )
        if migration_failed:
            with tempfile.NamedTemporaryFile(mode='wt', delete=False, prefix='pve-cli') as tmpfile:
                json.dump(vms_all, tmpfile, indent=2)
                raise PVECLIError(
                    f'Migration failed. Aborting cluster reboot. Initial VM-Mapping has been saved to {tmpfile.name}'
                )

        with Progress(spinner_col, TimeElapsedColumn(), text_col) as progress:
            task_id = progress.add_task(description=f'[white]Rebooting {node}...', total=1)
            proxmox_api.node.reboot(node)
            # wait for node to go offline
            while proxmox_api.node.get(node)['status'] == 'online':
                time.sleep(10)  # it is not necessary to check this to often, check node status every 10 seconds should be fine
            # wait for node to come online
            while proxmox_api.node.get(node)['status'] != 'online':
                time.sleep(10)  # it is not necessary to check this to often, check node status every 10 seconds should be fine
            progress.update(task_id, completed=1, refresh=True, description=f'[green]Done: Rebooted {node}')

        migration_failed = migrate_vms(
            api=proxmox_api,
            dest_node=node,
            vmid_list=node_running_vms,
            parallel_migrations=parallel_migrations,
            with_local_disks=with_local_disks,
        )
        if migration_failed:
            with tempfile.NamedTemporaryFile(mode='wt', delete=False, prefix='pve-cli') as tmpfile:
                json.dump(vms_all, tmpfile, indent=2)
                raise PVECLIError(
                    f'Migration failed. Aborting cluster reboot. Initial VM-Mapping has been saved to {tmpfile.name}'
                )


@cluster_cli.command('list')
def list_(ctx: typer.Context):
    cluster = ctx.obj['cluster']
    nodes = ctx.obj['nodes']

    table = Table(title=f'Nodes in cluster {cluster["name"]}')
    table.add_column('Node')
    table.add_column('Status', justify='center')
    table.add_column('Cores', justify='right')
    table.add_column('CPU Usage')
    table.add_column('RAM')
    table.add_column('RAM Usage')
    table.add_column('Disk Usage')
    table.add_column('Uptime')

    for node in nodes:
        status = '🚀 online' if node['status'] == 'online' else f'💀 {node["status"]}'
        ram = int(b2gb(node['maxmem']))
        cpu_bar = usage_bar(node['cpu'])
        ram_bar = usage_bar(node['mem'] / node['maxmem'])
        disk_bar = usage_bar(node['disk'] / node['maxdisk'])

        table.add_row(
            node['node'],
            status,
            str(node['maxcpu']),
            cpu_bar,
            f'{ram} GiB',
            ram_bar,
            disk_bar,
            str(timedelta(seconds=node['uptime'])),
        )

    console = Console()
    console.print(table)


def check_migration_status(
    api: Proxmox, progress: Progress, dest_node: str, running_tasks_list: list, running_tasks: dict[str, tuple[dict, TaskID]]
) -> bool:
    failed = False
    for upid in running_tasks_list:
        vm, task_id = running_tasks[upid]
        status = api.node.task_status(vm['node'], upid)
        if status['status'] == 'stopped':
            if status['exitstatus'] == 'OK':
                progress.update(
                    task_id,
                    completed=1,
                    refresh=True,
                    description=f'[green]✅ Migrated {vm["name"]} ({vm["vmid"]}) from {vm["node"]} to {dest_node}',
                )
            else:
                progress.update(
                    task_id,
                    completed=1,
                    refresh=True,
                    description=f'[red]❌ Failed migrating {vm["name"]} ({vm["vmid"]}) '
                    f'from {vm["node"]} to {dest_node}: {status["exitstatus"]}',
                )
                failed = True
            running_tasks_list.remove(upid)
    return failed


def migrate_vms(
    api: Proxmox, dest_node: str, vmid_list: list[int], parallel_migrations: int = 4, with_local_disks: bool = False
) -> bool:
    migration_failed = False
    running_tasks: dict[str, tuple[dict, TaskID]] = {}
    running_tasks_list: list[str] = []
    vm_list_working_copy = vmid_list[:]  # copy list to not empty the actual list
    if parallel_migrations == 0:
        parallel_migrations = len(vm_list_working_copy)

    with Progress(spinner_col, text_col) as progress:
        while vm_list_working_copy:
            while len(running_tasks_list) < parallel_migrations and vm_list_working_copy:
                vm_id = vm_list_working_copy.pop()
                vm = api.vm.get(vm_id)
                upid = api.vm.migrate(
                    node=vm['node'], vm_id=vm['vmid'], target_node=dest_node, with_local_disks=with_local_disks
                )
                task_id = migration_task(progress, vm, dest_node)
                running_tasks[upid] = (vm, task_id)
                running_tasks_list.append(upid)

            time.sleep(3)  # it is not necessary to check this to often, check migration status every 3 seconds should be fine
            migration_failed = check_migration_status(
                api=api,
                progress=progress,
                dest_node=dest_node,
                running_tasks_list=running_tasks_list,
                running_tasks=running_tasks,
            )

        while running_tasks_list:
            time.sleep(3)  # it is not necessary to check this to often, check migration status every 3 seconds should be fine
            migration_failed = check_migration_status(
                api=api,
                progress=progress,
                dest_node=dest_node,
                running_tasks_list=running_tasks_list,
                running_tasks=running_tasks,
            )

    return migration_failed


@vm_mapping_cli.command('dump')
def mapping_dump(
    ctx: typer.Context,
    outfile: Annotated[typer.FileTextWrite, typer.Argument(help='JSON output filepath')],
):
    proxmox_api: Proxmox = ctx.obj['proxmox_api']
    vms = proxmox_api.vm.list_()

    result = {vm['vmid']: vm['node'] for vm in vms}
    json.dump(result, outfile, indent=2)


@vm_mapping_cli.command('restore')
def mapping_restore(
    ctx: typer.Context,
    infile: Annotated[typer.FileText, typer.Argument(help='JSON input file (created with dump-vms')],
    verbose: Annotated[bool, typer.Option('--verbose', '-v', help='Verbose output')] = False,
):
    proxmox_api: Proxmox = ctx.obj['proxmox_api']
    vms = proxmox_api.vm.list_()
    nodes = ctx.obj['nodes']
    parallel_migrations = ctx.obj['parallel_migrations']

    mapping = json.load(infile)

    migration_vms: dict[str, list[dict]] = {node['node']: [] for node in nodes}
    for vm in vms:
        try:
            wanted_node = mapping[str(vm['vmid'])]
        except KeyError:
            continue

        if wanted_node == vm['node']:
            if verbose:
                rprint(spinner_col.finished_text, f'[green]✅ VM {vm["name"]} ({vm["vmid"]}) is on node {wanted_node}')
        else:
            migration_vms[wanted_node].append(vm)

    for dest_node, vms_to_migrate in migration_vms.items():
        if vms_to_migrate:
            with_local_disks = False
            for vm in vms_to_migrate:
                migration_check_result = check_vm_migrate(proxmox_api=proxmox_api, dest_node=dest_node, vm=vm)
                if migration_check_result['local_disks']:
                    with_local_disks = True
            migrate_vms(
                api=proxmox_api,
                dest_node=dest_node,
                vmid_list=[vm['vmid'] for vm in vms_to_migrate],
                parallel_migrations=parallel_migrations,
                with_local_disks=with_local_disks,
            )
