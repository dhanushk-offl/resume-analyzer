# Resume Analysis App

Welcome to the **Resume Analysis App**! This tool uses the power of **LangChain** and **Groq LLM** to help you quickly analyze and evaluate resumes based on specific job descriptions and skill sets. Perfect for HR professionals and recruiters, this app streamlines resume evaluation and provides insightful feedback in real-time.

## Features
- **PDF Resume Processing**: Upload multiple resumes in PDF format for simultaneous analysis.
- **Skills Matching**: Match the skills listed in a resume with your required skills and receive a detailed score.
- **Job Description Evaluation**: Get a recommendation on whether a candidate should be selected, placed on the waiting list, or not selected based on the job description.
- **Interactive Results**: View matched skills, scores, and evaluation results directly in the app.

## How It Works

1. **Upload Resume PDFs**: Upload one or multiple resumes in PDF format via the sidebar.
2. **Enter Required Skills**: Input the desired skills for evaluation in the provided text area.
3. **Enter Job Description**: Provide the job description to assess how well the candidate fits the role.
4. **Submit**: Click the "Submit" button to start the analysis.
5. **View Results**: The app will display:
   - Matched skills and scores for each candidate.
   - A job description match score and a final evaluation status.

## Technology Stack
- **Streamlit**: Frontend for creating the interactive user interface.
- **LangChain**: For processing and loading resumes from PDFs.
- **Groq LLM**: Provides intelligent resume and job description analysis.
- **Regular Expressions**: Used for text preprocessing to ensure accurate analysis.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/dhanushk-offl/resume-analyzer.git
   cd resume-analyzer
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:
   ```bash
   streamlit run app.py
   ```

## Usage
1. **Start the App**: Open your browser and visit `http://localhost:8501`.
2. **Upload Resumes**: Drag and drop the resumes you wish to analyze.
3. **Input Skills & Job Description**: Provide relevant details, then click "Submit."
4. **View Results**: Results will be displayed for each candidate, including skill match scores and job suitability status.

## Example Output

```
**Name:** John Doe
**Matched Skills and Scores:**
Python: 9/10
Data Analysis: 8/10
SQL: 7/10
Overall Match Score: 8.5/10

**Job Description Match and Evaluation Status:**
Selected with a score of 9/10
```

---

## Contributing
We welcome contributions! Feel free to open issues or submit pull requests to improve this project.

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

Enjoy analyzing resumes like never before with the **Resume Analysis App**!
