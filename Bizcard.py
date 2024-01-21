import pytesseract
import pandas as pd
from PIL import Image
import re
import pymysql
import streamlit as st
from streamlit_option_menu import option_menu


#pytesseract path extraction
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
# sql connection and database creating
mydb = pymysql.Connection(user='root', host='127.0.0.1', passwd='Praveen@1234')
cur = mydb.cursor()
cur.execute('create database if not exists bizcard')
mydb = pymysql.Connection(user='root', host='127.0.0.1', passwd='Praveen@1234', database='bizcard')
cur = mydb.cursor()
# Creating table in MySQL
cur.execute('''create table if not exists cards(
                                             CompanyName varchar(25) primary key,
                                             CardHolderName varchar(25),
                                             Designation varchar(25),
                                             PhoneNumber text,
                                             Email_Id varchar(25),
                                             Website_URL varchar(40),
                                             Area varchar(25),
                                             City varchar(20),
                                             State varchar(20),
                                             Pincode bigint,
                                             Image longblob                                            
)''')
# SIDEBAR ELEMENTS
with st.sidebar:
    st.markdown("### :green[BizCardX - Extracting Business Card Data with OCR]")
    st.caption('  - :black[**Image Processing**]')
    st.caption('  - :black[**OCR**]')
    st.caption('  - :black[**Python** Scripting]')
    st.caption('  - :black[Data **Collection and Management**]')
    st.caption('  - :black[**MySQL**]')
    st.caption('  - :black[streamlit **GUI**]')


#optionmenu
SELECT=option_menu(
    menu_title=None,
    options=["","Extract Upload card","Delete & Modify"],
    icons=["","upload","eraser"],
    default_index=1,
    orientation="horizontal",
    styles={"container":{"padding":"0!important","background-color":"green","size":"cover","width":"100%"},
            "icon":{"color":"black","font-size":"20px"},
            "nav-link":{"font-size":"20px","test-align":"center","margin":"-2px","--hover-color":"#DCDCDC"},
            "nav-link-selected":{"background-color":"#DCDCDC"}})


# Creating two tabs in streamlit interface
tab1, tab2 = st.tabs(['Extract and Upload', 'View and Modify'])

# On Extract and Upload tab
with tab1:
    # upload image into streamlit interface
    upload = st.file_uploader("Upload a :orange[Business card] Image", type=['jpg', 'png'])
    if upload is not None:
        a, b = st.columns([2, 3])
        with a:
            st.write('#### :green[You Have Uploaded a card]')
        with b:
            st.image(upload)
        # Convert Image into text
        img = Image.open(upload)
        res = pytesseract.image_to_string(img)
        # splitting the result and storing it in a list
        details = []
        for i in res.split("\n"):
            if i:
                details.append(i)
    card = {
        'company': [],
        'name': [],
        'designation': [],
        'mobile': [],
        'email': [],
        'web': [],
        'area': [],
        'city': [],
        'state': [],
        'pin': [],
        'image': []   
    }


 # Function to order the details corresponding to its nature
    def card_extraction(data):
        set1 = data.copy()
        for i, j in enumerate(data):
            # Get Name of the cardholder
            if i == 0:
                card['name'].append(j)
                set1.remove(j)
            # Get Designation
            if i == 1:
                if 'st' not in data[i].lower():
                    card['designation'].append(j)
                    set1.remove(j)           

             # Get Mobile Number
            if re.search("^.[0-9].{2}-|^[0-9].{2}-|.[0-9].-", j):
                num = j.split(' ')
                for n in num:
                    if len(n) > 5:
                        card['mobile'].append(n)
                        set1.remove(j)
                if len(card['mobile']) >= 2:
                    card['mobile'] = ' & '.join(card['mobile'])        

            # Get E-mail
            if re.search('@\w', j):
                mail = j.split(' ')
                for e in mail:
                    if re.search('@\w', e):
                        card['email'].append(e)
                        set1.remove(j)

            #Get web address
            if 'www.' in j:
                adr = j.split(' ')
                for a in adr:
                    if 'www.' in a:
                        card['web'].append(a)
                        set1.remove(j)                    

            # Get Street, Area, State, Pin
            if re.search('St', j):
                a = j.split(',')
                loc = []
                for b in a:
                    if b and len(b) > 3:
                        loc.append(b)
                if len(loc) == 2:
                    card['area'].append(loc[0])
                    card['city'].append(loc[1])
                    pc = data[i + 1].split(' ')
                    card['state'].append(pc[0])
                    card['pin'].append(pc[1])
                if len(loc) == 3:
                    card['area'].append(loc[0])
                    card['city'].append(loc[1])
                    card['state'].append(loc[2])
                    card['pin'].append(data[i + 1])
                set1.remove(j)
                set1.remove(data[i + 1])            

        # Get Company Name
        if set1:
            card['company'].append(' '.join(set1))
        with open(f"Bizcardproject/{upload.name}", 'rb') as file:
            card['image'].append(file.read())

        for c in card:
            if card[c]:
                pass
            else:
                card[c].append('Failed to Get')
        return 'The Text from Given Card has been Successfully Extracted'     
    

        # Button to extract data
    if upload is not None:
        sel = st.selectbox('', options=['ExtractData and Edit'], index=None, label_visibility='collapsed')
        if sel == 'ExtractData and Edit':
            out = card_extraction(details)
            st.info(out)
            table = pd.DataFrame(card)
            edited = st.data_editor(table)
            # Button to upload fetched data into SQL
            if st.button('UPLOAD'):
                if edited is not None:
                    for i, j in edited.iterrows():
                        query = '''insert ignore into cards values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
                        cur.execute(query, tuple(j))
                        mydb.commit()
                        st.info('Data has been successfully inserted into MySql DataBase')
                        st.balloons()


# On View and Modify tab
with tab2:

    # getting company name from sql
    cn = pd.read_sql_query("select CompanyName from cards", mydb)
    company = []
    for i, j in cn.itertuples():
        company.append(j)
    if company:
        # To view all the data
        if st.button('View Data'):
            view = pd.read_sql_query('select * from cards', mydb)
            st.write(view)
    else:
        st.warning('No Business card available in MySQL - Database, Add a card to view')
    
    column1, column2 = st.columns(2)


    # Modify the data in the selected company
    with column1:  
        selected = st.selectbox('', company, index=None, placeholder='SELECT A COMPANY TO MODIFY',
                                label_visibility='collapsed')       
        if selected is not None:
            st.markdown("### :green[Modify Data In DataBase]")
            det = pd.read_sql_query(f"select * from cards where CompanyName='{selected}'", mydb)
            modify = det.values.tolist()
            company = st.text_input('Company Name', modify[0][0])
            name = st.text_input('Cardholder', modify[0][1])
            desig = st.text_input('Designation', modify[0][2])
            ph = st.text_input('Contact Number', modify[0][3])
            email = st.text_input('E-Mail', modify[0][4])
            web = st.text_input('Website', modify[0][5])
            street = st.text_input('Area', modify[0][6])
            city = st.text_input('City', modify[0][7])
            state = st.text_input('State', modify[0][8])
            pin = st.text_input('Pincode', modify[0][9])
            # Button to commit changes in Database
            if st.button('Modify Changes to DataBase'):
                cur.execute(
                    f'''update cards set CompanyName="{company}", CardHolderName="{name}", Designation="{desig}",
                PhoneNumber="{ph}", Email_Id="{email}", Website_URL="{web}", Area="{street}", City="{city}", State="{state}",
                Pincode="{pin}" where CompanyName="{selected}"''')
                mydb.commit()
                st.success("Changes Committed in DataBase")
                st.balloons()

    if st.button("View Modified Card"):
     updated = pd.read_sql_query(f'select * from cards where CompanyName="{selected}"', mydb)
     st.write(updated)

    # Deleting the card
    with column2:
        del_list = []
        for i, j in cn.itertuples():
            del_list.append(j)
        delete = st.selectbox('', del_list, index=None, placeholder='Select a CompanyName to delete', label_visibility='collapsed')
        if delete is not None:
            st.write(f"Do you want to Delete the :red[{delete}] card data")
            st.write(':orange[click on the delete to drop the values in database]')
            if st.button('Delete'):
                cur.execute(f'''DELETE from cards where CompanyName="{delete}"''')
                mydb.commit()
                st.success(f'The "{delete}" card details has been deleted from database successfully')
                st.snow()            