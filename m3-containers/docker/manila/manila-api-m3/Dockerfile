FROM hub.global.cloud.sap/monsoon/ubuntu-source-manila-api:stable-mitaka
MAINTAINER marc.koderer@sap.com

RUN apt-get update -y

RUN cd /manila; git fetch; git reset --hard origin/mitaka/hpb-support

RUN /var/lib/kolla/venv/bin/pip --no-cache-dir install --upgrade /manila
