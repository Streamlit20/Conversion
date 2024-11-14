import streamlit as st
from pdf2docx import Converter
from io import BytesIO
from docx import Document
from docx2pdf import convert
import tempfile
import os
import base64

# Function to convert PDF to Word
def pdf_to_word(pdf_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf_file:
        temp_pdf_file.write(pdf_file.read())
        temp_pdf_path = temp_pdf_file.name

    word_io = BytesIO()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as temp_word_file:
        cv = Converter(temp_pdf_path)
        cv.convert(temp_word_file.name, start=0, end=None)
        cv.close()
        word_io.write(temp_word_file.read())
    word_io.seek(0)

    os.remove(temp_pdf_path)
    os.remove(temp_word_file.name)

    return word_io

# Function to convert Word to PDF with formatting
def word_to_pdf(word_file):
    # Save uploaded file to a temporary directory
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as temp_word_file:
        temp_word_file.write(word_file.read())
        temp_word_path = temp_word_file.name

    # Convert Word document to PDF using docx2pdf
    temp_pdf_path = temp_word_path.replace(".docx", ".pdf")
    convert(temp_word_path, temp_pdf_path)

    # Read the generated PDF into memory
    with open(temp_pdf_path, "rb") as pdf_file:
        pdf_bytes = pdf_file.read()

    # Cleanup temporary files
    os.remove(temp_word_path)
    os.remove(temp_pdf_path)

    # Return PDF as BytesIO object
    return BytesIO(pdf_bytes)

# Helper function to encode images in base64
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Page for PDF to Word conversion
def pdf_to_word_page():
    st.title("PDF to Word Converter")
    st.text("This application takes PDF Documents as input and converts them to Word Documents.")
    if st.sidebar.button("Home"):
        st.session_state["page"] = "Home"
        st.rerun()
    logo_filename = "Ai-automation.jpg"
    st.sidebar.image(logo_filename, use_column_width=True)
    uploaded_files = st.sidebar.file_uploader("Upload PDF resumes", type="pdf", accept_multiple_files=True)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            with st.spinner(f"Converting {uploaded_file.name} to Word..."):
                word_file = pdf_to_word(uploaded_file)
                st.success("Conversion completed!")
                st.download_button(
                    label="Download Word File",
                    data=word_file,
                    file_name=f"{uploaded_file.name.split('.')[0]}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

# Page for Word to PDF conversion
def word_to_pdf_page():
    st.title("Word to PDF Converter")
    st.text("This application takes Word Documents as input and converts them to PDF Documents.")
    if st.sidebar.button("Home"):
        st.session_state["page"] = "Home"
        st.rerun()
    logo_filename = "Ai-automation.jpg"
    st.sidebar.image(logo_filename, use_column_width=True)
    uploaded_files = st.sidebar.file_uploader("Upload Word documents", type="docx", accept_multiple_files=True)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            with st.spinner(f"Converting {uploaded_file.name} to PDF..."):
                pdf_file = word_to_pdf(uploaded_file)
                st.success("Conversion completed!")
                st.download_button(
                    label="Download PDF File",
                    data=pdf_file,
                    file_name=f"{uploaded_file.name.split('.')[0]}.pdf",
                    mime="application/pdf"
                )
# Define the CSS styling for buttons
button_css = """
    <style>
    .stButton > button {
        font-family: 'Times New Roman', Times, serif;
        background-color: transparent;
        color: white;
        padding: 10px 10px;
        font-size: 18px;
        border: transparent;
        border-radius: 10px;
        cursor: pointer;
    }
    .stButton > button:hover {
        background-color: transparent;
        border-color: transparent;
        color: #00c4ff;
    }
    </style>
"""

# Apply the CSS to the Streamlit page
st.markdown(button_css, unsafe_allow_html=True)
# Home Page with Clickable Image Links
def home_page():
    st.title("Document Converter")
    st.write("Choose a conversion type:")

    col1, col2 = st.columns(2)
    
    # PDF to Word clickable image link
    with col1:
        pdf_to_word_image = "pdf_word.jpeg"  # Replace with actual image file
        pdf_to_word_image_base64 = get_base64_image(pdf_to_word_image)
        

        st.markdown(
            f'<a href="#"><img src="data:image/jpeg;base64,{pdf_to_word_image_base64}" alt="PDF to Word" style="width:60%; cursor: pointer;"></a>',
            unsafe_allow_html=True
        )
        if st.button("Click Here for PDF to Word Conversion"):
            st.session_state["page"] = "PDF to Word"
            st.rerun()

    # Word to PDF clickable image link
    with col2:
        word_to_pdf_image = "word_pdf.jpeg"  # Replace with actual image file
        word_to_pdf_image_base64 = get_base64_image(word_to_pdf_image)
        
            
        st.markdown(
            f'<a href="#"><img src="data:image/jpeg;base64,{word_to_pdf_image_base64}" alt="Word to PDF" style="width:60%; cursor: pointer;"></a>',
            unsafe_allow_html=True
        )
        if st.button("Click Here for Word to PDF Conversion"):
            st.session_state["page"] = "Word to PDF"
            st.rerun()

# Main app controller
if "page" not in st.session_state:
    st.session_state["page"] = "Home"

# Page Navigation
if st.session_state["page"] == "Home":
    home_page()
elif st.session_state["page"] == "PDF to Word":
    pdf_to_word_page()
elif st.session_state["page"] == "Word to PDF":
    word_to_pdf_page()