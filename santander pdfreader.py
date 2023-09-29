from PIL import Image
import pytesseract
import pandas as pd
from pdf2image import convert_from_path
import os

Date = []
Amount =[]
Balance = []
filenames = []
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
          'Dec': '12',
          }

for root,dirs,files in os.walk('2019'):
        for f in files:
            filepath = f'{root}/{f}'
            filenames.append(filepath)

# Path to the scanned PDF file
for pdf_path in filenames:

    # Convert the scanned PDF to a list of images
    pages = convert_from_path(pdf_path)

    # Iterate through each page and perform OCR
    
    analyst_text = pytesseract.image_to_string(pages[1])
    year = analyst_text.split('Your transactions ')[1].split(' ')[2]
    extracted_text = analyst_text.split('Balance brought forward from previous statement')[1].split('Balance carried forward to next statement:')[0]
    i = 1
    for line in extracted_text.split('\n'):
        try:
            amount = line.split(' ')[-2]
            balance = line.split(' ')[-1]
            date = line.split(' ')[0].replace('th','').replace('nd','').replace('st','').replace('rd','') +'/'+ months[line.split(' ')[1]] +'/'+ year
            if i != 1 and i != len(extracted_text.split('\n')):
                Date.append(date)
                Amount.append(amount)
                Balance.append(balance)
        except:
            print('')
        i += 1

df = pd.DataFrame({'Date': Date,
                    'Amount': Amount,
                    'Balance': Balance})
print(df)
df.to_excel('result2019.xlsx', header=True, index=False)
    
