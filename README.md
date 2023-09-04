# MailSorting
Used for looking at and retrieving files from mail. 
Includes a Financial Dashboard template application for personal finance visualization.

## MailSorting 
In this case it is used for retrieving .xml and .pdf files, focused on getting information from .xml files to gather information related to taxes, creating a .csv file containing all information.
Contains multiple files customizable for each application [should be related to .xml files and retrieving subtotals/tax/totals]

## Dashboard
Uses main.py as backend for retreiving .csv data from each month. 
If file has not been created, it runs main.py to get the information and then displays it. 
If file was created before, it directly retrieves information from .csv file.
