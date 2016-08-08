#!/bin/bash

if [ "_$@" != "_" ]; then
  extra_args="-a \"$@\""  
fi

unset HTTP_PROXY HTTPS_PROXY http_proxy https_proxy all_proxy no_proxy ftp_proxy

# trigger discovery
/usr/share/python/monasca-agent/bin/monasca-setup --monasca_url "$MONASCA_API_ENDPOINT_PROTOCOL_INTERNAL://$MONASCA_API_ENDPOINT_HOST_INTERNAL:$MONASCA_API_PORT_INTERNAL/v2.0" --keystone_url "$OS_AUTH_URL" --ca_file "$OS_CACERT" -u "$MONASCA_AGENT_USERNAME" -p "$MONASCA_AGENT_PASSWORD" --user_domain_name "$MONASCA_AGENT_USER_DOMAIN_NAME" --project_domain_name "$MONASCA_ADMIN_DOMAIN_NAME" --project_name "$MONASCA_ADMIN_PROJECT" --config_dir "/etc/monasca/agent" --log_dir "/var/log/monasca/agent" --dimensions "kubernetes.container_name:$KUBE_RC_NAME,kubernetes.pod_name:$KUBE_POD_NAME,kubernetes.node_ip:$KUBE_NODE_IP" --skip_detection_plugins system vcenter -s "monitoring" $extra_args
echo "Wait for agent to come up"
sleep 3
while [ ! -f "/var/tmp/monasca-agent-supervisord.pid" ]; do echo -n "."; sleep 1; done
echo " started"

echo "Agent configured - stop for reconfiguration"
service monasca-agent stop
sleep 3
while [ -f "/var/tmp/monasca-agent-supervisord.pid" ]; do echo -n "."; sleep 1; done
echo " stopped"

sed "s|hostname:.*|hostname: $KUBE_NODE_IP|" -i /etc/monasca/agent/agent.yaml
service monasca-agent start
