import sys
import pyodbc
import configparser
import csv
import ntpath

from helpers.excel_manipulator import *
from helpers.tables import *

# TODO Error handling for the connection
class Database:
    def __init__(self, localDb=False):
        Config = configparser.ConfigParser()

        if localDb:
            Config.read("local_config.ini") 
            config_section = 'localdb'
        else:
            Config.read("config.ini") 
            config_section = 'SQLServerStage'

        params = 'DRIVER=' + Config.get(config_section, 'driver') + ';' \
                      'SERVER=' + Config.get(config_section, 'hostname') + ';' \
                      'PORT=' + Config.get(config_section, 'port') + ';' \
                      'DATABASE=' + Config.get(config_section, 'database') + ';' \
                      'UID=' + Config.get(config_section, 'username') + ';' \
                      'PWD=' + Config.get(config_section, 'password') + ';'
        
        self.cnxn = self.__startConnection(params, localDb)
        self.getConnectionStatus
        self.cursor = self.cnxn.cursor()

    def __startConnection(self, params, localDb):
        if localDb:
            cnxn = pyodbc.connect(params + 'TrustServerCertificate=yes;')
        else: 
            cnxn = pyodbc.connect(params)
        return cnxn

    def getConnectionStatus(self):
        if self.cnxn:
            print("Connection is open")
        else:
            print("Connection is closed")
    
    def getInfoFromTable(self, table_name):
        self.cursor.execute("SELECT * FROM " + table_name)
        rows = self.cursor.fetchall()
        for row in rows:
            print(row)

    # The table name has to follow the following format: [ev].[Median Household Income_Automated] (for local dev - Is this the case for the database in the server as well?)
    def inputDataIntoDb(self, excel_file_path, write_location):
        INSERT_SQL_STATEMENT = 'INSERT INTO {table_name} ({columns}) VALUES ({values})'
        csv_files = excel_to_csv(excel_file_path, write_location)

        for file in csv_files:
            print("File being processed: " + file)
            input_data = []
            num_columns = 0
            csv_table_name = ntpath.basename(file).replace(".csv", "")
            print(csv_table_name)

            try: 
                with open(file, newline='', encoding='utf-8') as csv_file:
                    reader = csv.reader(csv_file)
                    for indx, csv_row in enumerate(reader):
                        if(indx == 0):
                            # Eliminates the square brackets of the list representation and the quotes from the csv row
                            column_names = str(csv_row)[1 : -1].replace("'", "")
                            num_columns = len(csv_row)
                        else:
                            data_row = tuple(csv_row)
                            input_data.append(data_row)

                    # The executemany method requires the sql statement to be formatted in the following way: INSERT INTO table_name (column1, column2, column3) VALUES (?, ?, ?) 
                    # ('?,'*len(num_columns))[:-1] is used to create the number of question marks needed for the sql statement
                    sql_statement_for_table = INSERT_SQL_STATEMENT.format(table_name = economicVitality.get(csv_table_name), columns = column_names, values=('?,'*num_columns)[:-1])
                    print(sql_statement_for_table)
                    self.cursor.fast_executemany = True
                    self.cursor.executemany(sql_statement_for_table, input_data)
                    self.cnxn.commit()
                    break    
            except IOError as e:
                print("I/O error({0}): {1}".format(e.errno, e.strerror))
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise


    # The table name has to follow the following format: [ev].[Median Household Income_Automated] (for local dev - Is this the case for the database in the server as well?)
    # With this implementation, the first csv file is created and then added to the database, then the next csv file is created and added to the database, etc.
    def inputDataWithUserIntoDb(self, excel_file_path, write_location):
        INSERT_SQL_STATEMENT = 'INSERT INTO {table_name} ({columns}) VALUES ({values})'

        for file in excel_to_csv_generator(excel_file_path, write_location):
            print("File being processed: " + file)
            input_data = []
            num_columns = 0
            csv_table_name = ntpath.basename(file).replace(".csv", "")
            print(csv_table_name)

            with open(file, newline='') as csv_file:
                reader = csv.reader(csv_file)
                for indx, csv_row in enumerate(reader):
                    if(indx == 0):
                        # Eliminates the square brackets of the list representation and the quotes from the csv row
                        column_names = str(csv_row)[1 : -1].replace("'", "")
                        num_columns = len(csv_row)
                    else:
                        data_row = tuple(csv_row)
                        input_data.append(data_row)

                # The executemany method requires the sql statement to be formatted in the following way: INSERT INTO table_name (column1, column2, column3) VALUES (?, ?, ?) 
                # ('?,'*len(num_columns))[:-1] is used to create the number of question marks needed for the sql statement
                sql_statement_for_table = INSERT_SQL_STATEMENT.format(table_name = economicVitality.get(csv_table_name), columns = column_names, values=('?,'*num_columns)[:-1])
                print(sql_statement_for_table)
                self.cursor.fast_executemany = True
                # TODO: below line is causing problems 
                self.cursor.executemany(sql_statement_for_table, input_data)
                self.cnxn.commit()
                
                # user input should go here to allow continuation to the next file
                print("Check the data was inputted correctly into the database")
                print("File : " + file + " was processed. Table name: " + economicVitality.get(csv_table_name)) 
                user_input = input("Continue to the next file? (y/n): ")
                if user_input == 'y':
                    continue
                else:
                    break
                 


                    