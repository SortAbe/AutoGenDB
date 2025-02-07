#!/bin/bash

threads=$1
for((i = 0; i <= $threads; i++));do
	./fillnames.py $i $threads &
done
