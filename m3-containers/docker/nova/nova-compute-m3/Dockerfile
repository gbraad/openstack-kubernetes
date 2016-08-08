FROM hub.global.cloud.sap/monsoon/ubuntu-source-nova-compute:stable-mitaka
MAINTAINER andrew.battye@sap.com

RUN apt-get update -y

RUN /var/lib/kolla/venv/bin/pip --no-cache-dir install --upgrade -c requirements/upper-constraints.txt oslo.vmware

RUN apt-get install -y python-psycopg2 postgresql-client && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
