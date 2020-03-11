# cloud-cli

A Docker image that includes both [AWS CLI][a] and [Azure CLI][b] tools

```sh
$ docker image pull docker.pkg.github.com/informatica-na-presales-ops/cloud-cli/cloud-cli
```

[a]: https://aws.amazon.com/cli/
[b]: https://docs.microsoft.com/en-us/cli/azure/?view=azure-cli-latest

## Available tags

* `latest` &rarr; `2020.2`  
  `awscli==1.18.19`, `azure-cli==2.2.0`
* `2020.1`  
  `awscli==1.16.314`, `azure-cli==2.0.79`
* `2019.6`  
  `awscli==1.16.309`, `azure-cli==2.0.78`
* `2019.5`  
  `awscli==1.16.287`, `azure-cli==2.0.76`
* `2019.4`  
  `awscli==1.16.272`, `azure-cli==2.0.76`

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
