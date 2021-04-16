FROM python:3.9.4-alpine3.13

COPY requirements.txt /boto/requirements.txt
COPY tools /boto/tools

RUN /sbin/apk add --no-cache bash \
 && /usr/local/bin/pip install --no-cache-dir --requirement /boto/requirements.txt

ENV PS1='\n\[\033[1;36m\]\w\[\033[0m\] \$ ' \
    PYTHONUNBUFFERED='1' \
    TZ='Etc/UTC'

ENTRYPOINT ["/bin/bash"]
WORKDIR /boto/tools
