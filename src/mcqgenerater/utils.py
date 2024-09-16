import os
import PyPDF2
import json
import traceback
from src.mcqgenerater.logger import logger
import pandas as pd

def read_file(file):
    try:
        if file.name.endswith(".pdf"):
            pdf_reader = PyPDF2.PdfFileReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        elif file.name.endswith(".txt"):
            return file.read().decode("utf-8")
        else:
            raise Exception("Unsupported file format. Only PDF and text files are supported.")
    except Exception as e:
        logger.error(f"Error reading file: {e}")
        raise

def get_table_data(quiz):
    try:
        logger.info(f"Parsing quiz data: {quiz}")
        quiz_data = json.loads(quiz)

        table_data = []
        for q_num, q in quiz_data.items():
            mcq = q["mcq"]
            choices = " || ".join([f"{key}-> {choice}" for key, choice in q["options"].items()])
            correct = q["correct"]
            table_data.append({"MCQ": mcq, "Choices": choices, "Correct": correct})
        
        return pd.DataFrame(table_data)
    except Exception as e:
        logger.error(f"Error parsing quiz data: {e}")
        traceback.print_exception(type(e), e, e.__traceback__)
        return None


