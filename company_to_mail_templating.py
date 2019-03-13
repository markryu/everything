import pandas as pd
from mailmerge import MailMerge

template = 'Mail Letter Template.docx'

df = pd.read_csv('csv_version_list_batch(2).csv', encoding ='ISO-8859-1')
positions = ['CEO', 'COO/General Manager', 'HR Manager', 'Procurement Head', 'Sales Manager', 'Admin Manager']


df = df[df.number > 0]
df = df.astype(str)
print (df.dtypes)

for each_row in df.iterrows():
    
    for position in positions:
        
        document = MailMerge(template)
        # print(document.get_merge_fields())
        
        receiver_name = position
        prefix_name = ''
        receiver_last_name = position
        company_address = each_row[1].address
        company = each_row[1].company
        
        if len(each_row[1][position]) > 3:
            receiver_name = each_row[1][position]
            prefix_name = each_row[1][f"{position} Prefix"]
            receiver_last_name = [i for i in receiver_name.split(' ')][-1] 
            if receiver_last_name in ['Jr.', 'jr', 'JR', 'Jr', 'sr', 'Sr.', 'Sr', 'SR', 'III', ' ', '  ', '   ']:
                receiver_last_name = [i for i in receiver_name.split(' ')][-2]
            
        document.merge(
                name = str(receiver_name),  
                company_name = str(company),
                address = str(company_address),
                prefix = str(prefix_name),
                last_name = "  " + receiver_last_name)
        
        position = [p for p in position.split('/')][0]
        document.write(f"test-results/{company}-{position}.docx")
        document.close()