import pandas as pd
from mailmerge import MailMerge

def main():
    csv_filename = input('Enter csv filename: ')
    template_filename = input('Enter template filename: ')
    output_filename = input ('Enter output filename: ')
    positions_needed = input('Enter Positions separated by comma (format important): ')

    # template name without the docx
    template =f'{template_filename}.docx'
    # initiate document using the variables
    document = MailMerge(template)
    
    # csv file
    df = pd.read_csv(f'{csv_filename}.csv', encoding ='ISO-8859-1')
    df = df.astype(str)
    
    # positions needed
    # use choices from which positions to include when using only designation
    list_per_company_per_position = list()
    positions = positions_needed.split(',')
    for each_row in df.iterrows():

        for position in positions:
            company_address = each_row[1].address
            company = each_row[1].company
            receiver_name = position
    
            list_per_company_per_position.append({'receiver':receiver_name,
                             'address': company_address,
                             'company': company
                             })
    
    document.merge_rows('receiver', list_per_company_per_position)        
    # filename below
    document.write(f'{output_filename}.docx')
    document.close()

if __name__ == '__main__':
    main()
