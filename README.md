# snowflake-column-search
 
[![Python](https://img.shields.io/badge/-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[![Snowflake](https://img.shields.io/badge/-Snowflake-29B5E8?style=for-the-badge&logo=snowflake&logoColor=white)](https://snowflake.com/)
[![Streamlit](https://img.shields.io/badge/-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)

## Overview

Lets you search for specific columns across all databases

## Setup Instructions

### For Mac/Linux

1. **Creating a Virtual Environment and Installing Dependencies**

    ```bash
    python3 -m venv venv && source venv/bin/activate && pip3 install --upgrade pip && pip3 install -r requirements.txt &&     streamlit run app.py

    ```

2. **Running the Streamlit App**

    ```bash
    streamlit run app.py
    ```

### For Windows

1. **Allow Script Execution (if necessary)**

    ```powershell
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
    ```

2. **Creating a Virtual Environment and Installing Dependencies**

    ```powershell
    py -m venv venv; .\venv\Scripts\Activate.ps1; python -m pip install --upgrade pip; pip install -r requirements.txt
    ```

3. **Running the Streamlit App**

    ```powershell
    streamlit run app.py
    ```