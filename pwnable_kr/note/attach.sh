#!/bin/bash

p_id=$(pidof note)

# gcore -o ./note_core.bin $p_id
cat /proc/$p_id/maps

# gdb -p $p_id