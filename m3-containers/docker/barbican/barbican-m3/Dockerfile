FROM hub.global.cloud.sap/monsoon/ubuntu-source-openstack-base:stable-mitaka

MAINTAINER fabian.ruff@sap.com

RUN mkdir /etc/barbican

RUN git clone -c http.sslVerify=false --depth 1 --branch "stable/mitaka" https://github.com/openstack/barbican

RUN pip install -r barbican/requirements.txt

RUN cd /barbican && python setup.py install

RUN apt-get install -y python-psycopg2 postgresql-client && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
