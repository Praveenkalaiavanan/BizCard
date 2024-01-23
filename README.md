# BizCardX: Extracting Business Card Data with OCR

#Table of Contents:
>>About The Project
>>Getting Started
>>Prerequisites
>>Installation
>>Usage
>>Steps
>>Run


#1.About The Project :
   This project is focused on developing a Streamlit application that allows users to upload an image of a business card and 
   extract relevant information from it using 'pytesseract Python Module'. The extracted information should include the company 
   name, card holder name, designation, mobile number, email address, website URL, area, city, state, and pin code. The 
   extracted information should then be displayed in the application's graphical user interface (GUI).


#2.Before starting we need to install certain python libraries.

    PREREQUISITES :
    pytesseract
    re
    PIL
    pymysql
    streamlit
    pandas - are the Python libraries used in this project
    Get Youtube API key from google developer console



    INSTALLATION :
    Run these command separately on your python environment to install.
    
      pip install pytesseract
      pip install pymysql
      pip install streamlit
      pip install pandas
      pip install pillow
      pip install 


#3. USAGE :
    In this Project, I created a streamlit application that allows users to upload an image of a business card and extract 
    relevant information from it using easyOCR. The extracted information should include the company name, card holder name, 
    designation, mobile number, email address, website URL, area, city, state, and pin code.
    The application is simple and intuitive user interface that guides users through the process of uploading the business card 
    image and extracting its information. The extracted information will be displayed in a clean and organized manner, and 
    users should be able to easily add it to the database with the click of a button. And Allow the user to Read the data, 
    Update the data and Allow the user to delete the data through the streamlit UI


#4. STEPS :
    Import all the libraries that are used in this project.
    Created a Connection to MySQL Database
    Created streamlit interface sidebar
    Creating two tabs one to upload and extract the data and another to modify the data or delete
    Created a function to upload a image file and extract text from it using pytesseract and PIL library
    Created a Function to order the details corresponding to its nature
    Created a button to extract and upload the data to MySQL Database
    On Tab2 created dropdowns to modify the data in database or delete a card in database
    
#5. RUN :
    To Run this project we need to go to terminal and change its path to file_loacted_directory
    Then run streamlit code to execute,
           streamlit run file_name.py
    replace file_name with created python file name
    
    -To run this project use,
    >>streamlit run bizcardx.py 
