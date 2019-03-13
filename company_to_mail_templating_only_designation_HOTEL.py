import pandas as pd
from mailmerge import MailMerge

def main():
    df = pd.read_csv('4 stars Hotels sent colored as of Feb 2019.csv', encoding ='ISO-8859-1')
    df = df.astype(str)
    
    template = 'Hotel Letter Template.docx'
    positions = ['COO/General Manager', 'HR Manager', 'Procurement Head']
    for each_row in df.iterrows():
        
        for position in positions:
            document = MailMerge(template)

            receiver_name = position
            company_address = each_row[1].address
            print (company_address)
            company = each_row[1].company
            print (company)
            
            document.merge(
                    name = str(receiver_name),  
                    company_name = str(company),
                    address = str(company_address))
            
            position = [p for p in position.split('/')][0]
            document.write(f"2nd_batch_hotels/{company}-{position}.docx")
            document.close()
            
if __name__ == '__main__':
    main()
