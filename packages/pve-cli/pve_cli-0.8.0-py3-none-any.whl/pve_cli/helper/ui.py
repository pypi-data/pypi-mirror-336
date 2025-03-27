import time

from rich.bar import Bar
from rich.progress import Progress, SpinnerColumn, TaskID, TextColumn
from rich.table import Column, Table

from ..proxmox.api import Proxmox

spinner_col = SpinnerColumn(style='bold white')
text_col = TextColumn('[progress.description]{task.description}')


def progress_track_task(
    progress_obj: Progress,
    progress_task_id: TaskID,
    proxmox_api: Proxmox,
    vm: dict,
    utid: str,
    success_msg: str,
    fail_msg: str,
    check_interval: int = 1,
):
    status = proxmox_api.node.task_status(vm['node'], utid)
    while status.get('status') != 'stopped':
        time.sleep(check_interval)
        status = proxmox_api.node.task_status(vm['node'], utid)

    if status['exitstatus'] == 'OK':
        progress_obj.update(progress_task_id, completed=1, refresh=True, description=f'[green]✅ {success_msg}')
    else:
        progress_obj.update(
            progress_task_id, completed=1, refresh=True, description=f'[red]❌ {fail_msg}: {status["exitstatus"]}'
        )


def usage_bar(usage: float, description: str = '{percent}%', percentage_precision: int = 0, max_width: int = 30) -> Table:
    percent = int(round(usage * 100, percentage_precision))
    field = Table.grid(
        Column(no_wrap=True, max_width=max_width - 5), Column(no_wrap=True, min_width=5, justify='right'), padding=(0, 1)
    )
    field.add_row(
        Bar(size=1.0, begin=0.0, end=usage, color='bright_white', bgcolor='grey15'), description.format(percent=percent)
    )
    return field


def migration_task(progress: Progress, vm: dict, dest_node: str) -> TaskID:
    return progress.add_task(
        description=f'[white]🚚 Migrating {vm["name"]} ({vm["vmid"]}) from {vm["node"]} to {dest_node}...', total=1
    )
