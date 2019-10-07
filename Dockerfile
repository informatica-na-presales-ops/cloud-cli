FROM python:3.7.4-alpine3.10

ARG AWS_CLI_VERSION="1.16.254"
ARG AZURE_CLI_VERSION="2.0.74"

RUN /sbin/apk add --no-cache --virtual .deps gcc libffi-dev make musl-dev openssl-dev \
 && /sbin/apk add --no-cache bash ca-certificates curl jq openssh openssl \
 && /usr/local/bin/pip install --no-cache-dir "awscli==${AWS_CLI_VERSION}" "azure-cli==${AZURE_CLI_VERSION}" \
 && /sbin/apk del --no-cache .deps

ENV PS1="\n\[\033[1;36m\]\w\[\033[0m\] \$ " \
    PYTHONUNBUFERED="1" \
    IMAGE_VERSION="2019.2"

ENTRYPOINT ["/bin/bash"]

LABEL org.opencontainers.image.authors="William Jackson <wjackson@informatica.com>" \
      org.opencontainers.image.version="${IMAGE_VERSION}"
