# logs

`scripts/run` writes the output of each tool run here, one file for each run, with a time stamp
in its name. Git keeps this folder and this README. Git ignores the log files, so nobody commits
one. `make clean-logs` deletes them.

A log lets you inspect a run afterwards. It holds the values that a check printed before it
asserted them. That is the purpose of print-before-assert.
