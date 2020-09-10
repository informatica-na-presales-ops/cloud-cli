import os
import pathlib
import yaml

from azure.common.credentials import get_azure_cli_credentials
from azure.graphrbac import GraphRbacManagementClient


def read_config(config_file):
    print(f'Reading config from {config_file}')
    with pathlib.Path(config_file).open() as f:
        data = yaml.safe_load(f)
    return data


def get_az_credentials():
    credentials, _, tenant = get_azure_cli_credentials(resource='https://graph.windows.net', with_tenant=True)
    return credentials, tenant


def get_az_client():
    return GraphRbacManagementClient(*get_az_credentials())


def main():
    config = read_config(os.getenv('CONFIG_FILE'))
    client = get_az_client()
    for group in client.groups.list():
        if group.display_name in config.get('groups'):
            print(f'\n{group.display_name}')
            for member in client.groups.get_group_members(group.object_id):
                print(f'  {member.object_type.lower()[0]} / {member.display_name}')


if __name__ == '__main__':
    main()
