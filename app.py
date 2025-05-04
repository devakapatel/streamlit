import streamlit as st
import requests
import os
import time
from datetime import datetime, timedelta

import tempfile
DOWNLOAD_DIR = os.path.join(tempfile.gettempdir(), "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

EXPIRY_HOURS = 3

# Ensure download directory exists
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def cleanup_old_files():
    now = time.time()
    for fname in os.listdir(DOWNLOAD_DIR):
        path = os.path.join(DOWNLOAD_DIR, fname)
        if os.path.isfile(path):
            if now - os.path.getmtime(path) > EXPIRY_HOURS * 3600:
                os.remove(path)

def download_file_to_server(url):
    local_filename = url.split("/")[-1].split("?")[0]
    file_path = os.path.join(DOWNLOAD_DIR, local_filename)
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(file_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename, file_path

def main():
    st.title("🚀 Download Accelerator")
    st.write("Enter a URL to download the file server-side and then transfer it to your device.")

    url = st.text_input("Download URL")

    if st.button("Start Download") and url:
        try:
            with st.spinner("Downloading to server..."):
                filename, path = download_file_to_server(url)
                st.success(f"Downloaded to server: {filename}")
                with open(path, "rb") as f:
                    st.download_button(
                        label="Download to your device",
                        data=f,
                        file_name=filename,
                        mime="application/octet-stream"
                    )
        except Exception as e:
            st.error(f"Error: {e}")

    cleanup_old_files()

if __name__ == "__main__":
    main()
