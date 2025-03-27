from datetime import timedelta
from typing import Annotated

import typer
from rich.console import Console
from rich.progress import Progress
from rich.table import Column, Table

from .helper.check import check_vm_migrate
from .helper.conversion import b2gb
from .helper.ui import migration_task, progress_track_task, spinner_col, text_col, usage_bar
from .proxmox import Proxmox, ProxmoxVMNotFoundError
from .util.completion import node_complete, vm_complete
from .util.exceptions import PVECLIError
from .util.validators import node_validate

vm_cli = typer.Typer()


@vm_cli.callback()
def vm_callback(
    ctx: typer.Context,
    vm: Annotated[str, typer.Argument(..., autocompletion=vm_complete, help='VM Name or ID', show_default=False)],
):
    proxmox_api: Proxmox = ctx.obj['proxmox_api']

    try:
        vm_obj = proxmox_api.vm.get(vm)
    except ProxmoxVMNotFoundError:
        raise PVECLIError(f'VM {vm} was not found.') from None

    ctx.obj['vm'] = vm_obj


@vm_cli.command()
def status(ctx: typer.Context):
    proxmox_api: Proxmox = ctx.obj['proxmox_api']
    vm = ctx.obj['vm']

    vm_status = proxmox_api.vm.status(vm['node'], vm['vmid'])

    table_title = f'{vm["name"]} ({vm["vmid"]})'
    table = Table('Key', 'Value', title=table_title, min_width=len(table_title) + 2, show_header=False, show_lines=True)

    if vm_status['status'] == 'running':
        status_emoji = '🚀'
    elif vm_status['status'] == 'stopped':
        status_emoji = '🛑'
    else:
        status_emoji = '🤨'

    ips = Table.grid(Column(no_wrap=True), Column(no_wrap=True), padding=(0, 2))
    if vm_status['status'] == 'running':
        uptime = str(timedelta(seconds=vm_status['uptime']))
        if vm_status.get('agent') == 1:
            network_interfaces = proxmox_api.vm.agent.network_interfaces(vm['node'], vm['vmid'])
            for interface in network_interfaces:
                if interface['name'] == 'lo':
                    continue
                ifname = interface['name']
                for ip_addr in interface['ip-addresses']:
                    ips.add_row(ifname, f'{ip_addr["ip-address"]}/{ip_addr["prefix"]}')
                    ifname = ''
    else:
        uptime = ''
        ips.add_row('Guest Agent not running')

    cpu_description = '{percent}%' + f' of {vm_status["cpus"]} CPU(s)'
    mem = b2gb(vm_status['mem'], 2)
    maxmem = b2gb(vm_status['maxmem'], 2)
    mem_description = '{percent}%' + f' ({mem} of {maxmem}GiB)'

    table.add_row('Status', f'{status_emoji} {vm_status["status"]}')
    table.add_row('Uptime', uptime)
    table.add_row('Node', vm['node'])
    table.add_row('CPU Usage', usage_bar(vm_status['cpu'], description=cpu_description))
    table.add_row('Memory Usage', usage_bar(vm_status['mem'] / vm_status['maxmem'], description=mem_description))
    table.add_row('Bootdisk size', '{:.2f} GiB'.format(b2gb(vm_status['maxdisk'])))
    table.add_row('IPs', ips)

    console = Console()
    console.print(table)


@vm_cli.command()
def start(ctx: typer.Context):
    proxmox_api: Proxmox = ctx.obj['proxmox_api']
    vm = ctx.obj['vm']

    if vm['status'] == 'running':
        raise PVECLIError(f'VM {vm["name"]} ({vm["vmid"]}) is already running.')

    with Progress(spinner_col, text_col) as progress:
        task_id = progress.add_task(description=f'🚀 Starting VM {vm["name"]} ({vm["vmid"]})', total=1)
        start_task = proxmox_api.vm.start(vm['node'], vm['vmid'])

        progress_track_task(
            progress_obj=progress,
            progress_task_id=task_id,
            proxmox_api=proxmox_api,
            vm=vm,
            utid=start_task,
            success_msg=f'Started VM {vm["name"]} ({vm["vmid"]})',
            fail_msg=f'Failed starting VM {vm["name"]} ({vm["vmid"]})',
        )


@vm_cli.command()
def stop(
    ctx: typer.Context,
    force: Annotated[bool, typer.Option('--force', '-f', help='Make sure VM stops')] = False,
):
    proxmox_api: Proxmox = ctx.obj['proxmox_api']
    vm = ctx.obj['vm']

    if vm['status'] == 'stopped':
        raise PVECLIError(f'VM {vm["name"]} ({vm["vmid"]}) is already stopped.')

    with Progress(spinner_col, text_col) as progress:
        task_id = progress.add_task(description=f'🛑 Stopping VM {vm["name"]} ({vm["vmid"]})', total=1)
        stop_task = proxmox_api.vm.stop(vm['node'], vm['vmid'], force)

        progress_track_task(
            progress_obj=progress,
            progress_task_id=task_id,
            proxmox_api=proxmox_api,
            vm=vm,
            utid=stop_task,
            success_msg=f'Stopped VM {vm["name"]} ({vm["vmid"]})',
            fail_msg=f'Failed stopping VM {vm["name"]} ({vm["vmid"]})',
        )


@vm_cli.command()
def restart(ctx: typer.Context):
    proxmox_api: Proxmox = ctx.obj['proxmox_api']
    vm = ctx.obj['vm']

    with Progress(spinner_col, text_col) as progress:
        task_id = progress.add_task(description=f'🔁 Restarting VM {vm["name"]} ({vm["vmid"]})', total=1)
        restart_task = proxmox_api.vm.restart(vm['node'], vm['vmid'])

        progress_track_task(
            progress_obj=progress,
            progress_task_id=task_id,
            proxmox_api=proxmox_api,
            vm=vm,
            utid=restart_task,
            success_msg=f'Restarted VM {vm["name"]} ({vm["vmid"]})',
            fail_msg=f'Failed restarting VM {vm["name"]} ({vm["vmid"]})',
        )


@vm_cli.command()
def migrate(
    ctx: typer.Context,
    dest_node: Annotated[
        str,
        typer.Option('--dest', '-d', callback=node_validate, autocompletion=node_complete, help='Migration destination node'),
    ],
    online: Annotated[bool, typer.Option('--online/--offline', help='Online Migration')] = True,
    with_local_disks: Annotated[
        bool,
        typer.Option(
            '--with-local-disks/--without-local-disks',
            help='Migrate local disks (can take a long time without replicated disks)',
        ),
    ] = False,
):
    proxmox_api: Proxmox = ctx.obj['proxmox_api']
    vm = ctx.obj['vm']

    if dest_node == vm['node']:
        raise PVECLIError(f'VM {vm["name"]} ({vm["vmid"]}) is already on {dest_node}.')

    if vm['status'] == 'running' and not online:
        raise PVECLIError(f'Can not migrate running VM {vm["name"]} ({vm["vmid"]}) in offline mode.')

    migration_check_result = check_vm_migrate(proxmox_api=proxmox_api, vm=vm, dest_node=dest_node)
    if migration_check_result['local_disks']:
        with_local_disks = True

    with Progress(spinner_col, text_col) as progress:
        task_id = migration_task(progress=progress, vm=vm, dest_node=dest_node)
        migration_upid = proxmox_api.vm.migrate(
            vm['node'], vm['vmid'], target_node=dest_node, online=online, with_local_disks=with_local_disks
        )

        progress_track_task(
            progress_obj=progress,
            progress_task_id=task_id,
            proxmox_api=proxmox_api,
            vm=vm,
            utid=migration_upid,
            success_msg=f'Migrated {vm["name"]} ({vm["vmid"]}) from {vm["node"]} to {dest_node}',
            fail_msg=f'Failed migrating {vm["name"]} ({vm["vmid"]}) from {vm["node"]} to {dest_node}',
        )

