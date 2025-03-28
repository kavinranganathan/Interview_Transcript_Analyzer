import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from typing import List, Dict

# Load environment variables from .env file
load_dotenv()

# Configure Google Gemini API
def configure_gemini_api():
    """Configure the Google Gemini API with the API key from .env."""
    try:
        # Get API key from environment variable
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            st.error("Google API key not found in .env file.")
            return None
        
        genai.configure(api_key=api_key)
    except Exception as e:
        st.error(f"Error configuring API: {str(e)}")
        return None

# Function to generate interview summary using Gemini
def generate_interview_summary(transcript_text: str) -> Dict[str, str]:
    """
    Generate a structured summary of the interview transcript using Gemini.
    
    Args:
        transcript_text (str): Full text of the interview transcript
    
    Returns:
        Dict[str, str]: Structured summary with key interview sections
    """
    # Configure the model
    model = genai.GenerativeModel('gemini-2.5-pro-exp-03-25')
    
    # Detailed prompt for interview transcript analysis
    prompt = f"""Analyze the following interview transcript and provide a comprehensive, structured summary with the following sections:

1. Interview Overview
   - Candidate Name (if mentioned)
   - Position/Role Applied For
   - Interview Type (Technical, Behavioral, etc.)

2. Candidate Background
   - Key Professional Experiences
   - Educational Qualifications
   - Relevant Skills Highlighted

3. Interview Highlights
   - Significant Discussion Points
   - Technical or Role-Specific Questions and Answers
   - Candidate's Strengths
   - Areas of Potential Development

4. Interview Tone and Communication
   - Candidate's Communication Style
   - Confidence Level
   - Depth of Responses

5. Interviewer's Perspective
   - Key Observations
   - Potential Fit for the Role
   - Notable Reactions or Comments

6. Key Takeaways
   - Overall Impression
   - Recommendation or Next Steps

Transcript:
{transcript_text}

Provide insights and observations based on the conversation, maintaining objectivity and focusing on professional assessment."""

    try:
        # Generate summary
        response = model.generate_content(prompt)
        return {
            "summary": response.text
        }
    except Exception as e:
        st.error(f"Error generating summary: {str(e)}")
        return {"summary": "Could not generate summary."}

# Streamlit App
def main():
    st.set_page_config(
        page_title="Interview Transcript Analyzer", 
        page_icon="📋",
        layout="wide"
    )
    
    st.title("🤝 Interview Transcript Analyzer")

    # File uploader
    uploaded_file = st.file_uploader(
        "Upload Interview Transcript", 
        type=['txt', 'pdf', 'docx'],
        help="Upload a text file containing the interview transcript"
    )
    
    # Process the uploaded file
    if uploaded_file is not None:
        # Read the file content
        try:
            # Check file type and read accordingly
            if uploaded_file.type == 'application/pdf':
                import PyPDF2
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                transcript_text = ' '.join([page.extract_text() for page in pdf_reader.pages])
            elif uploaded_file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                import docx
                doc = docx.Document(uploaded_file)
                transcript_text = ' '.join([para.text for para in doc.paragraphs])
            else:
                # Assume it's a text file
                transcript_text = uploaded_file.getvalue().decode('utf-8')
            
            # Optional: Transcript Preview
            with st.expander("Original Transcript Preview"):
                st.text(transcript_text[:1000] + "..." if len(transcript_text) > 1000 else transcript_text)
            
            # Generate summary
            st.write("🔍 Analyzing Interview Transcript...")
            with st.spinner("Generating comprehensive analysis..."):
                summary = generate_interview_summary(transcript_text)
            
            # Display summary with enhanced formatting
            st.header("📄 Interview Analysis Report")
            st.markdown("### Comprehensive Insights")
            st.write(summary["summary"])
            
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")

# Requirements for the app
def get_requirements():
    """
    Returns a requirements.txt content for the project
    """
    return """
streamlit
google-generativeai
pypdf2
python-docx
python-dotenv
"""

# Run the app
if __name__ == "__main__":
    configure_gemini_api()
    main()
