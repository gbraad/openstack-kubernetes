FROM hub.global.cloud.sap/monsoon/ubuntu-source-glance-api:stable-mitaka
MAINTAINER andrew.battye@sap.com

# install the metrics middleware
RUN /var/lib/kolla/venv/bin/pip --no-cache-dir install git+https://github.com/sapcc/raven-python.git
RUN /var/lib/kolla/venv/bin/pip --no-cache-dir install git+https://github.com/sapcc/openstack-ops-middleware.git

# and the modified paste.ini that has the metrics middleware in it
COPY glance-api-paste.ini /etc/glance/
