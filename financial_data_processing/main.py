##
#  This is a redacted version of the code I use to extract and process data in my local environment.
##

from datetime import datetime

import pandas as pd

from financial_data_processing.utils import *


def main():
    """
    Clean the financial data from a payroll system extract
    """

    # global variables
    _costings = r'RAW_DATA'
    _keep_cols = ['Employees Name', 'Employees Surname', 'Employees Number', 'Group Date',
                  'Termination Date', 'Job Grade', 'Location', 'CCInter', 'Total Package',
                  'Net Pay', 'Amount This Month', 'Code', 'Description']

    raw_data = pd.read_csv(_costings, delimiter=';')
    df = raw_data.copy()

    # drop all columns but ones specified & drop all na
    df.drop(df.columns.difference(_keep_cols), axis=1, inplace=True)
    df = df.dropna(how='all')

    # keep unique ids as string
    df = df.astype({'Employees Number': str})

    # create new columns with refactored data and add them to the dataframe
    code_description = df['Code'].astype(str) + '-' + df['Description']
    Department = left(df['Location'].astype(str), 8)
    cc_interim = right(df['Location'].astype(str), 3)
    df = pd.concat([df, code_description, cc_interim, Department], axis=1)

    # define schema to match below net_pay schema
    column_names = ['Employees Name', 'Employees Surname', 'Employees Number', 'Group Date',
                    'Termination Date', 'Job Grade', 'Location', 'CCInter', 'Total Package',
                    'Net Pay', 'Amount This Month', 'Code', 'Description', 'Code_Description', 'Location', 'CC Interim']
    df.columns = column_names

    # define net_pay dataframe with a single occurrence from the employees multiple line entries
    net_pay = df.copy()
    net_pay.drop_duplicates('Employees Number', keep='last', inplace=True)

    print(net_pay['Employees Number'].nunique())

    # define schema to match above dataframe schema
    net_pay.drop(['Amount This Month'], axis=1, inplace=True)
    net_pay_cols = ['Employees Name', 'Employees Surname', 'Employees Number', 'Group Date',
                    'Termination Date', 'Job Grade', 'Location', 'CCInter', 'Total Package',
                    'Amount This Month', 'Code', 'Description', 'Code_Description', 'Department',
                    'CC Interim']
    net_pay.columns = net_pay_cols

    # adding literals and new columns to net_pay
    net_pay['Description'] = 'Net Pay'
    net_pay['Code'] = 'C'
    net_pay['Code_Description'] = 'C-Net Pay'

    # append both data frames with matching schemas
    df_processed = df.append(net_pay)
    df_processed = df_processed.fillna(0)

    # pivot to transpose descriptions to columns in order to balance
    df_pivot = pd.pivot_table(df_processed,
                              index=['Employees Number', 'CC Interim', 'Department', 'Job Grade', 'Employees Name',
                                     'Employees Surname', 'Group Date', 'Termination Date', 'Total Package'],
                              columns=['Code_Description'], values=['Amount This Month'], fill_value=0)

    date = datetime.now().strftime('%Y-%m-%d')
    df_pivot.to_csv(f'costings-{date}.csv')


if __name__ == '__main__':
    main()
