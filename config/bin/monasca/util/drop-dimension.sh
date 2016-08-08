#!/bin/bash

. /openstack-kube/openstack-kube/scripts/monasca/common_start

if [ "$1" = "" ]; then
  echo "No dimension given"
  exit 1
else
  dim=$1
fi

echo "Dropping all series using dimension ${dim} from the database 'mon'"
echo "Press Ctr-C to cancel within 10 secs ..."

sleep 10

/usr/bin/influx -username mon_api -password $MONASCA_INFLUXDB_MONAPI_PASSWORD -database mon -execute "show measurements where ${dim} != ''" | tail -n +4 | xargs -I %arg% /usr/bin/influx -username mon_api -password $MONASCA_INFLUXDB_MONAPI_PASSWORD -database mon -execute "drop series from \"%arg%\" where ${dim} != ''"

