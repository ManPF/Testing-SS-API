# Testing-SS-API
This repository links Smarsheet(SS) API with gutendex data, for verify and update(if it's necesary) the data contained in Smarsheet's sheet.

This script is linking Smarsheet API with Gutendex data for simple works as verification and update rows. 

In the introduction part important variables are declarated, also, the Smarsheet module are imported with its respective key of authorization(token).

## Methods

#### 'get_cell_by_column_name': 
takes as parameters, the name of a column and specific row of SS sheet. the function obtains column id using its name, and search the cell value in the row that croos with the specified column.

### 'summary':
builds a summary wich contains the information of the first ` n ` pages of books in the Gutendex server, based on its keys (e.g, id, authors, title...) and returns a summary structure with the information specified.

### 

