#!/bin/bash -eu
export AWS_PROFILE="default"
export SLACK_HOOK_URL="https://hooks.slack.com/services/ABC123ABC/XYZ987XYZ/ABCDEFG1234567HIJKLMNOPQ"
export SLACK_MENTION_MEMBERS="ABCDEF123,ABCDEF456"

export AWS_SDK_LOAD_CONFIG=true
export STAGE=dev
sls deploy
unset AWS_SDK_LOAD_CONFIG
unset STAGE
unset AWS_PROFILE
unset SLACK_TOKEN
unset SLACK_CHANNEL

