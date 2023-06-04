import re
import json
import sys

def convert_segment_to_subtexts(segment):
    """
    Because some questions/answers can be longer than single line,
    we extract from single segment subtexts that are either
    - multiline text wrapped in quotes
    - single line text otherwise
    """
    lines = segment.splitlines()
    subtexts = []
    current_subtext = []
    in_multiline = False

    for line in lines:
        line = line.strip()

        if line.startswith('"'):
            if line.endswith('"'):
                subtexts.append(line.strip('"'))
            else:
                current_subtext.append(line.strip('"'))
                in_multiline = True
        elif line.endswith('"'):
            current_subtext.append(line.strip('"'))
            subtexts.append('\n'.join(current_subtext))
            current_subtext = []
            in_multiline = False
        elif in_multiline:
            current_subtext.append(line)
        else:
            subtexts.append(line)

    return subtexts

def convert_raw_text_to_json(raw_text):
    """
    Split raw_text into segments.
    Each segment is a subtext that start and end with empty line.
    Segment is transformed to subtexts (as questions/answers can be multiline)
    and from those subtexts we produce singe question object.
    """
    segments = re.split(r"\n\s*\n", raw_text.strip())
    questions = []

    for segment in segments:
        lines = convert_segment_to_subtexts(segment)
        current_question = {}

        for line in lines:
            line = line.strip()

            question_number_match = re.match(r"^(\d+\.)", line)
            question_correct_answer_match = re.match(r"^[A-C]$", line)

            if question_number_match:
                current_question["question"] = line
            elif line.startswith("A."):
                current_question["answerA"] = line
            elif line.startswith("B."):
                current_question["answerB"] = line
            elif line.startswith("C."):
                current_question["answerC"] = line
            elif question_correct_answer_match:
                current_question["correctAnswer"] = line
            elif line.startswith("http") or line.startswith("data:image"):
                current_question["questionImage"] = line

        questions.append(current_question)
        current_question = {}

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
