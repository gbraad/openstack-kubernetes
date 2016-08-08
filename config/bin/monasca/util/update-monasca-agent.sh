#!/bin/bash

if [ "$1" == "--help" ] || [ "$1" == "" ]; then
  echo ""
  echo "Usage: update-monasca-agent.sh <version-prefix>, e.g. update-monasca.agent.sh 1.1.21"
  exit 1
fi

if [ "$MONASCA_REPO_ROOT" == "" ]; then
  echo ""
  echo "INFO: MONASCA_REPO_ROOT not set - setting it to the default value"
  echo ""
  # Ensure that the read ACL is set as follows: .r:*,.rlistings
  export MONASCA_REPO_ROOT="https://objectstore.eu-de-1.cloud.sap/v1/AUTH_p-7496766f1/monasca-apt"
fi

echo "downloading the latest deb files"
rm monasca-agent*.deb
for deb in $(curl --silent -X GET ${MONASCA_REPO_ROOT} | grep "monasca-agent_$1" | grep '.deb'; do
  echo "- discovered $deb"
  outfile=$(echo $deb | sed 's|\([a-zA-Z-]\+\)_\([0-9\.]\+\)\-\([0-9a-f-]\+\)\(.*\)|\1_\2\4|')  # cut off build-id to get short version and make latest build prevail
  curl --silent -o $outfile -X GET ${MONASCA_REPO_ROOT}/$deb
  RC=$?
  if [ $RC != 0 ]; then
    echo "*** ERROR downloading $deb"
  fi
done

# install new version over the previous one (this will keep the settings)
service monasca-agent stop
dpkg -i $outfile

