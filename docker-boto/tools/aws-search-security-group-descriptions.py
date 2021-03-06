"""
This tool will check all security groups in all regions for an AWS account, looking for text in rule descriptions
"""

import argparse
import boto3
import botocore.exceptions
import logging
import os
import sys

log = logging.getLogger(__name__)


class Settings:
    def __init__(self):
        self.log_format = os.getenv('LOG_FORMAT', '%(levelname)s [%(name)s] %(message)s')
        self.log_level = os.getenv('LOG_LEVEL', 'INFO')
        self.version = os.getenv('IMAGE_VERSION', 'unknown')


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('search_text')
    return parser.parse_args()


def get_available_regions():
    session = boto3.session.Session()
    return session.get_available_regions('ec2')


def search_rule_descriptions(region, sg, search_text: str):
    search_text = search_text.lower()
    for perm in sg.ip_permissions:
        for ip_range in perm.get('IpRanges'):
            description = ip_range.get('Description', '')
            if search_text in description.lower():
                cidr_ip = ip_range.get('CidrIp')
                log.info(f'{region} {sg.id} {sg.group_name} {cidr_ip} {description}')


def main():
    settings = Settings()
    logging.basicConfig(format=settings.log_format, level='DEBUG', stream=sys.stdout)
    log.debug(f'aws-search-security-group-descriptions {settings.version}')
    if not settings.log_level == 'DEBUG':
        log.debug(f'Changing log level to {settings.log_level}')
    logging.getLogger().setLevel(settings.log_level)

    args = parse_args()
    log.info(f'Searching security groups for {args.search_text!r}')
    for region in get_available_regions():
        ec2 = boto3.resource('ec2', region_name=region)
        try:
            for sg in ec2.security_groups.all():
                search_rule_descriptions(region, sg, args.search_text)
        except botocore.exceptions.ClientError:
            log.warning(f'Skipping region {region}')


if __name__ == '__main__':
    main()
