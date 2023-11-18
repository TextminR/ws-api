import json
import random
import re


input_file_path = 'data/newtrainv2.jsonl'
output_file_path = 'data/newtrainv3.jsonl'

def reformat_jsonl(input_file_path, output_file_path):
    with open(input_file_path, 'r') as input_file, open(output_file_path, 'w') as output_file:
        # Read the entire content of the file
        content = input_file.read()

        # Remove the opening and closing brackets
        content = content.strip()[1:-1]

        # Replace commas with new lines and write to the output file
        content = content.replace('},', '}\n')
        output_file.write(content)

def extract_first_1000_characters(input_file_path, output_file_path):
    with open(input_file_path, 'r') as input_file, open(output_file_path, 'w') as output_file:
        # Read the first 1000 characters
        content = input_file.read(1000)
        output_file.write(content)

def print_first_10_entries(input_file_path):
    with open(input_file_path, 'r') as file:
        for _ in range(10):
            line = file.readline()
            # If the file ends before reaching 10 entries, stop reading
            if not line:
                break
            print(line)


def process_jsonl_file(input_file_path, output_file_path):
    # Read the JSONL file
    with open(input_file_path, 'r') as file:
        lines = file.readlines()

    # Process each line
    data = []
    for line in lines:
        try:
            entry = json.loads(line)
            response = json.loads(entry["response"])

            # Skip entries with the date "circa 2000"
            if response["date"] != "circa 2000":
                data.append(entry)
        except json.JSONDecodeError:
            # Skip erroneous lines
            continue

    # Shuffle the data
    random.shuffle(data)

    # Write the processed data back to a new JSONL file
    with open(output_file_path, 'w') as file:
        for entry in data:
            file.write(json.dumps(entry) + '\n')

def print_lines_with_circa_2000(input_file_path):
    with open(input_file_path, 'r') as file:
        for line in file:
            try:
                # Parse the JSON line
                entry = json.loads(line)
                response = json.loads(entry["response"])

                # Check if the date in the response is 'circa 2000'
                if response["date"] == "circa 2000":
                    print(line)
            except json.JSONDecodeError:
                # If there's a parsing error, skip that line
                continue


def print_entries_with_circa_date(input_file_path):
    with open(input_file_path, 'r') as file:
        for line in file:
            try:
                # Parse the JSON line
                entry = json.loads(line)
                response = json.loads(entry["response"])

                # Check if the date in the response starts with 'circa'
                if response["date"].startswith("circa"):
                    print(line)
            except json.JSONDecodeError:
                # If there's a parsing error, skip that line
                continue

def filter_entries_by_date(input_file_path, output_file_path):
    with open(input_file_path, 'r') as input_file, open(output_file_path, 'w') as output_file:
        for line in input_file:
            try:
                # Parse the JSON line
                entry = json.loads(line)
                response = json.loads(entry["response"])

                # Check if the date in the response is exactly four numbers
                if re.fullmatch(r"\d{4}", response["date"]):
                    output_file.write(line)
            except json.JSONDecodeError:
                # If there's a parsing error, skip that line
                continue

def print_entries_with_non_four_digit_dates(input_file_path):
    with open(input_file_path, 'r') as file:
        for line in file:
            try:
                # Parse the JSON line
                entry = json.loads(line)
                response = json.loads(entry["response"])

                # Check if the date in the response is NOT exactly four numbers
                if not re.fullmatch(r"\d{4}", response["date"]):
                    print(line)
            except json.JSONDecodeError:
                # If there's a parsing error, skip that line
                continue




# reformat_jsonl(input_file_path, output_file_path)
# extract_first_1000_characters(input_file_path, output_file_path)
# process_jsonl_file(input_file_path, output_file_path)
# print_first_10_entries('data/newtrainv3.jsonl')
# print_entries_with_circa_date(output_file_path)
# print_lines_with_circa_2000(output_file_path)
# filter_entries_by_date('data/newtrainv3.jsonl', 'data/newtrainv4.jsonl')
print_entries_with_non_four_digit_dates('data/newtrainv4.jsonl')


