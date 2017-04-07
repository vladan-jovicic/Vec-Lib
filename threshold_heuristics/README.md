Usage:

bash gen_data.sh step filename

Generates a file contour_filename. Then

./threshold_heuristics contour_filename

Outputs best threshold to use.


gen_data.sh step file1 file2 ...
Files are considered to be in Vec-Lib/results/test-images/
Generate contour_file1.txt contour_file2.txt ..., which contains regular output of contourDetection with threshold from 0 to 99 (with step $step), each output is separated by "END $threshold" in the output file.

analyse.py is an example to use these data.
python analyse.py file1 file2 file3
Draws for each file, a graph with some data for each output, (some are commented), for instance, the number of curves, the longest curve with norm 1 or 2, or the sum of the length of all curves (again, in norm 1 and 2). To visualise better which curves can be significant, they are all normalize between 0 and 1.


