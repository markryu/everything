import pandas as pd
from mailmerge import MailMerge

def main():
    csv_filename = input('Enter csv filename: ')
    template_filename = input('Enter template filename: ')
    output_folder = input ('Enter output folder name: ')
    positions_needed = input('Enter Positions separated by comma (format important): ')
    df = pd.read_csv(f"{csv_filename}.csv", encoding ='ISO-8859-1')
    df = df.astype(str)
    
    template = f'{template_filename}.docx'
    positions = positions_needed.split(',')
    for each_row in df.iterrows():
            
        for position in positions:
            document = MailMerge(template)

            receiver_name = position
            company_address = each_row[1].address
            company = each_row[1].company

            document.merge(
                    name = str(receiver_name),  
                    company_name = str(company),
                    address = str(company_address))

            position = [p for p in position.split('/')][0]
            document.write(f"{output_folder}/{company}-{position}.docx")
            document.close()
            
if __name__ == '__main__':
    main()
