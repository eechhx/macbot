#!/bin/bash
################################################################################
#                              MDR1 init Script                                #
#                                                                              #
# A script for initing the bus for the motor driver network                    #
#                                                                              #
################################################################################
modprobe can
modprobe can-raw
modprobe slcan
slcand -s5 -S2000000 /dev/ttyUSB1 can0
sleep 1
ifconfig can0 up
echo " "
ifconfig can0
echo " "
echo "MDR1 Bus Init Finished"
