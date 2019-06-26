import csv
import random
import sre_yield
import sys
from os.path import join

skill_path = sys.argv[1]
total_number_of_tests = int(sys.argv[2]) if sys.argv[2] else 20
number_of_tests_per_intent = int(total_number_of_tests / 2)
offset = [3,5,8,9,12,20]
location = ['Seattle', 'Paris', 'Sydney', 'Toronto']
output_file = './tests_to_create.csv'
files_created = []

intents_to_test = [
    {
        'title': 'current_time',
        'intent_handlers': "[['or',['endsWith', 'intent_type', 'current_time_handler_simple'],['endsWith', 'intent_type', 'current_time_handler_query'],['endsWith', 'name', 'handle_query_current_time_padatious']]]",
        'input_strings': [
            "what time (is it|it is) (currently|right now|)",
            "((do|can you|) check the|check|the|) clock (((at|in|for) {0}|) ((right|) now|)|((right|) now|) ((at|in|for) {0}|)|)  (|please)".format(random.choice(location)),
            "(do you know|(could you|) (tell|give) (me|)|(can you|) (check|(tell|give) (me|))|may i (ask|know)|) (what time (is it|it is) ((currently|(right|) now|) ((at|in|for) {0}|)|((at|in|for) {0}|) (currently|(right|) now|))|the (current|) time ((at|in|for) {0}|)) (|please)".format(random.choice(location)),
            "(excuse me|) (what is|what\'s) the (current time ((at|in|for) {0}|) |time ((at|in|for) {0}|) (currently|(right|) now|)|time (currently|(right|) now|) ((at|in|for) {0}|))  (|please)".format(random.choice(location)),
            "((check (the|)|(tell|give) (me|) the|)|the|) (time (((right|) now|) ((at|in|for) {0}|)|((at|in|for) {0}|) ((right|) now|)|)|current time ((at|in|for) {0}|))  (|please)".format(random.choice(location))
        ]
    },
    {
        'title': 'future_time',
        'intent_handlers': "[['or',['endsWith', 'intent_type', 'future_time_handler_simple'],['endsWith', 'intent_type', 'future_time_handler_query'],['endsWith', 'name', 'handle_query_future_time_padatious']]]",
        'input_strings': [
            "(in|) {1} (hours|minutes|seconds) what (time will it be|will the time be) (from now|)".format(random.choice(location), random.choice(offset)),
            "(in|) {1} (hours|minutes|seconds) (from now|) what (time will it be|will the time be) (at|in|for) {0}".format(random.choice(location), random.choice(offset)),
            "what (time will it be|will the time be) in {1} (hours|minutes|seconds) ((at|in|for) {0}|)".format(random.choice(location), random.choice(offset)),
            "what (time will it be|will the time be) {1} (hours|minutes|seconds) from now ((at|in|for) {0}|)".format(random.choice(location), random.choice(offset)),
            "what time is it {1} (hours|minutes|seconds) from now ((at|in|for) {0}|)".format(random.choice(location), random.choice(offset)),
            "what time is it in {1} (hours|minutes|seconds) ((at|in|for) {0}|)".format(random.choice(location), random.choice(offset)),
            "((what is|what's|tell (me|)) the|) time in {1} (hours|minutes|seconds) ((at|in|for) {0}|) (|please)".format(random.choice(location), random.choice(offset)),
            "((what is|what's|tell (me|)) the|) time {1} (hours|minutes|seconds) from now ((at|in|for) {0}|) (|please)".format(random.choice(location), random.choice(offset))
        ]
    }
]

def test_template(utt, handler):
    return '\n'.join(['{',
                      '    "utterance": "{}",'.format(utt),
                      '    "assert": "{}"'.format(handler),
                      '}'])

def expand_regex(regex):
    result = list(sre_yield.AllStrings(regex))
    return result

def write_to_csv(data, csv_file):
    output = []
    for s in data:
        output.append([s.strip(), intent_handler])
    ## Preview first line of output
    print(output[0])
    ## Write output to csv
    with open(csv_file, 'w') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerows(output)

# write_to_csv(all_strings, output_file)

def create_test(utt, handler):
    # Remove invalid filename characters
    test_file_name = ''.join(
        x for x in utt if (x.isalnum() or x in '._-')) + '.intent.json'
    test_path = '{}/test/intent/{}'.format(skill_path, test_file_name)
    files_created.append(test_path)
    with open(test_path, "w+") as test_file:
        test_file.write(test_template(utt, handler))
        test_file.close()

for intent in intents_to_test:
    # Generate all variations of regex
    expanded_strings = []
    [expanded_strings.extend(expand_regex(regex)) for regex in intent['input_strings']]
    # Determine number of tests to create
    tests_to_skip = int(len(expanded_strings) / number_of_tests_per_intent)
    num_tests_created = len(expanded_strings[::tests_to_skip])
    print('Creating {} {} tests'.format(num_tests_created, intent["title"]))
    for utt in expanded_strings[::tests_to_skip]:
        create_test(utt, intent['intent_handlers'])
