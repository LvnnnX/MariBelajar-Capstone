import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
from process import *

PATH = Path(__file__).parent
df = pd.read_excel(f'{PATH}/clean_df1_reviewed_500_1000.xlsx')
if('Review' not in df.columns):
    df['Review'] = [0 for i in range(len(df))]

try:
    with open('removed_list.txt', 'r') as f:
        list_to_remove = f.read().splitlines()
        f.close()
except:
    list_to_remove = []

clear_background()

st.title(f'Kampus Mengajar Dataset Review')
st.sidebar.title('Review Data')

#FORM STreamlit
try:
    with open(f'{PATH}/number.txt', 'r') as f:
        number_doc = int(f.readline())
        mode = str(f.readline())
        f.close()
except Exception as e:
    st.write(e)
    number_doc = 0
    mode = 'asc'

#2 Button
col1, col2,col3,col4,col5 = st.columns(5, gap='small')
asc_button = col2.button('Ascending', key='asc')
col3.write('Mode: ' + mode.upper())
desc_button = col4.button('Descending', key='desc')

if asc_button:
    number_doc = 0
    while((df.iloc[number_doc, df.columns.get_loc('Review')] == 1)):
        if not(df.iloc[number_doc, df.columns.get_loc('Polarity')] == 'Positive'):
            break
        number_doc += 1
    with open('number.txt', 'w') as f:
        f.write(str(number_doc) + "\n")
        f.write('asc')
        f.close()
    st.rerun()

if desc_button:
    number_doc = len(df)-1
    while(df.iloc[number_doc, df.columns.get_loc('Review')] == 1):
        if (df.iloc[number_doc, df.columns.get_loc('Polarity')] == 'Positive'):
            break
        number_doc -= 1
    with open('number.txt', 'w') as f:
        f.write(str(number_doc) + "\n")
        f.write('desc')
        f.close()
    st.rerun()

with st.form(key='data-form', clear_on_submit=True):
    st.header('Review Data ke - ' + str(number_doc))  

    st.text_area('Full Text', df.iloc[number_doc]['full_text'], disabled=True)

    st.text_area('Tokenized Full Text', df.iloc[number_doc]['Tokenized_FullText'], disabled=True)

    st.text_input('Polarity', df.iloc[number_doc]['Polarity'], disabled=True)

    userInput = st.selectbox('Review', ['Positive', 'Neutral', 'Negative', 'Remove'])

    NextButton = st.form_submit_button('Next')
    if NextButton:
            
        if userInput == 'Positive':
            df.iloc[number_doc, df.columns.get_loc('Polarity')] = 'Positive'
        elif userInput == 'Negative':
            df.iloc[number_doc, df.columns.get_loc('Polarity')] = 'Negative'
        elif userInput == 'Remove':
            with open('removed_list.txt', 'a') as f:
                f.write(f'{number_doc}\n')
                f.close()
        elif userInput == 'Neutral':
            df.iloc[number_doc, df.columns.get_loc('Polarity')] = 'Neutral'
            
        df.iloc[number_doc, df.columns.get_loc('Review')] = 1
            
            
        df.to_excel(f'{PATH}/clean_df1_reviewed.xlsx', index=False)
        
        if mode == 'asc' : number_doc += 1
        else : number_doc -= 1
        while(not(df.iloc[number_doc, df.columns.get_loc('Polarity')] == 'Positive')):
            if mode == 'asc':
                number_doc += 1
            else:
                number_doc -= 1
        with open('number.txt', 'w') as f:
            f.write(str(number_doc) + "\n")
            f.write(mode)
            f.close()
            
        st.rerun()
    
        

