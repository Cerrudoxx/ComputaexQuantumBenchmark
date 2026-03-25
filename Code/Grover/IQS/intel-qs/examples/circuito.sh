#!/bin/bash

echo -e "\n############################################################"
echo -e   "######## Launching ejemplo executable ###########"
echo -e   "############################################################\n"

input_file="circuito.exe"
pars="12"  # Adjust this based on your needs

echo -e "\n-------------------"
echo "executable = " $input_file
echo "parameter values = " $pars

./bin/$input_file $pars