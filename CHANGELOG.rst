=========
Changelog
=========

0.2.0 // 2019-12-15
-------------------
- The `--instrument` parameter now requires value, e.g. `--instrument=json` (only one supported currently).
- Next to the "instr.report" logger there is now an "instr.log" logger you can use in your tests to emit records to the same file.
- The `.log` output file is no longer first written as a pickle, then converted to a json array. It is written immediately and contains json objects.
- Tests were added and existing ones were refactored.


0.1.0 // 2019-10-21
-------------------
- initial version
