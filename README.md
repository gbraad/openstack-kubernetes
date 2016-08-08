# Openstack Containers on Kubernetes

A set of Kubernetes specs, scripts and small templating framework to generate a set of
Kubernetes artifacts for deploying a scalable Openstack control plane. Where possible we
have split the control/data plane and run everything but DHCP on dedicated network or hypervisor hardware.

Its designed around the principle of 'Kuberenetes first'' and is designed to create an
Openstack 'release' comprising of a set of Kuberentes deployments and associated services/configmaps/secrets
that can be applied to deploy and maintain an Openstack deployment.

Its based on our current production deployments and includes support for the following Openstack components:

* Keystone
* Glance
* Nova (VMWare,KVM, Ironic compute)
* Ironic
* Neutron (Cisco L3, ACI and Arista L2 and F5 LBAASv2)
* Designate
* Cinder
* Manila
* Barbican
* Monasca

We use Postgres DBs and RabbitMQ messaging. Persistent is achaived with Kubernetes persistent volume/claims backed by either NFS or iSCSI

Our containers are based on standard Kolla built images, although we add to many containers (see /m3-containers) and all configuration and
start scripts, along with a few patches are injected via Kubernetes configmaps and secrets.

Its designed to support multiple regions/clusters but we extracted our region specific config (API endpoints, users, passwords) to protect
sensitive information an example can be found in /config/clusters/example-region. To generate a release for this region create a folder called
`openstack-kube-secrets` at the same level as this repo and copy the clusters folder over to it.


This is not designed to just work - you will need to adjust the deployment config, secrets and some of the specs to match your needs and build
or source your own Kolla images.

However, in principle, to deploy and update your Openstack just run `bin/os-deploy [your-namespace] example-region``.


Its anticpated that in teh very near future the crude bash/python deploy scripts will be replaced by a Go CLI.



