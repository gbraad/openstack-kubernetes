FROM hub.global.cloud.sap/monsoon/ubuntu-source-neutron-base:stable-mitaka
MAINTAINER andrew.battye@sap.com

RUN /var/lib/kolla/venv/bin/pip --no-cache-dir install --upgrade -c requirements/upper-constraints.txt oslo.vmware # required by DVS driver
RUN pip install ncclient    # required by ASR L3 agent
RUN pip install ciscoconfparse    # required by ASR L3 agent
RUN pip install pyasn1_modules    # required by F5
RUN pip install jsonrpclib  #Required by Arista
RUN pip install hash-ring  #Required by  ACI

RUN git clone -c http.sslVerify=false --depth 1 https://github.wdf.sap.corp/monsoon/networking-dvs.git
RUN cd /networking-dvs && python setup.py install

RUN git clone -c http.sslVerify=false --depth 1 https://github.wdf.sap.corp/monsoon/networking-aci.git
RUN cd /networking-aci && python setup.py install

RUN cd /networking-aci && curl -k https://apic1.labx.mo.sap.corp/cobra/_downloads/acicobra-1.3_2f-py2.7.egg > acicobra.egg
RUN cd /networking-aci && curl -k https://apic1.labx.mo.sap.corp/cobra/_downloads/acimodel-1.3_2f-py2.7.egg > acimodel.egg

RUN cd /networking-aci &&  easy_install -Z acicobra.egg
RUN cd /networking-aci &&  easy_install -Z acimodel.egg


RUN git clone -c http.sslVerify=false --depth 1 https://github.wdf.sap.corp/monsoon/networking-asr.git
RUN cd /networking-asr && python setup.py install

RUN git clone -c http.sslVerify=false --depth 1 https://github.wdf.sap.corp/monsoon/networking-f5-ml2.git
RUN cd /networking-f5-ml2 && python setup.py install

RUN git clone -c http.sslVerify=false --depth 1 https://github.wdf.sap.corp/monsoon/networking-manila.git
RUN cd /networking-manila && python setup.py install


RUN git clone -c http.sslVerify=false --depth 1 https://github.wdf.sap.corp/monsoon/networking-arista.git
RUN cd /networking-arista && python setup.py install


# Cisco ASR
RUN pip install git+https://github.com/openstack/networking-cisco.git

# F5 LBAAS
RUN pip install git+https://github.com/F5Networks/neutron-lbaas@v8.0.1
RUN pip install git+https://github.com/F5Networks/f5-openstack-lbaasv2-driver@v8.0.3
RUN pip install git+https://github.com/F5Networks/f5-openstack-agent@v8.0.3

#RUN pip uninstall f5-sdk
#RUN pip install f5-sdk==0.1.7

# install the metrics middleware
RUN /var/lib/kolla/venv/bin/pip --no-cache-dir install git+https://github.com/sapcc/raven-python.git
RUN /var/lib/kolla/venv/bin/pip --no-cache-dir install git+https://github.com/sapcc/openstack-ops-middleware.git
COPY api-paste.ini /etc/neutron

RUN apt-get install -y python-psycopg2 postgresql-client && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
