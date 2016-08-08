Remove User from :

        docker/ceilometer/ceilometer-collector/Dockerfile.j2
        docker/ceilometer/ceilometer-central/Dockerfile.j2
        docker/ceilometer/ceilometer-api/Dockerfile.j2
        docker/ceilometer/ceilometer-base/Dockerfile.j2
        docker/ceilometer/ceilometer-compute/Dockerfile.j2
        docker/ceilometer/ceilometer-notification/Dockerfile.j2
	docker/cinder/cinder-api/Dockerfile.j2
	docker/cinder/cinder-scheduler/Dockerfile.j2
	docker/cinder/cinder-volume/Dockerfile.j2
	docker/glance/glance-api/Dockerfile.j2
	docker/glance/glance-registry/Dockerfile.j2
	docker/ironic/ironic-api/Dockerfile.j2
	docker/ironic/ironic-conductor/Dockerfile.j2
	docker/manila/manila-api/Dockerfile.j2
	docker/manila/manila-scheduler/Dockerfile.j2
	docker/manila/manila-share/Dockerfile.j2
	docker/neutron/neutron-dhcp-agent/Dockerfile.j2
	docker/neutron/neutron-l3-agent/Dockerfile.j2
	docker/neutron/neutron-metadata-agent/Dockerfile.j2
	docker/neutron/neutron-openvswitch-agent/Dockerfile.j2
	docker/neutron/neutron-server/Dockerfile.j2
	docker/nova/nova-api/Dockerfile.j2
	docker/nova/nova-compute/Dockerfile.j2
	docker/nova/nova-conductor/Dockerfile.j2
	docker/nova/nova-consoleauth/Dockerfile.j2
	docker/nova/nova-novncproxy/Dockerfile.j2
	docker/nova/nova-scheduler/Dockerfile.j2
	docker/nova/nova-spicehtml5proxy/Dockerfile.j2
	docker/mongodb/Dockerfile.j2

plus copy the SAP certs into the base image folder, so that we can add them via kolla header in the kolla-configuration Makefile
