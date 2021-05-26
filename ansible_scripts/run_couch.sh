#!/bin/bash
#this sh allows the couch-playbook.yaml to launch 1 instance on the MRC
#of 50 GB volume each; as configured in the roles

whoami
date
. ./unimelb-comp90024-2021-grp-19-openrc.sh; ansible-playbook -i hosts --ask-become-pass  couch-playbook.yaml -v > couch_output.txt

