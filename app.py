from dotenv import load_dotenv
import streamlit as st
import os
import io
import base64
from PIL import Image
import pdf2image
import google.generativeai as genai
from fpdf import FPDF
import requests  # Needed for downloading the font file

# Load environment variables
load_dotenv()

# Configure Google Gemini API
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    st.error("GOOGLE_API_KEY not found. Please set it in your environment variables.")
    st.stop()

genai.configure(api_key=API_KEY)

def ensure_font_exists(font_path):
    """Check if the font file exists; if not, download it."""
    if not os.path.exists(font_path):
        url = "https://github.com/dejavu-fonts/dejavu-fonts/raw/master/ttf/DejaVuSans.ttf"
        st.info(f"Downloading DejaVuSans.ttf from {url} ...")
        response = requests.get(url)
        if response.status_code == 200:
            with open(font_path, "wb") as f:
                f.write(response.content)
            st.success(f"Downloaded DejaVuSans.ttf to {font_path}")
        else:
            raise FileNotFoundError(f"Font file not found at {font_path} and download failed with status code {response.status_code}.")

def get_gemini_response(input_text, pdf_content, prompt):
    """Generate a response using Google Gemini API."""
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_text, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    """Convert first page of uploaded PDF to an image and encode as base64."""
    if uploaded_file is not None:
        uploaded_file.seek(0)  # Reset file pointer
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]

        # Convert image to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [{
            "mime_type": "image/jpeg",
            "data": base64.b64encode(img_byte_arr).decode()  # Encode to base64
        }]
        return pdf_parts
    else:
        raise FileNotFoundError("No File Uploaded")

def generate_pdf(updated_resume_text):
    """Generate a downloadable PDF file with Unicode support."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Define correct font path and ensure it exists
    font_path = os.path.join(os.getcwd(), "DejaVuSans.ttf")
    
    pdf.add_font("DejaVu", "", font_path, uni=True)
    pdf.set_font("DejaVu", size=12)

    # Wrap long text in a multi-cell that fits A4 width
    pdf.multi_cell(190, 10, updated_resume_text, align="L")

    pdf_output_path = "updated_resume.pdf"
    pdf.output(pdf_output_path, "F")
    return pdf_output_path

# Streamlit App
st.set_page_config(page_title="A5 ATS Resume Expert")
st.header("MY A5 PERSONAL ATS")

input_text = st.text_area("Job Description:", key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=['pdf'])

if uploaded_file:
    st.success("PDF Uploaded Successfully.")

submit1 = st.button("Tell Me About the Resume")
submit3 = st.button("Percentage Match")
submit4 = st.button("Personalized Learning Path")
update_prompt = st.text_area("Describe how you want your resume updated:", key="update_prompt")
submit5 = st.button("Update Resume & Download")
submit6 = st.button("Generate Interview Questions")

input_prompt1 = """
You are an experienced HR with tech expertise in Data Science, Full Stack, Web Development, Big Data Engineering, DevOps, or Data Analysis.
Your task is to review the provided resume against the job description for these roles.
Please evaluate the candidate's profile, highlighting strengths and weaknesses in relation to the specified job role.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with expertise in Data Science, Full Stack, Web Development, Big Data Engineering, DevOps, and Data Analysis.
Your task is to evaluate the resume against the job description. Provide:
1. The percentage match.
2. Keywords missing.
3. Final evaluation.
"""

input_prompt4 = """
You are an experienced learning coach and technical expert. Create a 6-month personalized study plan for an individual aiming to excel in [Job Role], 
focusing on the skills, topics, and tools specified in the provided job description. Ensure the study plan includes:
- A list of topics and tools for each month.
- Suggested resources (books, online courses, documentation).
- Recommended practical exercises or projects.
- Periodic assessments or milestones.
- Tips for real-world applications.
"""

input_prompt5 = """
You are an expert resume writer with deep knowledge of Data Science, Full Stack, Web Development, Big Data Engineering, DevOps, and Data Analysis.
Your task is to refine and optimize the provided resume according to the job description.
Ensure the new resume:
- Highlights relevant experience and skills.
- Optimizes for ATS (Applicant Tracking Systems).
- Uses strong action words and quantifiable achievements.
- Incorporates key industry keywords.
"""

input_prompt6 = """
You are an AI-powered interview coach.
Generate {num_questions} interview questions based on the given job description,
focusing on the required skills and expertise.
"""

# Slider to choose the number of interview questions
num_questions = st.slider("Select number of interview questions:", min_value=1, max_value=30, value=5)
if submit6:
    if input_text.strip():
        response = get_gemini_response(input_text, [""], input_prompt6.format(num_questions=num_questions))
        st.subheader("Generated Interview Questions:")
        st.write(response)
    else:
        st.warning("Please provide a job description to generate questions.")
