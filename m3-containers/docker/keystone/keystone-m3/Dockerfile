FROM hub.global.cloud.sap/monsoon/ubuntu-source-keystone:stable-mitaka
MAINTAINER rudolf.vriend@sap.com

# this should come from kolla base. fixes the libldap2-dev libsasl2-dev install issues
RUN apt-get update && apt-get -y install --no-install-recommends apt-transport-https ca-certificates

# apply cherry-picked patches
COPY patches/*.patch /tmp/
RUN cd /keystone && \
    for patch in /tmp/*.patch; do \
     patch -p1 < "$patch"; \
    done
RUN rm -f /tmp/*.patch

RUN apt-get install -y python-dev libldap2-dev libsasl2-dev libssl-dev && apt-get clean
#RUN cd /keystone && /var/lib/kolla/venv/bin/pip --no-cache-dir install -e ".[memcache,ldap]" wtf: ldap not pinned
RUN cd /keystone && /var/lib/kolla/venv/bin/pip --no-cache-dir install "python-memcached>=1.56"
RUN cd /keystone && /var/lib/kolla/venv/bin/pip --no-cache-dir install "python-ldap==2.4.25"
RUN cd /keystone && /var/lib/kolla/venv/bin/pip --no-cache-dir install "ldappool>=1.0:python_version=='2.7'"

# install keystone-extensions & middleware
RUN cd /keystone && /var/lib/kolla/venv/bin/pip --no-cache-dir install git+https://github.wdf.sap.corp/monsoon/keystone-extensions.git
RUN cd /keystone && /var/lib/kolla/venv/bin/pip --no-cache-dir install git+https://github.com/sapcc/raven-python.git
RUN cd /keystone && /var/lib/kolla/venv/bin/pip --no-cache-dir install git+https://github.com/sapcc/openstack-ops-middleware.git
COPY keystone-paste.ini /etc/keystone/
RUN chown keystone /etc/keystone/keystone-paste.ini && chgrp keystone /etc/keystone/keystone-paste.ini

# install keystone-config-tools
RUN cd /keystone && /var/lib/kolla/venv/bin/pip --no-cache-dir install git+https://github.wdf.sap.corp/monsoon/keystone-config-tools.git

RUN apt-get install -y python-psycopg2 postgresql-client && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
