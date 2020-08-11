#! /usr/bin/env bash

python -m demo_performance.even_decay &
python -m demo_performance.sdk_decay &

read -rn1