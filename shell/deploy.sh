#!/bin/bash -eu
export AWS_PROFILE="aiueo"
export SLACK_TOKEN="abcd-0000000000-000000000000-abcdefg123456789abcdefgh"
export SLACK_CHANNEL="#test-slack-channel"
export SLACK_MENTION_MEMBERS="ABCDEF123,ABCDEF456"

export AWS_SDK_LOAD_CONFIG=true
export STAGE=dev
sls deploy
unset AWS_SDK_LOAD_CONFIG
unset STAGE
unset AWS_PROFILE
unset SLACK_TOKEN
unset SLACK_CHANNEL
