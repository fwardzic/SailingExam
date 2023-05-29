import re
import json
import sys

def convert_raw_text_to_json(raw_text):
    segments = re.split(r"\n\s*\n", raw_text.strip())
    questions = []

    for segment in segments:
        lines = segment.split("\n")
        question = {}
        question["question"] = re.sub(r'^[\d.]+', '', lines[0].strip())
        question["answerA"] = lines[1].strip()[2:]
        question["answerB"] = lines[2].strip()[2:]
        question["answerC"] = lines[3].strip()[2:]
        question["correctAnswer"] = lines[4].strip()

        if len(lines) > 5:
            question["questionImage"] = lines[5].strip()

        questions.append(question)

    return questions

if len(sys.argv) < 3:
    print("Please provide the file name and output file name as parameters.")
    print("Usage example: python convert_to_questions_with_answers.py raw_questions_input questions.json")
    sys.exit(1)

input_file_name = sys.argv[1]
output_file_name = sys.argv[2]

try:
    with open(input_file_name, 'r') as file:
        raw_text = file.read()
        questions = convert_raw_text_to_json(raw_text)

        json_data = json.dumps(questions, indent=2)

        with open(output_file_name, 'w') as output_file:
            output_file.write(json_data)

        print("Conversion completed. Result saved to: " + output_file_name)

except FileNotFoundError:
    print("File not found: " + input_file_name)
    sys.exit(1)
