from readercsv import load_csv_data
from connection_pool import get_connection
import database


def sql_uploader():
    data = load_csv_data()
    database_table_name = input("please provide required name of the PostgreSQL table: ")
    columns_with_datatypes = []
    print("provide expected type of these columns: ")
    for column in data[0]: #we get first item bcs it is a list of columns names
        datatype = input(column + ": ")
        columns_with_datatypes.append(f"{column} {datatype}")
    with get_connection() as connection:
        database.create_table(connection, database_table_name, ", ".join(columns_with_datatypes))
        database.add_data(connection, database_table_name, data)

def add_position():       #we will:
    with get_connection() as connection:
        tables_names = database.select_tables_names(connection, False)     #print available tables in format {number} : {table name}, we set x argument of `select_tab....` as False to get data returned in default format using default cursor factory
    tables_count = range(1, 1 + len(tables_names))       ##----------i could use here RealDict cursor factory, but how? i tried to implement it, but things seemed to happen illogicaly and i didn't know how to get data from generator in list comprehension (i decided it was worse to use for loop)
    dict_tables = dict(zip(tables_count, tables_names))
    del tables_names
    print("\n".join("{}:\t{}".format(k, v[0]) for k, v in dict_tables.items()))    #-------- i'm sure there is a better way to write ouput in demanded format, but how?
    name_choice = input("Choose your table (input proper number): ")    #then ask user which table he want to add data to
    data_prompt = input("Do you want to upload data from a file (U) or manually (M) (one row accepted only)? U/M: ")       #manually or from a file
    if data_prompt.lower() == 'u':
        data = load_csv_data()
    elif data_prompt.lower() == 'm':
        values = []
        while (information := input("Input value of single column, input nothing when you are done: ")):         #user can add manually a single row only
            values.append(information)
        data = [ ]      #we have to set proper type of data, since loading from csv returns data in specific format
        data.append(", ".join(values))
    else:
        print("Wrong Key!")
        return
    with get_connection() as connection:
        database.add_data(connection, *dict_tables[int(name_choice)], data)           #we need table to convey table's name and columns into SQL query

def list_tables():
    with get_connection() as connection:
        tables = database.all_tables(connection)
        for table in tables:
            print(table)



menu_prompt = """-- Menu --
1) Create new table and fill it with csv data
2) Add data to existing PostGreSQL table
3) List all the tables
6) Exit.

Enter your choice: """

menu_options = {
    '1': sql_uploader,
    '2': add_position,
    '3': list_tables,
}

def menu():
    while (selection := input(menu_prompt)) != "6":
        try:
            menu_options[selection]()
        except KeyError:
            print("you input wrong key!")

menu()