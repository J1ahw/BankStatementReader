from PIL import Image
import pytesseract
import pandas as pd
from pdf2image import convert_from_path
import os

Date = []
Amount =[]
Balance = []
Describe = []
filenames = []
months = {'JAN': '01',
          'FEB': '02',
          'MAR': '03',
          'APR': '04',
          'MAY': '05',
          'JUN': '06',
          'JUL': '07',
          'AUG': '08',
          'SEP': '09',
          'OCT': '10',
          'NOV': '11',
          'DEC': '12',
          }

pdf_path = 'Monzo_bank_2019-12-28-2022-04-06_93691.pdf' 


# Convert the scanned PDF to a list of images

pages = convert_from_path(pdf_path)
del pages[-1]
for page in pages:
    extracted_text = pytesseract.image_to_string(page).split('Description')[1].split('Monzo Bank Limited')[0]
    i = 1
    k = 1
    for line in extracted_text.split('\n'):
        try:
            amount = line.split(' ')[-2]
            balance = line.split(' ')[-1]
            date = line.split(' ')[0]
            description = line.split(' ')
            del description[0]
            del description[-1]
            del description[-1]
            new_des = ''
            for t in description:
                new_des += f'{t} ' 
            if i != 1 and i != len(extracted_text.split('\n')):
                Date.append(date)
                Amount.append(amount)
                Balance.append(balance)
                Describe.append(new_des)
                
        except:
            k += 1
        i += 1

df = pd.DataFrame({'Date': Date,
                   'Description': Describe,
                    'Amount': Amount,
                    'Balance': Balance})
print(df)
df.to_excel('result.xlsx', header=True, index=False)
    
