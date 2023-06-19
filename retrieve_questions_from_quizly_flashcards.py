import os
import re
from bs4 import BeautifulSoup

def fetch_div_elements_with_class(file_path, class_name):
    """
    Read HTML page (not fetching it because of authorization issues) and try retrieve questions:
    - find all elements with given `class_name` in class attribute
    - iterate over found elements
    - get all <p> from element and try parse them to questions object in format:
    ```
     {
        "question": "QUESTION_NUMBER. Question content:",
        "answerA": "A. Answer A",
        "answerB": "B. Answer B",
        "answerC": "C. Answer C",
        "correctAnswer": "A",
        "questionImage": "https://image-is-here.com/imgXYZ" // optional property
    }
    ```
    
    """
    # Read the HTML file
    with open(file_path, 'r') as file:
        html_content = file.read()

    # Create BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all <div> elements with the specified class
    div_elements = soup.find_all('div', class_=class_name)

    # Transform the data into a dictionary with <p> elements for each <div>
    result = []
    for div in div_elements:
        retrieved_question = {}
        p_elements = div.find_all('p')  # Find all <p> elements within the <div>
        p_texts = [p.get_text(strip=True) for p in p_elements]  # Extract the text from each <p> element
        question_number = int(re.match(r'^\d+', p_texts[0]).group()) # first <p> has question that start with question number
        p_elements = div.find_all('p')
        for p_element in p_elements:
            p_element_text = p_element.get_text(strip=True) # Extract the text from each <p> element
            match = re.match(r'^\d+', p_element_text)
            if match:
                question_number = int(match.group())
                retrieved_question['question'] = p_element_text 
            elif p_element_text.startswith('A.'):
                retrieved_question['answerA'] = p_element_text
                if p_element.find('strong'):
                    retrieved_question['correctAnswer'] = 'A'
            elif p_element_text.startswith('B.'):
                retrieved_question['answerB'] = p_element_text
                if p_element.find('strong'):
                    retrieved_question['correctAnswer'] = 'B'
            elif p_element_text.startswith('C.'):
                retrieved_question['answerC'] = p_element_text
                if p_element.find('strong'):
                    retrieved_question['correctAnswer'] = 'C'
        question_image_element =div.find('img', class_='ZoomableImage-rawImage')
    
        if question_image_element:
            retrieved_question['questionImage'] = question_image_element['src']

        if all(key in retrieved_question for key in ('question', 'answerA', 'answerB', 'answerC', 'correctAnswer')):
            result.append(retrieved_question)
        else:
            print(f"Retrieved question don't have all required fields: {retrieved_question}")
        

    return result

# Example usage
file_path = os.path.join(os.path.dirname(__file__), 'flashcards.html')  # Replace 'example.html' with your HTML file name
class_name = 'SetPageTerm-content'  # Replace with the class name of the <div> elements you want to retrieve
output_filename = 'test4'

div_elements_data = fetch_div_elements_with_class(file_path, class_name)

with open(output_filename, "w") as file:
    for question in div_elements_data:
        # Write each property in a single line
        file.write(f"{question['question']}\n")
        file.write(f"{question['answerA']}\n")
        file.write(f"{question['answerB']}\n")
        file.write(f"{question['answerC']}\n")
        file.write(f"{question['correctAnswer']}\n")
        if 'questionImage' in question:
            file.write(f"{question['questionImage']}\n")
        # Separate objects with an empty line
        file.write("\n")