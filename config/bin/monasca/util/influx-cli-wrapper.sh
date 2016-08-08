#!/bin/bash

MONASCA_INFLUX_COMMAND='/usr/bin/influx'

$MONASCA_INFLUX_COMMAND -username mon_api -password $MONASCA_INFLUXDB_MONAPI_PASSWORD -database mon -execute "$*"
