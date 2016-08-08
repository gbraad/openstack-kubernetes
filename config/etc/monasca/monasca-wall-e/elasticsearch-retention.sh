#!/bin/bash

unset http_proxy https_proxy all_proxy no_proxy ftp_proxy

export STDOUT_LOC=${STDOUT_LOC:-/proc/1/fd/1}  
export STDERR_LOC=${STDERR_LOC:-/proc/1/fd/2}

# set some env variables from the openstack env properly based on env
. /openstack-kube/openstack-kube/scripts/common

/usr/local/bin/curator --http_auth ${{cluster_config['monasca_elasticsearch_user']}}:${{cluster_config['monasca_elasticsearch_password']}} --host ${{cluster_config['monasca_elasticsearch_endpoint_host_internal']}} --port 9200 show indices --older-than ${{cluster_config['monasca_elasticsearch_data_retention']}} --time-unit days --timestring '%Y-%m-%d' --prefix logstash > ${STDOUT_LOC} 2> ${STDERR_LOC}
/usr/local/bin/curator --http_auth ${{cluster_config['monasca_elasticsearch_user']}}:${{cluster_config['monasca_elasticsearch_password']}} --host ${{cluster_config['monasca_elasticsearch_endpoint_host_internal']}} --port 9200 delete indices --older-than ${{cluster_config['monasca_elasticsearch_data_retention']}} --time-unit days --timestring '%Y-%m-%d' --prefix logstash > ${STDOUT_LOC} 2> ${STDERR_LOC}
/usr/local/bin/curator --http_auth ${{cluster_config['monasca_elasticsearch_user']}}:${{cluster_config['monasca_elasticsearch_password']}} --host ${{cluster_config['monasca_elasticsearch_endpoint_host_internal']}} --port 9200 show indices --older-than ${{cluster_config['monasca_elasticsearch_data_retention']}} --time-unit days --timestring '%Y.%m.%d' > ${STDOUT_LOC} 2> ${STDERR_LOC}
/usr/local/bin/curator --http_auth ${{cluster_config['monasca_elasticsearch_user']}}:${{cluster_config['monasca_elasticsearch_password']}} --host ${{cluster_config['monasca_elasticsearch_endpoint_host_internal']}} --port 9200 delete indices --older-than ${{cluster_config['monasca_elasticsearch_data_retention']}} --time-unit days --timestring '%Y.%m.%d'> ${STDOUT_LOC} 2> ${STDERR_LOC}
