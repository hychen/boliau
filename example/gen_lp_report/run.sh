#!/bin/bash

# find all bugtasks of laika project.
boliau-lp-findbugtasks project laika > m1
# find all bugtasks of bzr project which status is in progress.
boliau-lp-findbugtasks project bzr --status 'In Progress' > m2
# put outputs of m1 and m2 to a list as the input of prepare_data.py
# the output of prepare_data.py is a 2-tuple (outputs of m1 and m2, today bugtasks status of m1 and m2)
boliau-arr-combine m1 m2 | ./prepare_data.py > m3
# use mako template to create a html.
# -- mvar option means to assign the result provied from a mission which should be a Python object and and used in mako directly.
# -- var optoin meaans to substitute by a string.
boliau-tpl-sub report_tpl.html --mvar btsdata m3 --var title "Test Report" --output report_result.html

# cleanup
rm m1
rm m2
rm m3
