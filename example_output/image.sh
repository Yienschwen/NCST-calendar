#!/bin/bash

for var in *.svg
do
    rsvg-convert -f pdf -o $var.pdf $
done