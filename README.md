# Testing-SS-API
This repository links Smarsheet (SS) API with gutendex data, for verify and update(if it's necesary) the data contained in Smarsheet's sheet.

This script is linking Smarsheet API with Gutendex data for simple works as verification and update rows. 

In the introduction part important variables are declarated, also, the Smarsheet module are imported with its respective key of authorization(token).

## Methods

### 'get_cell_by_column_name': 
takes as parameters, the name of a column and specific row of SS sheet. the function obtains column id using its name, and search the cell value in the row that croos with the specified column.

### 'summary':
builds a summary wich contains the information of the first ` n ` (e.g. 25) pages of books in the Gutendex server, based on its keys (e.g, id, authors, title...) and returns a summary structure with the information specified.

### 'evaluate_and_update_rows':
receive as parameters, the sheet and the summary of reference.

This method delete all rows that no has an id, after that, takes the sheet row by row  and evaluate the cell values with summary values, if the values ar equal don't take action, but, if are different check if the cell are ` None ` or not. In  the first case (` None ` cells), builds a new row with its appropiate values in the summary. In the second case, replace the cell values with the correct value of summary. Finally, in both cases the method update the rows of sheet.
At the end, return a `list` wich contains, number of rows verfied, number of rows updated and another ` list ` with all of books ids in the sheet.

### 'append_new_rows':
takes as parameters, the summary created with ` summary ` and the ` list ` of books ids in the sheet returned in ` evaluate_and_update_rows `. 

first, the method check books ids in the summary that are not in the sheet, after, finds the values based on the `id_to_append ` and appends to the sheet, finally, update the sheet with `.add_rows`.

Returns the updated sheet.

## Test

### 'if __name__ == "__main__"':
structure used to execute all script, here all methods are called and tested, also contains indicative messages wich shows the start, progress and final of the execution.


