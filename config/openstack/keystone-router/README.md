# Keystone-Router Kubernetes Setup

First create the redis database within the chosen namespace as described under `specs/redis/README.md`

Assuming you checked out the `monsoon/monsoon-kube-secrets` repository next to this one and your current working-directory is the same as this file,
create the keystone-router with the following command sequence:

```bash
export CONTEXT=<context> NAMESPACE=keystone-router
export CERT_DIR=../../../../openstack-kube-secrets/clusters/$CONTEXT/certs
function k8ctl() {  http_proxy= https_proxy= kubectl --context=$CONTEXT --namespace=$NAMESPACE "$@" ; }

k8ctl create secret generic certificates --from-file=identity.chained.crt=$CERT_DIR/identity.$CONTEXT.cloud.sap.pem --from-file=identity.key=$CERT_DIR/identity.$CONTEXT.cloud.sap.key
k8ctl create -f keystone-router-config-$CONTEXT.yaml
k8ctl create -f keystone-router-rc.yaml
k8ctl create -f keystone-router-sv-$CONTEXT.yaml
```
