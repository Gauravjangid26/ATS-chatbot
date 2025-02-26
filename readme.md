# A5 ATS Resume Expert

A Streamlit-based AI-powered ATS Resume Expert that helps job seekers optimize their resumes, evaluate percentage match, generate interview questions, and create a personalized learning path based on job descriptions.

## Features
- **Resume Analysis**: Evaluates strengths and weaknesses in a resume.
- **Percentage Match**: Compares resume content with job description and highlights missing keywords.
- **Personalized Learning Path**: Creates a 6-month study plan for skill enhancement.
- **Resume Optimization**: Improves the resume with ATS-friendly formatting and keywords.
- **Interview Questions Generator**: Generates customizable interview questions based on job description.

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/Gauravjangid26/ATS-chatbot.git
   cd ATS-chatbot
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up your **Google API Key** in a `.env` file:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

## Usage
Run the application with:
```
streamlit run app.py
```

Upload a resume in PDF format, enter a job description, and use the available options:
- **Tell Me About the Resume**: Get feedback on your resume.
- **Percentage Match**: Check how well your resume aligns with the job description.
- **Personalized Learning Path**: Receive a study plan to improve relevant skills.
- **Update Resume & Download**: Get an ATS-optimized resume.
- **Generate Interview Questions**: Choose the number of questions and get job-specific interview queries.

## Technologies Used
- **Python**
- **Streamlit**
- **Google Gemini API**
- **PDF Processing (pdf2image, FPDF)**
- **Environment Variables (dotenv)**

## Repository
[GitHub: ATS-chatbot](https://github.com/Gauravjangid26/ATS-chatbot.git)



