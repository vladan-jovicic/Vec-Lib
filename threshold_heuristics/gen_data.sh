#!/bin/bash

pas=$1
shift
for file in "$@"
do
	rm contour_${file%.*}.txt
	for i in `seq 0 ${pas} 99`
	do
		../contour_detection/contourDetection ../results/test-images/${file} $i >> contour_${file%.*}.txt
		echo "END $i" >> contour_${file%.*}.txt
	done
	echo "${file} cases finished"
done