# from helpers.excel_manipulator import excel_to_csv
# from helpers.csv_manipulator import clean_csv_manual
from database_actions import *

def main():
    excel_file = "/Users/estefaniasanchez/Desktop/Projects/python/csvtest/revised_Economic_Vitality_MSA_Data.xlsx"
    write_location = '/Users/estefaniasanchez/Desktop/Projects/python/csvtest/'
    table_name = "[ev].[Median Household Income_Automated]"

    localDb = Database(True)
    # localDb.getConnectionStatus()
    # localDb.getInfoFromTable("[ev].[Median Household Income_Automated]")
    # localDb.__startConnection
    localDb.inputDataWithUserIntoDb(excel_file, write_location)
    # localDb.inputDataIntoDb(excel_file, write_location)

    # test=[('foo','bar', 'ham'), ('hoo','far', 'bam')]
    # values= '(' + ('?,'*len(test))[:-1] + ')'
    # INSERT_SQL_STATEMENT = 'INSERT INTO [{table_name}] ({columns}) VALUES ({values})'
    # second_sql = INSERT_SQL_STATEMENT.format(table_name = economicVitality.get('test_name'), columns = "columns1, colums2", values='(' + ('?,'*len(test))[:-1] + ')')
    # print(second_sql)
    


    # csv_file = "/Users/estefaniasanchez/Desktop/Projects/tbp/completedtemplates/economic_vitality copy/Advanced Industry Job Share Copy.csv"
    # clean_csv_directory = "/Users/estefaniasanchez/Desktop/Projects/tbp/completedtemplates/economic_vitality copy/"
    
    # clean_csv_manual(csv_file, 6, clean_csv_directory)
    # excel_to_csv(excel_path, clean_csv_directory)


if __name__ == '__main__':
    main()