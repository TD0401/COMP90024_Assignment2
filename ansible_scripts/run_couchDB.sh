#!/bin/bash
#this sh allows the couchDB-playbook.yaml to launch two instances on the MRC
#of 120 GB volume each; as configured in the roles

whoami
date
. ./unimelb-comp90024-2021-grp-19-openrc.sh; ansible-playbook --ask-become-pass couchDB-playbook.yaml > couch_output.txt
# N2VhYmYwYjIxNjFkZWI0
