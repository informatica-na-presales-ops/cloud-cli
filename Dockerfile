FROM python:3.7.4-alpine3.10

ARG AWS_CLI_VERSION="1.16.252"
ARG AZURE_CLI_VERSION="2.0.74"

# This version combination currently produces the following error:

# Collecting colorama<=0.3.9,>=0.2.5 (from awscli==1.16.252)
# ERROR: azure-cli 2.0.74 has requirement colorama~=0.4.1, but you'll have colorama 0.3.9 which is incompatible.

# This is okay, because Colorama doesn't do anything on Linux

RUN /sbin/apk add --no-cache --virtual .deps gcc libffi-dev make musl-dev openssl-dev \
 && /sbin/apk add --no-cache bash ca-certificates curl jq openssh openssl \
 && /usr/local/bin/pip install --no-cache-dir "awscli==${AWS_CLI_VERSION}" "azure-cli==${AZURE_CLI_VERSION}" \
 && /sbin/apk del --no-cache .deps

ENV PS1="\n\[\033[1;36m\]\w\[\033[0m\] \$ " \
    PYTHONUNBUFERED="1" \
    IMAGE_VERSION="2019.1"

ENTRYPOINT ["/bin/bash"]

LABEL org.opencontainers.image.authors="William Jackson <wjackson@informatica.com>" \
      org.opencontainers.image.version="${IMAGE_VERSION}"
