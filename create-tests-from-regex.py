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
date = ["19th of August", "July 25th", "8 October", "November 1"]
output_file = './tests_to_create.csv'
files_created = []

intents_to_test = [
    # {
    #     'title': 'current_time',
    #     'intent_handlers': "[['or',['endsWith', 'intent_type', 'current_time_handler_simple'],['endsWith', 'intent_type', 'current_time_handler_query'],['endsWith', 'name', 'handle_query_current_time_padatious']]]",
    #     'input_strings': [
    #         "what time (is it|it is) (currently|right now|)",
    #         "((do|can you|) check the|check|the|) clock (((at|in|for) {0}|) ((right|) now|)|((right|) now|) ((at|in|for) {0}|)|)  (|please)".format(random.choice(location)),
    #         "(do you know|(could you|) (tell|give) (me|)|(can you|) (check|(tell|give) (me|))|may i (ask|know)|) (what time (is it|it is) ((currently|(right|) now|) ((at|in|for) {0}|)|((at|in|for) {0}|) (currently|(right|) now|))|the (current|) time ((at|in|for) {0}|)) (|please)".format(random.choice(location)),
    #         "(excuse me|) (what is|what\'s) the (current time ((at|in|for) {0}|) |time ((at|in|for) {0}|) (currently|(right|) now|)|time (currently|(right|) now|) ((at|in|for) {0}|))  (|please)".format(random.choice(location)),
    #         "((check (the|)|(tell|give) (me|) the|)|the|) (time (((right|) now|) ((at|in|for) {0}|)|((at|in|for) {0}|) ((right|) now|)|)|current time ((at|in|for) {0}|))  (|please)".format(random.choice(location))
    #     ]
    # },
    # {
    #     'title': 'future_time',
    #     'intent_handlers': "[['or',['endsWith', 'intent_type', 'future_time_handler_simple'],['endsWith', 'intent_type', 'future_time_handler_query'],['endsWith', 'name', 'handle_query_future_time_padatious']]]",
    #     'input_strings': [
    #         "(in|) {1} (hours|minutes|seconds) what (time will it be|will the time be) (from now|)".format(random.choice(location), random.choice(offset)),
    #         "(in|) {1} (hours|minutes|seconds) (from now|) what (time will it be|will the time be) (at|in|for) {0}".format(random.choice(location), random.choice(offset)),
    #         "what (time will it be|will the time be) in {1} (hours|minutes|seconds) ((at|in|for) {0}|)".format(random.choice(location), random.choice(offset)),
    #         "what (time will it be|will the time be) {1} (hours|minutes|seconds) from now ((at|in|for) {0}|)".format(random.choice(location), random.choice(offset)),
    #         "what time is it {1} (hours|minutes|seconds) from now ((at|in|for) {0}|)".format(random.choice(location), random.choice(offset)),
    #         "what time is it in {1} (hours|minutes|seconds) ((at|in|for) {0}|)".format(random.choice(location), random.choice(offset)),
    #         "((what is|what's|tell (me|)) the|) time in {1} (hours|minutes|seconds) ((at|in|for) {0}|) (|please)".format(random.choice(location), random.choice(offset)),
    #         "((what is|what's|tell (me|)) the|) time {1} (hours|minutes|seconds) from now ((at|in|for) {0}|) (|please)".format(random.choice(location), random.choice(offset))
    #     ]
    # },
    {
        'title': 'date',
        'intent_handlers': "[['or',['endsWith', 'intent_type', 'handle_query_date'],['endsWith', 'intent_type', 'handle_date_for_relative_day'],['endsWith', 'intent_type', 'handle_query_for_relative_day']]]",
        'input_strings': [
            "what date is it (today|tomorrow|)",
            "what's (today's|tomorrow's|yesterday's) date",
            "what's the date (today|tomorrow|)",
            "(today's|tomorrow's|yesterday's) date (is what|)",
            "date (today|tomorrow|yesterday)",
            "what date of the month is it",
            "what date is next (Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)",
            "what (date is|dates are|is the date) next weekend",
            "what (was the date|date was it) {0} (day|days|week|weeks) ago".format(random.choice(offset)),
            "what is the date {0} (day|days|week|weeks) from (today|now)".format(random.choice(offset)),
            "what is the date in {0} (day|days|week|weeks)".format(random.choice(offset)),
            "what was the date last (Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)",
            "what is the date (this|next) (Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)"
        ]
    },
    {
        'title': 'day',
        'intent_handlers': "[['or',['endsWith', 'intent_type', 'handle_query_date'],['endsWith', 'intent_type', 'handle_date_for_relative_day'],['endsWith', 'intent_type', 'handle_query_for_relative_day']]]",
        'input_strings': [
            "what day is (it|) (today|tomorrow|)",
            "(what is|what's) (today|tomorrow|yesterday|the day)",
            "(today's|tomorrow's|yesterday's) day (is what|)",
            "(today|tomorrow|yesterday) is what day (of the (week|month)|)",
            "what is the day (of the (week|month)|)",
            "(when is|what day is (it|)|what is the day) (this|next) (Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)",
            "what ((are the|) days|day is) next weekend",
            "what (was the day|day was it) {0} (day|days|week|weeks) ago".format(random.choice(offset)),
            "what (is the day|day was it) {0} (day|days|week|weeks) from (now|today)".format(random.choice(offset)),
            "(what day|when) (is|was (it|)) {0}".format(random.choice(date)),
            "what day of the week (will it be|was it) on {0}".format(random.choice(date)),
            "what day is it (in|at|for) {0}".format(random.choice(location))
        ]
    },
    # {
    #     'title': 'holidays',
    #     'intent_handlers': [],
    #     'input_strings': [
    #         "(when is|when's) {0} ((this|next) year's|)".format(random.choice(holiday)),
    #         "(when is|when's) ((this|next) year's) {0}".format(random.choice(holiday)),
    #         "what day (of the year|) is {0} ((this|next) year's|)".format(random.choice(holiday)),
    #         "what day (of the year|) is ((this|next) year's) {0}".format(random.choice(holiday))
    #     ]
    # },
    # {
    #     'title': 'holidays_how_long_until',
    #     'intent_handlers': [],
    #     'input_strings': [
    #         "how (many days|long) (left|) until {0}".format(random.choice(holiday))
    #     ]
    # },
    # {
    #     'title': 'leap_year',
    #     'intent_handlers': [],
    #     'input_strings': [
    #         "(when|what year) is (the|) (next|closest) leap year"
    #     ]
    # },
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
    if tests_to_skip < 1:
        tests_to_skip = None
    num_tests_created = len(expanded_strings[::tests_to_skip])
    print('Creating {}/{} {} tests'.format(num_tests_created, len(expanded_strings), intent["title"]))
    for utt in expanded_strings[::tests_to_skip]:
        create_test(utt, intent['intent_handlers'])
