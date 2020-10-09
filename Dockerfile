FROM python:3.9.0-alpine3.12

COPY requirements.txt /cloud-cli/requirements.txt

RUN /sbin/apk add --no-cache bash ca-certificates curl groff jq openssh openssl
RUN /usr/local/bin/pip install --no-cache-dir --requirement /cloud-cli/requirements.txt

ENV IMAGE_VERSION="2020.4" \
    PS1="\n\[\033[1;36m\]\w\[\033[0m\] \$ " \
    PYTHONUNBUFERED="1"

ENTRYPOINT ["/bin/bash"]

LABEL org.opencontainers.image.authors="William Jackson <wjackson@informatica.com>" \
      org.opencontainers.image.version="${IMAGE_VERSION}"
