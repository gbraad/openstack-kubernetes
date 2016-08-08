FROM hub.global.cloud.sap/monsoon/ubuntu-source-horizon:stable-mitaka
MAINTAINER andrew.battye@sap.com

RUN git clone -c http.sslVerify=false --depth 1 --branch "stable/mitaka" https://github.com/openstack/manila-ui.git

RUN pip install -e /manila-ui/

RUN cp ../manila-ui/manila_ui/enabled/_90_manila_*.py /var/lib/kolla/venv/lib/python2.7/site-packages/openstack_dashboard/enabled/


RUN git clone -c http.sslVerify=false --depth 1 --branch "stable/mitaka" https://github.com/openstack/neutron-lbaas-dashboard.git

RUN cd /neutron-lbaas-dashboard && python setup.py install


RUN cp /neutron-lbaas-dashboard/neutron_lbaas_dashboard/enabled/_1481_project_ng_loadbalancersv2_panel.py /var/lib/kolla/venv/lib/python2.7/site-packages/openstack_dashboard/enabled/

RUN cd /neutron-lbaas-dashboard && chmod 700 manage.py && ./manage.py collectstatic --noinput

RUN git clone -c http.sslVerify=false --depth 1 --branch "stable/mitaka" https://github.com/openstack/designate-dashboard.git
RUN cd /designate-dashboard && python setup.py install
RUN cp /designate-dashboard/designatedashboard/enabled/_17*.py /var/lib/kolla/venv/lib/python2.7/site-packages/openstack_dashboard/enabled/

RUN apt-get install -y python-psycopg2 postgresql-client && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
