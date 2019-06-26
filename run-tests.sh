#!/bin/bash

origin_dir=${pwd}
skill_dir='/opt/mycroft/skills/skill-to-test'
output_dir='/home/user/some-dir'
output_file=test.results.$1.txt

rm $skill_dir/test/intent/*
# get directory of this script
test_skill_dir="$( cd "$(dirname "$0")" ; pwd -P )"
cd $test_skill_dir
python3 ./create-tests-from-regex.py

mycroft-skill-testrunner $skill_dir > $output_dir/$output_file 2>&1

cd $skill_dir/test/intent/
cat $output_dir/$output_file |
  grep "FAIL: test_Intent" |
  sed 's/FAIL\: test_Intent\[.*\://' |
  sed 's/\].*__main__.*//' |
  xargs -L1 cat
echo ""
echo "======== TESTS COMPLETED ========"
echo ""
cat $output_dir/$output_file | grep "FAILED (failures="

cd $origin_dir
