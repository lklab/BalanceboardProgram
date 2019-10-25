#!/bin/bash

gcc -c -fPIC keyboard_input.c -o keyboard_input.o
gcc keyboard_input.o -shared -o keyboard_input.so
