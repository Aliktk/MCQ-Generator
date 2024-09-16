# **MCQ Generator: AI-Powered Multiple-Choice Question Creator**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/ali-nawaz-khattak/)

## Overview

The **MCQ Generator** is an AI-driven project that automates the generation of multiple-choice questions (MCQs) from a given text, evaluates their difficulty, and presents them through an interactive web interface. This tool combines OpenAI's language models with LangChain and Streamlit to deliver a seamless experience for creating and interacting with educational content.

---

## 📝 Table of Contents

- [**MCQ Generator: AI-Powered Multiple-Choice Question Creator**](#mcq-generator-ai-powered-multiple-choice-question-creator)
  - [Overview](#overview)
  - [📝 Table of Contents](#-table-of-contents)
  - [📁 Project Structure](#-project-structure)
  - [✨ Features](#-features)
  - [💻 Installation](#-installation)
  - [🚀 Usage](#-usage)
  - [⚙️ Configuration](#️-configuration)
  - [📊 Data](#-data)
  - [🔬 Experiments](#-experiments)
  - [🙏 Acknowledgements](#-acknowledgements)

---

## 📁 Project Structure

```bash
MCQ-Generator/
├── .gitignore
├── README.md
├── mcq_training_data.txt
├── requirements.txt
├── response.json
├── setup.py
├── streamlit.py
├── experiments/
│   ├── data/Machine_Learning_Quiz.csv
│   └── mcq.ipynb
└── src/
    ├── __init__.py
    └── mcqgenerator/
        ├── MCQgenerator.py
        ├── logger.py
        └── utils.py
```

## ✨ Features

- **MCQ Generation**: Generate MCQs from provided text using advanced natural language processing techniques.
- **Complexity Evaluation**: Assess the complexity of the generated MCQs.
- **Web Interface**: User-friendly web interface to interact with the MCQ generator.

## 💻 Installation

To install the necessary dependencies, run the following command:

```bash
pip install -r requirements.txt
```

## 🚀 Usage

To use the MCQ generator, run the `streamlit.py` script:

```bash
streamlit run streamlit.py
```

## ⚙️ Configuration
* Adjust project settings in `setup.py`.
* Manage logging configurations in `src/mcqgenerator/logger.py`.

You can configure various aspects of the project in the `setup.py` file and adjust logging settings in `src/mcqgenerater/logger.py`.

## 📊 Data
* Sample training data is available in `mcq_training_data.txt`.
* Example responses are provided in `response.json`.

## 🔬 Experiments

The `experiments` directory contains a Jupyter notebook (`mcq.ipynb`) and a CSV file with machine learning quiz data (`machine_learning_quiz.csv`).

## 🙏 Acknowledgements

A huge thanks to the teams behind LangChain and Streamlit for providing robust tools. Special appreciation to ineuron for the project opportunity.
