import csv
import os

def create_clean_csv(values_array, sheetname, write_directory):
    # final_data = []
    # clean_row = []
    # column_counter = 0

    with open(write_directory + sheetname, "w", newline='') as clean_file:
        writer = csv.writer(clean_file)

        for i in range(len(values_array)):
            writer.writerow(values_array[i])
    
    return clean_file
    
                
# This function assumes that extra commas are always produced at the end of each row
# def clean_csv_automated(directory):
#     file_counter = 1
#     for file in os.listdir(directory):
#         first_pass = True
#         init_column_amount = 0

#         filename = os.fsdecode(file)
#         if filename.endswith(".csv"):
#             full_path = directory + "/" + filename
#             print(full_path)

#             clean_data = []
#             final_data = []
#             clean_row = []
#             column_counter = 0

#             with open(full_path, newline='') as csv_file:
#                 reader = csv.reader(csv_file)
#                 for row in reader:
#                     for item in row:
#                         if item != "":
#                             clean_data.append(item)
#                             init_column_amount += 1
#                         else:
#                             if first_pass:
#                                 final_column_amount = init_column_amount
#                                 first_pass = False

#             with open(directory + "/" + "test_" + str(file_counter), "w", newline='') as clean_file:
#                 writer = csv.writer(clean_file)

#                 for i in range(len(clean_data) + 1):
#                     if i == len(clean_data):
#                         final_data.append(clean_row)
#                         writer.writerow(clean_row)
#                         file_counter += 1
#                         break
#                     if column_counter < final_column_amount:
#                         clean_row.append(clean_data[i])
#                         column_counter += 1
#                     else:
#                         final_data.append(clean_row)
#                         writer.writerow(clean_row)  
#                         clean_row = []
#                         clean_row.append(clean_data[i])
#                         column_counter = 1

# This function can be used to clean a csv produced by Excel as sometimes those csv files contain multiple commas at the end of each row. 
def clean_csv_manual(file, columns, write_directory):
    clean_data = []
    clean_row = []
    column_counter = 0
    filename = "clean_file"

    with open(file, newline='') as csv_file:
        reader = csv.reader(csv_file)
        
        for row in reader:
            for item in row:
                if item != "":
                    if column_counter < columns:
                        clean_row.append(item)
                        column_counter += 1
                    else:
                        clean_data.append(clean_row)
                        clean_row = []
                        clean_row.append(item)
                        column_counter = 1
        # Appends the last clean_row of the file
        clean_data.append(clean_row)
            
    create_clean_csv(clean_data, filename, write_directory)





    



    