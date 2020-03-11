import azure.common.credentials
import azure.mgmt.resource
import azure.mgmt.subscription
import os


def get_subscriptions(credentials: azure.common.credentials.ServicePrincipalCredentials):
    with azure.mgmt.subscription.SubscriptionClient(credentials) as client:
        yield from client.subscriptions.list()


def main():
    credentials = azure.common.credentials.ServicePrincipalCredentials(client_id=os.getenv('AZ_CLIENT_ID'),
                                                                       secret=os.getenv('AZ_SECRET'),
                                                                       tenant=os.getenv('AZ_TENANT'))
    tag_names = set()
    for sub in get_subscriptions(credentials):
        with azure.mgmt.resource.resources.ResourceManagementClient(credentials, sub.subscription_id) as client:
            tag_names.update(set([t.tag_name for t in client.tags.list()]))
    for tag_name in sorted(tag_names):
        print(repr(tag_name))


if __name__ == '__main__':
    main()
