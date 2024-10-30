import streamlit as st
from langchain.document_loaders import PyPDFLoader
from groq import Groq
from typing import List
import os
import re
from dotenv import load_dotenv
load_dotenv()

# Initialize Groq client using the API key from environment variables
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def extract_text_from_pdf(pdf_path: str) -> str:
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    full_text = "\n".join([doc.page_content for doc in documents])
    return full_text

def preprocess_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    return text

def extract_name(pdf_path: str) -> str:
    base_name = os.path.basename(pdf_path)
    name, _ = os.path.splitext(base_name)
    return name

def analyze_resume_using_prompt(pdf_paths: List[str], skills_input: str, job_description: str):
    for pdf_path in pdf_paths:
        resume_text = extract_text_from_pdf(pdf_path)
        resume_text = preprocess_text(resume_text)
        name = extract_name(pdf_path)

        # Skills analysis prompt
        skills_prompt = f"""
        Based on the following resume text, match the provided skills with the skills mentioned in the resume. 
        Provide only the matched skills in the skills to evaluate with a score from 1 out of 10 for each matched skill. 
        Also, provide the overall score from 1 to 10 of matching for the provided skills with evaluated skills and final thoughts.

        Resume Text:
        {resume_text}
        Skills to evaluate:
        {skills_input}
        """
        skills_response = client.chat.completions.create(
            messages=[{"role": "user", "content": skills_prompt}],
            model="llama3-8b-8192",
        )
        skills_response_text = skills_response.choices[0].message.content.strip()
        st.write(f"**Name:** {name}")
        st.write(f"**Matched Skills and Scores:**\n{skills_response_text}")

        # Job description matching prompt
        job_description_prompt = f"""
        Based on the following resume text, determine if the resume is suitable for the role described in the job description. 
        Put the candidate into 3 categories: selected, not selected or waiting list.
        Provide the overall score from 1 to 10 on how well the resume matches the job description.

        Resume Text:
        {resume_text}
        Job Description:
        {job_description}
        """
        job_description_response = client.chat.completions.create(
            messages=[{"role": "user", "content": job_description_prompt}],
            model="llama3-8b-8192",
        )
        job_description_response_text = job_description_response.choices[0].message.content.strip()

        st.write(f"**Job Description Match and Evaluation Status:**\n{job_description_response_text}")
        st.write("-" * 50)

st.title("Resume Analysis App")
with st.sidebar:
    st.header("Upload Resume PDFs")
    uploaded_files = st.file_uploader("Upload Resume PDFs", type="pdf", accept_multiple_files=True)

col1, col2 = st.columns(2)
with col1:
    skills_input = st.text_area("Enter the Skills..", height=100, key="skills")
    with st.sidebar:
        st.subheader("Skills to evaluate")
        st.write(skills_input)

with col2:
    job_description = st.text_area("Enter the Job Description..", height=100, key="job_description")

button = st.button("Submit")

if button:
    if uploaded_files:
        pdf_paths = []

        # Use temporary files to manage uploaded PDFs
        for uploaded_file in uploaded_files:
            with st.spinner(f"Processing {uploaded_file.name}..."):
                with open(uploaded_file.name, "wb") as temp_file:
                    temp_file.write(uploaded_file.getbuffer())
                    pdf_paths.append(temp_file.name)

        analyze_resume_using_prompt(pdf_paths, skills_input, job_description)

        # Clean up temporary files after processing
        for pdf_path in pdf_paths:
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
