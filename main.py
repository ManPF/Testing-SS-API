import smartsheet
import logging
import os
import json
import requests
import pandas as pd
import openpyxl

workspace = 1234567890 #WS ID
sheetid=9876543210 #Sheet ID
_dir = os.path.dirname(os.path.abspath(__file__))

column_map = {} #dict of columns ids as a value and its names as a key

with open(_dir + "/myfile.txt") as token: #import the token of SS saved in myfile.txt (create the file with your own token)
    os.environ['SMARTSHEET_ACCESS_TOKEN'] = token.read()
    #print(token.read())

smart = smartsheet.Smartsheet()

smart.errors_as_exceptions(True)

logging.basicConfig(filename='rwsheet.log', level=logging.INFO)

#print(json.dumps(data, indent=4))

def get_cell_by_column_name(row, column_name):

    """_get_cell_by_column_name_

    Args:
        row (SmarsheetModel): object from Smarsheet Sheet, a row.
        column_name (_str_): name of specific column of sheet.

    Returns:
        _str_: cell value of specific row and column
    """

    column_id = column_map[column_name]
    return row.get_column(column_id)

def evaluate_and_update_row(sheet, dict): 

    """_evaluate_and_update_row_

    Args:
        sheet (_smarsheet_model_): Smarsheet sheet obtained by id and previously imported
        dict (_dict_): dict structure (summary) created with _summary_ method.

    Returns:
        _list_: list with 3 values, 1st and 2nd int numbers, 3rd list of ids (_str_).
    """

    save_id = 0
    rows_procs = []
    rows_ver = 0
    rows_upd = 0
    rows_del = 0
    id_in_sheet = []

    for source_row in sheet.rows: #access to 'n' row by position & give it to 'evaluate_and_update_row' function, return # columns updated & verfied
        #print(len(sheet.rows))
        rows_ver += 1 
        id_cell = get_cell_by_column_name(source_row, 'Column1')
        id_value=id_cell.display_value
        if id_value is None or id_value in id_in_sheet or id_value not in list(dict.keys()):
            rows_del += 1
            smart.Sheets.delete_rows(sheetid,source_row.id)
        else:
            id_in_sheet.append(id_value)
            #VERIFICATION
            for column in list(column_map.keys()): #making a list of 'column_map' keys
                #print(list(column_map.keys())[2])
                status_cell = get_cell_by_column_name(source_row, column)
                status_value = status_cell.display_value
                #print(status_value)
                if column == 'Column1':
                    save_id = status_value
                    test = dict.get(save_id)
                else:
                    #print(column, status_value)
                    testing = test.get(column)
                    #print(type(testing),type(status_value))
                    if len(testing) != 0:
                        if str(testing) != status_value: #verifiying sheet values with dict values
                            #UPDATE  
                            rows_upd += 1
                            if status_value is not None:
                                # Build new cell value
                                new_cell = smart.models.Cell()
                                new_cell.column_id = column_map.get(column)
                                new_cell.value = str(testing)

                                # Build the row to update
                                new_row = smart.models.Row()
                                new_row.id = source_row.id
                                new_row.cells.append(new_cell)
                                sheet = smart.Sheets.update_rows(sheetid, new_row)

                            else: #updating None cells
                                new_row = smart.models.Row()
                                new_row.id = source_row.id
                                new_row.cells.append({'column_id':column_map.get(column), 'value':str(testing)})
                                sheet = smart.Sheets.update_rows(sheetid, new_row)
                        else:
                            None
                    else:
                            # Build new cell value
                            new_cell = smart.models.Cell()
                            new_cell.column_id = column_map.get(column)
                            new_cell.value = "null"

                            # Build the row to update
                            new_row = smart.models.Row()
                            new_row.id = source_row.id
                            new_row.cells.append(new_cell)
                            sheet = smart.Sheets.update_rows(sheetid, new_row)
    rows_procs.append(rows_ver)
    rows_procs.append(rows_upd)
    rows_procs.append(id_in_sheet)
    print(str(rows_del) + " rows with None, unexisting or duplicated ids deleted ")  
    return rows_procs
            
def append_new_rows(test, k):
    """_append_new_rows_

    Args:
        test (_dict_): same _dict_ parameter as in _evaluate_and_update_row_ method.
        k (_list_): list of ids (_str_) returned _evaluate_and_update_row_.

    Returns:
        _smarsheet_model_: updated Smarsheet sheet with new rows.
    """

    row_add = 0
    id_to_append=list(set(test.keys()) - set(k))
    rows_to_append=[]  
    for j in id_to_append:
        row_add += 1
        row_a = smartsheet.models.Row()
        row_a.to_top = True
        for i in list(column_map.keys()): #accesing to column's ids using the name
            if i =='Column1':
                row_a.cells.append({'column_id':column_map.get('Column1'), 'value':j})
            else:
                row_a.cells.append({'column_id':column_map.get(i), 'value': str(test[j][i])})#building new rows with column id and taking the value of dict 
        #print('Succesfully Added Row ' + str(j))
        rows_to_append.append(row_a) 
    updated_sheet = smart.Sheets.add_rows(sheetid, rows_to_append) #updating the sheet with the new row using ID
    print(str(row_add) + " new rows have been added")
    print("Total rows: " + str(len(sheet.rows)+row_add))
    return updated_sheet

def summary(keys):
    """_summary_

    Args:
        keys (_list_): list of keys to obtained from Gutendex

    Returns:
        _dict_: summary structure with information about books based on keys entered.
    """
    response = requests.get(url = "https://gutendex.com/books/?sort=ascending")# upload the dataset with ascending sort
    data = response.json()

    next = response.json()["next"]

    all_pages = {}
    all_pages[1] = response.json()["results"]
    test={}

    count_pages = 1
    while count_pages != 2: #taking the first 25 pages of books.

        count_pages +=1
        response = requests.get(url = next)
        data = response.json()

        next = response.json()["next"]
        all_pages[int(count_pages)] = response.json()["results"]
        listkeys = all_pages.keys()
    aux = {}
    k = 0
    for i in listkeys:
        for j in all_pages.get(i): #get dict 'j' by 'i' key of 'all_pages' dict
            for l in range(len(keys)): 
                #print(j)
                aux[keys[l]] = j[keys[l]] #assign to 'aux' dict te values of 'j' based on key
            k += 1
            test[str(j['id'])] = dict(aux)
                #print(aux)
    #print(json.dumps(test, indent=4))
    #print(len(test))
    #print(test[200]['title'],test[200]['authors'][0]['name'])

    df = pd.DataFrame(data = test)
    df = (df.T)

    return test

if __name__ == "__main__":

    print("Starting ...")

    sheet = smart.Sheets.get_sheet(sheetid) #import the sheet using sheet id
    print("Sheet imported Succesfully")
    print("Processing...")
    for column in sheet.columns:#adding columns id and names from sheet to column_map dict
        column_map[column.title] = column.id
    #print(column_map)

    print("Columns added Succesfully")
    print("Processing...")

    test = summary(['title','authors']) #using the summary function to build a summary with the keys assigned
    #print(test.keys())
    #print(set(test.keys())-set(id_in_sheet))

    print("Summary for evaluation created")
    print("Processing...")

    k = evaluate_and_update_row(sheet, test)
    print('Succesfully Verified ' + str(k[0]) + ' rows, & Updated ' + str(k[1]) + ' rows.')

    print("Processing...")

    new_sheet = append_new_rows(test,k[2])

    #print(new_sheet.data)
    print("Done")

else:
    print("File was imported")
    #print(id_in_sheet)
