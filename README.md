# automated-test-runner
Generate and run range of Mycroft intent tests

## Configuration
In `run-tests.sh` modify lines 4 and 5 to define which skill to test and where the results will be saved.
```
skill_dir='/opt/mycroft/skills/skill-to-test'
output_dir='/home/user/some-dir'
```
Be sure to make `run-tests.sh` executable by running:
```
$ chmod u+x run_tests.sh
```

### Intents to test
Intent tests are defined in `create-tests-from-regex.py`
Input strings are simple regular expressions.
Tests must use valid syntax for the [Mycroft Integration Test Runner](https://mycroft.ai/documentation/skills/automatic-testing/)

## Usage
`./run_tests.sh` takes two positional arguments. The number of tests and a string to include in the output file name.

As an example:
`./run_tests.sh 20 small-test`
will generate 20 intent tests and save the resuls in `test.results.small-test.txt`

The shell output will also print any test files that failed and provide a short summary of the number that failed .
