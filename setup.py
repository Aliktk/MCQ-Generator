from setuptools import setup, find_packages
from typing import List

hyphen_e_dot = "-e ." # to avoid this to cause error
def get_requirements(filepath: str) -> List[str]:
    """
    Reads the requirements from a given file path and returns a list of required packages.
    
    Args:
        filepath (str): The path to the requirements file.
    
    Returns:
        List[str]: A list of required packages.
    """
    requirements = []
    with open(filepath) as file_object:
        requirements = file_object.readlines()
        requirements = [req.replace("\n", "") for req in requirements]

        if hyphen_e_dot in requirements:
            requirements.remove(hyphen_e_dot)

    return requirements

setup(
    name='MCQ Generator',
    packages=find_packages(),
    version='0.1.0',
    description='Generative AI Project: MCQ Generator using OpenAI, Langchain Streamlit',
    author='Muhammad Adil Naeem',
    author_email='madilnaeem0@gmail.com',
    install_requires=get_requirements('requirements.txt')
)
