#!/bin/bash
#this sh allows the harvester-playbook.yaml to launch one instance on the MRC
#vol: 50 GB volume each; installs docker and tweepy for running the harvester py file.

whoami
date
. ./unimelb-comp90024-2021-grp-19-openrc.sh; ansible-playbook -i hosts --ask-become-pass harvester-playbook.yaml -v  > harvester_out.txt


