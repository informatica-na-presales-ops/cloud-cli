# cloud-cli

A Docker image that includes both [AWS CLI][a] and [Azure CLI][b] tools

```sh
$ docker image pull ghcr.io/informatica-na-presales-ops/cloud-cli
```

[a]: https://aws.amazon.com/cli/
[b]: https://docs.microsoft.com/en-us/cli/azure/?view=azure-cli-latest

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
