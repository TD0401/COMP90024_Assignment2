#!/bin/bash
#this sh allows the frontend-playbook.yaml to launch 1 instance on the MRC
#of 50 GB volume each; as configured in the roles

whoami
date
. ./unimelb-comp90024-2021-grp-19-openrc.sh; ansible-playbook --ask-become-pass frontend-playbook.yaml > frontend_output.txt
# N2VhYmYwYjIxNjFkZWI0
