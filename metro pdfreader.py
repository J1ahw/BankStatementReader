from PIL import Image
import pytesseract
import pandas as pd
from pdf2image import convert_from_path
import os

Date = []
Amount =[]
Balance = []
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

for root,dirs,files in os.walk('CURRENT'):
        for f in files:
            filepath = f'{root}/{f}'
            filenames.append(filepath)

# Path to the scanned PDF file
for pdf_path in filenames:

    # Convert the scanned PDF to a list of images
    pages = convert_from_path(pdf_path)

    # Iterate through each page and perform OCR
    if len(pages) == 2:
        analyst_text1 = pytesseract.image_to_string(pages[0])
        extracted_text = analyst_text1.split('DATE')[1].split('Does not includ')[0]
    else:
        analyst_text1 = pytesseract.image_to_string(pages[0])
        analyst_text2 = pytesseract.image_to_string(pages[1])
        extracted_text1 = analyst_text1.split('DATE')[1].split('Does not includ')[0]
        extracted_text2 = analyst_text2.split('DATE')[1].split('Closing Balance')[0]
        extracted_text = extracted_text1 + extracted_text2
    i = 1
    k = 1
    for line in extracted_text.split('\n'):
        try:
            amount = line.split(' ')[-2]
            balance = line.split(' ')[-1]
            date = line.split(' ')[0] +'/'+ months[line.split(' ')[1]] +'/'+ line.split(' ')[2]
            if i != 1 and i != len(extracted_text.split('\n')):
                Date.append(date)
                Amount.append(amount)
                Balance.append(balance)
        except:
            k += 1
        i += 1
    print(pdf_path)

df = pd.DataFrame({'Date': Date,
                    'Amount': Amount,
                    'Balance': Balance})
print(df)
df.to_excel('result.xlsx', header=True, index=False)
    
