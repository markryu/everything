import pandas as pd
from mailmerge import MailMerge

template = 'template for sticker.docx'

df = pd.read_csv('csv_version.csv', encoding ='ISO-8859-1')
positions = ['Ceo', 'Coo/General Manager', 'HR Manager', 'Procurement Head', 'Sales Manager', 'Admin Manager']

document = MailMerge(template)
print(document.get_merge_fields())

df = df[df.number > 0]
df = df.astype(str)
print (df.dtypes)

all_items = list()
document = MailMerge(template)
print(document.get_merge_fields())

for each_row in df.iterrows():
    
    for position in positions:
        
        company_address = each_row[1].address
        company = each_row[1].company

        if len(each_row[1][position]) > 3:
            receiver_name = each_row[1][position]
            prefix_name = each_row[1][f"{position} Prefix"]
            receiver_name = prefix_name + ' ' + receiver_name

        else:
            receiver_name = position
            prefix_name = ''
            receiver_last_name = position
            
        print (receiver_name)
        all_items.append({'receiver':receiver_name,
                         'address': company_address,
                         'company': company
                         })

document.merge_rows('receiver', all_items)        
document.write('test-final-table.docx')
document.close()
