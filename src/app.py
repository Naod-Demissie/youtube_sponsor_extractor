"""
Streamlit app for YouTube Sponsor Extractor
"""
import re
import streamlit as st
import pandas as pd

from youtube_api import extract_video_id, get_video_details
from sponsor_extraction import extract_sponsor_info
from export_utils import (
    create_safe_filename, 
    create_json_export, 
    create_csv_export, 
    create_excel_export, 
    create_text_export, 
    create_docx_export
)

def setup_page():
    """Set up the Streamlit page configuration."""
    st.set_page_config(
        page_title="YouTube Sponsor Extractor",
        page_icon="🎬",
        layout="centered"
    )
    
    st.title("YouTube Sponsor Extractor")
    st.write(
        "Extract sponsor information (brand name and URL) from YouTube video descriptions."
    )

def validate_youtube_url(youtube_url):
    """Validate the YouTube URL format."""
    if not youtube_url:
        st.write("Please enter a YouTube URL.")
        return False
        
    if not re.match(r"https?://(www\.)?(youtube\.com|youtu\.be)/", youtube_url):
        st.error("Please enter a valid YouTube URL.")
        return False
        
    return True

def display_results(sponsor_info, video_title):
    """Display the extracted sponsor information."""
    if sponsor_info:
        st.write(f"### Video: {video_title}")
        st.write("### Extracted Sponsor Information")
        df = pd.DataFrame(sponsor_info)
        st.table(df)
        
        # Prepare download options
        st.write("### Download Results")
        
        # Create columns for download buttons
        col1, col2, col3, col4, col5 = st.columns(5)
        
        # Create sanitized filename from video title
        safe_title = create_safe_filename(video_title)
        
        # JSON download
        with col1:
            json_data = create_json_export(sponsor_info)
            st.download_button(
                label="JSON",
                data=json_data,
                file_name=f"{safe_title}_sponsors.json",
                mime="application/json"
            )
        
        # CSV download
        with col2:
            csv_data = create_csv_export(sponsor_info)
            st.download_button(
                label="CSV",
                data=csv_data,
                file_name=f"{safe_title}_sponsors.csv",
                mime="text/csv"
            )
        
        # Excel download
        with col3:
            excel_data = create_excel_export(sponsor_info)
            st.download_button(
                label="Excel",
                data=excel_data,
                file_name=f"{safe_title}_sponsors.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        
        # TXT download
        with col4:
            text_data = create_text_export(sponsor_info)
            st.download_button(
                label="TXT",
                data=text_data,
                file_name=f"{safe_title}_sponsors.txt",
                mime="text/plain"
            )
        
        # DOCX download
        with col5:
            try:
                docx_data = create_docx_export(sponsor_info)
                st.download_button(
                    label="DOCX",
                    data=docx_data,
                    file_name=f"{safe_title}_sponsors.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
            except ImportError:
                st.error("DOCX export requires python-docx library")
    else:
        st.write(f"### Video: {video_title}")
        st.write("No sponsor information found in the description.")

def run_app():
    """Run the main Streamlit application."""
    setup_page()
    
    # Input YouTube URL
    youtube_url = st.text_input(
        "YouTube URL", placeholder="https://www.youtube.com/watch?v=VIDEO_ID"
    )
    
    # Process button
    if st.button("Extract Sponsors"):
        if not validate_youtube_url(youtube_url):
            return
            
        try:
            # Fetch video information
            with st.spinner("Fetching video information..."):
                video_details = get_video_details(youtube_url)
                
                if not video_details:
                    st.error("Could not fetch video information. Check the URL or API key.")
                    return
                    
                description = video_details["description"]
                video_title = video_details["title"]
            
            # Extract sponsor info
            with st.spinner("Extracting sponsor information..."):
                sponsor_info = extract_sponsor_info(description)
            
            # Display results
            display_results(sponsor_info, video_title)
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    run_app()