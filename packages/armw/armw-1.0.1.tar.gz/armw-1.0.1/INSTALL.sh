#!/bin/bash

printf 'Installing apt dependancies for ARMW...\n'
printf '=======================================\n'

sudo apt install -y \
	ros-noetic-ddynamic-reconfigure \
	ros-noetic-ddynamic-reconfigure-python
