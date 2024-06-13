import pandas as pd
import numpy as np
import re
import os
from pathlib import Path

PATH = Path(__file__).parent
df = pd.read_excel(f'{PATH}/clean_df1.xlsx')
if('Review' not in df.columns):
    df['Review'] = [0 for i in range(len(df))]

try:
    with open('removed_list.txt', 'r') as f:
        list_to_remove = f.read().splitlines()
        f.close()
except:
    list_to_remove = []

#Review 1 by 1 via CLI
for i in range(len(df)-1,0,-1):
    if df.iloc[i, df.columns.get_loc('Review')] == 1:
        continue
    os.system('cls')
    print('Reviewing Data')
    print('=================')
    print(f'Index: {i}')
    print(f'Full Text: {df.iloc[i]["full_text"]}')
    print('=================')
    print(f'Tokenized: {df.iloc[i]["Tokenized_FullText"]}')
    print('=================')
    print(f'Polarity: {df.iloc[i]["Polarity"]}')
    print('=================')
    userInput = input('Review (1 Positive, 0 Neutral, 2 Negative, 3 Remove): ')
    df.iloc[i, df.columns.get_loc('Review')] = 1
    if userInput == '1':
        df.iloc[i, df.columns.get_loc('Polarity')] = 'Positive'
    elif userInput == '2':
        df.iloc[i, df.columns.get_loc('Polarity')] = 'Negative'
    elif userInput == '3':
        list_to_remove.append(i)
    else:
        df.iloc[i, df.columns.get_loc('Polarity')] = 'Neutral'
    with open(f'{PATH}/removed_list.txt', 'a') as f:
        f.write(f'{i}\n')
        f.close()
    df.to_excel(f'{PATH}/clean_df1_reviewed.xlsx', index=False)

df.drop(list_to_remove, inplace=True)