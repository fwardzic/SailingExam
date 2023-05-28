import re
import json
import sys

def convert_raw_text_to_json(raw_text):
    questions = []
    lines = raw_text.strip().split('\n')

    for i in range(0, len(lines), 5):
        question = lines[i][3:].strip()
        answers = {
            "A": lines[i + 1][3:].strip(),
            "B": lines[i + 2][3:].strip(),
            "C": lines[i + 3][3:].strip()
        }
        correct_answer = lines[i + 4].strip()

        questions.append({
            "question": question,
            "answerA": answers["A"],
            "answerB": answers["B"],
            "answerC": answers["C"],
            "correctAnswer": correct_answer
        })

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
