import csv



def load_csv_data() -> csv.reader:
    data_file_name = input("please provide the name of the csv file: ") #first we prompt for the name of the file
    with open(data_file_name, 'r', newline='') as csv_file:  #opens file and reads its contents
        data = list(csv.reader(csv_file))
        return data

