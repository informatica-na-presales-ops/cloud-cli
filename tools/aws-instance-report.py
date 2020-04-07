import boto3
import botocore.exceptions
import csv
import logging
import os
import pathlib
import sys

from typing import Dict

log = logging.getLogger(__name__)


class Settings:
    def __init__(self):
        self.log_format = os.getenv('LOG_FORMAT', '%(levelname)s [%(name)s] %(message)s')
        self.log_level = os.getenv('LOG_LEVEL', 'INFO')
        self.output_file = pathlib.Path(os.getenv('OUTPUT_FILE', '/data/instances.csv')).resolve()
        self.version = os.getenv('IMAGE_VERSION', 'unknown')


def get_available_regions():
    session = boto3.session.Session()
    return session.get_available_regions('ec2')


def tag_list_to_dict(tag_list):
    if tag_list is None:
        return {}
    return {t.get('Key'): t.get('Value') for t in tag_list}


def get_instance_data(region, instance) -> Dict:
    tags = tag_list_to_dict(instance.tags)
    state_reason = instance.state_reason
    if state_reason is None:
        state_reason = {}
    return {
        'ami_launch_index': instance.ami_launch_index,
        'architecture': instance.architecture,
        'volumes': ' '.join([b.get('Ebs', {}).get('VolumeId') for b in instance.block_device_mappings]),
        'capacity_reservation_id': instance.capacity_reservation_id,
        'capacity_reservation_preference': instance.capacity_reservation_specification.get('CapacityReservationPreference'),
        'client_token': instance.client_token,
        'cpu_core_count': instance.cpu_options.get('CoreCount'),
        'cpu_threads_per_core': instance.cpu_options.get('ThreadsPerCore'),
        'ebs_optimized': instance.ebs_optimized,
        'ena_support': instance.ena_support,
        'hypervisor': instance.hypervisor,
        'image_id': instance.image_id,
        'instance_id': instance.instance_id,
        'instance_lifecycle': instance.instance_lifecycle,
        'instance_type': instance.instance_type,
        'kernel_id': instance.kernel_id,
        'key_name': instance.key_name,
        'launch_time': instance.launch_time,
        'platform': instance.platform,
        'private_dns_name': instance.private_dns_name,
        'private_ip_address': instance.private_ip_address,
        'public_dns_name': instance.public_dns_name,
        'public_ip_address': instance.public_ip_address,
        'state': instance.state.get('Name'),
        'state_reason': state_reason.get('Message'),
        'state_transition_reason': instance.state_transition_reason,
        'tag_NAME': tags.get('NAME'),
        'tag_OWNEREMAIL': tags.get('OWNEREMAIL'),
        'region': region
    }


def main():
    settings = Settings()
    logging.basicConfig(format=settings.log_format, level='DEBUG', stream=sys.stdout)
    log.debug(f'aws-instance-report {settings.version}')
    if not settings.log_level == 'DEBUG':
        log.debug(f'Changing log level to {settings.log_level}')
    logging.getLogger().setLevel(settings.log_level)

    log.info(f'Writing data to {settings.output_file}')

    csv_field_names = [
        'ami_launch_index', 'architecture', 'volumes', 'capacity_reservation_id', 'capacity_reservation_preference',
        'client_token', 'cpu_core_count', 'cpu_threads_per_core', 'ebs_optimized', 'ena_support', 'hypervisor',
        'image_id', 'instance_id', 'instance_lifecycle', 'instance_type', 'kernel_id', 'key_name', 'launch_time',
        'platform', 'private_dns_name', 'private_ip_address', 'public_dns_name', 'public_ip_address', 'state',
        'state_reason', 'state_transition_reason', 'tag_NAME', 'tag_OWNEREMAIL', 'region'
    ]

    with settings.output_file.open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=csv_field_names)
        writer.writeheader()
        for region in get_available_regions():
            ec2 = boto3.resource('ec2', region_name=region)
            try:
                for instance in ec2.instances.all():
                    writer.writerow(get_instance_data(region, instance))
            except botocore.exceptions.ClientError:
                log.warning(f'Skipping region {region}')


if __name__ == '__main__':
    main()
