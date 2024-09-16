# Importing libraries
import streamlit as st
import pandas as pd
import json
import traceback
import os
from io import BytesIO
from fpdf import FPDF
from langchain.callbacks.manager import get_openai_callback
from src.mcqgenerater.logger import logger
from src.mcqgenerater.utils import read_file, get_table_data
from src.mcqgenerater.MCQgenerater import generate_evaluate_chain
from dotenv import load_dotenv

# Read JSON file
file_path = "experiments/data/response.json"

try:
    with open(file_path, 'r') as file:
        response_json = json.load(file)
except json.JSONDecodeError as e:
    st.error("The JSON file is malformed: " + str(e))
    logger.error("The JSON file is malformed: " + str(e))
    st.stop()

# Create title for Streamlit app
st.set_page_config(page_title="MCQ Generator 🤖📚", layout="wide")
st.title("MCQ Generator Application With Langchain 🤖📚")

# Add custom CSS
st.markdown(
    """
    <style>
        h1, h2, h3, h4, h5, h6 {
            color: #4CAF50;
        }
        
        button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        
        button:hover {
            background-color: #45a049;
        }
        
        .download-button {
            display: flex;
            justify-content: center;
            margin-top: 20px;
        }
        
        .output-container {
            background-color: #f1f1f1;
            padding: 20px;
            border-radius: 4px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Create a form using st.form
with st.form("user_inputs"):
    # Upload File
    uploaded_file = st.file_uploader("Upload a PDF, Text, DOCX, HTML File")

    # Input fields
    mcq_count = st.number_input("Enter number of MCQs", min_value=1, max_value=50)

    # Text input
    subject = st.text_input("Enter Subject", max_chars=20)

    # Tone
    tone = st.text_input("Complexity Level of Questions", max_chars=20, placeholder="Simple")

    # Submit button
    button = st.form_submit_button("Generate MCQs")

# Check if button is clicked and all fields are filled
if button and uploaded_file is not None and mcq_count and subject and tone:
    with st.spinner("Generating MCQs..."):
        try:
            logger.info("Received user inputs and file upload.")
            text = read_file(uploaded_file)
            if text is None:
                st.error("Unsupported file format.")
                logger.error("Unsupported file format.")
                st.stop()

            # Count tokens and cost of operation
            with get_openai_callback() as cb:
                response = generate_evaluate_chain(
                    {
                        "text": text,
                        "number": mcq_count,
                        "subject": subject,
                        "tone": tone,
                        "response_json": json.dumps(response_json)
                    }
                )
                logger.info(f"Received response: {response}")

                quiz = response.get("quiz", None)
                if quiz:
                    table_data = get_table_data(quiz)
                    if table_data is not None:
                        st.markdown("## Generated MCQs 🎉")
                        st.write("Here are the generated MCQs:")
                        st.markdown("---")
                        st.dataframe(table_data)

                        # Download options
                        def convert_to_pdf(df):
                            pdf = FPDF()
                            pdf.add_page()
                            pdf.set_auto_page_break(auto=True, margin=15)
                            pdf.set_font("Arial", size=12)
                            for index, row in df.iterrows():
                                pdf.multi_cell(0, 10, f"{index+1}. {row['MCQ']}\nChoices: {row['Choices']}\nCorrect: {row['Correct']}\n")
                            pdf_output = BytesIO()
                            pdf_output.write(pdf.output(dest='S').encode('latin1'))
                            pdf_output.seek(0)
                            return pdf_output

                        pdf_data = convert_to_pdf(table_data)

                        with st.container():
                            st.markdown("### Download Options 📥")
                            st.write("Choose your preferred format:")
                            download_button = st.download_button(
                                label="Download as PDF",
                                data=pdf_data,
                                file_name="quiz.pdf",
                                mime="application/pdf"
                            )

                        logger.info("MCQs displayed and download options provided.")
                    else:
                        st.error("Error in table data")
                        logger.error("Error in table data")
                else:
                    st.write("No quiz data found in response.")
                    logger.info("No quiz data found in response.")

        except Exception as e:
            st.error("Error: " + str(e))
            logger.error(f"Error generating MCQs: {e}")

        else:
            logger.info(f"Total Tokens: {cb.total_tokens}")
            logger.info(f"Prompt Tokens: {cb.prompt_tokens}")
            logger.info(f"Completion Tokens: {cb.completion_tokens}")
            logger.info(f"Total Cost: {cb.total_cost}")