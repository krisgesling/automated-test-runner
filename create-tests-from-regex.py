import csv
import random
import sre_yield
import sys
from os.path import join
import regex_for_volume_old as regex_tests

skill_path = sys.argv[1]
total_number_of_tests = int(sys.argv[2]) if sys.argv[2] else 20

output_file = './tests_to_create.csv'
files_created = []

intents_to_test = regex_tests.intents

def handlers_one_of(handlers, test_type):
    """Concatenate handlers into single test string

    Args:
        handlers (tuple(str)): one or more handler names

    Returns:
        str: "[['or',['endsWith', 'name', 'handle_increase_volume'], ['endsWith', 'name', 'handle_increase_volume_verb'], ['endsWith', 'name', 'handle_increase_volume_phrase']]]"
    """
    if handlers[0] is None:
        return ""
    elif len(handlers) < 2:
        return "[['endsWith', '{}', '{}']]".format(test_type, handlers[0])

    test_string = "[['or'"
    for h in handler:
        test_string += (", ['endsWith', '{}', '{}']".format(test_type, h))
    test_string += "]]"
    return test_string


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

number_of_tests_per_intent = int(total_number_of_tests / len(intents_to_test))
if number_of_tests_per_intent < 1:
    number_of_tests_per_intent = 1

for intent in intents_to_test:
    # Generate all variations of regex
    expanded_strings = []
    [expanded_strings.extend(expand_regex(regex)) for regex in intent['input_strings']]
    # Determine number of tests to create
    tests_to_skip = int(len(expanded_strings) / number_of_tests_per_intent)
    print('* {} expanded_strings'.format(len(expanded_strings)))
    print('* {} number_of_tests_per_intent'.format(number_of_tests_per_intent))
    print('* {} tests_to_skip'.format(tests_to_skip))
    if tests_to_skip < 1:
        tests_to_skip = None
    num_tests_created = len(expanded_strings[::tests_to_skip])
    print('Creating {}/{} {} tests'.format(num_tests_created, len(expanded_strings), intent["title"]))
    for utt in expanded_strings[::tests_to_skip]:
        create_test(utt, intent['intent_handlers'])
