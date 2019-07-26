#!/bin/bash

origin_dir=${pwd}
skill_dir=$1
num_tests=$2
test_name=$3
output_file=$test_name-result.txt
output_dir='/home/kris/Projects/automated-test-runner/test-results'

rm $skill_dir/test/intent/*.json
# get directory of this script
test_skill_dir="$( cd "$(dirname "$0")" ; pwd -P )"
cd $test_skill_dir
python3 ./create-tests-from-regex.py $skill_dir $num_tests

cd ~/mycroft-core
mycroft-skill-testrunner $skill_dir > $output_dir/$output_file 2>&1

cd $skill_dir/test/intent/
mkdir -p ./failed/$test_name
cat $output_dir/$output_file |
  grep "FAIL: test_Intent" |
  sed 's/FAIL\: test_Intent\[.*\://' |
  sed 's/\].*__main__.*//' |
  xargs -L1 cp -t ./failed/$test_name
echo ""
echo "======== TESTS COMPLETED ========"
echo ""
cat $output_dir/$output_file | grep "FAILED (failures="

cd $origin_dir
