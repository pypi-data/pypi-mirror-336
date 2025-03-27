from proxmoxer import ResourceException

from ..proxmox import Proxmox
from ..util.exceptions import PVECLIMigrationCheckError


def check_vm_migrate(proxmox_api: Proxmox, vm: dict, dest_node: str) -> dict:
    try:
        migrate_check_result = proxmox_api.vm.migrate_check(node=vm['node'], vm_id=vm['vmid'], target=dest_node)
    except ResourceException as err:
        raise PVECLIMigrationCheckError(f'Can not migrate VM {vm["name"]} ({vm["vmid"]}): {err.content}') from err
    if migrate_check_result['local_disks']:
        local_disks_without_replication = [
            f'{disk["drivename"]} ({disk["volid"]})' for disk in migrate_check_result['local_disks'] if disk['replicate'] == 0
        ]
        local_disks_with_replication = [
            f'{disk["drivename"]} ({disk["volid"]})' for disk in migrate_check_result['local_disks'] if disk['replicate'] == 1
        ]
        if local_disks_without_replication:
            raise PVECLIMigrationCheckError(
                f'Can not migrate VM {vm["name"]} ({vm["vmid"]}) because of local disks'
                f' without replication: {", ".join(local_disks_without_replication)}.'
            )
        if local_disks_with_replication:
            replications = proxmox_api.vm.get_replications(node=vm['node'], vm_id=vm['vmid'])
            target_replication = [replication for replication in replications if replication['target'] == dest_node]
            if not target_replication:
                raise PVECLIMigrationCheckError(
                    f'Can not migrate VM {vm["name"]} ({vm["vmid"]}) because of disks have'
                    f' no replication to {dest_node}: {", ".join(local_disks_with_replication)}.'
                )
    if migrate_check_result['local_resources']:
        raise PVECLIMigrationCheckError(
            f'Can not migrate VM {vm["name"]} ({vm["vmid"]}) '
            f'gbecause of local resources {migrate_check_result["local_resources"]}.'
        )
    if vm['status'] == 'stopped' and dest_node not in migrate_check_result['allowed_nodes']:
        raise PVECLIMigrationCheckError(
            f'Can not migrate VM {vm["name"]} ({vm["vmid"]}). '
            f'Migration to {dest_node} is not allowed because of {migrate_check_result["not_allowed_nodes"][dest_node]}.'
        )
    return migrate_check_result
