import pandas as pd
import numpy as np 
import sqlite3
import shutil
import os
import boto3
import botocore
from IPython.core.magic import register_line_magic

global __AWS_ACCESS_KEY
global __AWS_SECRET_KEY
global __S3_BUCKET_NAME

global connection
global cursor
global database_name
global s3_client
global _sqldf

def configure_aws(aws_access_key_id,aws_secret_key,s3_bucket_name):
    """Configure AWS Credentials by passing the Access Key, Secret Key and Bucket Name"""
    global __AWS_ACCESS_KEY
    global __AWS_SECRET_KEY
    global __S3_BUCKET_NAME
    __AWS_ACCESS_KEY = aws_access_key_id
    __AWS_SECRET_KEY = aws_secret_key
    __S3_BUCKET_NAME = s3_bucket_name

def configure_aws():
    """Configure AWS Credentials from Environment Variables
    AWS ACCESS KEY : aws_key
    AWS SECRET KEY : aws_secret
    AWS Bucket Name : aws_bucket"""
    global __AWS_ACCESS_KEY
    global __AWS_SECRET_KEY
    global __S3_BUCKET_NAME
    __AWS_ACCESS_KEY = os.getenv('aws_key')
    __AWS_SECRET_KEY = os.getenv('aws_secret')
    __S3_BUCKET_NAME =  os.getenv('aws_bucket')

def connect_db(dbname):
    global connection
    global cursor
    global database_name
    global s3_client
    global __AWS_ACCESS_KEY
    global __AWS_SECRET_KEY
    global __S3_BUCKET_NAME
    database_name = dbname
    s3_client = boto3.client('s3', aws_access_key_id=__AWS_ACCESS_KEY, aws_secret_access_key=__AWS_SECRET_KEY)
    if not os.path.exists("./.sqldb"):
        os.mkdir("./.sqldb")
    try:
        s3_client.download_file(__S3_BUCKET_NAME, f"sql_db/{dbname}.db", f"./.sqldb/{dbname}.db")
        os.chmod(f"./.sqldb/{dbname}.db", 0o666)
    except botocore.exceptions.ClientError as e:
        print(f"Database not found in S3, creating new database {dbname}")
    # Create Connection
    connection = sqlite3.connect(f'./.sqldb/{dbname}.db')
    cursor = connection.cursor()
    database_name = dbname
    print(f"Successfully connected to database : {dbname}")

def show_tables():
    try:
        query = "SELECT name FROM sqlite_master WHERE type='table';"
        tables_df = pd.read_sql(query, connection)
        return tables_df
    except Exception as e:
        print(e)

def describe_table(table_name):
    try:
        query = f"PRAGMA table_info({table_name});"
        table_info = pd.read_sql(query, connection)
        table_description = table_info[['name', 'type']].rename(columns={'name': 'Column', 'type': 'Data Type'})
        return table_description
    except Exception as e:
        print(e)

def run_sql_script(sql):
    try:
        cursor.executescript(sql)
        connection.commit()  # Save changes to the database
    except Exception as e:
        print(e)

@register_line_magic
def sql(sqlquery):
    global _sqldf
    try:
        _sqldf = pd.read_sql(sqlquery, connection)
        connection.commit() 
        return _sqldf
    except Exception as e:
        print(e)

def run_sql_file(filename):
    with open(filename, 'r') as file:
        sql_script = file.read()

    # Run the SQL script
    run_sql_script(sql_script)

def close_connection():
    cursor.close()
    connection.close()
    # Copy DB to teamspace
    s3_client.upload_file(f"./.sqldb/{database_name}.db", __S3_BUCKET_NAME, f"sql_db/{database_name}.db")
    os.remove(f"./.sqldb/{database_name}.db")