FROM hub.global.cloud.sap/monsoon/ubuntu-source-designate-api:v2quota

MAINTAINER andrew.battye@sap.com

USER root

RUN apt-get -y update
RUN apt-get -y install python-mysqldb

# install the metrics middleware
RUN /var/lib/kolla/venv/bin/pip --no-cache-dir install git+https://github.com/sapcc/raven-python.git
RUN /var/lib/kolla/venv/bin/pip --no-cache-dir install git+https://github.com/sapcc/openstack-ops-middleware.git

# and the modified paste.ini that has the metrics middleware in it
COPY api-paste.ini /etc/designate/

RUN apt-get install -y python-psycopg2 postgresql-client && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
