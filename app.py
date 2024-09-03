import streamlit as st
from langchain.document_loaders import PyPDFLoader
from langchain_groq import ChatGroq
from typing import List
import os
import re

llm = ChatGroq(
    model="mixtral-8x7b-32768",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

def extract_text_from_pdf(pdf_path: str) -> str:
    loader= PyPDFLoader(pdf_path)
    documents= loader.load()
    full_text= "\n".join([doc.page_content for doc in documents])
    return full_text

def preprocess_text(text: str) -> str:
    text= text.lower()
    text= re.sub(r"[^a-z0-9\s]", "", text)
    return text

def extract_name(pdf_path: str) -> str:
    base_name= os.path.basename(pdf_path)
    name, _= os.path.splitext(base_name)
    return name

def analyze_resume_using_prompt(pdf_paths: List[str], skills_input: str, job_description: str, llm: ChatGroq):
    for pdf_path in pdf_paths:
        resume_text= extract_text_from_pdf(pdf_path)
        resume_text= preprocess_text(resume_text)
        name= extract_name(pdf_path)

        skills_prompt= f"""
        Based on the following resume text, match the provided skills with the skills mentioned in the resume. 
        Provide only the matched skills in the skills to evaluate with a score from 1 out of 10 for each matched skill. 
        Also, provide the overall score from 1 to 10 of matching for the provided skills with evaluated skills and final thoughts.

        Resume Text:
        {resume_text}
        Skills to evaluate:
        {skills_input}
        """
        response= llm.invoke(skills_prompt)
        response_text= response.content.strip()
        st.write(f"**Name:** {name}")
        st.write(f"**Matched Skills and Scores:**\n{response_text}")

        job_description_prompt= f"""
        Based on the following resume text, determine if the resume is suitable for the role described in the job description. 
        Put the candidate into 3 categories: selected, not selected or waiting list.
        Provide the overall score from 1 to 10 on how well the resume matches the job description.

        Resume Text:
        {resume_text}
        Job Description:
        {job_description}
        """

        job_description_response= llm.invoke(job_description_prompt)
        job_description_response_text= job_description_response.content.strip()

        st.write(f"**Job Description Match and Evaluation Status:**\n{job_description_response_text}")
        st.write("-" * 50)

        

st.title("Resume Analysis App")
with st.sidebar:
    st.header("Upload Resume PDFs")
    uploaded_files= st.file_uploader("Upload Resume PDFs", type="pdf", accept_multiple_files=True)

col1, col2= st.columns(2)
with col1:
    skills_input= st.text_area("Enter the Skills..", height=100, key="skills")
    with st.sidebar:
        st.subheader("Skills to evaluate")
        st.write(skills_input)

with col2:
    job_description= st.text_area("Enter the Job Description..", height=100, key="job_description")

button= st.button("Submit")

if button:
    if uploaded_files:
        pdf_paths= []

        for uploaded_file in uploaded_files:
            with open(uploaded_file.name, "wb") as f:
                f.write(uploaded_file.getbuffer())
                pdf_paths.append(uploaded_file.name)

        analyze_resume_using_prompt(pdf_paths, skills_input, job_description, llm)

        for pdf_path in pdf_paths:
            os.remove(pdf_path)
