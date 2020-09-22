import argparse
import sqlite3

from azure.common.credentials import get_azure_cli_credentials
from azure.graphrbac import GraphRbacManagementClient


class Database:
    def __init__(self):
        self.cnx = sqlite3.connect(':memory:')
        self.cnx.row_factory = sqlite3.Row
        self.cnx.isolation_level = None
        self.cnx.execute('''
            create table groups (
                object_id text,
                display_name text,
                got_members text
            )
        ''')
        self.cnx.execute('''
            create table group_members (
                group_object_id text,
                member_object_id text,
                member_object_type text,
                member_display_name text
            )
        ''')

    def get_groups(self):
        sql = '''
            select object_id, display_name from groups
        '''
        cur = self.cnx.execute(sql)
        return cur.fetchall()

    def get_members(self, group_object_id):
        sql = '''
            select member_object_id, member_object_type, member_display_name from group_members
            where group_object_id = :group_object_id
        '''
        params = {
            'group_object_id': group_object_id
        }
        cur = self.cnx.execute(sql, params)
        return cur.fetchall()

    def add_group(self, object_id, display_name):
        print(f'Adding a group: {display_name}')
        sql = '''
            insert into groups (object_id, display_name, got_members) values (:object_id, :display_name, 'false')
        '''
        params = {
            'object_id': object_id,
            'display_name': display_name
        }
        self.cnx.execute(sql, params)

    def group_exists(self, object_id):
        sql = '''
            select object_id from groups where object_id = :object_id
        '''
        params = {
            'object_id': object_id
        }
        cur = self.cnx.execute(sql, params)
        return cur.fetchone() is not None

    def add_member(self, params):
        sql = '''
            insert into group_members (group_object_id, member_object_id, member_object_type, member_display_name)
            values (:group_object_id, :member_object_id, :member_object_type, :member_display_name)
        '''
        self.cnx.execute(sql, params)

    def close_group(self, object_id):
        sql = '''
            update groups set got_members = 'true'
            where object_id = :object_id
        '''
        params = {
            'object_id': object_id
        }
        self.cnx.execute(sql, params)

    def get_group_to_load(self):
        sql = '''
            select object_id, display_name from groups where got_members = 'false'
        '''
        cur = self.cnx.execute(sql)
        return cur.fetchone()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('group_name')
    return parser.parse_args()


def get_az_credentials():
    credentials, _, tenant = get_azure_cli_credentials(resource='https://graph.windows.net', with_tenant=True)
    return credentials, tenant


def get_az_client():
    return GraphRbacManagementClient(*get_az_credentials())


def print_results(db):
    for group in db.get_groups():
        group_object_id = group['object_id']
        group_display_name = group['display_name']
        print(f'\n{group_display_name}')
        for member in db.get_members(group_object_id):
            member_object_type = member['member_object_type'].lower()[0]
            member_display_name = member['member_display_name']
            print(f'  {member_object_type} / {member_display_name}')


def main():
    db = Database()
    args = parse_args()
    client = get_az_client()
    for group in client.groups.list():
        if group.display_name == args.group_name:
            db.add_group(group.object_id, group.display_name)
            break
    while True:
        group = db.get_group_to_load()
        if group is None:
            break
        group_object_id = group['object_id']
        display_name = group['display_name']
        print(f'Adding members for a group: {display_name}')
        for member in client.groups.get_group_members(group_object_id):
            db.add_member({
                'group_object_id': group_object_id,
                'member_object_id': member.object_id,
                'member_object_type': member.object_type,
                'member_display_name': member.display_name
            })
            if member.object_type == 'Group' and not db.group_exists(member.object_id):
                db.add_group(member.object_id, member.display_name)
        db.close_group(group_object_id)

    print_results(db)


if __name__ == '__main__':
    main()
