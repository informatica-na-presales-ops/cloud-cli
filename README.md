# cloud-cli

A Docker image that includes both [AWS CLI][a] and [Azure CLI][b] tools

[a]: https://aws.amazon.com/cli/
[b]: https://docs.microsoft.com/en-us/cli/azure/?view=azure-cli-latest

## Available tags

* `latest` &rarr; `2019.1`  
  `awscli==1.16.252`, `azure-cli==2.0.74`

## Usage

### AWS CLI

For the AWS CLI, set the following environment variables when running the container:

* `AWS_ACCESS_KEY_ID`
* `AWS_DEFAULT_REGION`
* `AWS_SECRET_ACCESS_KEY`

Alternatively, mount a volume at `/root/.aws`, then run `aws configure` inside the container to save authentication
information.

### Azure CLI

For the Azure CLI, after successfully using `az login`, authentication information is saved in the directory
`/root/.azure`. Mount a volume at this location to preserve the authentication information across container runs.
