import pandas as pd


def left(s, amount):
    """
    Consumes a string (s) and returns (amount) characters from the left
    :param s: str - The string variable the function consumes
    :param amount: int - The number of characters
    :return: str - left indexed
    """
    return s.str[:amount]


def right(s, amount):
    """
    Consumes a string (s) and returns (amount) characters from the Right
    :param s: str - The string variable the function consumes
    :param amount: int - The number of characters
    :return: str - Right indexed
    """
    return s.str[-amount:]


def main():
    """
    Clean the costing data for Nissan Wages and write pivot table to file for Detailed Paylist In Excel
    """
    raw_data = pd.read_csv(
        r'Z:\Payroll\Clients\Nissan - NI100\1554 - Nissan South Africa(Pty)Ltd W\2021\10-Dec 2020\Run 1 (04-12-2020)\Extracts\Company.xls',
        delimiter=';')

    df = raw_data.copy()

    df.drop(['Sequence Number', 'Paypoint', 'Initials', 'Period From', 'Period To', 'Birth Date', 'Gender',
             'ID Number', 'Passport number', 'Tax Reference number', 'Address Line 1',
             'Address Line 2', 'Address Line 3', 'Post Code', 'Tax Start Date',
             'Contract End Date', 'Bank Name', 'Bank Branch',
             'Bank Code', 'Bank Account Number', 'Pay Date', 'Job Title', 'Company', 'Company Number', 'Branch',
             'Region',
             'Department', 'Location', 'Division', 'Subdivision', 'Reports To',
             'ZodeCode', 'JobGradeCode', 'TermReason', 'EETermReason',
             'Employee Status', 'Leave Due', 'Leave Accrued', 'Cash Component',
             'Employer Contribution', 'Components paid in cash', 'Total Deductions',
             'Total Earnings', 'Gross Pay', 'Hours', 'Amount This Tax Year', 'Age', 'Race', 'Months of Service',
             'Permanent Employee', 'OCC Level', 'Cycle Days', 'Standard Hours'], axis=1, inplace=True)

    df = df.dropna(how='all')

    df.drop(df[df['Amount This Month'] == 0].index, inplace=True)

    df = df.astype({'Employees Number': str})

    code_description = df['Code'].astype(str) + '-' + df['Description']

    cc_minor = left(df['CCMajor'].astype(str), 8)
    cc_interim = right(df['CCMajor'].astype(str), 3)

    df = pd.concat([df, code_description, cc_interim, cc_minor], axis=1)

    column_names = ['Employees Name', 'Employees Surname', 'Employees Number', 'Group Date',
                    'Termination Date', 'Job Grade', 'CCMajor', 'CCInter', 'Total Package',
                    'Net Pay', 'Amount This Month', 'Code', 'Description', 'Code_Description', 'CC Minor', 'CC Interim']
    df.columns = column_names

    net_pay = df.copy()
    net_pay.drop_duplicates('Employees Number', keep='last', inplace=True)
    net_pay.drop_duplicates('Employees Number', keep='last', inplace=True)

    print(net_pay['Employees Number'].nunique())

    net_pay.drop(['Amount This Month'], axis=1, inplace=True)
    net_pay_cols = ['Employees Name', 'Employees Surname', 'Employees Number', 'Group Date',
                    'Termination Date', 'Job Grade', 'CCMajor', 'CCInter', 'Total Package',
                    'Amount This Month', 'Code', 'Description', 'Code_Description', 'CC Minor',
                    'CC Interim']

    net_pay.columns = net_pay_cols

    net_pay['Description'] = 'Net Pay'
    net_pay['Code'] = 'C'
    net_pay['Code_Description'] = 'C-Net Pay'

    df_processed = df.append(net_pay)
    df_processed = df_processed.fillna(0)

    df_pivot = pd.pivot_table(df_processed,
                              index=['Employees Number', 'CC Interim', 'CC Minor', 'Job Grade', 'Employees Name',
                                     'Employees Surname', 'Group Date', 'Termination Date', 'Total Package'],
                              columns=['Code_Description'], values=['Amount This Month'], fill_value=0)

    dff = df_pivot.copy()
    print(dff.head())
    # df_pivot.to_csv(
    #     r'Z:\Payroll\Clients\Nissan - NI100\1554 - Nissan South Africa(Pty)Ltd W\2021\10-Dec 2020\Run 1 (04-12-2020)\Extracts\Pivot of Company.csv')


if __name__ == '__main__':
    main()
