import pandas as pd
import PyPDF2
import json
import os
import logging
from docx import Document
from bs4 import BeautifulSoup
from src.mcqgenerater.logger import logger
from src.mcqgenerater.utils import read_file, get_table_data
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from langchain.callbacks.manager import get_openai_callback

# Load environment variables from the .env file
load_dotenv()

# Access the environment variables just like you would with os.environ
key = os.getenv("OPENAI_API_KEY")

# Create an instance of LLM with the api key and model name
llm = ChatOpenAI(openai_api_key=key, model_name="gpt-3.5-turbo", temperature=0.7)

# Let's create a prompt template
TEMPLATE = """
Text:{text}
You are an expert MCQ maker. Given the above text, it is your job to
create a quiz of {number} multiple choice questions for {subject} students in {tone} tone.
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like RESPONSE_JSON below and use it as a guide.
Ensure to make {number} MCQs

RESPONSE_JSON
{response_json}

"""

# Input prompt template
quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "subject", "tone", "response_json"],
    template=TEMPLATE
)

# Define llm chain to generate quiz
quiz_chain = LLMChain(
    llm=llm,
    prompt=quiz_generation_prompt,
    output_key="quiz",
    verbose=True
)

# Prompt template to generate quiz from text
TEMPLATE2 = """
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis.
if the quiz is not at per with the cognitive and analytical abilities of the students,
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""

# This prompt template is used to evaluate the complexity of the quiz
quiz_evaluation_prompt = PromptTemplate(input_variables=["subject", "quiz"], template=TEMPLATE2)

# Review chain to evaluate the quiz and give feedback
review_chain = LLMChain(llm=llm, prompt=quiz_evaluation_prompt, output_key="review", verbose=True)

# Sequential chain to generate quiz and evaluate it
generate_evaluate_chain = SequentialChain(
    chains=[quiz_chain, review_chain],
    input_variables=["text", "number", "subject", "tone", "response_json"],
    output_variables=["quiz", "review"],
    verbose=True
)

def read_file(file):
    try:
        logger.info(f"Reading file: {file.name}")
        file_extension = os.path.splitext(file.name)[1].lower()
        if file_extension == '.pdf':
            reader = PyPDF2.PdfFileReader(file)
            text = ""
            for page_num in range(reader.numPages):
                page = reader.getPage(page_num)
                text += page.extractText()
        elif file_extension == '.docx':
            doc = Document(file)
            text = "\n".join([para.text for para in doc.paragraphs])
        elif file_extension == '.txt':
            text = file.read().decode('utf-8')
        elif file_extension == '.html':
            html = file.read().decode('utf-8')
            soup = BeautifulSoup(html, 'html.parser')
            text = soup.get_text()
        else:
            logger.error("Unsupported file format.")
            return None
        logger.info("File read successfully.")
        return text
    except Exception as e:
        logger.error(f"Error reading file: {e}")
        return None