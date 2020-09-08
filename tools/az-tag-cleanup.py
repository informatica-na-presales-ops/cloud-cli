import azure.common.credentials
import azure.mgmt.resource
import azure.mgmt.subscription
import os


def get_subscriptions(credentials: azure.common.credentials.ServicePrincipalCredentials):
    with azure.mgmt.subscription.SubscriptionClient(credentials) as client:
        yield from client.subscriptions.list()


def check_tags(resource):
    if resource.tags is None:
        resource.tags = {}
    for k in resource.tags.keys():
        if k in (' APPLICATIONENV', 'APPLCATIONROLE', 'APPLICATIOENV', 'BUSINESSUNIT\xa0', '\xa0BUSINESSUNIT'):
            print(resource.id)
            print(repr(k))


def main():
    credentials = azure.common.credentials.ServicePrincipalCredentials(client_id=os.getenv('AZ_CLIENT_ID'),
                                                                       secret=os.getenv('AZ_SECRET'),
                                                                       tenant=os.getenv('AZ_TENANT'))
    for sub in get_subscriptions(credentials):
        with azure.mgmt.resource.resources.ResourceManagementClient(credentials, sub.subscription_id) as client:
            for r in client.resources.list():
                check_tags(r)


if __name__ == '__main__':
    main()
