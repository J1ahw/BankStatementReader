from PIL import Image
import pytesseract
import pandas as pd
from pdf2image import convert_from_path
import os


filenames = []
Date = []
Amount =[]
Balance = []
Desc = [] 

months = {'Jan': '01',
          'Feb': '02',
          'Mar': '03',
          'Apr': '04',
          'May': '05',
          'Jun': '06',
          'Jul': '07',
          'Aug': '08',
          'Sep': '09',
          'Oct': '10',
          'Nov': '11',
          'Dec': '12'}

for root,dirs,files in os.walk('Halifax Current AC 4262'):
        for f in files:
            filepath = f'{root}/{f}'
            filenames.append(filepath)

for pdf_path in filenames:
    try:    
        pages = convert_from_path(pdf_path)
        for page in pages:
            analyst_text1 = pytesseract.image_to_string(page)
            try:
                extracted_text = analyst_text1.split('Description')[1].split('Continued on next page')[0]
            except:
                extracted_text = analyst_text1.split('Description')[1].split('Transaction types')[0]

            i = 0
            k = 1

            for line in extracted_text.split('\n'):
                try:
                    amount = line.split(' ')[-2]
                    balance = line.split(' ')[-1]
                    date = line.split(' ')[0] +'/'+ months[line.split(' ')[1]] +'/20'+ line.split(' ')[2]
                    description = line.split(' ')
                    del description[0]
                    del description[0]
                    del description[0]
                    del description[-1]
                    del description[-1]
                    new_des = ''
                    for t in description:
                        new_des += f'{t} '
                    if i != 1 and i != len(extracted_text.split('\n')):
                        Date.append(date)
                        Desc.append(new_des)
                        Amount.append(amount)
                        Balance.append(balance)
                    i += 1
                except:
                    k+=1
            print(pdf_path)
    except:
        print(f'canot read {pdf_path}')
df = pd.DataFrame({'Date': Date,
                   'Description': Desc,
                    'Amount': Amount,
                    'Balance': Balance})
print(df)
df.to_excel('result2.xlsx', header=True, index=False)
    
