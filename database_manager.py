from db_credentials import database_name, server_name

connection_URI = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server_name};DATABASE={database_name};Trusted_Connection=yes;'
