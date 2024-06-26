import psycopg2
import pandas as pd
import openpyxl
import os
import bcrypt
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
import psycopg2.errorcodes
import uuid
import base64
from pydantic import BaseModel
import logging
import traceback
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from datetime import timedelta,timezone
import jwt
import secrets
from fastapi.responses import FileResponse
import pandas as pd
import uuid
from dotenv import load_dotenv
import os

# Load the .env file

# from dotenv import load_dotenv,find_Dotenv
logger = logging.getLogger(__name__)

hostURL = 'http://localhost:8000'
ALG = 'HS256'
FILE_DIRECTORY = './downloads'

month_map = {
    1:"Jan",
    2:"Feb",
    3:"Mar",
    4:"Apr",
    5:"May",
    6:"Jun",
    7:"Jul",
    8:"Aug",
    9:"Sep",
    10:"Oct",
    11:"Nov",
    12:"Dec"
}

def logMessage(cursor: psycopg2.extensions.connection.cursor,query : str, arr: list = None):
    cursor.execute(query,arr)
    if arr is not None:
        return f'QUERY IS : <{cursor.mogrify(query,arr).decode("utf-8")}>'
    else:
        return f'QUERY IS : <{query}>'

# PostgreSQL database UR
#todo : need to source user, password and ip port from variables
load_dotenv()

# Get the value of DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL")

def getdata(conn: psycopg2.extensions.connection):
    return [
        usernames(conn),
        paymentmode(conn),
        entity(conn),
        paymentfor(conn),
        paymentreqstatus(conn)
    ]

def ifNotExist(criteria : str,table_name : str,conn: psycopg2.extensions.connection,value):
    try:
        with conn[0].cursor() as cursor:
            query = f"SELECT {criteria} FROM {table_name} WHERE {criteria} = %s"
            logMessage(cursor,query,(value,))
            s = len(cursor.fetchall())
            logging.info(s)
        if s!=0:
            return False
        else:
            return True
    except Exception as e:
        logging.info(traceback.print_exc())
        return False
def usernames(conn : psycopg2.extensions.connection):
    try:
        with conn.cursor() as cursor:
            query = 'SELECT firstname,lastname,id,username FROM usertable order by firstname'
            msg = logMessage(cursor,query)
            logging.info(msg)
            data = cursor.fetchall()
        if data:
            res = {}
            for i in data:
                res[i[2]] = f'{i[0]} {i[1]}'
        return res
    except Exception as e:
        print(traceback.print_exc())
        return None

def paymentfor(conn: psycopg2.extensions.connection):
    try:
        with conn.cursor() as cursor:
            query = 'SELECT DISTINCT id,name from payment_for order by name'
            msg = logMessage(cursor,query)
            logging.info(msg)
            data = cursor.fetchall()
        res = {}
        for i in data:
            res[i[0]] = i[1]
        # logging.info(res)
        return res
    except Exception as e:
        logging.info(traceback.print_exc())
        logging.info(f"Error is {e}")
        return None
    
def paymentreqstatus(conn: psycopg2.extensions.connection):
    try:
        with conn.cursor() as cursor:
            query = 'SELECT DISTINCT id,status from z_paymentrequeststatus order by status'
            msg = logMessage(cursor,query)
            logging.info(msg)
            data = cursor.fetchall()
        res = {}
        for i in data:
            res[i[0]] = i[1]
        # logging.info(res)
        return res
    except Exception as e:
        logging.info(traceback.print_exc())
        logging.info(f"Error is {e}")
        return None


def paymentmode(conn: psycopg2.extensions.connection):
    try:
        with conn.cursor() as cursor:
            query = 'SELECT DISTINCT id,name from mode_of_payment order by name'
            msg = logMessage(cursor,query)

            data = cursor.fetchall()
        res = {}
        for i in data:
            res[i[0]] = i[1]
        # logging.info(res)
        return res
    except Exception as e:
        logging.info(traceback.print_exc())
        logging.info(f"Error is {e}")
        return None
def entity(conn):
    try:
        with conn.cursor() as cursor:
            query = 'SELECT DISTINCT id,name from entity order by name'
            msg = logMessage(cursor,query)
            logging.info(msg)
            data = cursor.fetchall()
        res = {}
        for i in data:
            res[i[0]] = i[1]
        # logging.info(res)
        return res
    except Exception as e:
        logging.info(traceback.print_exc())
        logging.info(f"Error is {e}")
        return None

def roles(conn):
    try:
        with conn.cursor() as cursor:
            query = 'SELECT DISTINCT id,role_name from roles order by role_name'
            msg = logMessage(cursor,query)
            logging.info(msg)
            data = cursor.fetchall()
        res = {}
        for i in data:
            res[i[0]] = i[1]
        # logging.info(res)
        return res
    except Exception as e:
        logging.info(traceback.print_exc())
        logging.info(f"Error is {e}")
        return None


def filterAndPaginate(db_config,
                      required_columns,
                      table_name,
                      filters=None,
                      sort_column=None,
                      sort_order='asc',
                      page_number=1,
                      page_size=10,
                      query = None,
                      whereinquery = False,
                      search_key = None):
    try:
        # Base query
        query_frontend = False
        if query is None:
            query = f"SELECT {','.join(required_columns)} FROM {table_name}"
            query_frontend = True
        # Adding filters
        where_clauses = []
        for column, filter_type, value in (filters or []):
            if value != '':
                if filter_type == 'startsWith':
                    where_clauses.append(f"lower({column}) LIKE '{value.lower()}%'")
                elif filter_type == 'endsWith':
                    where_clauses.append(f"lower({column}) LIKE '%{value.lower()}'")
                elif filter_type == 'contains':
                    where_clauses.append(f"lower({column}) LIKE '%{value.lower()}%'")
                elif filter_type == 'exactMatch':
                    where_clauses.append(f"lower({column}) = '{value.lower()}'")
                elif filter_type == 'isNull':
                    where_clauses.append(f"{column} is null")
                elif filter_type == 'isNotNull':
                    where_clauses.append(f"{column} is not null")
        # handle where clause and sorting
        if where_clauses and not whereinquery:
            query += " WHERE " + " AND ".join(where_clauses)
        elif where_clauses and whereinquery:
            query += " AND " + " AND ".join(where_clauses)
        if sort_column:
            query += f" ORDER BY {sort_column[0]} {sort_order}"
        # Handle pagination
        counts_query = query
        if page_number !=0 and page_size !=0 and search_key is None:
            # Calculate OFFSET
            offset = (page_number - 1) * page_size
            # Adding pagination
            query += f" LIMIT {page_size} OFFSET {offset}"
        else:
            pass
            # when page_number=0 and page_size=0
            # do not paginate - return all. This is
            # for downloading all the filtered data.

        logging.info(f'filtAndPaginate: Prepared final query [{query}]')
        # fetch results and return to caller
        conn = psycopg2.connect(db_config)
        cur = conn.cursor()
        cur.execute(query)
        logging.info(f"filtAndPaginate: Cursor message is {cur.statusmessage}")
        rows = cur.fetchall()
        cur = conn.cursor()
        cur.execute(counts_query)
        rows_for_counts = cur.fetchall()
        total_count = len(rows_for_counts)
        colnames = [desc[0] for desc in cur.description]
        logging.info(f'filterAndPaginate: Given filter yeilds <{total_count}> entries')
        cur.close()
        conn.close()

        if search_key is not None:
            search_results = []
            for row in rows:
                concatenated_row = " ".join( str(item) for item in row)
                if str(search_key).lower() in concatenated_row.lower():
                    search_results.append(row)
                else:
                    pass
            total_count = len(search_results)
            logging.info(f'filterAndPaginate: Given search key <{search_key}> yeilds <{total_count}> entries')
            start_index = (page_number - 1) * page_size
            end_index = start_index + page_size
            logging.info(f'filterAndPaginate: Given search key <{search_key}> yeilds <{total_count}> entries and before filtered rows are <{len(rows)}>')
            if start_index != end_index:
                rows = search_results[start_index:end_index]
            else:
                rows = search_results
            logging.info(f'filterAndPaginate: Given search key <{search_key}> yeilds <{total_count}> entries and after filtered rows are <{len(rows)}>')


        return {'data':rows, 'total_count' : total_count, 'message':'success', 'colnames':colnames}
    except Exception as e:
        logging.exception(traceback.print_exc())
        msg = str(e).replace("\n","")
        return {'data':None, 'message':f'exception due to <{msg}>'}

def generateExcelOrPDF(downloadType=None, rows=None, colnames=None,mapping = None):
    try:
        logging.info("Here")
        if mapping:
            colnames = [mapping[i] for i in colnames]
        df = pd.DataFrame(rows, columns=colnames)
        df.reset_index(inplace=True)
        df['index'] += 1
        df.rename(columns={"index":"Sr No."},inplace=True)
        filename = f'{uuid.uuid4()}.xlsx'
        fname = f'./downloads/{filename}'
        df.to_excel(fname, engine='openpyxl',index=False)
        logging.info(f'generated excel file <{fname}>')
        return filename
    except Exception as e:
        msg = str(e).replace("\n","")
        logging.info(traceback.print_exc())
        logging.exception(f'failed to generate excel file due to <{msg}>')
        return None

def filterAndPaginate_v2(db_config,
                         required_columns,
                         table_name,
                         filters=None,
                         sort_column=None,
                         sort_order='asc',
                         page_number=1,
                         page_size=10,
                         query = None,
                         search_key = None,
                         whereinquery=False,
                         #if isdeleted is a flag in the db table
                         isdeleted = False,
                         downloadType=None,
                         mapping = None,
                         group_by = None,
                         static = True):
    try:
        # Base query
        query_frontend = False

        if query is None:
            query = f"SELECT {','.join(required_columns)} FROM {table_name}"
            if isdeleted:
                query += ' WHERE isdeleted = false '
            query_frontend = True
        # Adding filters
        where_clauses = []
        for column, filter_type, value, dataType in (filters or []):
            ##########################################################
            #                     STRING FILTERS
            ##########################################################
            if dataType == 'String':
                if filter_type == 'contains':
                    where_clauses.append(f"lower({column}) LIKE '%{value.lower()}%'")
                elif filter_type == 'doesNotContain':
                    where_clauses.append(f"lower({column}) NOT LIKE '%{value.lower()}%'")
                elif filter_type == 'startsWith':
                    where_clauses.append(f"lower({column}) LIKE '{value.lower()}%'")
                elif filter_type == 'endsWith':
                    where_clauses.append(f"lower({column}) LIKE '%{value.lower()}'")
                elif filter_type == 'equalTo':
                    where_clauses.append(f"lower({column}) = '{value.lower()}'")
                elif filter_type == 'isNull':
                    where_clauses.append(f"{column} is null OR {column} = ''")
                elif filter_type == 'isNotNull':
                    where_clauses.append(f"{column} is not null AND {column} != ''")
            ##########################################################
            #                     NUMERIC FILTERS
            ##########################################################
            elif dataType == 'Numeric':
                if filter_type == 'equalTo':
                    where_clauses.append(f"{column} = {value}")
                elif filter_type == 'notEqualTo':
                    where_clauses.append(f"{column} != {value}")
                elif filter_type == 'greaterThan':
                    where_clauses.append(f"{column} > {value}")
                elif filter_type == 'lessThan':
                    where_clauses.append(f"{column} < {value}")
                elif filter_type == 'greaterThanOrEqualTo':
                    where_clauses.append(f"{column} >= {value}")
                elif filter_type == 'lessThanOrEqualTo':
                    where_clauses.append(f"{column} <= {value}")
                elif filter_type == 'between':
                    where_clauses.append(f" ({column} >= {value[0]} AND {column} <= {value[1]}) ")
                elif filter_type == 'notBetween':
                    where_clauses.append(f" ({column} <= {value[0]} OR {column} >= {value[1]}) ")
                elif filter_type == 'isNull':
                    where_clauses.append(f"{column} is null")
                elif filter_type == 'isNotNull':
                    where_clauses.append(f"{column} is not null")
            ##########################################################
            #                     DATE FILTERS
            ##########################################################
            elif dataType == 'Date':
                if filter_type == 'equalTo':
                    where_clauses.append(f"{column} = '{value}'")
                elif filter_type == 'notEqualTo':
                    where_clauses.append(f"{column} != '{value}'")
                elif filter_type == 'greaterThan':
                    where_clauses.append(f"{column} > '{value}'")
                elif filter_type == 'lessThan':
                    where_clauses.append(f"{column} < '{value}'")
                elif filter_type == 'greaterThanOrEqualTo':
                    where_clauses.append(f"{column} >= '{value}'")
                elif filter_type == 'lessThanOrEqualTo':
                    where_clauses.append(f"{column} <= '{value}'")
                elif filter_type == 'isNull':
                    where_clauses.append(f"{column} is null")
                elif filter_type == 'isNotNull':
                    where_clauses.append(f"{column} is not null")
                elif filter_type == 'between':
                    where_clauses.append(f" {column} >= '{value[0]}' AND {column} <= '{value[1]}' ")
            else:
                # must throw a warning here
                pass
        # handle where clause and sorting
        if where_clauses and not whereinquery:
            query += " WHERE " + " AND ".join(where_clauses)
        elif where_clauses and whereinquery:
            query += " AND " + " AND ".join(where_clauses)
        logging.info(where_clauses)
        if sort_column and static:
            q = f'SELECT pg_typeof({sort_column[0]}) from {table_name} limit 1'
            conn = psycopg2.connect(db_config)
            cursor = conn.cursor()
            cursor.execute(q)
            datatype = cursor.fetchone()[0]
            if datatype != 'text':
                query += f" ORDER BY {sort_column[0]} {'asc NULLS FIRST' if sort_order == 'asc' else 'desc  NULLS LAST'}"
            if datatype == 'text':
                query += f" ORDER BY LOWER({sort_column[0]}) {'asc NULLS FIRST' if sort_order == 'asc' else 'desc  NULLS LAST'}"
        # Handle pagination
        
        if group_by:
            query+= f"GROUP BY {','.join(group_by)}"
        counts_query = query
        if page_number !=0 and page_size !=0 and search_key is None:
            # Calculate OFFSET
            offset = (page_number - 1) * page_size
            # Adding pagination
            query += f" LIMIT {page_size} OFFSET {offset}"
        else:
            pass
            # when page_number=0 and page_size=0
            # do not paginate - return all. This is
            # for downloading all the filtered data.

        logging.info(f' Prepared final query [{query}]')
        # fetch results and return to caller
        conn = psycopg2.connect(db_config)
        cur = conn.cursor()
        cur.execute(query)
        logging.info(f"Cursor message is {cur.statusmessage}")
        rows = cur.fetchall()
        cur = conn.cursor()
        cur.execute(counts_query)
        rows_for_counts = cur.fetchall()
        total_count = len(rows_for_counts)
        colnames = [desc[0] for desc in cur.description]
        logging.info(f' Given filter yeilds <{total_count}> entries')
        cur.close()
        conn.close()

        if search_key is not None:
            search_results = []
            for row in rows:
                concatenated_row = " ".join( str(item) for item in row)
                if str(search_key).lower() in concatenated_row.lower():
                    search_results.append(row)
                else:
                    pass
            total_count = len(search_results)
            logging.info(f' Given search key <{search_key}> yeilds <{total_count}> entries')
            start_index = (page_number - 1) * page_size
            end_index = start_index + page_size
            if start_index!=end_index:
                rows = search_results[start_index:end_index]
            else:
                rows = search_results
        resp_payload = {'data': rows, 'total_count': total_count, 'message': 'success', 'colnames': colnames}
        # generate downloadable file
        if page_number == 0 and page_size == 0 and (downloadType == 'excel' or downloadType == 'pdf'):
            filename = generateExcelOrPDF(downloadType, rows, colnames,mapping)
            resp_payload['filename'] = filename
        elif page_number == 0 and page_size == 0 and downloadType == None:
            logging.info(f'downloadType is <None>')

        return resp_payload
    except Exception as e:
        logging.exception(f' exception {traceback.print_exc()}')
        #print(traceback.print_exc())
        msg = str(e).replace("\n","")
        return {'data':None, 'message':f'exception due to <{msg}>'}


def givenowtime():
    s = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return s

def get_db_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        yield conn, cursor
    except psycopg2.OperationalError as e:
        logging.exception(f'Database connection error: {e}')
        raise HTTPException(status_code=404, detail="Database connection error")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def get_countries_from_id(conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        with conn[0].cursor() as cursor:
            query = 'SELECT * FROM country'
            msg = logMessage(cursor,query)
            logging.info(msg)
            data = cursor.fetchall()
            res = {}
            for row in data:
                res[row[0]] = row[1]
            return res
    except:
        logging.exception(traceback.print_exc())
        return {}
    
def get_city_from_id(conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        with conn[0].cursor() as cursor:
            query = 'SELECT id,city FROM cities'
            msg = logMessage(cursor,query)
            logging.info(msg)
            data = cursor.fetchall()
            res = {}
            for row in data:
                res[row[0]] = row[1]
            return res
    except:
        logging.exception(traceback.print_exc())
        return {}
        
def get_name(id : int,name_dict:dict):
    if id in name_dict:
        return name_dict[id]
    else:
        return f"NA_{id}"

def get_city_details(conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        with conn[0].cursor() as cursor:
            query = 'SELECT id,city,state,countryid FROM cities '
            msg = logMessage(cursor,query)
            logging.info(msg)
            data = cursor.fetchall()
            res = {}
            for row in data:
                res[row[0]] = row[1:]
            return res
    except:
        logging.exception(traceback.print_exc())
        return {}

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/validateCredentials')
async def validate_credentials(payload : dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'validate_credentials: received payload <{payload}>')
    try:
        with conn[0].cursor() as cursor:
            query = 'SELECT password,id,roleid FROM usertable where username = %s'
            query2 = "SELECT EXISTS (SELECT 1 FROM companykey WHERE companycode = %s)"

            msg = logMessage(cursor,query,(payload['username'],))
            logging.info(msg)
            userdata = cursor.fetchone()
            msg = logMessage(cursor,query2, (str(payload['company_key']),))
            logging.info(msg)
            company_key = cursor.fetchone()
            if userdata is None:
                raise HTTPException(status_code=401,detail="Unauthorised")
            logger.info(f"{userdata[0]} is password hashed")
            encoded_pw = payload['password'].encode('utf-8')
            logger.info(f"{type(encoded_pw)} is type")
            # encoded_pw = payload["password"] if isinstance(payload["password"], bytes) else payload["password"].encode('utf-8')
            # encoded_pw = userdata[0].encode('utf-8')
            # database_pw = userdata[0] if isinstance(userdata[0], bytes) else userdata[0].encode('utf-8')
            database_pw = bytes(userdata[0],'ascii')
            if bcrypt.checkpw(encoded_pw,database_pw) and company_key[0]:
            # if userdata and payload=userdata[0],userdata[0]) and key[0]:
                logger.info('Password is ok')
                resp = {
                    "result": "success",
                    "user_id":userdata[1],
                    "role_id":userdata[2],
                    "token": await gentoken({"user_id":userdata[1]},conn,False)
                }
                return resp
            else:
                return HTTPException(status_code=401,detail="Unauthorized")
    except KeyError as ke:
        return HTTPException(status_code=400,detail=f"Bad Request,{ke} missing")
    except Exception as e:
        logging.info(traceback.print_exc())
        return HTTPException(status_code=400,detail="Bad Request")


def giveSuccess(uid,rid,data=[], total_count=None, filename=None):
    final_data =  {
        "filename": filename,
        "result":"success",
        "user_id":uid,
        "role_id":rid,
        "data":data
    }
    if total_count is not None:
        final_data['total_count'] = total_count
    else:
        pass
    #logging.debug(f'prepared final response <{final_data}>')
    return final_data

def giveFailure(msg,uid,rid,data=[]):
    # send_email("",msg,"theruderaw678@gmail.com")
    return {
        "result":"error",
        "message":msg,
        "user_id":uid,
        "role_id":rid,
        "data":data
    }

def check_role_access(conn, payload: dict,request: Request = None):
    if request and request.headers.get('authorization'):
        with conn[0].cursor() as cursor:
            token = request.headers['authorization'][7:]
            logging.info(f"Token is <{token}>")
            cursor.execute("SELECT key FROM tokens WHERE token = %s", (token,))
            key = cursor.fetchone()
            logging.info(key)
        if key[0]:
            payload = jwt.decode(token,key[0],algorithms=ALG)
        else:
            raise HTTPException(status_code=403,detail="Invalid Token")
    if 'user_id' in payload:
        identifier_id = payload['user_id']
        identifier_name = None
    elif 'username' in payload:
        identifier_name = payload['username']
        identifier_id = None
    else:
        logging.info(traceback.print_exc())
        raise HTTPException(status_code=400, detail="Please provide either 'user_id' or 'username' in the payload")
    cursor = conn[0].cursor()
    try:
        if identifier_id:
            msg = logMessage(cursor,"SELECT roleid FROM usertable WHERE id = %s", (identifier_id,))
            logging.info(msg)
        elif identifier_name:
            msg = logMessage(cursor,"SELECT roleid FROM usertable WHERE username = %s", (identifier_name,))
            logging.info(msg)
        else:
            return None
        role_id = cursor.fetchone()

        if role_id is not None:
            return role_id[0]
        else:
            return 0
    except KeyError as ke:
        return {
            "result": "error",
            "message": "key {ke} not found",
            "user_id": payload['user_id']
        }  
    except Exception as e:
        logging.exception(traceback.print_exc())
    finally:
        cursor.close()

@app.post('/paymentForAdmin')
async def payment_for_admin(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f':payload received is {payload}')

    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status==1:
            res = paymentfor(conn[0])
            arr = []
            for i in res:
                arr.append({'id':i,'name':res[i]})
            return giveSuccess(payload['user_id'],role_access_status,arr,total_count=len(arr))
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        return giveFailure("Invalid Credentials",0,0)

# FastAPI route to get roleid based on id or username
@app.post("/getRoleID")
async def get_role_id(payload: dict, request: Request,conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'get_role_id:payload received is {payload}')
    role_id = check_role_access(conn, payload,request)
    if role_id is not None:
        if role_id!=0:
            return {
                "result":"Success",
                "data":{"role id": role_id}
            }
        else:
            return {
                "result":"error",
                "messgae":"role_id not obtainable",
                "data":{}
            }
    else:
        return {
            "result" : "Error",
            "message":"RoleID not found",
            "data":{}
            }


@app.post('/getCountries')
async def get_countries(payload : dict,conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    payload['table_name'] = 'country'
    return await runInTryCatch(
        conn = conn,
        fname = 'get_countries',
        payload = payload,
        isPaginationRequired=True,
        formatData=True,
        whereinquery=False,
        isdeleted=False
    )

@app.post('/addCountry')
async def add_country(payload:dict,conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'add_country: received payload <{payload}>')
    try:
        with conn[0].cursor() as cursor:
            role_access_status = check_role_access(conn,payload)
            # if 'country_id' not in payload:
            #     logMessage(cursor,'select max(id) from country')
            #     payload['country_id'] = cursor.fetchone()[0]+1
            if role_access_status == 1 and ifNotExist('name','country',conn,payload['country_name']):
            # Insert new country data into the database
                query_insert = 'INSERT INTO country (name) VALUES (%s)'
                msg = logMessage(cursor,query_insert, ( payload['country_name'],))
                logging.info(msg)

            # Commit the transaction
                conn[0].commit()
                data = {"added":payload['country_name']}
                return giveSuccess(payload['user_id'],role_access_status,data)
            elif role_access_status!=1:
                return giveFailure("Access Denied",payload['user_id'],role_access_status)
            else:
                return giveFailure("Already Exists",payload['user_id'],role_access_status)
    except KeyError as ke:
        return giveFailure(f"key {ke} not found",payload['user_id'],0)
    except Exception as e:
        return giveFailure(f"Error {e}",payload["user_id"],0)
    
def checkcountry(payload: str,conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        with conn[0].cursor() as cursor:
            query_find = "SELECT EXISTS (SELECT 1 FROM country WHERE name=%s)"
            msg = logMessage(cursor,query_find, (payload,))
            logging.info(msg)
            ans = cursor.fetchone()[0]
            if ans==1:
                return True
            else:
                return False
    except Exception as e:
        logging.exception(traceback.print_exc())
        return False

@app.post("/editCountry")
async def edit_country(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'edit_country: received payload <{payload}>')
    try:
        # Check user role
        role_access_status = check_role_access(conn,payload)

        if role_access_status == 1 and checkcountry(payload['old_country_name'],conn):
            with conn[0].cursor() as cursor:
                # Update country name in the database
                query_update = "UPDATE country SET name = %s WHERE name = %s"
                msg = logMessage(cursor,query_update, (payload['new_country_name'], payload['old_country_name']))
                logging.info(msg)
                # Commit the transaction
                conn[0].commit()
                data={
                    "original":payload['old_country_name'],
                    "new country":payload['new_country_name']
                }
            return giveSuccess(payload['user_id'],role_access_status,data)
        elif not checkcountry(payload['old_country_name'],conn):
            return giveFailure("No country Exists",payload['user_id'],role_access_status)
        elif role_access_status!=1:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)
        
        else:
            return giveFailure("Invalid Credentials",payload['user_id'],role_access_status)
    except KeyError as ke:
        return giveFailure(f"key {ke} not found",payload['user_id'],0)
    except Exception as e:
        return giveFailure("Invalid Credentials",payload['user_id'],0)

@app.post('/deleteCountry')
async def delete_country(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'delete_country: received payload <{payload}>')
    try:
        with conn[0].cursor() as cursor:
            role_access_status = check_role_access(conn,payload)
            if role_access_status == 1 and checkcountry(payload['country_name'],conn):
            # Delete country data from the database
                query_delete = 'DELETE FROM country WHERE name = %s'
                msg = logMessage(cursor,query_delete,(payload['country_name'],))
                logging.info(msg)
            # Commit the transaction
                conn[0].commit()
                data = {
                        "deleted":payload["country_name"]
                        }
                return giveSuccess(payload['user_id'],role_access_status,data)
            elif role_access_status!=1:
                return giveFailure("Invalid Credentials",payload['user_id'],role_access_status)

            elif not checkcountry(payload['name'],conn):
                return giveFailure("Already Exists",payload['user_id'],role_access_status)
            else:
                return giveFailure("Invalid Credentials",payload['user_id'],role_access_status)

    except Exception as e:
        return giveFailure("Invalid Credentials",payload['user_id'],0)


@app.post('/addBuilderInfo')
async def add_builder_info(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'add_builder_info: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn, payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = '''
                    INSERT INTO builder (
                        buildername, phone1, phone2, email1, email2, addressline1, addressline2,
                        suburb, city, state, country, zip, website, comments, dated, createdby, isdeleted
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    ) RETURNING id
                '''
                msg = logMessage(cursor,query, (
                    payload['buildername'],
                    payload['phone1'],
                    payload['phone2'],
                    payload['email1'],
                    payload.get('email2', ''), 
                    payload['addressline1'],
                    payload['addressline2'],
                    payload['suburb'],
                    payload['city'],
                    payload['state'],
                    payload['country'],
                    payload['zip'],
                    payload['website'],
                    payload['comments'],
                    givenowtime(),
                    payload['user_id'],
                    False
                ))
                logging.info(msg)
                id = cursor.fetchone()[0]
                 # Commit the transaction
                conn[0].commit()
                data= {
                    "entered":id
                }
            return giveSuccess(payload['user_id'],role_access_status,data)
        elif role_access_status!=1:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)
        else:
            return giveFailure("Already Exists",payload['user_id'],role_access_status)
    except Exception as e:
        logging.exception(traceback.print_exc())
        return giveFailure("Invalid Credentials",payload['user_id'],0)

#BUILDER UPDATED
@app.post('/getBuilderInfo')
def getBuilderInfo(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'get_builder_info: received payload <{payload}>')
    countries = get_countries_from_id(conn=conn)
    cities = get_city_from_id(conn=conn)
    try:
        role_access_status = check_role_access(conn, payload)

        if role_access_status == 1:  
            with conn[0].cursor() as cursor:
                data = filterAndPaginate_v2(DATABASE_URL, payload['rows'], 'get_builder_view', payload['filters'],
                                        payload['sort_by'], payload['order'], payload["pg_no"], payload["pg_size"],
                                        search_key = payload['search_key'] if 'search_key' in payload else None,isdeleted=True,whereinquery=True,
                                            downloadType=payload['downloadType'] if 'downloadType' in payload else None )

                colnames = data['colnames']
                total_count = data['total_count']
                filename = data['filename'] if "filename" in data else None
                res = []
                for row in data['data']:
                    row_dict = {}
                    for i,colname in enumerate(colnames):
                        row_dict[colname] = row[i]
                    # row_dict['country'] = get_name(row_dict['country'],countries)
                    # row_dict['city'] = get_name(row_dict['city'],cities)
                    res.append(row_dict)
                    data={
                        "builder_info":res
                    }
                
                return giveSuccess(payload['user_id'],role_access_status,data,total_count,filename)
        else:
            return giveFailure("Access Denied",payload["user_id"],role_access_status)
    except Exception as e:
        logging.exception(traceback.print_exc())
        return giveFailure("Invalid Credentials",payload['user_id'],0)
    
@app.post("/editBuilder")
async def edit_builder(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'edit_builder: received payload <{payload}>')
    try:
        # Check user role
        role_access_status = check_role_access(conn, payload)

        with conn[0].cursor() as cursor:
            # Check if the builder exists
            query_check_builder = "SELECT EXISTS (SELECT 1 FROM builder WHERE id = %s)"
            msg = logMessage(cursor,query_check_builder, (payload['builder_id'],))
            logging.info(msg)
            builder_exists = cursor.fetchone()[0]
            logging.info(builder_exists)
        if role_access_status == 1 and builder_exists:
            with conn[0].cursor() as cursor:
                # Update builder information in the database
                query_update = """
                    UPDATE builder 
                    SET buildername = %s, phone1 = %s, phone2 = %s, email1 = %s, email2 = %s,
                    addressline1 = %s, addressline2 = %s, suburb = %s, city = %s, 
                    state = %s, country = %s, zip = %s, website = %s, comments = %s, 
                    dated = %s, createdby = %s, isdeleted = %s
                    WHERE id = %s
                """
                msg = logMessage(cursor,query_update, (
                    payload['builder_name'],
                    payload['phone_1'],
                    payload['phone_2'],
                    payload['email1'],
                    payload['email2'],
                    payload['addressline1'],
                    payload['addressline2'],
                    payload['suburb'],
                    payload['city'],
                    payload['state'],
                    payload['country'],
                    payload['zip'],
                    payload['website'],
                    payload['comments'],
                    givenowtime(),
                    payload['user_id'],
                    False,
                    payload['builder_id']
                ))
                logging.info(msg)
                # Commit the transaction
                conn[0].commit()

            return giveSuccess(payload['user_id'],role_access_status,{"updated":payload})
        elif not builder_exists:
            return giveFailure("Builder does not exist",payload['user_id'],role_access_status)
        elif role_access_status != 1:
            return giveFailure("Access denied",payload['user_id'],role_access_status)
        else:
            return giveFailure("Invalid credentials",payload['user_id'],role_access_status)
    except KeyError as ke:
        logging.info(traceback.print_exc)
        return giveFailure(f"key {ke} not found",payload['user_id'],0)
    except Exception as e:
        logging.info(traceback.print_exc)

        return giveFailure(str(e),payload['user_id'],0)

@app.post('/deleteBuilder')
async def deleteBuilder(payload:dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'delete_builder: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status==1:
            with conn[0].cursor() as cursor:
                query = 'UPDATE builder SET isdeleted=true WHERE id=%s'
                msg = logMessage(cursor,query,(payload['builder_id'],))
                logging.info(msg)
                conn[0].commit()
                data = {
                    "deleted_user":payload['builder_id']
                    }
                return giveSuccess(payload['user_id'],role_access_status,data)

        else:
            return giveFailure("Access Denoed",payload['user_id'],0)

    except Exception as e:
        logging.exception(traceback.print_exc())
        return giveFailure("Invalid Credentials",payload['user_id'],0)

#STATES UPDATED
@app.post('/getStatesAdmin')
async def get_states_admin(payload:dict,conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'get_states_admin: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status==1:
            # query = "SELECT DISTINCT  b.name as countryname, a.state, b.id as id FROM cities a,country b WHERE a.countryid=b.id order by a.state"
            data = filterAndPaginate_v2(DATABASE_URL, payload['rows'],'get_states_view', payload['filters'],
                                        payload['sort_by'], payload['order'], payload["pg_no"], payload["pg_size"],
                                        search_key = payload['search_key'] if 'search_key' in payload else None,whereinquery=True,
                                        downloadType=payload['downloadType'] if 'downloadType' in payload else None )
            total_count = data['total_count']
            return giveSuccess(payload["user_id"],role_access_status,data['data'], total_count=total_count)
        else:
            return giveFailure("Invalid Credentials",payload['user_id'],role_access_status)
    except Exception as e:
        logging.exception(traceback.print_exc())
        return giveFailure("Invalid Credentials",payload['user_id'],0)
    
@app.post('/getStates')
async def get_states(payload : dict,conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'get_states: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn,payload)
        logging.info(role_access_status)
        if role_access_status != 0:
            if role_access_status == 1:
                with conn[0].cursor() as cursor:
                    query = "SELECT DISTINCT state FROM cities WHERE countryid = %s order by state"
                    msg =logMessage(cursor,query,(payload['country_id'],))
                    #data = [i[0] for i in cursor.fetchall()]
                    logging.info(msg)
                    data = cursor.fetchall()

                return giveSuccess(payload['user_id'],role_access_status,data)
            else:
                return giveFailure("Access denied",payload['user_id'],role_access_status)
        else:
            return giveFailure("User does not exist",payload['user_id'],role_access_status)
    except ValueError as ve:
        logging.info(traceback.print_exc())
        return giveFailure(f"{ve} error found",payload["user_id"],0)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure(f"{e} error found",payload['user_id'],0)

@app.post('/getCities')
async def get_cities(payload : dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'get_cities: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status==1:
            with conn[0].cursor() as cursor:
                query = "SELECT distinct id,city FROM cities where state=%s order by city"
                msg = logMessage(cursor,query,(payload['state_name'],))
                logging.info(msg)
                data = cursor.fetchall()
            colnames = [desc[0] for desc in cursor.description]
                
            res = []
            for row in data:
                row_dict = {}
                for i,colname in enumerate(colnames):
                    row_dict[colname] = row[i]
                res.append(row_dict)
            return giveSuccess(payload["user_id"],role_access_status,res)
        else:
            return giveFailure("Invalid Credentials",payload['user_id'],role_access_status)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure(f"{e} error found",payload['user_id'],0)

#CITIES UPDATED
@app.post('/getCitiesAdmin')
async def get_cities_admin(payload:dict,conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    payload['table_name'] = 'get_cities_view'
    return await runInTryCatch(
        conn = conn,
        fname = 'get_cities_admin',
        payload = payload,
        isPaginationRequired=True,
        whereinquery=False,
        formatData=True,
        isdeleted=False
    )


@app.post('/getProjects')
async def get_projects(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    payload['table_name'] = 'get_projects_view'
    return await runInTryCatch(
        conn=conn,
        fname='getProjects',
        payload=payload,
        isPaginationRequired=True,
        whereinquery=True,
        formatData=True,
        isdeleted=True
    )
    
@app.post('/deleteProject')
async def delete_project(payload:dict,conn : psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'delete_project: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn, payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                msg = logMessage(cursor,"""UPDATE project SET isdeleted=true WHERE id=%s""",(payload['id'],))
                logging.info(msg)
                # Commit the transaction
                conn[0].commit()
                data= {
                        "deleted": payload['id']
                    }
                return giveSuccess(payload['user_id'],role_access_status,data)
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        print(traceback.print_exc())
        return giveFailure("Invalid Credentials",payload['user_id'],0)
    
@app.post('/addNewBuilderContact')
async def add_new_builder_contact(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'add_new_builder_contact: received payload <{payload}>')
    try:
        if 'builderid' not in payload:
            return {
                "result": "error",
                "message": "Missing 'builderid' in payload",
                "user_id": payload.get('user_id', None),
                "data": {}
            }
        
        role_access_status = check_role_access(conn, payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = '''
                    INSERT INTO builder_contacts (
                        builderid, contactname, email1, jobtitle,
                        businessphone, homephone, mobilephone, addressline1,
                        addressline2, suburb, city, state, country,
                        zip, notes, dated, createdby, isdeleted
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                '''
                msg = logMessage(cursor,query, (
                    payload['builderid'],
                    payload['contactname'],
                    payload['email1'],
                    payload['jobtitle'],
                    payload['businessphone'],
                    payload['homephone'],
                    payload.get('mobilephone', None),
                    payload['addressline1'],
                    payload['addressline2'],
                    payload['suburb'],
                    payload['city'],
                    payload['state'],
                    payload['country'],
                    payload['zip'],
                    payload['notes'],
                    givenowtime(),
                    payload['user_id'],
                    False
                ))
                logging.info(msg)
                # Commit changes to the database
                conn[0].commit()
            data= {
                    "entered": payload['contactname']
                } 
            return giveSuccess(payload['user_id'],role_access_status,data)
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        print(traceback.format_exc())
        return giveFailure(str(e),payload['user_id'],0)

@app.post('/getLocality')
async def get_localties(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'get_localities: received payload <{payload}>')
    payload['table_name'] = 'get_locality_view'
    return await runInTryCatch(
        conn = conn,
        fname = 'get_locality',
        payload=payload,
        isPaginationRequired=True,
        whereinquery=False,
        formatData=True,
        isdeleted=False
    )

@app.post('/addLocality')
async def add_localities(payload: dict, conn : psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'add_locality: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1 and ifNotExist('locality','locality',conn,payload['locality']):
            payload['dated'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with conn[0].cursor() as cursor:
                query = 'INSERT INTO locality (locality,cityid) VALUES (%s,%s)'
                msg = logMessage(cursor,query,(payload['locality'],payload['cityid']))
                logging.info(msg)
                conn[0].commit()
            data = {
                "Inserted Locality" : payload['locality']
            }
            return giveSuccess(payload['user_id'],role_access_status,data)
        elif role_access_status!=1:
            return HTTPException(status_code=403,detail="Access Denied")
        else:
            return HTTPException(status_code=403,detail="Already Exists")
    except Exception as e:
        print(traceback.print_exc())
        return HTTPException(status_code=400,detail="Invalid Credentials")

@app.post('/editLocality')
async def edit_localities(payload: dict, conn : psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'edit_locality: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status==1:
            payload['dated'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with conn[0].cursor() as cursor:
                query = 'UPDATE locality SET locality = %s,cityid = %s WHERE id=%s'
                msg =logMessage(cursor,query,(payload['locality'],payload['cityid'],payload['id']))
                logging.info(msg)
                conn[0].commit()
            data = {
                "Updated Locality":payload['locality']
            }
            return giveSuccess(payload['user_id'],role_access_status,data)
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        return giveFailure("Invalid Credentials",payload['user_id'],0)

@app.post('/deleteLocality')
async def delete_localities(payload : dict,conn : psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'delete_locality: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'DELETE FROM locality WHERE id=%s'
                msg =logMessage(cursor,query, (payload['id'],))
                logging.info(msg)
                conn[0].commit()
            data = {"Deleted Locality ID":payload['id']}
            return giveSuccess(payload['user_id'],role_access_status,data)
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        print(traceback.print_exc())
        return giveFailure("Invalid Credentials",payload['user_id'],0)

@app.post('/getBankSt')
async def get_bank_statement(payload : dict, conn : psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'get_bank_statement: received payload <{payload}>')
    payload['table_name'] = 'get_bankst_view'
    data =  await runInTryCatch(
        conn = conn,
        fname = 'get_bank_statement',
        payload=payload,
        isPaginationRequired=True,
        whereinquery=True,
        formatData=True,
        isdeleted=True
    )
    with conn[0].cursor() as cursor:
        query = '''SELECT
    COALESCE(SUM(CASE WHEN lower(crdr) = 'cr' THEN amount ELSE 0 END), 0) - 
    COALESCE(SUM(CASE WHEN lower(crdr) = 'dr' THEN amount ELSE 0 END), 0) AS difference
FROM
    get_bankst_view
'''
        cursor.execute(query)
        data['total_amount'] = cursor.fetchone()[0]
        return data


@app.post('/addBankSt')
async def add_bank_statement(payload : dict, conn : psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'add_bank_statement: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status==1:
            with conn[0].cursor() as cursor:
                payload['dated'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                query = (
                    'INSERT INTO bankst (modeofpayment,date,amount,particulars,crdr,vendorid,createdby) '
                    'VALUES (%s,%s,%s,%s,%s,%s,%s)'
                         )
                msg = logMessage(cursor,query,(payload['modeofpayment'],payload['date'],payload['amount'],payload['particulars'],payload['crdr'],payload['vendorid'],payload['createdby']))
                logging.info(msg)
                conn[0].commit()
            data = {
                "added_data": f"added bank statement for amount <{payload['amount']}>"
            }
            return giveSuccess(payload['user_id'],role_access_status,data)
        elif role_access_status!=1:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)
        else:
            return giveFailure("Already Exists",payload['user_id'],role_access_status)
    except Exception as e:
        print(traceback.print_exc())
        return giveFailure(f"failed to add bank statement due to exception <{str(e)}>",payload['user_id'],0)

@app.post('/editBankSt')
async def edit_bank_statement(payload : dict, conn : psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'edit_bank_statement: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                payload['dated'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                query = ('UPDATE bankst SET modeofpayment=%s,'
                         'date=%s,amount=%s,particulars=%s,'
                         'crdr=%s,vendorid=%s,createdby=%s WHERE id=%s')
                msg = logMessage(cursor,query,(payload['modeofpayment'],payload['date'],payload['amount'],payload['particulars'],payload['crdr'],payload['vendorid'],payload['user_id'],payload['id']))
                logging.info(msg)
                if cursor.statusmessage == "UPDATE 0":
                    return giveFailure("No Bank st available",payload['user_id'],role_access_status)
                conn[0].commit()
            data = {
                "edited_data":payload['id']
            }
            return giveSuccess(payload['user_id'],role_access_status,data)
        else:
            giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        print(traceback.print_exc())
        giveFailure("Invalid Credentials",payload['user_id'],0)

@app.post('/deleteBankSt')
async def delete_bank_statement(payload : dict, conn : psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'delete_bank_statement: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'UPDATE bankst SET isdeleted=true WHERE id=%s AND isdeleted=false'
                msg = logMessage(cursor,query,(payload['id'],))
                logging.info(msg)
                if cursor.statusmessage == "UPDATE 0":
                    return giveFailure(f"No Bank Stantement with id {payload['id']}",payload['user_id'],role_access_status)
                conn[0].commit()
            data = {
                "deleted_data":payload['id']
            }
            return giveSuccess(payload['user_id'],role_access_status,data)
        else:
            giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        print(traceback.print_exc())
        giveFailure("Invalid Credentials",payload['user_id'],0)  

@app.post('/getEmployee')
async def get_employee(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'get_employee: received payload <{payload}>')
    payload['table_name'] = 'get_employee_view'
    return await runInTryCatch(
        conn = conn,
        fname = 'get_employee',
        payload=payload,
        isPaginationRequired=True,
        whereinquery=True,
        formatData=True,
        isdeleted=True
    )

@app.post('/addEmployee')
async def add_employee(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'add_employee: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1 and ifNotExist('employeeid','employee',conn,payload['employeeid']):
            with conn[0].cursor() as cursor:
                payload['dated'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                query = 'INSERT INTO employee (employeename,employeeid, userid,roleid, dateofjoining, dob, panno,status, phoneno, email, addressline1, addressline2,suburb, city, state, country, zip,dated, createdby, isdeleted, entityid,lobid, lastdateofworking, designation)VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                msg = logMessage(cursor,query,(  payload['employeename'],
                                        payload['employeeid'],
                                        payload['userid'],
                                        payload['roleid'],
                                        payload['dateofjoining'],
                                        payload['dob'],
                                        payload['panno'],
                                        payload['status'],
                                        payload['phoneno'],
                                        payload['email'],
                                        payload['addressline1'],
                                        payload['addressline2'],
                                        payload['suburb'],
                                        payload['city'],
                                        payload['state'],
                                        payload['country'],
                                        payload['zip'],
                                        givenowtime(),
                                        payload['user_id'],
                                        False,
                                        payload['entityid'],
                                        payload['lobid'],
                                        payload['lastdateofworking'],     
                                        payload['designation']))
                logging.info(msg)
                conn[0].commit()
            data = {
                "Inserted Employee" : payload['employeename']
            }
            return giveSuccess(payload['user_id'],role_access_status,data)
        elif role_access_status!=1:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)
        else:
            return giveFailure("Already Exists",payload['user_id'],role_access_status)
    except Exception as e:
        print(traceback.print_exc())
        return giveFailure("Invalid Credentials",payload['user_id'],0)

@app.post('/editEmployee')
async def edit_employee(payload: dict, conn : psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'edit_employee: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status==1:
            with conn[0].cursor() as cursor:
                payload['dated'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                query = '''UPDATe employee SET employeename=%s,employeeid=%s, userid=%s,roleid=%s, dateofjoining=%s, dob=%s, panno=%s,status=%s, phoneno=%s, email=%s, addressline1=%s, addressline2=%s,suburb=%s, city=%s, state=%s, country=%s, zip=%s,dated=%s, createdby=%s, isdeleted=%s, entityid=%s,lobid=%s, lastdateofworking=%s, designation=%s WHERE id=%s'''
                msg = logMessage(cursor,query,(
                                        payload['employeename'],
                                        payload['employeeid'],
                                        payload['userid'],
                                        payload['roleid'],
                                        payload['dateofjoining'],
                                        payload['dob'],
                                        payload['panno'],
                                        payload['status'],
                                        payload['phoneno'],
                                        payload['email'],
                                        payload['addressline1'],
                                        payload['addressline2'],
                                        payload['suburb'],
                                        payload['city'],
                                        payload['state'],
                                        payload['country'],
                                        payload['zip'],
                                        payload['dated'],
                                        payload['createdby'],
                                        payload['isdeleted'],
                                        payload['entityid'],
                                        payload['lobid'],
                                        payload['lastdateofworking'],     
                                        payload['designation'],
                                        payload['id'],))
                logging.info(msg)
                conn[0].commit()
            data = {
                "Updated Employee":payload['employeename']
            }
            return giveSuccess(payload['user_id'],role_access_status,data)
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        print(traceback.print_exc())
        return giveFailure("Invalid Credentials",payload['user_id'],0)


@app.post('/deleteEmployee')
async def delete_employee(payload: dict, conn : psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'delete_employee: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status==1:
            with conn[0].cursor() as cursor:
                query = 'UPDATE employee SET isdeleted=true WHERE id=%s and isdeleted=false'
                msg = logMessage(cursor,query,(payload['id'],))
                
                if cursor.statusmessage == "UPDATE 0":
                    return giveFailure(f"No Employee with id {payload['id']}",payload['user_id'],role_access_status)
                logging.info(msg)
                conn[0].commit()
            data = {
                "deleted_user":payload['id']
            }
            return giveSuccess(payload["user_id"],role_access_status,data)
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)        
    except Exception as e:
        print(traceback.print_exc())
        giveFailure("Invalid Credentials",payload['user_id'],0)  

@app.post('/getLob')
async def get_lob(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    payload['table_name'] = 'get_lob_view'
    return await runInTryCatch(
        conn = conn,
        fname = 'get_lob',
        payload=payload,
        isPaginationRequired=True,
        whereinquery=False,
        formatData=True,
        isdeleted=False
    )

@app.post('/addLob')
async def add_lob(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'add_lob: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1 and ifNotExist('name','lob',conn,payload['name']):
            with conn[0].cursor() as cursor:
                payload['dated'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                query = 'INSERT INTO lob (name) VALUES (%s)'
                msg = logMessage(cursor,query,(payload['name'],))
                logging.info(msg)
                conn[0].commit()
            data = {
                "added_data":payload['name']
            }
            return giveSuccess(payload['user_id'],role_access_status,data)
        elif role_access_status!=1:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)
        else:
            return giveFailure("Already Exists",payload['user_id'],role_access_status)
    except Exception as e:
        print(traceback.print_exc())
        giveFailure("Invalid Credentials",payload['user_id'],0)

@app.post('/editLob')
async def edit_lob(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'edit_lob: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                payload['dated'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                query = 'UPDATE lob SET name=%s WHERE name=%s'
                msg = logMessage(cursor,query,(payload['new_name'],payload['old_name']))
                logging.info(msg)
                logging.info(f'editLob: cursor status message is <{cursor.statusmessage}>')
                if cursor.statusmessage == "UPDATE 0":
                    return giveFailure(f"No lob <{payload['old_name']}> exists. unable to edit",payload['user_id'],role_access_status)
                conn[0].commit()
            data = {
                "edited_lob":payload['old_name']
            }
            return giveSuccess(payload['user_id'],role_access_status,data)
        else:
            giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        print(traceback.print_exc())
        giveFailure("Invalid Credentials",payload['user_id'],0)

@app.post('/deleteLob')
async def delete_lob(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'delete_lob: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'DELETE FROM lob WHERE name=%s'
                msg = logMessage(cursor,query,(payload['name'],))
                logging.info(msg)
                if cursor.statusmessage == "DELETE 0":
                    return giveFailure(f"No LOB available with name <{payload['name']}>",payload['user_id'],role_access_status)
                conn[0].commit()
            data = {
                "deleted_lob":payload['name']
            }
            return giveSuccess(payload['user_id'],role_access_status,data)
        else:
            giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        print(traceback.print_exc())
        giveFailure("Invalid Credentials",payload['user_id'],0)
        
@app.post('/getResearchProspect')
async def get_research_prospect(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    payload['table_name'] = 'get_research_prospect_view'
    return await runInTryCatch(
        conn = conn,
        fname = 'get_research_prospect',
        payload=payload,
        isPaginationRequired=True,
        whereinquery=True,
        formatData=True,
        isdeleted=True
    )
        
@app.post('/addResearchProspect')
async def add_research_prospect(payload: dict, conn : psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'add_research_prospect: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                payload['dated'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                query = 'INSERT INTO research_prospect (personname,suburb,city,state,country,propertylocation,possibleservices,dated,createdby,isdeleted,phoneno,email1) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id'
                msg =logMessage(cursor,query,(payload['personname'],payload['suburb'],payload['city'],payload['state'],payload['country'],payload['propertylocation'],payload['possibleservices'],givenowtime(),payload['user_id'],False,payload['phoneno'],payload['email1']))
                id = cursor.fetchone()[0]
                logging.info(msg)
                conn[0].commit()
            data = {
                "added_prospect":id
            }
            return giveSuccess(payload['user_id'],role_access_status,data)
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        print(traceback.print_exc())
        return giveFailure("Invalid Credentials",payload['user_id'],0)

@app.post('/editResearchProspect')
async def edit_research_prospect(payload: dict, conn : psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'edit_research_prospect: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                payload['dated'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                query = 'UPDATE research_prospect SET personname=%s,phoneno=%s,email1=%s,suburb=%s,city=%s,state=%s,country=%s,propertylocation=%s,possibleservices=%s,dated=%s,createdby=%s,isdeleted=%s WHERE id=%s'
                msg =logMessage(cursor,query,(payload['personname'],payload['phoneno'],payload['email1'],payload['suburb'],payload['city'],payload['state'],payload['country'],payload['propertylocation'],payload['possibleservices'],givenowtime(),payload['user_id'],False,payload['id']))
                logging.info(msg)
                if cursor.statusmessage == "UPDATE 0":
                    return giveFailure("No Prospect available",payload['user_id'],role_access_status)
                conn[0].commit()
            data = {
                "edited_data":payload['id']
            }
            return giveSuccess(payload['user_id'],role_access_status,data)
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        print(traceback.print_exc())
        return giveFailure("Invalid Credentials",payload['user_id'],0)

@app.post('/deleteResearchProspect')
async def delete_research_prospect(payload: dict, conn : psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'delete_research_prospect: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'UPDATE research_prospect SET isdeleted=true WHERE id=%s'
                msg = logMessage(cursor,query,(payload['id'],))
                logging.info(msg)
                if cursor.statusmessage == "DELETE 0":
                    return giveFailure("No Prospect available",payload['user_id'],role_access_status)
                conn[0].commit()
            data = {
                "deleted_prospect":payload['id']
            }
            return giveSuccess(payload['user_id'],role_access_status,data)
        else:
            giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        print(traceback.print_exc())
        giveFailure("Invalid Credentials",payload['user_id'],0)

@app.post('/getPayments')
async def get_payments(payload: dict, conn : psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'get_payments: received payload <{payload}>')    
    payload['table_name'] = 'get_payments_view'
    return await runInTryCatch(
        conn = conn,
        fname = 'get_payments',
        payload=payload,
        isPaginationRequired=True,
        whereinquery=True,
        formatData=True,
        isdeleted=True
    )


@app.post('/addPayment')
async def add_payment(payload: dict,conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'add_payment: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                payload['dated'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                query = 'INSERT INTO ref_contractual_payments (paymentto,paymentby,amount,paidon,paymentmode,description,paymentfor,dated,isdeleted,createdby,entityid,tds,professiontax,month,deduction) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id'                
                msg = logMessage(cursor,query,(payload['paymentto'],payload['paymentby'],payload['amount'],payload['paidon'],payload['paymentmode'],payload['description'],payload['paymentfor'],givenowtime(),False,payload['user_id'],payload['entityid'],payload['tds'],payload['professiontax'],payload['month'],payload['deduction']))
                logging.info(msg)
                id = cursor.fetchone()
                conn[0].commit()
                conn[0].close()
            data = {
                "added_payment_id":id
            }
            return giveSuccess(payload['user_id'],role_access_status,data)
        else:
            giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        print(traceback.print_exc())
        giveFailure("Invalid Credentials",payload['user_id'],0)

@app.post('/getPaymentStatusAdmin')
async def get_payment_status_admin(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'SELECT DISTINCT id,status from z_paymentrequeststatus order by status'
                msg = logMessage(cursor,query)
                _data = cursor.fetchall()
                logging.info(msg)
                
                colnames = [desc[0] for desc in cursor.description]
                res = []
                for data in _data:
                    res.append({colname:val for colname,val in zip(colnames,data)})
                if not data:
                    res = {colname:None for colname in colnames}
            return giveSuccess(payload['user_id'],role_access_status,res)
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure("Invalid Credentials",0,0)

@app.post('/editPayment')
async def edit_payment(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'edit_payment: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                payload['dated'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                query = 'UPDATE ref_contractual_payments SET paymentto=%s,paymentby=%s,amount=%s,paidon=%s,paymentmode=%s,description=%s,paymentfor=%s,dated=%s,createdby=%s,isdeleted=%s,entityid=%s,officeid=%s,tds=%s,professiontax=%s,month=%s,deduction=%s WHERE id=%s'
                msg = logMessage(cursor,query,(payload['paymentto'],payload['paymentby'],payload['amount'],payload['paidon'],payload['paymentmode'],payload['description'],payload['paymentfor'],givenowtime(),payload['user_id'],False,payload['entityid'],payload['officeid'],payload['tds'],payload['professiontax'],payload['month'],payload['deduction'],payload['id']))
                logging.info(msg)
                conn[0].commit()
            data = {
                "edited_data":payload['id']
            }
            return giveSuccess(payload['user_id'],role_access_status,data)
        else:
            giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        print(traceback.print_exc())
        giveFailure("Invalid Credentials",payload['user_id'],0)   

@app.post('/deletePayment')
async def delete_payment(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'delete_payment: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'UPDATE ref_contractual_payments  SET isdeleted=true WHERE id=%s'
                msg = logMessage(cursor,query,(payload['id'],))
                logging.info(msg)
                if cursor.statusmessage == "DELETE 0":
                    return giveFailure("No Payment available",payload['user_id'],role_access_status)
                else:
                    logging.info(f'deletePayment: Successful {cursor.statusmessage}>')

                conn[0].commit()
            data = {
                "deleted_payment":payload['id']
            }
            return giveSuccess(payload['user_id'],role_access_status,data)
        else:
            giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        print(traceback.print_exc())
        giveFailure("Invalid Credentials",payload['user_id'],0)

@app.post('/getVendorAdmin')
async def get_vendor_admin(payload: dict, conn : psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'get_vendor_admin: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'SELECT DISTINCT id,vendorname FROM vendor order by vendorname'
                msg = logMessage(cursor,query)
                logging.info(msg)
                data = cursor.fetchall()
                return giveSuccess(payload['user_id'],role_access_status,data)
        else:
            giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        giveFailure('Invalid Credentials',payload['user_id'],0)

async def runInTryCatch(conn, fname, payload,query = None,isPaginationRequired=False,whereinquery=True,formatData = False,isdeleted=False):#, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'{fname}:RT: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn, payload)
        if role_access_status != 1:
            return giveFailure("Access Denied", payload['user_id'], role_access_status)
        else:
            with conn[0].cursor() as cursor:
                res = []
                data = []
                colnames = []
                total_count = 0
                filename = None
                if isPaginationRequired:
                    logging.info("Pagination")
                    data = filterAndPaginate_v2(DATABASE_URL,
                                             query=query,
                                             filters=payload['filters'] if 'filters' in payload else None,
                                             table_name=payload['table_name'] if 'table_name' in payload else None,
                                             required_columns=payload['rows'] if 'rows' in payload else None,
                                             sort_column=payload['sort_by'] if 'sort_by' in payload else None,
                                             sort_order=payload['order'] if 'order' in payload else None,
                                             page_number=payload['pg_no'] if 'pg_no' in payload else 1,
                                             page_size=payload['pg_size'] if 'pg_size' in payload else 10,
                                             search_key=payload['search_key'] if 'search_key' in payload else None,
                                             whereinquery=whereinquery,
                                             isdeleted=isdeleted,
                                            downloadType=payload['downloadType'] if 'downloadType' in payload else None,
                                            mapping=payload['colmap'] if 'colmap' in payload else None,
                                            group_by=payload['group_by'] if 'group_by' in payload else None,
                                            static=True if 'static' not in payload else False)
                    logging.info(data.keys())
                    if 'total_count' not in data:
                        return giveFailure(data['message'],payload['user_id'],role_access_status)
                    colnames = data['colnames']
                    total_count = data['total_count']
                    filename = data['filename'] if 'filename' in data else None
                    data = data['data']
                else:
                    msg = logMessage(cursor,query)
                    logging.info(msg)
                    res_ = cursor.fetchall()
                    colnames = [desc[0] for desc in cursor.description]
                    filename = generateExcelOrPDF(payload['downloadType'] if 'downloadType' in payload else None,rows=res_, colnames=colnames)
                    data = res_
                    success = giveSuccess(payload['user_id'], role_access_status, data, total_count, filename=filename)

                if formatData:
                    logging.info(f"Formatting in progress for process {fname}")
                    for row in data:
                        row_dict = {}
                        for i,colname in enumerate(colnames):
                            row_dict[colname] = row[i]
                        res.append(row_dict)
                    return giveSuccess(payload['user_id'], role_access_status, res,total_count,  filename=filename)
                else:
                    return giveSuccess(payload['user_id'],role_access_status,data,total_count,  filename=filename)
                return success
                
    
    except Exception as e:
            logging.exception(f'{fname}_EXCEPTION: <{str(e)}>')
            giveFailure('Invalid Credentials', payload['user_id'], 0)

@app.post('/getClientAdminPaginated')
async def get_client_admin_paginated(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    return await runInTryCatch(
        conn=conn,
        fname='getClientAdminPaginated',
        query="select distinct id, clientname from get_client_info_view ORDER BY clientname",
        payload=payload,
        isPaginationRequired=True,
        whereinquery=False,
        formatData=False
    )


@app.post('/getClientAdmin')
async def get_client_admin(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'get_client_admin: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn, payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = "select distinct id, concat_ws(' ',firstname,lastname) as client_name from client order by concat_ws(' ',firstname,lastname)"
                msg = logMessage(cursor,query)
                logging.info(msg)
                data = cursor.fetchall()
                return giveSuccess(payload['user_id'], role_access_status, data)
        else:
            giveFailure("Access Denied", payload['user_id'], role_access_status)
    except Exception as e:
        logging.exception(f'getClientAdmin_Exception: <{str(e)}>')
        giveFailure('Invalid Credentials', payload['user_id'], 0)

@app.post('/getModesAdmin')
async def get_modes_admin(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'get_modes_admin: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn, payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = "select distinct id, name, entityid from mode_of_payment order by name"
                msg = logMessage(cursor,query)
                logging.info(msg)
                data = cursor.fetchall()
                return giveSuccess(payload['user_id'], role_access_status, data)
        else:
            giveFailure("Access Denied", payload['user_id'], role_access_status)
    except Exception as e:
        logging.exception(f'getModesAdmin_Exception: <{str(e)}>')
        giveFailure('Invalid Credentials', payload['user_id'], 0)

@app.post('/getEntityAdmin')
async def get_entity_admin(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'get_entity_admin: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn, payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = "select distinct id, name from entity order by name"
                msg = logMessage(cursor,query)
                logging.info(msg)
                data = cursor.fetchall()
                return giveSuccess(payload['user_id'], role_access_status, data)
        else:
            giveFailure("Access Denied", payload['user_id'], role_access_status)
    except Exception as e:
        logging.exception(f'getModesAdmin_Exception: <{str(e)}>')
        giveFailure('Invalid Credentials', payload['user_id'], 0)

@app.post('/getHowReceivedAdmin')
async def get_howreceived_admin(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'get_howreceived_admin: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn, payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = "select distinct id, name from howreceived order by name"
                msg = logMessage(cursor,query)
                logging.info(msg)
                data = cursor.fetchall()
                return giveSuccess(payload['user_id'], role_access_status, data)
        else:
            giveFailure("Access Denied", payload['user_id'], role_access_status)
    except Exception as e:
        logging.exception(f'getHowReceivedAdmin_Exception: <{str(e)}>')
        giveFailure('Invalid Credentials', payload['user_id'], 0)

@app.post('/getUsersAdmin')
async def get_users_admin(payload: dict, conn : psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'get_users_admin:payload received is {payload}')
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status==1:
            with conn[0].cursor() as cursor:
                query = "SELECT firstname,lastname,id,username from usertable order by firstname"
                msg = logMessage(cursor,query)
                logging.info(msg)
                arr = []
                data = cursor.fetchall()
                for fname,lname,id,uname in data:
                    arr.append({'id':id,'name':fname+' '+lname,"username":uname})
            return giveSuccess(payload['user_id'],role_access_status,arr,total_count=len(arr))
        else:
           
            return giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure("Invalid Credentials",0,0)

@app.post('/getRolesAdmin')
async def get_roles(payload: dict, conn : psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'get_roles:payload received is {payload}')
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status==1:
            res = roles(conn[0])
            arr = []
            for i in res:
                arr.append({'id':i,'name':res[i]})
            return giveSuccess(payload['user_id'],role_access_status,arr,total_count=len(arr))
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        return giveFailure("Invalid Credentials",0,0)

def clienttype(payload,conn):
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'SELECT id,name from client_type'
                msg = logMessage(cursor,query)
                logging.info(msg)
                logging.info(cursor.statusmessage)
                data = cursor.fetchall()
            colnames = [desc[0] for desc in cursor.description]
            res = {}
            for row in data:
                res[row[0]] = row[1]
            return giveSuccess(payload['user_id'],role_access_status,res)
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        return giveFailure("Invalid Credentials",0,0)

@app.post('/getClientInfo')
async def get_client_info(payload : dict, conn : psycopg2.extensions.connection = Depends(get_db_connection)):
    payload['table_name'] = 'get_client_info_view'
    res = await runInTryCatch(
        conn = conn,
        fname="get_client_info",
        payload=payload,
        isdeleted=True,
        whereinquery=True,
        isPaginationRequired=True,
        formatData=True
    )
    if 'data' in res:
        return giveSuccess(res['user_id'],res['role_id'],{"client_info":res['data']},res['total_count'],filename=res['filename'])
    else:
        return giveFailure("Access Denied",res['user_id'],res['role_id'])





@app.post('/getClientInfoByClientId')
async def get_client_info_by_clientid(payload : dict, conn : psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"get_client_info_by_clientid:received payload <{payload}>")
    try:
        role_access_status = check_role_access(conn, payload)

        if role_access_status == 1:
            data = dict()
            with conn[0].cursor() as cursor:
                ############### Arrange Client Info ##################
                query = f'''
                    select distinct id, salutation, firstname, middlename, lastname,clienttype,
                    country, state, city ,addressline1, addressline2,
                    zip, suburb, email1, email2, mobilephone, homephone, localcontact1name, localcontact1details,
                    localcontact1address, workphone, localcontact2name, localcontact2details, includeinmailinglist,
                    localcontact2address, employername, entityid, comments, tenantof, tenantofproperty 
                    from client where id = {payload['id']}
                '''
                msg = logMessage(cursor,query)
                logging.info(msg)
                colnames = [desc[0] for desc in cursor.description]
                client_info_ = cursor.fetchall()
                client_info = dict()
                for row in client_info_:
                    row_dict = {colname: value for colname, value in zip(colnames, row)}
                    client_info = row_dict
                data["client_info"]  = client_info
                ############### Arrange client access ##################
                query = f'''
                    select id,clientid, onlinemailid, onlinepwd, onlineclue  
                    from client_access where clientid = {payload['id']}
                '''
                msg = logMessage(cursor,query)
                logging.info(msg)
                colnames = [desc[0] for desc in cursor.description]
                _data = cursor.fetchall()
                client_access = []
                for row in _data:
                    row_dict = {colname: value for colname, value in zip(colnames, row)}
                    client_access.append(row_dict)
                data["client_access"] = client_access

                ############### Arrange client bank info ##################
                query = f'''
                    select id,bankname, bankbranch, bankcity, bankaccountno, bankaccountholdername, 
                    bankifsccode, bankmicrcode, bankaccounttype,description
                    from client_bank_info where clientid = {payload['id']}
                '''
                msg = logMessage(cursor,query)
                logging.info(msg)
                colnames = [desc[0] for desc in cursor.description]
                _data = cursor.fetchall()
                client_bankinfo = []
                for row in _data:
                    row_dict = {colname: value for colname, value in zip(colnames, row)}
                    client_bankinfo.append(row_dict)
                data["client_bank_info"] = client_bankinfo

                ############### Arrange client legal info ##################
                query = f'''
                    select distinct id, fulllegalname, panno, addressline1, addressline2, suburb, city, state, country, zip, occupation, birthyear, employername, relation, relationwith
                    from client_legal_info where clientid = {payload['id']}
                '''
                msg = logMessage(cursor,query)
                logging.info(msg)
                colnames = [desc[0] for desc in cursor.description]
                _data = cursor.fetchall()
                client_legalinfo = dict()
                for row in _data:
                    row_dict = {colname: value for colname, value in zip(colnames, row)}
                    client_legalinfo = row_dict
                data["client_legal_info"] = client_legalinfo

                ############### Arrange client poa info ##################
                query = f'''
                    select id,poalegalname, poapanno, poaaddressline1, poaaddressline2, poasuburb, poacity, poastate, poacountry, poazip, poaoccupation, poabirthyear, poaphoto, poaemployername, 
                    poarelation, poarelationwith, poaeffectivedate, poaenddate, poafor, scancopy 
                    from client_poa where clientid = {payload['id']}
                '''
                msg = logMessage(cursor,query)
                logging.info(msg)
                colnames = [desc[0] for desc in cursor.description]
                _data = cursor.fetchall()
                client_poainfo = dict()
                for row in _data:
                    row_dict = {colname: value for colname, value in zip(colnames, row)}
                    client_poainfo = row_dict
                data["client_poa"] = client_poainfo


                return giveSuccess(payload['user_id'],role_access_status,data)
        else:
            return giveFailure("Access Denied",payload["user_id"],role_access_status)
    except Exception as e:
        logging.exception(traceback.print_exc())
        return giveFailure("Invalid Credentials",payload['user_id'],0)


    
@app.post('/getItembyId')
async def get_item_by_id(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f":get_item_by_idreceived payload <{payload}>")
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status==1:
            
            with conn[0].cursor() as cursor:
                query = f"SELECT * FROM {payload['table_name']} WHERe id =%s LIMIT 1"
                msg = logMessage(cursor,query,(payload['item_id'],))
                logging.info(msg)
                data = cursor.fetchone()
                
                colnames = [desc[0] for desc in cursor.description]
                
                res = {}
                if data is None:
                    res = {colname:None for colname in colnames}
                else:
                    for i,e in enumerate(data):
                        res[colnames[i]] = e
            return giveSuccess(payload['user_id'],role_access_status,res)
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        logging.info(traceback.print_exc())
        return {
            giveFailure("Invalid Credentials",0,0)
        }
            
@app.post('/getViewScreenDataTypes')
async def get_view_screen_types(payload: dict, conn : psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'get_view_screen_data_types: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            cursor = conn[0].cursor()
            column_info_list = []
            if 'columns' not in payload:
                query = """SELECT column_name,data_type
                    FROM information_schema.columns
                    WHERE table_name = %s"""
                msg = logMessage(cursor,query,(payload['table_name'],))
                logging.info(msg)
                columns = cursor.fetchall()
                column_info_list = [{"column": col[0], "type": col[1]} for col in columns]
            else:
                for column_name in payload['columns']:
                    query ="""
                        SELECT data_type
                        FROM information_schema.columns
                        WHERE table_name = %s
                        AND column_name = %s
                    """
                    logMessage(cursor,query, (payload['table_name'], column_name))
                    data_type = cursor.fetchone()[0]
                    column_info_list.append({"column": column_name, "type": data_type})
            return giveSuccess(payload['user_id'],role_access_status,column_info_list)
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)
    except psycopg2.Error as e:
        return giveFailure("Invalid Credentials",payload['user_id'],role_access_status)
        
@app.post('/getProjectsByBuilderId')
async def get_projects_by_builder_id(payload: dict,conn : psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"get_projects_by_builder_id:received payload <{payload}>")
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status==1:
            # query = 'SELECT distinct a.id,concat(b.firstname,' ',b.lastname) as paymentby,concat(c.firstname,' ',c.lastname) as paymentto, a.amount,a.paidon,d.name as paymentmode,a.paymentstatus,a.description,a.banktransactionid,e.name as paymentfor,a.dated,a.createdby,a.isdeleted,a.entityid,a.officeid,a.tds,a.professiontax,a.month,a.deduction FROM ref_contractual_payments a,usertable b, usertable c, mode_of_payment d, payment_for e where a.paymentto = b.id and a.paymentby = c.id and a.paymentmode = d.id and a.paymentfor = e.id;'
            table_name = 'get_projects_view'
            # data = filterAndPaginate(DATABASE_URL, payload['rows'], table_name, payload['filters'], payload['sort_by'], payload['order'], payload["pg_no"], payload["pg_size"],query = query,search_key = payload['search_key'] if 'search_key' in payload else None)

            data = filterAndPaginate(DATABASE_URL, payload['rows'], table_name, payload['filters'], payload['sort_by'], payload['order'], payload["pg_no"], payload["pg_size"],search_key = payload['search_key'] if 'search_key' in payload else None)
            total_count = data['total_count']
            colnames = payload['rows']
            res = []
            for row in data['data']:
                row_dict = {}
                for i,colname in enumerate(colnames):
                    row_dict[colname] = row[i]
                if row_dict['builderid'] == payload['builderid']:
                    res.append(row_dict)
            return giveSuccess(payload["user_id"],role_access_status,res, total_count=len(res))
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)        
    except Exception as e:
        print(traceback.print_exc())
        giveFailure("Invalid Credentials",payload['user_id'],0) 

@app.post('/getBuilderContactsById')
async def get_builder_contacts(payload: dict,conn : psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"get_builder_contacts:received payload <{payload}>")
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status==1:
            # query = 'SELECT distinct a.id,concat(b.firstname,' ',b.lastname) as paymentby,concat(c.firstname,' ',c.lastname) as paymentto, a.amount,a.paidon,d.name as paymentmode,a.paymentstatus,a.description,a.banktransactionid,e.name as paymentfor,a.dated,a.createdby,a.isdeleted,a.entityid,a.officeid,a.tds,a.professiontax,a.month,a.deduction FROM ref_contractual_payments a,usertable b, usertable c, mode_of_payment d, payment_for e where a.paymentto = b.id and a.paymentby = c.id and a.paymentmode = d.id and a.paymentfor = e.id;'
            table_name = 'get_builder_contact_view'
            # data = filterAndPaginate(DATABASE_URL, payload['rows'], table_name, payload['filters'], payload['sort_by'], payload['order'], payload["pg_no"], payload["pg_size"],query = query,search_key = payload['search_key'] if 'search_key' in payload else None)
            payload['filters'].append(["builderid","equalTo",payload['builderid'],"Numeric"])
            data = filterAndPaginate_v2(DATABASE_URL, payload['rows'], table_name,payload['filters'], payload['sort_by'],
                                        payload['order'], payload["pg_no"], payload["pg_size"],
                                        search_key = payload['search_key'] if 'search_key' in payload else None,
                                        downloadType=payload['downloadType'] if 'downloadType' in payload else None )
            total_count = data['total_count']
            colnames = payload['rows']
            res = []
            for row in data['data']:
                row_dict = {}
                for i,colname in enumerate(colnames):
                    row_dict[colname] = row[i]
                res.append(row_dict)
            return giveSuccess(payload["user_id"],role_access_status,res, data['total_count'])
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)        
    except Exception as e:
        print(traceback.print_exc())
        giveFailure("Invalid Credentials",payload['user_id'],0) 

@app.post('/getClientProperty')
async def get_client_property(payload : dict, conn : psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'get_client_property: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn, payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                data = filterAndPaginate_v2(DATABASE_URL, payload['rows'], 'get_client_property_view', payload['filters'],
                                        payload['sort_by'], payload['order'], payload["pg_no"], payload["pg_size"],
                                        search_key = payload['search_key'] if 'search_key' in payload else None,
                                        downloadType=payload['downloadType'] if 'downloadType' in payload else None )
                colnames = data['colnames']
                total_count = data['total_count']
                res = []
                filename = data['filename'] if "filename" in data else None
                for row in data['data']:
                    row_dict = {}
                    for i,colname in enumerate(colnames):
                        row_dict[colname] = row[i]
                    # row_dict['country'] = get_name(row_dict['country'],countries)
                    # row_dict['city'] = get_name(row_dict['city'],cities)
                    res.append(row_dict)
                    data={
                        "client_info":res
                    }
                
                return giveSuccess(payload['user_id'],role_access_status,data,total_count,filename)
        else:
            return giveFailure("Access Denied",payload["user_id"],role_access_status)
    except Exception as e:
        logging.exception(traceback.print_exc())
        return giveFailure("Invalid Credentials",payload['user_id'],0)

@app.post('/getBuildersAndProjectsList')
async def get_builders_and_projects_list(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'get_builders_and_projects_list: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn, payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'select distinct a.id as builderid, a.buildername, b.id as projectid, b.projectname from builder a, project b where a.id = b.builderid order by a.buildername asc'
                msg = logMessage(cursor,query)
                logging.info(msg)
                data_ = cursor.fetchall()
                data = []
                for row in data_:
                    dictrow = {"builderid" : row[0], "buildername" : row[1], "projectid" : row[2], "projectname" : row[3]}
                    data.append(dictrow)
                logging.info(f'getBuildersAndProjectsList: fetched <{len(data)}> rows')
                return giveSuccess(payload['user_id'], role_access_status, data)
        else:
            return giveFailure("Access Denied", payload["user_id"], role_access_status)
    except Exception as e:
        logging.exception(traceback.print_exc())
        return giveFailure("Invalid Credentials", payload['user_id'], 0)

@app.post('/addClientInfo')
async def add_client_info(payload : dict, conn : psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"add_client_info:received payload <{payload}>")
    try:
        role_access_status =check_role_access(conn,payload)
        client_info = payload['client_info']
        if role_access_status == 1:
            # tempdata = {
            #     "cliententrydone":{
            #         client
            #     }
            # }
            client_info = payload['client_info']
            global id
            with conn[0].cursor() as cursor:
                query = "INSERT INTO client (firstname,middlename,lastname,salutation,clienttype,addressline1,addressline2,suburb,city,state,country,zip,homephone,workphone,mobilephone,email1,email2,employername,comments,photo,onlineaccreated,localcontact1name,localcontact1address,localcontact1details,localcontact2name,localcontact2address,localcontact2details,includeinmailinglist,dated,createdby,isdeleted,entityid,tenantof,tenantofproperty) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id"
                msg = logMessage(cursor,query,(client_info["firstname"],client_info["middlename"],client_info["lastname"],client_info["salutation"],client_info["clienttype"],client_info["addressline1"],client_info["addressline2"],client_info["suburb"],client_info["city"],client_info["state"],client_info["country"],client_info["zip"],client_info["homephone"],client_info["workphone"],client_info["mobilephone"],client_info["email1"],client_info["email2"],client_info["employername"],client_info["comments"],client_info["photo"],client_info["onlineaccreated"],client_info["localcontact1name"],client_info["localcontact1address"],client_info["localcontact1details"],client_info["localcontact2name"],client_info["localcontact2address"],client_info["localcontact2details"],client_info["includeinmailinglist"],givenowtime(),payload['user_id'],False,client_info["entityid"],client_info["tenantof"],client_info["tenantofproperty"]))
                logging.info(msg)
                #--insert query for client_access table--
                id = cursor.fetchone()[0]
                conn[0].commit()
                client_access_list = payload['client_access']
                client_bank_info_list = payload['client_bank_info']
                client_legal_info = payload['client_legal_info']
                client_poa = payload['client_poa']
                for client_access in client_access_list:
                    client_access['clientid'] = id 
                    query = "INSERT INTO client_access (clientid,onlinemailid,onlinepwd,onlineclue,dated,createdby,isdeleted) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                    logMessage(cursor,query,(client_access['clientid'],client_access["onlinemailid"],client_access["onlinepwd"],client_access["onlineclue"],givenowtime(),payload['user_id'],False))
                for client_bank_info in client_bank_info_list:
                    client_bank_info['clientid'] = id
                    query = "INSERT INTO client_bank_info (clientid,bankname,bankbranch,bankcity,bankaccountno,bankaccountholdername,bankifsccode,bankmicrcode,bankaccounttype,dated,createdby,isdeleted,description) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    logMessage(cursor,query,(client_bank_info['clientid'],client_bank_info["bankname"],client_bank_info["bankbranch"],client_bank_info["bankcity"],client_bank_info["bankaccountno"],client_bank_info["bankaccountholdername"],client_bank_info["bankifsccode"],client_bank_info["bankmicrcode"],client_bank_info["bankaccounttype"],givenowtime(),payload['user_id'],False,client_bank_info["description"]))
                client_legal_info['clientid'] = id
                query = "INSERT INTO client_legal_info (clientid,fulllegalname,panno,addressline1,addressline2,suburb,city,state,country,zip,occupation,birthyear,employername,relation,relationwith,dated,createdby,isdeleted) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                logMessage(cursor,query,(client_legal_info['clientid'],client_legal_info["fulllegalname"],client_legal_info["panno"],client_legal_info["addressline1"],client_legal_info["addressline2"],client_legal_info["suburb"],client_legal_info["city"],client_legal_info["state"],client_legal_info["country"],client_legal_info["zip"],client_legal_info["occupation"],client_legal_info["birthyear"],client_legal_info["employername"],client_legal_info["relation"],client_legal_info["relationwith"],givenowtime(),payload['user_id'],False))
                client_poa['clientid'] = id
                query = ("INSERT INTO client_poa (clientid,poalegalname,poapanno,poaaddressline1,poaaddressline2,poasuburb,poacity,"
                         "poastate,poacountry,poazip,poaoccupation,poabirthyear,poaphoto,poaemployername,poarelation,poarelationwith,"
                         "poaeffectivedate,poaenddate,poafor,scancopy,dated,createdby,isdeleted) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
                logMessage(cursor,query,(client_poa['clientid'],client_poa["poalegalname"],client_poa["poapanno"],client_poa["poaaddressline1"],
                                      client_poa["poaaddressline2"],client_poa["poasuburb"],client_poa["poacity"],client_poa["poastate"],
                                      client_poa["poacountry"],client_poa["poazip"],client_poa["poaoccupation"],client_poa["poabirthyear"],
                                      client_poa["poaphoto"],client_poa["poaemployername"],client_poa["poarelation"],client_poa["poarelationwith"],
                                      client_poa["poaeffectivedate"],client_poa["poaenddate"],client_poa["poafor"],client_poa["scancopy"],
                                      givenowtime(),payload['user_id'],False))
                conn[0].commit()
                return giveSuccess(payload['user_id'],role_access_status,{"inserted_id":id})
        else:
            return giveFailure("Access Denied",client_info['user_id'],role_access_status)
    except KeyError as ke:
        logging.info(traceback.print_exc())
        try:
            conn = psycopg2.cursor(DATABASE_URL)
            with conn.cursor() as cursor:
                msg = logMessage(cursor,"DELETE FROM client WHERE id=%s",(id,))
                logging.info(msg)
                conn.commit()
            
            # conn[0].rollback()
            return giveFailure(f"Error: {ke} not present",0,0)
        except Exception as e:
            logging.info(f"Client id {id} could not be deleted")  
    except Exception as e:
        logging.info(traceback.print_exc())
        # print(traceback.print_exc())
        try:
            with conn[0].cursor() as cursor:
                logMessage(cursor,"DELETE FROM client WHERE id=%s",(id,))
                conn[0].commit()
            
            conn[0].rollback()
            return giveFailure(f"Error {e}",0,0)
        except Exception as e:
            logging.info(f"Client id {id} could not be deleted")

# @app.post("/addClientProperty")
# async def add_client_property(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
#     return True

@app.post('/getClientTypeAdmin')
async def get_client_type_admin(payload : dict, conn: psycopg2.extensions.connection =Depends(get_db_connection)):
    logging.info(f":get_client_type_adminreceived payload <{payload}>")
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'SELECT distinct id,name from client_type order by name'
                msg = logMessage(cursor,query)
                logging.info(msg)
                data = cursor.fetchall()
            colnames = [desc[0] for desc in cursor.description]
            res = []
            for row in data:
                row_dict = {}
                for i,e in enumerate(colnames):
                    row_dict[e] = row[i]
                res.append(row_dict)
            return giveSuccess(payload['user_id'],role_access_status,res)
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        return giveFailure("Invalid Credentials",0,0)
    
@app.post('/getRelationAdmin')
async def get_relation_admin(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"get_relation_admin:received payload <{payload}>")
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'SELECT distinct id,name from relation order by name'
                msg = logMessage(cursor,query)
                logging.info(msg)
                data = cursor.fetchall()
            colnames = [desc[0] for desc in cursor.description]
            res = []
            for row in data:
                row_dict = {}
                for i,e in enumerate(colnames):
                    row_dict[e] = row[i]
                res.append(row_dict)
            return giveSuccess(payload['user_id'],role_access_status,res)
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        return giveFailure("Invalid Credentials",0,0)
       
@app.post('/getTenantOfPropertyAdmin')
async def get_tenant_of_property_admin(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"get_tenant_of_property_admin:received payload <{payload}>")
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'SELECT distinct id,propertydescription,suburb from client_property order by suburb'
                msg = logMessage(cursor,query)
                logging.info(msg)
                data = cursor.fetchall()
            colnames = [desc[0] for desc in cursor.description]
            res = []
            for row in data:
                row_dict = {}
                for i,e in enumerate(colnames):
                    row_dict[e] = row[i]
                res.append(row_dict)
            return giveSuccess(payload['user_id'],role_access_status,res)
        else:
            
            return giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure("Invalid Credentials",0,0)
    
@app.post('/deleteClientInfo')
async def delete_client_info(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"delete_client_info:received payload <{payload}>")
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'UPDATE client SET isdeleted=true WHERE id=%s AND isdeleted=false'
                msg = logMessage(cursor,query,(payload['id'],))
                logging.info(msg)
                if cursor.statusmessage == "UPDATE 0":
                    return giveFailure(f"No Client available with id {payload['id']}",payload['user_id'],role_access_status)

                query = "UPDATE client_access SET isdeleted=true WHERE clientid=%s"
                logMessage(cursor,query,(payload['id'],))
                query = "UPDATE client_bank_info SET isdeleted=true WHERE clientid=%s"
                logMessage(cursor,query,(payload['id'],))
                query = "UPDATE client_legal_info SET isdeleted=true WHERE clientid=%s"
                logMessage(cursor,query,(payload['id'],))
                query = "UPDATE client_poa SET isdeleted=true WHERE clientid=%s"
                logMessage(cursor,query,(payload['id'],))
                conn[0].commit()
            data = {
                "deleted_client":payload['id']
            }
            return giveSuccess(payload['user_id'],role_access_status,data)
        else:
            giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        print(traceback.print_exc())
        giveFailure("Invalid Credentials",payload['user_id'],0)

@app.post("/addProject")
async def add_project(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'add_project: received payload <{payload}>')
    try:
        global id
        role_access_status = check_role_access(conn, payload)
        if role_access_status == 1:
            project_info = payload['project_info']
            project_amenities = payload['project_amenities']
            bank_details_list = payload['project_bank_details']
            project_contacts_list = payload['project_contacts']
            project_photos_list = payload['project_photos']
            with conn[0].cursor() as cursor:
                query = "insert into project(builderid,projectname,addressline1,addressline2,suburb,city,state,country,zip,nearestlandmark,project_type,mailgroup1,mailgroup2,website,project_legal_status,rules,completionyear,jurisdiction,taluka,corporationward,policestation,policechowkey,maintenance_details,numberoffloors,numberofbuildings,approxtotalunits,tenantstudentsallowed,tenantworkingbachelorsallowed,tenantforeignersallowed,otherdetails,duespayablemonth,dated,createdby,isdeleted) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) returning id"
                msg = logMessage(cursor,query,(project_info["builderid"],project_info["projectname"],project_info["addressline1"],project_info["addressline2"],project_info["suburb"],project_info["city"],project_info["state"],project_info["country"],project_info["zip"],project_info["nearestlandmark"],project_info["project_type"],project_info["mailgroup1"],project_info["mailgroup2"],project_info["website"],project_info["project_legal_status"],project_info["rules"],project_info["completionyear"],project_info["jurisdiction"],project_info["taluka"],project_info["corporationward"],project_info["policestation"],project_info["policechowkey"],project_info["maintenance_details"],project_info["numberoffloors"],project_info["numberofbuildings"],project_info["approxtotalunits"],project_info["tenantstudentsallowed"],project_info["tenantworkingbachelorsallowed"],project_info["tenantforeignersallowed"],project_info["otherdetails"],project_info["duespayablemonth"],givenowtime(),payload['user_id'],False))
                logging.info(msg)
                id = cursor.fetchone()[0]
                conn[0].commit()
                query = 'insert into project_amenities(projectid,swimmingpool,lift,liftbatterybackup,clubhouse,gym,childrensplayarea,pipedgas,cctvcameras,otheramenities,studio,"1BHK","2BHK","3BHK","4BHK","RK",other,duplex,penthouse,rowhouse,otheraccomodationtypes,sourceofwater,dated,createdby,isdeleted) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) returning id'
                logMessage(cursor,query,(id,project_amenities["swimmingpool"],project_amenities["lift"],project_amenities["liftbatterybackup"],project_amenities["clubhouse"],project_amenities["gym"],project_amenities["childrensplayarea"],project_amenities["pipedgas"],project_amenities["cctvcameras"],project_amenities["otheramenities"],project_amenities["studio"],project_amenities["1BHK"],project_amenities["2BHK"],project_amenities["3BHK"],project_amenities["4BHK"],project_amenities["RK"],project_amenities["other"],project_amenities["duplex"],project_amenities["penthouse"],project_amenities["rowhouse"],project_amenities["otheraccomodationtypes"],project_amenities["sourceofwater"],givenowtime(),payload['user_id'],False))
                data = {
                    "added project id":id
                }
                for bank_details in bank_details_list:
                    query = 'insert into project_bank_details(projectid,bankname,bankbranch,bankcity,bankaccountholdername,bankaccountno,bankifsccode,banktypeofaccount,bankmicrcode,dated,createdby,isdeleted) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                    logMessage(cursor,query,(id,bank_details["bankname"],bank_details["bankbranch"],bank_details["bankcity"],bank_details["bankaccountholdername"],bank_details["bankaccountno"],bank_details["bankifsccode"],bank_details["banktypeofaccount"],bank_details['bankmicrcode'],givenowtime(),payload['user_id'],False))
                for project_contacts in project_contacts_list:
                    query = 'insert into project_contacts(projectid,contactname,phone,email,role,effectivedate,tenureenddate,details,dated,createdby,isdeleted) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                    logMessage(cursor,query,(id,project_contacts["contactname"],project_contacts["phone"],project_contacts["email"],project_contacts["role"],project_contacts["effectivedate"],project_contacts["tenureenddate"],project_contacts["details"],givenowtime(),payload['user_id'],False))
                for project_photos in project_photos_list:
                    query = 'insert into project_photos(projectid,photo_link,description,date_taken,dated,createdby,isdeleted) values(%s,%s,%s,%s,%s,%s,%s)'
                    logMessage(cursor,query,(id,project_photos["photo_link"],project_photos["description"],project_photos["date_taken"],givenowtime(),payload['user_id'],False))
                conn[0].commit()
                return giveSuccess(payload['user_id'],role_access_status,data)
        elif role_access_status!=1:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)
        # else:
        #     return giveFailure("Already Exists",payload['user_id'],role_access_status)
    except Exception as e:
        return giveFailure("Invalid Credentials",payload['user_id'],0)
@app.post('/addClientProperty')
async def add_client_property(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"add_client_property:received payload <{payload}>")
    try:
        global prop_id
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                client_property = payload['client_property']
                client_property_photos_list = payload['client_property_photos']
                client_property_poa = payload['client_property_poa']
                client_property_owner = payload['client_property_owner']
                query = "INSERT INTO client_property (clientid,projectid,propertydescription,propertytype,suburb,city,state,country,layoutdetails,numberofparkings,internalfurnitureandfittings,leveloffurnishing,status,initialpossessiondate,poagiven,poaid,electricityconsumernumber,electricitybillingunit,otherelectricitydetails,gasconnectiondetails,propertytaxnumber,clientservicemanager,propertymanager,comments,propertyownedbyclientonly,textforposting,electricitybillingduedate,dated,createdby,isdeleted,indexiicollected) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id"
                msg = logMessage(cursor,query,(client_property["clientid"],client_property["projectid"],client_property["propertydescription"],client_property['propertytype'],client_property["suburb"],client_property["city"],client_property["state"],client_property["country"],client_property["layoutdetails"],client_property["numberofparkings"],client_property["internalfurnitureandfittings"],client_property["leveloffurnishing"],client_property["status"],client_property["initialpossessiondate"],client_property["poagiven"],client_property["poaid"],client_property["electricityconsumernumber"],client_property["electricitybillingunit"],client_property["otherelectricitydetails"],client_property["gasconnectiondetails"],client_property["propertytaxnumber"],client_property["clientservicemanager"],client_property["propertymanager"],client_property["comments"],client_property["propertyownedbyclientonly"],client_property["textforposting"],client_property["electricitybillingduedate"],givenowtime(),payload['user_id'],False,client_property['indexiicollected']))
                logging.info(msg)
                prop_id = cursor.fetchone()[0]
                conn[0].commit()
                for client_property_photos in client_property_photos_list:
                    query = "INSERT INTO client_property_photos (clientpropertyid,photolink,description,phototakenwhen,dated,createdby,isdeleted) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                    logMessage (cursor,query,(prop_id,client_property_photos["photolink"],client_property_photos["description"],client_property_photos["phototakenwhen"],givenowtime(),payload['user_id'],False))
                query = "INSERT INTO client_property_poa (clientpropertyid,poalegalname,poapanno,poaaddressline1,poaaddressline2,poasuburb,poacity,poastate,poacountry,poazip,poaoccupation,poabirthyear,poaphoto,poaemployername,poarelation,poarelationwith,poaeffectivedate,poaenddate,poafor,scancopy,dated,createdby,isdeleted) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                logMessage (cursor,query,(prop_id,client_property_poa["poalegalname"],client_property_poa["poapanno"],client_property_poa["poaaddressline1"],client_property_poa["poaaddressline2"],client_property_poa["poasuburb"],client_property_poa["poacity"],client_property_poa["poastate"],client_property_poa["poacountry"],client_property_poa["poazip"],client_property_poa["poaoccupation"],client_property_poa["poabirthyear"],client_property_poa["poaphoto"],client_property_poa["poaemployername"],client_property_poa["poarelation"],client_property_poa["poarelationwith"],client_property_poa["poaeffectivedate"],client_property_poa["poaenddate"],client_property_poa["poafor"],client_property_poa["scancopy"],givenowtime(),payload['user_id'],False))
                query = "INSERT INTO client_property_owner (propertyid,owner1name,owner1panno,owner1aadhaarno,owner1pancollected,owner1aadhaarcollected,owner2name,owner2panno,owner2aadhaarno,owner2pancollected,owner2aadhaarcollected,owner3name,owner3panno,owner3aadhaarno,owner3pancollected,owner3aadhaarcollected,comments,dated,createdby,isdeleted) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                logMessage (cursor,query,(prop_id,client_property_owner["owner1name"],client_property_owner["owner1panno"],client_property_owner["owner1aadhaarno"],client_property_owner["owner1pancollected"],client_property_owner["owner1aadhaarcollected"],client_property_owner["owner2name"],client_property_owner["owner2panno"],client_property_owner["owner2aadhaarno"],client_property_owner["owner2pancollected"],client_property_owner["owner2aadhaarcollected"],client_property_owner["owner3name"],client_property_owner["owner3panno"],client_property_owner["owner3aadhaarno"],client_property_owner["owner3pancollected"],client_property_owner["owner3aadhaarcollected"],client_property_owner["comments"],givenowtime(),payload['user_id'],False))
                conn[0].commit()
                return giveSuccess(payload['user_id'],role_access_status,{"inserted_property":prop_id})
        else:
            return giveFailure("Access denied",payload['user_id'],role_access_status)
    except KeyError as e:
        logging.info(traceback.print_exc)
        return giveFailure(f"Key missing {e}",0,0)
    except Exception as e:
        print(traceback.print_exc())
        try:
            conn = psycopg2.connect(DATABASE_URL)
            conn.cursor().execute("delete from client_property where id=%s",(prop_id,))
            return giveFailure('Invalid Credentials',0,0)
        

        
        except Exception as e:
            logging.info(traceback.print_exc())
            return giveFailure(f"Could not delete id: {prop_id}",0,0)
    



@app.post('/editClientInfo')
async def edit_client_info(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'edit_client_info: received payload <{payload}>')
    try:
        data = f"successfully edited client info for clientid {payload['client_id']}"
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            ci = payload['client_info']
            clientid = payload['client_id']
            with conn[0].cursor() as cursor:
                # update client information in 'client' table
                query = ('UPDATE client SET '
                         'firstname=%s,' 'middlename=%s,' 'lastname=%s,' 'salutation=%s,' 'clienttype=%s,'
                         'addressline1=%s,' 'addressline2=%s,' 'suburb=%s,' 'city=%s,' 'state=%s,'
                         'country=%s,' 'zip=%s,' 'homephone=%s,' 'workphone=%s,' 'mobilephone=%s,'
                         'email1=%s,' 'email2=%s,' 'employername=%s,' 'comments=%s,' 
                         'localcontact1name=%s,' 'localcontact1address=%s,' 'localcontact1details=%s,'
                         'localcontact2name=%s,' 'localcontact2address=%s,' 'localcontact2details=%s,' 
                         'includeinmailinglist=%s,' 'entityid=%s,' 'tenantof=%s,' 'tenantofproperty=%s WHERE ID=%s')
                msg = logMessage(cursor,
                    query,(
                        ci["firstname"],ci["middlename"],ci["lastname"],ci["salutation"],
                        ci["clienttype"],ci["addressline1"],ci["addressline2"],ci["suburb"],ci["city"],ci["state"],
                        ci["country"],ci["zip"],ci["homephone"],ci["workphone"],ci["mobilephone"],
                        ci["email1"],ci["email2"],ci["employername"],ci["comments"],
                        ci["localcontact1name"],ci["localcontact1address"],ci["localcontact1details"],
                        ci["localcontact2name"],ci["localcontact2address"],ci["localcontact2details"],
                        ci["includeinmailinglist"], ci["entityid"], ci["tenantof"],ci["tenantofproperty"],ci['id']))
                logging.info(msg)
                conn[0].commit()
                logging.info(f'editClientInfo: client_info update status is <{cursor.statusmessage}>')
                # perform CRUD for client accesses in 'client_access' table
                if 'client_access' in payload and 'update' in payload['client_access']:
                    for u in payload['client_access']['update']:
                        query = ('UPDATE client_access SET onlinemailid=%s,' 'onlinepwd=%s,' 'onlineclue=%s  WHERE ID=%s and clientid=%s')
                        data = logMessage(cursor, query,(u["onlinemailid"], u["onlinepwd"], u["onlineclue"], u["id"], clientid))
                        conn[0].commit()
                        logging.info(f'editClientInfo: client_access clientid <{clientid}>, rowid <{u["id"]}> UPDATE status is <{cursor.statusmessage}>')
                if 'client_access' in payload and 'insert' in payload['client_access']:
                    for u in payload['client_access']['insert']:
                        query = ('INSERT into client_access (onlinemailid,onlinepwd,onlineclue,clientid) values (%s,%s,%s,%s)')
                        data = logMessage(cursor, query,(u["onlinemailid"], u["onlinepwd"], u["onlineclue"], clientid))
                        conn[0].commit()
                        logging.info(f'editClientInfo: client_access clientid <{clientid}> INSERT status is <{cursor.statusmessage}>')

                # perform CRUD for client bank information in 'client_bank_info' table
                if 'client_bank_info' in payload and 'update' in payload['client_bank_info']:
                    for u in payload['client_bank_info']['update']:
                        # todo: may need to add "description" when UI starts sending it. It is part of the bank_info section
                        query = ('UPDATE client_bank_info SET bankname=%s,bankaccountholdername=%s,bankaccountno=%s,bankaccounttype=%s,'
                                 'bankbranch=%s,bankcity=%s,bankifsccode=%s, bankmicrcode=%s, description=%s  WHERE ID=%s and clientid=%s')
                        data = logMessage(cursor, query,(u['bankname'],
                            u["bankaccountholdername"], u["bankaccountno"], u["bankaccounttype"],
                            u["bankbranch"], u["bankcity"], u["bankifsccode"], u["bankmicrcode"], u['description'],u["id"], clientid))
                        conn[0].commit()
                        logging.info(f'editClientInfo: client_access clientid <{clientid}>, rowid <{u["id"]}> UPDATE status is <{cursor.statusmessage}>')
                if 'client_bank_info' in payload and 'insert' in payload['client_bank_info']:
                    for u in payload['client_bank_info']['insert']:
                        query = ('INSERT into client_bank_info (bankname,bankaccountholdername,bankaccountno,bankaccounttype,bankbranch,bankcity,bankifsccode,bankmicrcode,description,clientid) '
                                 'values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)')
                        data = logMessage(cursor, query,(u["bankname"],u["bankaccountholdername"], u["bankaccountno"], u["bankaccounttype"],
                            u["bankbranch"], u["bankcity"], u["bankifsccode"], u["bankmicrcode"], u['description'],clientid))
                        conn[0].commit()
                        logging.info(f'editClientInfo: client_bank_info clientid <{clientid}> INSERT status is <{cursor.statusmessage}>')

                # update client legalinfo in 'client_legal_info' table
                li = payload['client_legal_info']
                query = ('UPDATE client_legal_info SET '
                         'fulllegalname=%s,' 'panno=%s,' 'addressline1=%s,' 'addressline2=%s,' 'suburb=%s,'
                         'city=%s,' 'state=%s,' 'country=%s,' 'zip=%s,' 'occupation=%s,'
                         'birthyear=%s,' 'employername=%s,' 'relation=%s,' 'relationwith=%s '
                         'WHERE ID=%s and clientid=%s')
                data = logMessage(cursor,
                    query,(li['fulllegalname'],li['panno'], li['addressline1'], li['addressline2'],
                           li['suburb'], li['city'], li['state'], li['country'], li['zip'], li['occupation'],
                           li['birthyear'], li['employername'], li['relation'], li['relationwith'], li['id'],
                           clientid))
                conn[0].commit()
                logging.info(f'editClientInfo: client_legal_info update status is <{cursor.statusmessage}>')

                # update client_poa in 'client_poa' table
                pi = payload['client_poa']
                query = ('UPDATE client_poa SET '
                         'poaaddressline1=%s,' 'poaaddressline2=%s,' 'poabirthyear=%s,' 'poacity=%s,' 'poacountry=%s,'
                         'poaeffectivedate=%s,' 'poaemployername=%s,' 'poaenddate=%s,' 'poafor=%s,' 'poalegalname=%s,'
                         'poaoccupation=%s,' 'poapanno=%s,' 'poaphoto=%s,' 'poarelation=%s, poarelationwith=%s, poastate=%s,'
                         'poasuburb=%s, poazip=%s,scancopy=%s WHERE ID=%s and clientid=%s')
                data = logMessage(cursor, query,(pi['poaaddressline1'],pi['poaaddressline2'], pi['poabirthyear'], pi['poacity'], pi['poacountry'],
                           pi['poaeffectivedate'], pi['poaemployername'], pi['poaenddate'], pi['poafor'], pi['poalegalname'],
                           pi['poaoccupation'], pi['poapanno'], pi['poaphoto'], pi['poarelation'], pi['poarelationwith'],
                           pi['poastate'],pi['poasuburb'], pi['poazip'],pi['scancopy'],pi['id'], clientid))
                conn[0].commit()
                logging.info(f'editClientInfo: client_poa update status is <{cursor.statusmessage}>')
        return giveSuccess(payload['user_id'],role_access_status,data)
    except Exception as e:
         logging.info(traceback.print_exc())
         return giveFailure(f"Failed To Edit given client info due to <{traceback.print_exc()}>",0,0)

@app.post('/deleteClientProperty')
async def delete_client_property(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"delete_client_property:received payload <{payload}>")
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'UPDATE client_property SET isdeleted=true WHERE id=%s AND isdeleted = false'
                msg = logMessage(cursor,query,(payload['id'],))
                logging.info(msg)
                if cursor.statusmessage == "UPDATE 0":
                    return giveFailure("No Property available",payload['user_id'],role_access_status)

                query = "UPDATE client_property_poa SET isdeleted=true WHERE clientpropertyid = %s"
                logMessage(cursor,query,(payload['id'],))
                query = "UPDATE client_property_photos  SET isdeleted=true WHERE clientpropertyid = %s"
                logMessage(cursor,query,(payload['id'],))
                query = "UPDATE client_property_owner SET isdeleted=true WHERE propertyid = %s"
                logMessage(cursor,query,(payload['id'],))
                conn[0].commit()
            data = {
                "deleted_client_property":payload['id']
            }
            return giveSuccess(payload['user_id'],role_access_status,data)
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        print(traceback.print_exc())
        giveFailure("Invalid Credentials",payload['user_id'],0)


@app.post('/getPropertyStatusAdmin')
async def get_property_status_admin(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"get_property_status_admin:received payload <{payload}>")
    try:
        with conn[0].cursor() as cursor:
            query = 'SELECT DISTINCT id,name from property_status order by id'
            msg = logMessage(cursor,query)
            logging.info(msg)
            data = cursor.fetchall()
        res = []
        for i in data:
            res.append({
                "id":i[0],
                "name":i[1]
            })
        return res
    except Exception as e:
        logging.info(traceback.print_exc())
        logging.info(f"Error is {e}")
        return None    

@app.post('/getLevelOfFurnishingAdmin')
async def get_level_of_furnishing(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"get_level_of_furnishing:received payload <{payload}>")
    try:
        with conn[0].cursor() as cursor:
            query = 'SELECT DISTINCT id,name from level_of_furnishing order by id'
            msg = logMessage(cursor,query)
            logging.info(msg)
            data = cursor.fetchall()
        res = []
        for i in data:
            res.append({
                "id":i[0],
                "name":i[1]
            })
            
        # logging.info(res)
        return res
    except Exception as e:
        logging.info(traceback.print_exc())
        logging.info(f"Error is {e}")
        return None    

@app.post('/getPropertyType')
async def get_property_type(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"get_property_type :received payload <{payload}>")
    try:
        with conn[0].cursor() as cursor:
            query = 'SELECT DISTINCT id,name from property_type order by id'
            msg = logMessage(cursor,query)
            logging.info(msg)
            data = cursor.fetchall()
        res = []
        for i in data:
            res.append({
                "id":i[0],
                "name":i[1]
            })
        return res
    except Exception as e:
        logging.info(traceback.print_exc())
        logging.info(f"Error is {e}")
        return None    


@app.post('/editClientProperty')
async def edit_client_property(payload: dict,conn : psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"edit_client_property :received payload <{payload}>")
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            ci = payload['client_property_info']
            propertyid = payload['client_property_id']
            with conn[0].cursor() as cursor:
                # update client information in 'client' table
                query = ''.join(('UPDATE client_property SET '
                         'clientid=%s,' 'propertytype=%s,' 'leveloffurnishing=%s,' 'numberofparkings=%s,' 'state=%s,' 'city=%s,' 
                         'suburb=%s,' 'projectid=%s,' 'status=%s,'
                         'propertydescription=%s,' 'layoutdetails=%s,' 'email=%s,' 'website=%s,' 'initialpossessiondate=%s,'
                         'electricityconsumernumber=%s,' 'otherelectricitydetails=%s,' 'electricitybillingduedate=%s,' 'comments=%s,' 
                         'gasconnectiondetails=%s,' 'indexiicollected=%s,' 'textforposting=%s WHERE ID=%s and isdeleted = false'))
                msg = logMessage(cursor,
                    query,(
                        ci["clientid"],ci["propertytype"],ci["leveloffurnishing"],ci["numberofparkings"],
                        ci["state"],ci["city"],ci["suburb"],ci["projectid"],ci["status"],ci["propertydescription"],
                        ci["layoutdetails"],ci["email"],ci["website"],ci["initialpossessiondate"],ci["electricityconsumernumber"],
                        ci["otherelectricitydetails"],ci["electricitybillingduedate"],ci["comments"],ci["gasconnectiondetails"],
                        ci["indexiicollected"],ci["textforposting"],propertyid))
                logging.info(msg)
                if cursor.statusmessage == 'UPDATE 0':
                    return giveFailure('No record found',payload['user_id'],role_access_status)
                conn[0].commit()
                
                logging.info(f'editClientproperty: client_property_info update status is <{cursor.statusmessage}>')
                # perform CRUD for client accesses in 'client_access' table
                if 'client_property_photos' in payload and 'update' in payload['client_property_photos']:
                    for u in payload['client_property_photos']['update']:
                        query = ('UPDATE client_property_photos SET photolink=%s,' 'description=%s,' 'phototakenwhen=%s  WHERE id=%s and clientpropertyid=%s')
                        data = logMessage(cursor, query,(u["photolink"], u["description"], u["phototakenwhen"], u["id"], propertyid))
                        conn[0].commit()
                        logging.info(f'editClientProperty: client_property_photos propertyid <{propertyid}>, rowid <{u["id"]}> UPDATE status is <{cursor.statusmessage}>')
                if 'client_property_photos' in payload and 'insert' in payload['client_property_photos']:
                    for u in payload['client_property_photos']['insert']:
                        query = ('INSERT into client_property_photos (photolink,description,phototakenwhen,clientpropertyid) values (%s,%s,%s,%s)')
                        data = logMessage(cursor, query,(u["photolink"], u["description"], u["phototakenwhen"], propertyid))
                        conn[0].commit()
                        logging.info(f'editClientProperty: client_property_photos clientid <{propertyid}> INSERT status is <{cursor.statusmessage}>')

                # # perform CRUD for client bank information in 'client_bank_info' table
                # if 'client_bank_info' in payload and 'update' in payload['client_bank_info']:
                #     for u in payload['client_bank_info']['update']:
                #         # todo: may need to add "description" when UI starts sending it. It is part of the bank_info section
                #         query = ('UPDATE client_bank_info SET bankaccountholdername=%s,bankaccountno=%s,bankaccounttype=%s,'
                #                  'bankbranch=%s,bankcity=%s,bankifsccode=%s, bankmicrcode=%s  WHERE ID=%s and clientid=%s')
                #         data = logMessage(cursor, query,(
                #             u["bankaccountholdername"], u["bankaccountno"], u["bankaccounttype"],
                #             u["bankbranch"], u["bankcity"], u["bankifsccode"], u["bankmicrcode"], u["id"], propertyid))
                #         conn[0].commit()
                #         logging.info(f'editClientInfo: client_access clientid <{propertyid}>, rowid <{u["id"]}> UPDATE status is <{cursor.statusmessage}>')
                # if 'client_bank_info' in payload and 'insert' in payload['client_bank_info']:
                #     for u in payload['client_bank_info']['insert']:
                #         query = ('INSERT into client_bank_info (bankaccountholdername,bankaccountno,bankaccounttype,bankbranch,bankcity,bankifsccode,bankmicrcode,clientid) '
                #                  'values (%s,%s,%s,%s,%s,%s,%s,%s)')
                #         data = logMessage(cursor, query,(u["bankaccountholdername"], u["bankaccountno"], u["bankaccounttype"],
                #             u["bankbranch"], u["bankcity"], u["bankifsccode"], u["bankmicrcode"], propertyid))
                #         conn[0].commit()
                #         logging.info(f'editClientInfo: client_bank_info clientid <{propertyid}> INSERT status is <{cursor.statusmessage}>')

    #             # update client legalinfo in 'client_legal_info' table
                li = payload['client_property_owner']
                query = ('UPDATE client_property_owner SET owner1name=%s,owner1panno=%s,owner1aadhaarno=%s,owner1pancollected=%s,owner1aadhaarcollected=%s,owner2name=%s,owner2panno=%s,owner2aadhaarno=%s,owner2pancollected=%s,owner2aadhaarcollected=%s,owner3name=%s,owner3panno=%s,owner3aadhaarno=%s,owner3pancollected=%s,owner3aadhaarcollected=%s,comments=%s WHERE propertyid=%s')
                data = logMessage(cursor,
                    query,(li["owner1name"],li["owner1panno"],li["owner1aadhaarno"],li["owner1pancollected"],li["owner1aadhaarcollected"],li["owner2name"],li["owner2panno"],li["owner2aadhaarno"],li["owner2pancollected"],li["owner2aadhaarcollected"],li["owner3name"],li["owner3panno"],li["owner3aadhaarno"],li["owner3pancollected"],li["owner3aadhaarcollected"],li["comments"],
                           propertyid))
                conn[0].commit()
                logging.info(f'editClientProperty: client_property_owner update status is <{cursor.statusmessage}>')

    #             # update client_poa in 'client_poa' table
                pi = payload['client_property_poa']
                query = ('UPDATE client_property_poa SET '
                         'poaaddressline1=%s,' 'poaaddressline2=%s,' 'poabirthyear=%s,' 'poacity=%s,' 'poacountry=%s,'
                         'poaeffectivedate=%s,' 'poaemployername=%s,' 'poaenddate=%s,' 'poafor=%s,' 'poalegalname=%s,'
                         'poaoccupation=%s,' 'poapanno=%s,' 'poaphoto=%s,' 'poarelation=%s, poarelationwith=%s, poastate=%s,'
                         'poasuburb=%s, poazip=%s WHERE clientpropertyid=%s')
                data = logMessage(cursor, query,(pi['poaaddressline1'],pi['poaaddressline2'], pi['poabirthyear'], pi['poacity'], pi['poacountry'],
                           pi['poaeffectivedate'], pi['poaemployername'], pi['poaenddate'], pi['poafor'], pi['poalegalname'],
                           pi['poaoccupation'], pi['poapanno'], pi['poaphoto'], pi['poarelation'], pi['poarelationwith'],
                           pi['poastate'],pi['poasuburb'], pi['poazip'], propertyid))
                conn[0].commit()
                logging.info(f'editClientProperty: client_property_poa update status is <{cursor.statusmessage}>')
            return giveSuccess(payload['user_id'],role_access_status,{"edited_property":propertyid})
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)
    except KeyError as e:
        logging.info(traceback.print_exc())
        return giveFailure(f"Missing key : {e}",0,0)
    except Exception as e:
         logging.info(traceback.print_exc())
         return giveFailure(f"Failed To Edit given client info due to <{traceback.print_exc()}>",0,0)


@app.post('/getClientPropertyById')
async def get_client_property_by_id(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"get_client_property_by_id:received payload <{payload}>")
    try:
        role_access_status = check_role_access(conn, payload)

        if role_access_status == 1:
            data = dict()
            with conn[0].cursor() as cursor:
                ############### Arrange Client Property ##################
                query = f'''
                    select distinct id,clientid,leveloffurnishing,numberofparkings,state,
                    city,suburb,country,projectid,status,propertydescription,propertytype,layoutdetails,
                    email,website,initialpossessiondate,electricityconsumernumber,
                    otherelectricitydetails,electricitybillingduedate,comments,
                    propertytaxnumber,clientservicemanager,propertymanager,
                    propertyownedbyclientonly,gasconnectiondetails,internalfurnitureandfittings,
                    textforposting,poagiven,poaid,electricitybillingunit,indexiicollected
                    from client_property where id = {payload['id']}
                '''
                msg = logMessage(cursor,query)
                logging.info(msg)
                colnames = [desc[0] for desc in cursor.description]
                property_info_ = cursor.fetchall()
                property_info = dict()
                for row in property_info_:
                    row_dict = {colname: value for colname, value in zip(colnames, row)}
                    property_info = row_dict
                if property_info == {}:
                    property_info = {colname: None for colname in colnames}
                data["client_property"]  = property_info
                ############### Arrange Client Property Photos ##################
                query = f'''
                    select photolink,description,phototakenwhen  
                    from client_property_photos where clientpropertyid = {payload['id']}
                '''
                logMessage(cursor,query)
                colnames = [desc[0] for desc in cursor.description]
                _data = cursor.fetchall()
                property_photos = []
                for row in _data:
                    row_dict = {colname: value for colname, value in zip(colnames, row)}
                    property_photos.append(row_dict)
                # if not property_photos:
                #     property_photos = [{colname: None for colname in colnames}]
                data["client_property_photos"] = property_photos

                ############### Arrage Client Property Owner Info ##################
                query = f'''
                    select distinct propertyid,owner1name,owner1panno,owner1aadhaarno,owner1pancollected,owner1aadhaarcollected,owner2name,owner2panno,owner2aadhaarno,owner2pancollected,owner2aadhaarcollected,owner3name,owner3panno,owner3aadhaarno,owner3pancollected,owner3aadhaarcollected,comments from client_property_owner 
                    where propertyid = {payload['id']}
                '''
                logMessage(cursor,query)
                colnames = [desc[0] for desc in cursor.description]
                _data = cursor.fetchall()
                property_owner = dict()
                for row in _data:
                    row_dict = {colname: value for colname, value in zip(colnames, row)}
                    property_owner = row_dict
                if not property_owner:
                    property_owner = {colname: None for colname in colnames}
                data["client_property_owner"] = property_owner

                ############### Arrange Client Property POA info ##################
                query = f'''select distinct poalegalname,poapanno,poaaddressline1,poaaddressline2,poasuburb,poacity,
                    poastate,poacountry,poazip,poaoccupation,poabirthyear,poaphoto,poaemployername,
                    poarelation,poarelationwith,poaeffectivedate,poaenddate,poafor,scancopy
                    from client_property_poa where clientpropertyid = {payload['id']}
                '''
                logMessage(cursor,query)
                colnames = [desc[0] for desc in cursor.description]
                _data = cursor.fetchall()
                logging.info(f'The data is <{_data}>')
                property_poa = dict()
                for row in _data:
                    row_dict = {colname: value for colname, value in zip(colnames, row)}
                    property_poa = row_dict
                if not property_poa:
                    property_poa = {colname: None for colname in colnames}
                data["client_property_poa"] = property_poa
                

                return giveSuccess(payload['user_id'],role_access_status,data)
        else:
            return giveFailure("Access Denied",payload["user_id"],role_access_status)
    except Exception as e:
        logging.exception(traceback.print_exc())
        return giveFailure("Invalid Credentials",payload['user_id'],0)

@app.post('/getClientReceipt')
async def get_client_receipt(payload: dict,conn : psycopg2.extensions.connection = Depends(get_db_connection)):
    payload['table_name'] = 'get_client_receipt_view'
    return await runInTryCatch(
        conn=conn,
        fname='get_client_receipt',
        payload=payload,
        isPaginationRequired=True,
        whereinquery=True,
        formatData=True,
        isdeleted=True
    )

@app.post('/addClientReceipt')
async def add_client_receipt(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"add_client_receipt :received payload <{payload}>")
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = "INSERT INTO client_receipt(receivedby,amount,tds,paymentmode,recddate,clientid,receiptdesc,serviceamount,reimbursementamount,entityid,howreceivedid,officeid,dated,createdby,isdeleted) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id"
                msg = logMessage(cursor,query,[
                    payload["receivedby"],
                    payload["amount"],
                    payload["tds"],
                    payload["paymentmode"],
                    payload["recddate"],
                    payload["clientid"],
                    payload["receiptdesc"],
                    payload["serviceamount"],
                    payload["reimbursementamount"],
                    payload["entityid"],
                    payload["howreceivedid"],
                    payload["officeid"],
                    givenowtime(),
                    payload["user_id"],
                    False
                ])
                logging.info(msg)
                data = cursor.fetchone()[0]
                conn[0].commit()
                return giveSuccess(payload['user_id'],role_access_status,{"Inserted_Receipt":data})
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)
    except KeyError as ke:
        logging.info(traceback.print_exc())
        return giveFailure(f"Missing key {ke}",0,0)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure("Invalid Credentials",0,0)
    
@app.post('/editClientReceipt')
async def edit_client_receipt(payload: dict, conn : psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"edit_client_receipt:received payload <{payload}>")
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = "UPDATE client_receipt SET receivedby = %s, amount = %s, tds = %s, paymentmode = %s,recddate=%s ,clientid = %s,receiptdesc = %s, serviceamount=%s, reimbursementamount = %s, entityid = %s, howreceivedid = %s,officeid = %s,dated=%s,createdby=%s,isdeleted=%s WHERE id=%s"
                msg = logMessage(cursor,query,[
                    payload["receivedby"],
                    payload["amount"],
                    payload["tds"],
                    payload["paymentmode"],
                    payload['recddate'],
                    payload["clientid"],
                    payload["receiptdesc"],
                    payload["serviceamount"],
                    payload["reimbursementamount"],
                    payload["entityid"],
                    payload["howreceivedid"],
                    payload["officeid"],
                    givenowtime(),
                    payload["user_id"],
                    False,
                    payload["id"]
                ])
                logging.info(msg)
                conn[0].commit()
                if cursor.statusmessage!="UPDATE 0":
                    return giveSuccess(payload['user_id'],role_access_status,{"Edited_Receipt":payload['id']})
                else:
                    return giveFailure("No Record Available",payload['user_id'],role_access_status)
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)
    except KeyError as ke:
        logging.info(traceback.print_exc())
        return giveFailure(f"Missing key {ke}",0,0)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure("Invalid Credentials",0,0)

@app.post('/deleteClientReceipt')
async def delete_client_receipt(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"delete_client_receipt :received payload <{payload}>")
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = "UPDATE client_receipt SET isdeleted=true WHERE id=%s AND isdeleted=False"
                msg = logMessage(cursor,query,(payload['id'],))
                if cursor.statusmessage == "UPDATE 0":
                    return giveFailure(f"No Order Receipt with id {payload['id']}",payload['user_id'],role_access_status)
                logging.info(msg)
                conn[0].commit()
            if cursor.statusmessage !="UPDATE 0":
                return giveSuccess(payload['user_id'],role_access_status,{"Deleted_Receipt":payload['id']})
            else:
                    return giveFailure("No Record Available",payload['user_id'],role_access_status)
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)
    except KeyError as ke:
        logging.info(traceback.print_exc())
        return giveFailure(f"Missing key {ke}",0,0)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure("Invalid Credentials",0,0)

@app.post('/getClientPMAAgreement')
async def get_client_pma_agreement(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    payload['table_name'] = 'get_client_property_pma_view'
    return await runInTryCatch(
        conn=conn,
        fname='get_client_pma_agreement',
        payload=payload,
        isPaginationRequired=True,
        whereinquery=True,
        formatData=True,
        isdeleted=True
    )

@app.post('/addClientPMAAgreement')
async def add_client_pma_agreement(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"add_client_pma_agreement:received payload <{payload}>")
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = "INSERT INTO client_property_caretaking_Agreement (clientpropertyid,startdate,enddate,actualenddate,active,scancopy,reasonforearlyterminationifapplicable,description,rented,fixed,rentedtax,fixedtax,orderid,poastartdate,poaenddate,poaholder,dated,createdby,isdeleted) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id"
                msg = logMessage(cursor,query,[
                    payload["clientpropertyid"],payload["startdate"],payload["enddate"],payload["actualenddate"],payload["active"],
                    payload["scancopy"],payload["reasonforearlyterminationifapplicable"],payload["description"],payload["rented"],
                    payload["fixed"],payload["rentedtax"],payload["fixedtax"],payload["orderid"],payload["poastartdate"],payload["poaenddate"],
                    payload["poaholder"],givenowtime(),payload["user_id"],False
                ])
                logging.info(msg)
                id = cursor.fetchone()[0]
                conn[0].commit()
                return giveSuccess(payload['user_id'],role_access_status,{"Inserted_PMA":id})
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)
    except KeyError as ke:
        logging.info(traceback.print_exc())
        return giveFailure(f"Missing key {ke}",0,0)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure("Invalid Credentials",0,0)

@app.post('/editClientPMAAgreement')
async def edit_client_pma_agreement(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"edit_client_pma_agreement:received payload <{payload}>")
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = "UPDATE client_property_caretaking_agreement SET clientpropertyid=%s,startdate=%s,enddate=%s,actualenddate=%s,active=%s,scancopy=%s,reasonforearlyterminationifapplicable=%s,description=%s,rented=%s,fixed=%s,rentedtax=%s,fixedtax=%s,orderid=%s,poastartdate=%s,poaenddate=%s,poaholder=%s,dated=%s,createdby=%s,isdeleted=%s WHERE id=%s"
                msg = logMessage(cursor,query,[
                    payload["clientpropertyid"],payload["startdate"],payload["enddate"],payload["actualenddate"],payload["active"],
                    payload["scancopy"],payload["reasonforearlyterminationifapplicable"],payload["description"],payload["rented"],
                    payload["fixed"],payload["rentedtax"],payload["fixedtax"],payload["orderid"],payload["poastartdate"],payload["poaenddate"],
                    payload["poaholder"],givenowtime(),payload["user_id"],False,payload['id']
                ])
                logging.info(msg)
                conn[0].commit()
            if cursor.statusmessage !="UPDATE 0":
                return giveSuccess(payload['user_id'],role_access_status,{"Edited_PMA":payload['id']})
            else:
                return giveFailure("No Record Available",payload['user_id'],role_access_status)
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)
    except KeyError as ke:
        logging.info(traceback.print_exc())
        return giveFailure(f"Missing key {ke}",0,0)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure("Invalid Credentials",0,0)

@app.post('/deleteClientPMAAgreement')
async def delete_client_pma_agreement(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"delete_client_pma_agreement:received payload <{payload}>")
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = "UPDATE client_property_caretaking_agreement SET isdeleted=true WHERE id=%s"
                msg = logMessage(cursor,query,(payload['id'],))
                logging.info(msg)
                conn[0].commit()
            if cursor.statusmessage !="UPDATE 0":
                return giveSuccess(payload['user_id'],role_access_status,{"Deleted_PMA":payload['id']})
            else:
                    return giveFailure("No Record Available",payload['user_id'],role_access_status)
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure("Invalid Credentials",0,0)

@app.post('/getClientLLAgreement')
async def get_ll_agreement(payload: dict, conn:psycopg2.extensions.connection = Depends(get_db_connection)):
    payload['table_name'] = 'get_client_property_lla_view'
    return await runInTryCatch(
        conn = conn,
        fname = 'get_ll_agreement',
        payload=payload,
        isPaginationRequired=True,
        whereinquery=True,
        formatData=True,
        isdeleted=True
    )

@app.post('/addClientLLAgreement')
async def add_client_ll_agreement(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"add_client_ll_agreement:received payload <{payload}>")
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = "INSERT INTO client_property_leave_license_details (clientpropertyid,orderid,durationinmonth,startdate,actualenddate,depositamount,rentamount,registrationtype,rentpaymentdate,noticeperiodindays,active,llscancopy,dated,createdby,isdeleted) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id"
                msg = logMessage(cursor,query,[payload["clientpropertyid"],payload["orderid"],payload["durationinmonth"],payload['startdate'],
                                      payload['actualenddate'],payload['depositamount'],payload["rentamount"],payload["registrationtype"],
                                      payload["rentpaymentdate"],payload["noticeperiodindays"],payload["active"],
                                      payload["llscancopy"],givenowtime(),payload["user_id"],False
                ])
                logging.info(msg)
                id = cursor.fetchone()[0]
                conn[0].commit()
                return giveSuccess(payload['user_id'],role_access_status,{"Inserted_L&L":id})
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)
    except KeyError as ke:
        logging.info(traceback.print_exc())
        return giveFailure(f"Missing key {ke}",0,0)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure("Invalid Credentials",0,0)

@app.post('/editClientLLAgreement')
async def edit_client_ll_agreement(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"edit_client_ll_agreement:received payload <{payload}>")
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'UPDATE client_property_leave_license_details SET clientpropertyid=%s,orderid=%s,durationinmonth=%s,startdate=%s,depositamount=%s,actualenddate=%s,rentamount=%s,registrationtype=%s,rentpaymentdate=%s,noticeperiodindays=%s,active=%s,llscancopy=%s,dated=%s,createdby=%s,isdeleted=%s WHERE id=%s'
                msg = logMessage(cursor,query,[payload["clientpropertyid"],payload["orderid"],payload["durationinmonth"],payload["startdate"],payload['depositamount'],
                                      payload["actualenddate"],payload["rentamount"],payload["registrationtype"],payload["rentpaymentdate"],
                                      payload["noticeperiodindays"],payload["active"],payload["llscancopy"],givenowtime(),payload['user_id']
                                      ,False,payload['id']])
                logging.info(msg)
            conn[0].commit()
            if cursor.statusmessage !="UPDATE 0":
                return giveSuccess(payload['user_id'],role_access_status,{"Edited_LLA":payload['id']})
            else:
                    return giveFailure("No Record Available",payload['user_id'],role_access_status)
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)
    except KeyError as ke:
        logging.info(traceback.print_exc())
        return giveFailure(f"Missing key {ke}",0,0)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure("Invalid Credentials",0,0)
    
@app.post('/deleteClientLLAgreement')
async def delete_client_pma_agreement(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"delete_client_pma_agreement:received payload <{payload}>")
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = "UPDATE client_property_leave_license_details SET isdeleted=true WHERE id=%s AND isdeleted=false"
                msg = logMessage(cursor,query,(payload['id'],))
                logging.info(msg)
                conn[0].commit()
            if cursor.statusmessage !="UPDATE 0":
                return giveSuccess(payload['user_id'],role_access_status,{"Deleted_L&L":payload['id']})
            else:
                    return giveFailure("No Record Available",payload['user_id'],role_access_status)
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)
    except KeyError as ke:
        logging.info(traceback.print_exc())
        return giveFailure(f"Missing key {ke}",0,0)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure("Invalid Credentials",0,0)

@app.post('/getClientPropertyByClientId')
async def get_client_property_admin(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"get_client_property_admin:received payload <{payload}>")
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = "SELECT DISTINCT id,property as propertyname from get_client_property_view WHERE clientid=%s ORDER BY property"
                msg = logMessage(cursor,query,(payload['client_id'],))
                logging.info(msg)
                data = cursor.fetchall()
            colnames = [desc[0] for desc in cursor.description]
            res = []
            for row in data:
                row_dict = {key:value for key,value in zip(colnames,row)}
                res.append(row_dict)
            return giveSuccess(payload['user_id'],role_access_status,res)
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure("Invalid Credentials",0,0)
    
@app.post('/getOrdersByClientId')
async def get_order_by_client_id(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"get_client_property_admin:received payload <{payload}>")
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = '''SELECT DISTINCT id,briefdescription
                            as ordername from orders WHERE clientid = %s order by briefdescription'''
                msg = logMessage(cursor,query,(payload['client_id'],))
                logging.info(msg)
                data = cursor.fetchall()
            colnames = [desc[0] for desc in cursor.description]
            res = []
            for row in data:
                row_dict = {key:value for key,value in zip(colnames,row)}
                res.append(row_dict)
            return giveSuccess(payload['user_id'],role_access_status,res)
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure("Invalid Credentials",0,0)

@app.post('/getProjectById')
async def getprojectbyid(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"getprojectbyid:received payload <{payload}>")
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:

                #===============Project_info=====================
                query = 'SELECT * FROM project where id=%s'
                msg = logMessage(cursor,query,(payload['id'],))
                logging.info(msg)
                _data = cursor.fetchall()
                colnames = [desc[0] for desc in cursor.description]

                if _data:
                    project_info = {col:val for col,val in zip(colnames,_data[0])}
                else:
                    project_info = {col:None for col in colnames}
                
                #======================Project_details============
                query = 'SELECT * FROM project_amenities where projectid = %s'
                logMessage(cursor,query,(payload['id'],))
                _data = cursor.fetchall()
                colnames = [desc[0] for desc in cursor.description]

                if _data:
                    project_amenities = {col:val for col,val in zip(colnames,_data[0])}
                else:
                    project_amenities = {col:None for col in colnames}

                #================Project_Bank_details=============
                query = 'SELECT * FROM project_bank_details where projectid=%s order by id'
                logMessage(cursor,query,(payload['id'],))
                _data = cursor.fetchall()
                colnames = [desc[0] for desc in cursor.description]

                if _data:
                    project_bank_details = [{col:val for col,val in zip(colnames,data)} for data in _data]
                else:
                    project_bank_details = [{col:None for col in colnames}]
                
                #==============Project_Contacts===================
                query = 'SELECT * FROM project_contacts where projectid=%s order by id'
                logMessage(cursor,query,(payload['id'],))
                _data = cursor.fetchall()
                colnames = [desc[0] for desc in cursor.description]

                if _data:
                    project_contacts = [{col:val for col,val in zip(colnames,data)} for data in _data]
                else:
                    project_contacts = [{col:None for col in colnames}]

                #=============Project_Photos======================
                query = 'SELECT * FROM project_photos where projectid=%s order by id'
                logMessage(cursor,query,(payload['id'],))
                _data = cursor.fetchall()
                colnames = [desc[0] for desc in cursor.description]

                if _data:
                    project_photos = [{col:val for col,val in zip(colnames,data)} for data in _data]
                else:
                    project_photos = [{col:None for col in colnames}]

                data = {
                    'project_info':project_info,
                    'project_amenities':project_amenities,
                    'project_bank_details':project_bank_details,
                    'project_photos':project_photos,
                    'project_contacts':project_contacts
                }
                return giveSuccess(payload['user_id'],role_access_status,data)
        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure('Invalid Credentials',payload['user_id'],role_access_status)

@app.post('/editProject')
async def edit_project(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"edit_project:received payload <{payload}>")
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:

                #==============Project_Info=================
                project_info = payload['project_info']
                logging.info(f'project id is <{payload["projectid"]}>')
                query = '''UPDATE project SET builderid=%s,projectname=%s,addressline1=%s,addressline2=%s,
                        suburb=%s,city=%s,state=%s,country=%s,zip=%s,nearestlandmark=%s,project_type=%s,mailgroup1=%s,
                        mailgroup2=%s,website=%s,project_legal_status=%s,rules=%s,completionyear=%s,jurisdiction=%s,
                        taluka=%s,corporationward=%s,policechowkey=%s,policestation=%s,maintenance_details=%s,numberoffloors=%s,
                        numberofbuildings=%s,approxtotalunits=%s,tenantstudentsallowed=%s,tenantworkingbachelorsallowed=%s,
                        tenantforeignersallowed=%s,otherdetails=%s,duespayablemonth=%s,dated=%s,createdby=%s,isdeleted=%s WHERE id=%s'''
                msg = logMessage(cursor,query,(project_info["builderid"],project_info["projectname"],project_info["addressline1"],
                                        project_info["addressline2"],project_info["suburb"],project_info["city"],
                                        project_info["state"],project_info["country"],project_info["zip"],project_info["nearestlandmark"],
                                        project_info["project_type"],project_info["mailgroup1"],project_info["mailgroup2"],project_info["website"],
                                        project_info["project_legal_status"],project_info["rules"],project_info["completionyear"],
                                        project_info["jurisdiction"],project_info["taluka"],project_info["corporationward"],project_info['policestation'],project_info["policechowkey"],
                                        project_info["maintenance_details"],project_info["numberoffloors"],project_info["numberofbuildings"],
                                        project_info["approxtotalunits"],project_info["tenantstudentsallowed"],project_info["tenantworkingbachelorsallowed"],
                                        project_info["tenantforeignersallowed"],project_info["otherdetails"],project_info["duespayablemonth"]
                                        ,givenowtime(),payload['user_id'],False,project_info['id']))
                logging.info(msg)
                if cursor.statusmessage == 'UPDATE 0':
                    return giveFailure('No entry with given ID',payload['user_id'],role_access_status)
                #===============Project_Amenities===========
                project_amenities = payload['project_amenities']
                query = '''UPDATE project_amenities SET swimmingpool=%s,lift=%s,liftbatterybackup=%s,
                        clubhouse=%s,gym=%s,childrensplayarea=%s,pipedgas=%s,cctvcameras=%s,otheramenities=%s,
                        studio=%s,"1BHK"=%s,"2BHK"=%s,"3BHK"=%s,"4BHK"=%s,"RK"=%s,other=%s,duplex=%s,penthouse=%s,
                        rowhouse=%s,otheraccomodationtypes=%s,sourceofwater=%s,dated=%s,createdby=%s,isdeleted=%s WHERE id=%s'''
                logMessage(cursor,query,(project_amenities["swimmingpool"],project_amenities["lift"],project_amenities["liftbatterybackup"],project_amenities["clubhouse"],
                                        project_amenities["gym"],project_amenities["childrensplayarea"],project_amenities["pipedgas"],project_amenities["cctvcameras"],
                                        project_amenities["otheramenities"],project_amenities["studio"],project_amenities["1BHK"],project_amenities["2BHK"],project_amenities["3BHK"],
                                        project_amenities["4BHK"],project_amenities["RK"],project_amenities["other"],project_amenities["duplex"],project_amenities["penthouse"],
                                        project_amenities["rowhouse"],project_amenities["otheraccomodationtypes"],project_amenities["sourceofwater"],givenowtime(),
                                        payload['user_id'],False,project_amenities['id']))
                #===============Project_Bank_Details========
                if 'update' in payload['project_bank_details']:
                    _bank_update = payload['project_bank_details']['update']
                    for bank_update in _bank_update:
                        query = '''UPDATE project_bank_details SET bankname=%s,bankbranch=%s,bankcity=%s,bankaccountholdername=%s,
                                    bankaccountno=%s,bankifsccode=%s,banktypeofaccount=%s,bankmicrcode=%s,dated=%s,createdby=%s,isdeleted=%s WHERE id=%s'''
                        logMessage(cursor,query,(bank_update["bankname"],bank_update["bankbranch"],bank_update["bankcity"],
                                              bank_update["bankaccountholdername"],bank_update["bankaccountno"],bank_update["bankifsccode"],
                                              bank_update["banktypeofaccount"],bank_update['bankmicrcode'],givenowtime(),
                                              payload['user_id'],False,bank_update['id']))
                if 'insert' in payload['project_bank_details']:
                    _bank_insert = payload['project_bank_details']['insert']
                    for bank_insert in _bank_insert:
                        query = '''INSERT INTO project_bank_details(projectid,bankname,bankbranch,bankcity,bankaccountholdername,bankaccountno,bankifsccode
                                    ,banktypeofaccount,bankmicrcode,dated,createdby,isdeleted) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
                        logMessage(cursor,query,(payload['projectid'],bank_insert["bankname"],bank_insert["bankbranch"],bank_insert["bankcity"],bank_insert["bankaccountholdername"],
                                              bank_insert["bankaccountno"],bank_insert["bankifsccode"],bank_insert["banktypeofaccount"],bank_insert["bankmicrcode"],
                                              givenowtime(),payload['user_id'],False))
                if 'delete' in payload['project_bank_details']:
                    _bank_delete = payload['project_bank_details']['delete']
                    for bank_delete in _bank_delete:
                        query = '''DELETE FROM project_bank_details where id=%s'''
                        logMessage(cursor,query,(bank_delete['id'],))
                #===============Project_Photos===============
                if 'update' in payload['project_photos']:
                    _photo_update = payload['project_photos']['update']
                    for photo_update in _photo_update:
                        query = '''UPDATE project_photos SET photo_link=%s,description=%s,date_taken=%s,dated=%s,createdby=%s,isdeleted=%s WHERE id=%s'''
                        logMessage(cursor,query,(photo_update["photo_link"],photo_update["description"],photo_update["date_taken"],givenowtime(),payload['user_id'],False,photo_update['id']))
                if 'insert' in payload['project_photos']:
                    _photo_insert = payload['project_photos']['insert']
                    for photo_insert in _photo_insert:
                        query = '''INSERT INTO project_photos(projectid,photo_link,description,date_taken,dated,createdby,isdeleted) VALUES (%s,%s,%s,%s,%s,%s,%s)'''
                        logMessage(cursor,query,(payload['projectid'],photo_insert["photo_link"],photo_insert["description"],photo_insert["date_taken"],
                                              givenowtime(),payload['user_id'],False))
                if 'delete' in payload['project_photos']:
                    _photo_delete = payload['project_photos']['delete']
                    for photo_delete in _photo_delete:
                        query = '''DELETE FROM project_photos where id=%s'''
                        logMessage(cursor,query,(photo_delete['id'],))
                #============Project_Contacts==================
                if 'update' in payload['project_contacts']:
                    _contact_update = payload['project_contacts']['update']
                    for contact_update in _contact_update:
                        query = '''UPDATE project_contacts SET contactname=%s,phone=%s,email=%s,role=%s,effectivedate=%s,tenureenddate=%s,details=%s,dated=%s,createdby=%s,isdeleted=%s WHERE id=%s'''
                        logMessage(cursor,query,(contact_update["contactname"],contact_update["phone"],contact_update["email"],contact_update["role"],contact_update["effectivedate"],contact_update["tenureenddate"],contact_update["details"],givenowtime(),payload['user_id'],False,contact_update['id']))
                if 'insert' in payload['project_contacts']:
                    _contact_insert = payload['project_contacts']['insert']
                    for contact_insert in _contact_insert:
                        query = '''INSERT INTO project_contacts(projectid,contactname,phone,email,role,effectivedate,tenureenddate,details,dated,createdby,isdeleted) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
                        logMessage(cursor,query,(payload['projectid'],contact_insert["contactname"],contact_insert["phone"],contact_insert["email"],contact_insert["role"],contact_insert["effectivedate"],contact_insert["tenureenddate"],contact_insert["details"],
                                              givenowtime(),payload['user_id'],False))
                if 'delete' in payload['project_contacts']:
                    _contact_delete = payload['project_contacts']['delete']
                    for contact_delete in _contact_delete:
                        query = '''DELETE FROM project_contacts where id=%s'''
                        logMessage(cursor,query,(contact_delete['id'],))
                conn[0].commit() 
                return giveSuccess(payload['user_id'],role_access_status,{"edited project":payload['projectid']})
        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure('Invalid Credentials',payload['user_id'],role_access_status)            

@app.post('/addCities')
async def add_cities(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"add_cities:received payload <{payload}>")
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'INSERT INTO cities (city,state,countryid) VALUES (%s,%s,%s)'
                msg = logMessage(cursor,query,[
                    payload['city'],
                    payload['state'],
                    payload['countryid']
                ])
                logging.info(msg)
                conn[0].commit()
            return giveSuccess(payload['user_id'],role_access_status,{"inserted_city":payload['city']})
        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure('Invalid Credentials',payload['user_id'],role_access_status)            
  
@app.post('/editCities')
async def edit_cities(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"edit_cities:received payload <{payload}>")
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'UPDATE cities SET city=%s,state=%s,countryid=%s WHERE id=%s'
                msg = logMessage(cursor,query,[
                    payload['city'],
                    payload['state'],
                    payload['countryid'],
                    payload['id']
                ])
                logging.info(msg)
                conn[0].commit()
                if cursor.statusmessage == 'UPDATE 0':
                    return giveFailure('Does not exist',payload['user_id'],role_access_status)
            return giveSuccess(payload['user_id'],role_access_status,{"editted_city":payload['city']})
        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure('Invalid Credentials',payload['user_id'],role_access_status)            
   
@app.post('/deleteCities')
async def delete_cities(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"delete_cities:received payload <{payload}>")
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'DELETE FROM cities WHERE id=%s'
                msg = logMessage(cursor,query,[
                    payload['id']
                ])
                logging.info(msg)
                conn[0].commit()
            return giveSuccess(payload['user_id'],role_access_status,{"deleted_city":payload['id']})
        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure('Invalid Credentials',payload['user_id'],role_access_status)            

@app.post('/getOrders')
async def get_orders(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    payload['table_name'] = 'get_orders_view'
    return await runInTryCatch(
        conn=conn,
        fname = 'get_orders_view',
        payload=payload,
        isPaginationRequired=True,
        whereinquery=True,
        formatData=True,
        isdeleted=True
    )
@app.post('/addOrders')
async def add_orders(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"add_orders:received payload <{payload}>")
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            order_info = payload['order_info']
            # _order_status_change = payload['order_status_change']
            _order_photos = payload['order_photos']
            with conn[0].cursor() as cursor:
                #===============Order_Info===========================
                query = ('INSERT INTO orders (assignedtooffice,entityid,owner,status,clientpropertyid,service,'
                         'clientid,orderdate,earlieststartdate,expectedcompletiondate,actualcompletiondate,'
                         'vendorid,tallyledgerid,briefdescription,comments,additionalcomments,dated,createdby,isdeleted) '
                         'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id')
                msg = logMessage(cursor,query,(order_info['assignedtooffice'],order_info['entityid'],order_info['owner'],order_info['status'],
                                      order_info['clientpropertyid'],order_info['service'],order_info['clientid'],
                                      order_info['orderdate'],order_info['earlieststartdate'],order_info['expectedcompletiondate'],
                                      order_info['actualcompletiondate'],order_info['vendorid'],order_info['tallyledgerid'],
                                      order_info['briefdescription'],order_info['comments'],order_info['additionalcomments'],givenowtime(),payload['user_id'],False))
                logging.info(msg)
                data = cursor.fetchone()[0]
                conn[0].commit()
  
                #==============Order_Photos=========================
                for order_photos in _order_photos:
                    query = 'INSERT INTO order_photos (orderid,photolink,description,phototakenwhen,dated,createdby,isdeleted) VALUES (%s,%s,%s,%s,%s,%s,%s)'
                    logging.info('inserting photos')
                    logMessage(cursor,query,(data,order_photos['photolink'],order_photos['description'],order_photos['phototakenwhen'],givenowtime(),payload['user_id'],False))
                logging.info(cursor.statusmessage)
                conn[0].commit()                            
                return giveSuccess(payload['user_id'],role_access_status,data={"inserted data":data})
        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure('Invalid Credentials',payload['user_id'],role_access_status)  
    
@app.post('/editOrders')
async def edit_orders(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"edit_orders:received payload <{payload}>")
    try:
        logging.info(f'payload for edit_orders : <{payload}>')
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            order_info = payload['order_info']
            # _order_status_change_update = payload['order_status_change']['update']
            # _order_status_change_insert = payload['order_status_change']['insert']
            _order_photos_update = payload['order_photos']['update']
            _order_photos_insert = payload['order_photos']['insert']
            with conn[0].cursor() as cursor:
                #===============Order_Info===========================
                query = ('UPDATE orders SET assignedtooffice=%s,entityid=%s,owner=%s,status=%s,'
                         'clientpropertyid=%s,service=%s,clientid=%s,orderdate=%s,earlieststartdate=%s,'
                         'expectedcompletiondate=%s,actualcompletiondate=%s,vendorid=%s,' 'tallyledgerid=%s,'
                         'comments=%s,additionalcomments=%s,dated=%s,createdby=%s,isdeleted=%s, briefdescription=%s WHERE id=%s')
                msg = logMessage(cursor,query,(order_info['assignedtooffice'],order_info['entityid'],order_info['owner'],order_info['status'],
                                      order_info['clientpropertyid'],order_info['service'],order_info['clientid'],order_info['orderdate'],
                                      order_info['earlieststartdate'],order_info['expectedcompletiondate'],order_info['actualcompletiondate'],
                                      order_info['vendorid'],order_info['tallyledgerid'],order_info['comments'],order_info['additionalcomments'],
                                      givenowtime(),payload['user_id'],False,order_info['briefdescription'],order_info['id']))
                # data = cursor.fetchone()[0]
                logging.info(msg)
                conn[0].commit()
                #===============Order_Status_Change==================
                # for order_status_change_update in _order_status_change_update:
                #     query = 'UPDATE order_status_change SET orderid=%s,statusid=%s,dated=%s WHERE id=%s'
                #     logMessage(cursor,query,(order_status_change_update['orderid'],order_status_change_update['statusid'],order_status_change_update['timestamp'],order_status_change_update['id']))
                #     conn[0].commit()       
                # for order_status_change_insert in _order_status_change_insert:
                #     query = 'INSERT INTO order_status_change (orderid,statusid,dated) VALUES (%s,%s,%s)'
                #     logMessage(cursor,query,(order_status_change_insert['orderid'],order_status_change_insert['statusid'],order_status_change_insert['timestamp']))
                #     conn[0].commit()      
                #==============Order_Photos=========================
                for order_photos_update in _order_photos_update:
                    query = 'UPDATE order_photos SET orderid=%s,photolink=%s,description=%s,phototakenwhen=%s,dated=%s,createdby=%s,isdeleted=%s WHERE id=%s'
                    logMessage(cursor,query,(order_photos_update['orderid'],order_photos_update['photolink'],order_photos_update['description'],order_photos_update['phototakenwhen'],givenowtime(),payload['user_id'],False,order_photos_update['id']))
                    conn[0].commit()       
                for order_photos_insert in _order_photos_insert:
                    query = 'INSERT INTO order_photos (orderid,photolink,description,phototakenwhen,dated,createdby,isdeleted) VALUES (%s,%s,%s,%s,%s,%s,%s)'
                    logMessage(cursor,query,(order_photos_insert['orderid'],order_photos_insert['photolink'],order_photos_insert['description'],order_photos_insert['phototakenwhen'],givenowtime(),payload['user_id'],False))
                    conn[0].commit() 
                return giveSuccess(payload['user_id'],role_access_status,data={"edited data":order_info['id']})
        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure('Invalid Credentials',payload['user_id'],role_access_status)    

@app.post('/deleteOrders')
async def delete_orders(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"delete_orders:received payload <{payload}>")
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'UPDATE orders SET isdeleted=true WHERE id=%s and isdeleted=False'
                msg = logMessage(cursor,query,[payload['order_id']])
                logging.info(msg)
                if cursor.statusmessage == 'UPDATE 0':
                    return giveFailure("No record available",payload['user_id'],role_access_status)
                query = 'DELETE FROM order_status_change WHERE orderid=%s'
                logMessage(cursor,query,[payload['order_id']])
                query = 'UPDATE order_photos SET isdeleted=true where orderid = %s'
                logMessage(cursor,query,[payload['order_id']])
                conn[0].commit()
            return giveSuccess(payload['user_id'],role_access_status,{"Deleted Data":payload['order_id']})
        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure('Invalid Credentials',payload['user_id'],role_access_status)
    
@app.post('/getOrdersInvoice')
async def get_orders_invoice(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    payload['table_name'] = 'get_orders_invoice_view'
    return await runInTryCatch(
        conn=conn,
        fname='get_orders_invoice',
        payload=payload,
        whereinquery=True,
        formatData=True,
        isPaginationRequired=True,
        isdeleted=True
    )

@app.post('/addOrdersInvoice')
async def add_order_invoice(payload: dict,conn:psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"add_order_invoice:received payload <{payload}>")
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'INSERT INTO order_invoice (clientid,orderid,estimatedate,estimateamount,invoicedate,invoiceamount,quotedescription,createdon,baseamount,tax,entityid,dated,createdby,isdeleted) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id'
                msg = logMessage(cursor,query,[
                    payload["clientid"],payload["orderid"],payload["estimatedate"],payload["estimateamount"],
                    payload["invoicedate"],payload["invoiceamount"],payload["quotedescription"],datetime.date.today(),
                    payload["baseamount"],payload["tax"],payload["entity"],givenowtime(),payload['user_id'],False
                ])
                logging.info(msg)
                data = cursor.fetchone()[0]
            conn[0].commit()
            return giveSuccess(payload['user_id'],role_access_status,{"inserted data":data})
        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure('Invalid Credentials',payload['user_id'],role_access_status)   

@app.post('/getServiceAdmin')
async def get_service_admin(payload: dict, conn :psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"get_service_admin:received payload <{payload}>")
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'SELECT id,service FROM services order by service'
                msg = logMessage(cursor,query)
                logging.info(msg)
                data = cursor.fetchall()
                return giveSuccess(payload['user_id'],role_access_status,data)
        else:
            giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        giveFailure('Invalid Credentials',payload['user_id'],0)

@app.post('/getClientPropertyAdmin')
async def get_client_property_admin(payload: dict, conn : psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"get_client_property_admin:received payload <{payload}>")
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = "SELECT id, property FROM get_client_property_view order by property"
                msg = logMessage(cursor,query)
                logging.info(msg)
                data = cursor.fetchall()
                return giveSuccess(payload['user_id'],role_access_status,data)
        else:
            giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        giveFailure('Invalid Credentials',payload['user_id'],0)

@app.post('/getOrderStatusAdmin')
async def get_order_status_admin(payload: dict, conn : psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"get_order_status_admin:received payload <{payload}>")
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = "SELECT id,name FROM order_status order by name"
                msg = logMessage(cursor,query)
                logging.info(msg)
                data = cursor.fetchall()
                return giveSuccess(payload['user_id'],role_access_status,data)
        else:
            giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        logging.info(traceback.print_exc())
        giveFailure('Invalid Credentials',payload['user_id'],0)   

@app.post('/getTallyLedgerAdmin')
async def get_tally_ledger_admin(payload: dict, conn: psycopg2.extensions.connection=Depends(get_db_connection)):
    logging.info(f"get_tally_ledger_admin:received payload <{payload}>")
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = "SELECT DISTINCT id,tallyledger FROM tallyledger order by tallyledger"
                msg = logMessage(cursor,query)
                logging.info(msg)
                data = cursor.fetchall()
                return giveSuccess(payload['user_id'],role_access_status,data)
        else:
            giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        logging.info(traceback.print_exc())
        giveFailure('Invalid Credentials',payload['user_id'],0)     

@app.post('/editOrdersInvoice')
async def edit_order_invoice(payload: dict,conn:psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"edit_order_invoice:received payload <{payload}>")
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'UPDATE order_invoice SET clientid=%s,orderid=%s,estimatedate=%s,estimateamount=%s,invoicedate=%s,invoiceamount=%s,quotedescription=%s,createdon=%s,baseamount=%s,tax=%s,entityid=%s,dated=%s,createdby=%s,isdeleted=%s WHERE id=%s'
                msg = logMessage(cursor,query,[
                    payload["clientid"],payload["orderid"],payload["estimatedate"],payload["estimateamount"],
                    payload["invoicedate"],payload["invoiceamount"],payload["quotedescription"],datetime.date.today(),
                    payload["baseamount"],payload["tax"],payload["entity"],givenowtime(),payload['user_id'],False,
                    payload['id']
                ])
                logging.info(msg)
            conn[0].commit()
            return giveSuccess(payload['user_id'],role_access_status,{"edited data":payload['id']})
        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure('Invalid Credentials',payload['user_id'],role_access_status)

@app.post('/deleteOrdersInvoice')
async def delete_order_invoice(payload: dict,conn:psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"delete_order_invoice:received payload <{payload}>")
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'UPDATE order_invoice SET isdeleted=true WHERE id=%s and isdeleted=false'
                msg = logMessage(cursor,query,[
                    payload['id']
                ])
                if cursor.statusmessage == "UPDATE 0":
                    return giveFailure(f"No client invoice with id {payload['id']}",payload['user_id'],role_access_status)
                logging.info(msg)
            conn[0].commit()
            return giveSuccess(payload['user_id'],role_access_status,{"deleted data":payload['id']})
        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure('Invalid Credentials',payload['user_id'],role_access_status)

@app.post('/getOrderReceipt')
async def get_order_receipt(payload: dict, conn : psycopg2.extensions.connection = Depends(get_db_connection)):
    payload['table_name']  = 'get_orders_receipt_view'
    return await runInTryCatch(
        conn = conn,
        fname = 'get_order_receipt',
        payload = payload,
        isPaginationRequired=True,
        whereinquery=True,
        formatData=True,
        isdeleted=True
    )

@app.post('/addOrderReceipt')
async def add_order_receipt(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"get_order_receipt:received payload <{payload}>")
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'INSERT INTO order_receipt (receivedby,amount,tds,recddate,receiptdesc,paymentmode,orderid,dated,createdby,isdeleted,createdon,entityid,officeid) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id'
                msg = logMessage(cursor,query,[payload["receivedby"],payload["amount"],payload["tds"],
                                      payload["recddate"],payload["receiptdesc"],payload["paymentmode"],
                                      payload["orderid"],givenowtime(),payload["user_id"],False,
                                      datetime.date.today(),payload["entityid"],payload['officeid']])
                logging.info(msg)
                conn[0].commit()
                data = cursor.fetchone()[0]
                
            return giveSuccess(payload['user_id'],role_access_status,{"inserted data":data})
        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure('Invalid Credentials',payload['user_id'],role_access_status)   

@app.post('/editOrdersReceipt')
async def edit_order_receipt(payload: dict,conn:psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"editOrdersReceipt:received payload <{payload}>")
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'UPDATE order_receipt SET receivedby=%s,amount=%s,tds=%s,recddate=%s,receiptdesc=%s,paymentmode=%s,orderid=%s,dated=%s,createdby=%s,isdeleted=%s,createdon=%s,entityid=%s,officeid=%s WHERE id=%s'
                msg = logMessage(cursor,query,[payload["receivedby"],payload["amount"],payload["tds"],
                                      payload["recddate"],payload["receiptdesc"],payload["paymentmode"],
                                      payload["orderid"],givenowtime(),payload["user_id"],False,
                                      datetime.date.today(),payload["entityid"],
                                      payload['officeid'],payload['id']])
                logging.info(msg)
                conn[0].commit()
            return giveSuccess(payload['user_id'],role_access_status,{"edited data":payload['id']})
        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure('Invalid Credentials',payload['user_id'],role_access_status)
    
@app.post('/deleteOrdersReceipt')
async def delete_order_receipt(payload: dict,conn:psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"delete_order_receipt:received payload <{payload}>")
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'UPDATE order_receipt SET isdeleted=true WHERE id=%s AND isdeleted=false'
                msg = logMessage(cursor,query,[
                    payload['id']
                ])
                if cursor.statusmessage == "UPDATE 0":
                    return giveFailure(f"No Order Receipt with id {payload['id']}",payload['user_id'],role_access_status)
                logging.info(msg)
            conn[0].commit()
            return giveSuccess(payload['user_id'],role_access_status,{"deleted data":payload['id']})
        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure('Invalid Credentials',payload['user_id'],role_access_status)



@app.post('/getOrderById')
async def get_order_by_id(payload: dict, conn : psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"get_order_by_id:received payload <{payload}>")
    try:
        role_access_status = check_role_access(conn,payload)
        data = {}
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                #====================ORDER-INFO===================
                query = 'SELECT assignedtooffice,entityid,owner,status,clientpropertyid,service,clientid,orderdate,earlieststartdate,expectedcompletiondate,actualcompletiondate,vendorid,tallyledgerid,briefdescription,comments,additionalcomments FROM orders WHERE id=%s'
                msg = logMessage(cursor,query,[payload['id']])
                logging.info(msg)
                order_info_ = cursor.fetchall()

                colnames = [desc[0] for desc in cursor.description]
                order_info = dict()
                for row in order_info_:
                    row_dict = {colname: value for colname, value in zip(colnames, row)}
                    order_info = row_dict
                if not order_info:
                    order_info = {colname: None for colname in colnames}
                data["order_info"]  = order_info
                #====================ORDER-PHOTOS=================
                query = f'''
                    select id,orderid,photolink,description,phototakenwhen  
                    from order_photos where orderid = {payload['id']}
                '''
                logMessage(cursor,query)
                colnames = [desc[0] for desc in cursor.description]
                _data = cursor.fetchall()
                order_photos = []
                for row in _data:
                    row_dict = {colname: value for colname, value in zip(colnames, row)}
                    order_photos.append(row_dict)  
                data["order_photos"] = order_photos
            return giveSuccess(payload['user_id'],role_access_status,data)
        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure('Invalid Credentials',payload['user_id'],role_access_status)

@app.post('/getOrderStatusHistory')
async def get_order_status_history(payload: dict,conn:psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"get_order_status_history:received payload <{payload}>")
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status==1:
            with conn[0].cursor() as cursor:
                query = 'SELECT distinct a.id,b.briefdescription,c.name,a.dated FROM order_status_change a LEFT JOIN orders b ON a.orderid = b.id LEFT JOIN order_status c ON a.statusid = c.id WHERE a.orderid = %s'
                msg = logMessage(cursor,query,[payload['id']])
                logging.info(msg)
                data = cursor.fetchall()
            
                colnames = [desc[0] for desc in cursor.description]
            order_status_history=  []
            for row in data:
                row_dict = {colname: value for colname, value in zip(colnames, row)}
                order_status_history.append(row_dict)
            return giveSuccess(payload['user_id'],role_access_status,order_status_history)
        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure('Invalid Credentials',payload['user_id'],role_access_status)
    
@app.post('/addOrderStatusChange')
async def add_order_status_change(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"add_order_status_change:received payload <{payload}>")
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'INSERT INTO order_status_change (orderid,statusid,dated) VALUES (%s,%s,%s)'
                msg = logMessage(cursor,query,(payload['orderid'],payload['statusid'],givenowtime()))
                logging.info(msg)
                conn[0].commit()
            return giveSuccess(payload['user_id'],role_access_status,{"edited history":payload['orderid']})
        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure('Invalid Credentials',payload['user_id'],role_access_status)

@app.post('/getBuildersAdmin')
async def get_builders_admin(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"get_builders_admin:received payload <{payload}>")
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'SELECT id,buildername from builder ORDER BY buildername'
                msg = logMessage(cursor,query)
                logging.info(msg)
                data = cursor.fetchall()

                colnames = [desc[0] for desc in cursor.description]
                res = []
                for row in data:
                    row_dict = {col:value for col,value in zip(colnames,row)}
                    res.append(row_dict)
                return giveSuccess(payload['user_id'],role_access_status,res)
        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure('Invalid Credentials',payload['user_id'],role_access_status)

@app.post('/getProjectLegalStatusAdmin')
async def get_project_legal_status_admin(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"getProjectLegalStatusAdmin:received payload <{payload}>")
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'SELECT id,name from project_legal_status ORDER BY name'
                msg = logMessage(cursor,query)
                logging.info(msg)
                data = cursor.fetchall()

                colnames = [desc[0] for desc in cursor.description]
                res = []
                for row in data:
                    row_dict = {col:value for col,value in zip(colnames,row)}
                    res.append(row_dict)
                return giveSuccess(payload['user_id'],role_access_status,res)
        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure('Invalid Credentials',payload['user_id'],role_access_status)  
     

@app.post('/getProjectTypeAdmin')
async def get_project_type_admin(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"getProjectTypeAdmin:received payload <{payload}>")
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'SELECT id,name from project_type ORDER BY name'
                msg = logMessage(cursor,query)
                logging.info(msg)
                data = cursor.fetchall()

                colnames = [desc[0] for desc in cursor.description]
                res = []
                for row in data:
                    row_dict = {col:value for col,value in zip(colnames,row)}
                    res.append(row_dict)
                return giveSuccess(payload['user_id'],role_access_status,res)
        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure('Invalid Credentials',payload['user_id'],role_access_status)  

@app.post('/getVendors')
async def get_vendors(payload : dict, conn : psycopg2.extensions.connection = Depends(get_db_connection)):
    payload['table_name'] = 'get_vendor_view'
    return await runInTryCatch(
        conn = conn,
        fname = 'get_orders',
        payload=payload,
        isPaginationRequired=True,
        whereinquery=True,
        formatData=True,
        isdeleted=True
    )

@app.post('/addVendors')
async def add_vendors(payload : dict, conn : psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"add_vendors:received payload <{payload}>")
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'INSERT INTO vendor (vendorname,addressline1,addressline2,suburb,city,state,country,type,details,category,phone1,email,ownerinfo,panno,tanno,gstservicetaxno,tdssection,bankname,bankbranch,bankcity,bankacctholdername,bankacctno,bankifsccode,bankaccttype,companydeductee,tallyledgerid,dated,createdby,isdeleted) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id'
                msg = logMessage(cursor,query,[payload["vendorname"],payload["addressline1"],payload["addressline2"],payload["suburb"],payload["city"],
                                      payload["state"],payload["country"],payload["type"],payload["details"],payload["category"],payload["phone1"],
                                      payload["email"],payload["ownerinfo"],payload["panno"],payload["tanno"],payload["gstservicetaxno"],
                                      payload["tdssection"],payload["bankname"],payload["bankbranch"],payload["bankcity"],
                                      payload["bankacctholdername"],payload["bankacctno"],payload["bankifsccode"],payload["bankaccttype"],
                                      payload["companydeductee"],payload["tallyledgerid"],givenowtime(),payload['user_id'],False])
                logging.info(msg)
                id = cursor.fetchone()[0]
                conn[0].commit()
                return giveSuccess(payload['user_id'],role_access_status,{"Inserted Vendor":id})
        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure('Invalid Credentials',payload['user_id'],role_access_status)  

@app.post('/editVendors')
async def edit_vendors(payload : dict, conn : psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"edit_vendors:received payload <{payload}>")
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'UPDATE vendor SET vendorname=%s,addressline1=%s,addressline2=%s,suburb=%s,city=%s,state=%s,country=%s,type=%s,details=%s,category=%s,phone1=%s,email=%s,ownerinfo=%s,panno=%s,tanno=%s,gstservicetaxno=%s,tdssection=%s,bankname=%s,bankbranch=%s,bankcity=%s,bankacctholdername=%s,bankacctno=%s,bankifsccode=%s,bankaccttype=%s,companydeductee=%s,tallyledgerid=%s,dated=%s,createdby=%s,isdeleted=%s WHERE id=%s'
                msg = logMessage(cursor,query,[payload["vendorname"],payload["addressline1"],payload["addressline2"],payload["suburb"],payload["city"],
                                      payload["state"],payload["country"],payload["type"],payload["details"],payload["category"],payload["phone1"],
                                      payload["email"],payload["ownerinfo"],payload["panno"],payload["tanno"],payload["gstservicetaxno"],
                                      payload["tdssection"],payload["bankname"],payload["bankbranch"],payload["bankcity"],
                                      payload["bankacctholdername"],payload["bankacctno"],payload["bankifsccode"],payload["bankaccttype"],
                                      payload["companydeductee"],payload["tallyledgerid"],givenowtime(),payload['user_id'],False,
                                      payload["id"]])
                logging.info(msg)
                conn[0].commit()
                return giveSuccess(payload['user_id'],role_access_status,{"Edited Vendor":payload['id']})
        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure('Invalid Credentials',payload['user_id'],role_access_status)

@app.post('/deleteVendors')
async def delete_vendors(payload : dict, conn : psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"delete_vendors:received payload <{payload}>")
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'UPDATE vendor SET isdeleted=true WHERE id=%s and isdeleted=false'
                msg = logMessage(cursor,query,[payload['id']])
                if cursor.statusmessage == "UPDATE 0":
                    return giveFailure(f"No Vendors with id {payload['id']}",payload['user_id'],role_access_status)
                logging.info(msg)
                conn[0].commit()
                return giveSuccess(payload['user_id'],role_access_status,{"Deleted Vendor":payload['id']})
        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure('Invalid Credentials',payload['user_id'],role_access_status)

@app.post('/getVendorInvoice')
async def get_vendor_invoice(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    payload['table_name'] = "get_vendor_invoice_view"
    return await runInTryCatch(
        conn = conn,
        fname = 'get_vendor_invoice',
        payload=payload,
        isPaginationRequired=True,
        whereinquery=True,
        formatData=True,
        isdeleted=True
    )

@app.post('/addVendorInvoice')
async def add_vendor_invoice(payload: dict, conn : psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"add_vendor_invoice:received payload <{payload}>")
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'INSERT INTO order_vendorestimate (estimatedate,amount,estimatedesc,orderid,vendorid,invoicedate,invoiceamount,notes,vat1,vat2,servicetax,invoicenumber,entityid,officeid,dated,createdby,createdon,isdeleted) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id'
                msg = logMessage(cursor,query,[
                    payload["estimatedate"],payload["amount"],payload["estimatedesc"],payload["orderid"],
                    payload["vendorid"],payload["invoicedate"],payload["invoiceamount"],payload["notes"],
                    payload["vat1"],payload["vat2"],payload["servicetax"],payload["invoicenumber"],
                    payload["entityid"],payload["officeid"],givenowtime(),payload['user_id'],datetime.date.today(),False
                ])
                logging.info(msg)
                id = cursor.fetchone()[0]
                conn[0].commit()
            return giveSuccess(payload['user_id'],role_access_status,{"Inserted Invoice":id})
        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure('Invalid Credentials',payload['user_id'],role_access_status)
                
@app.post('/editVendorInvoice')
async def edit_vendor_invoice(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"edit_vendor_invoice:received payload <{payload}>")
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'UPDATE order_vendorestimate SET estimatedate=%s,amount=%s,estimatedesc=%s,orderid=%s,vendorid=%s,invoicedate=%s,invoiceamount=%s,notes=%s,vat1=%s,vat2=%s,servicetax=%s,invoicenumber=%s,entityid=%s,officeid=%s,dated=%s,createdby=%s,createdon=%s,isdeleted=%s WHERE id=%s'
                msg = logMessage(cursor,query,[
                    payload["estimatedate"],payload["amount"],payload["estimatedesc"],payload["orderid"],
                    payload["vendorid"],payload["invoicedate"],payload["invoiceamount"],payload["notes"],
                    payload["vat1"],payload["vat2"],payload["servicetax"],payload["invoicenumber"],
                    payload["entityid"],payload["officeid"],givenowtime(),payload['user_id'],datetime.date.today(),False,payload["id"]
                ])
                logging.info(msg)
                conn[0].commit()
            return giveSuccess(payload['user_id'],role_access_status,{"Edited Invoice":payload['id']})
        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure('Invalid Credentials',payload['user_id'],role_access_status)    

@app.post('/deleteVendorInvoice')
async def delete_vendor_invoice(payload: dict,conn:psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"delete_vendor_invoice:received payload <{payload}>")
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'UPDATE order_vendorestimate SET isdeleted=true WHERE id=%s and isdeleted=False'
                msg = logMessage(cursor,query,[payload['id']])
                logging.info(msg)
                if cursor.statusmessage == "UPDATE 0":
                    return giveFailure(f"No vendor invoice with id {payload['id']}",payload['user_id'],role_access_status)
                conn[0].commit()
                return giveSuccess(payload['user_id'],role_access_status,{"Deleted Vendor":payload['id']})
        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure('Invalid Credentials',payload['user_id'],role_access_status)  

@app.post('/getVendorCategoryAdmin')
async def get_vendor_category_admin(payload:dict,conn:psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"get_vendor_category_admin:received payload <{payload}>")
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'SELECT DISTINCT id,name FROM vendor_category ORDER BY name' 
                msg = logMessage(cursor,query) 
                logging.info(msg)
                data = cursor.fetchall()

                colnames = [desc[0] for desc in cursor.description]
                res = []
                for row in data:
                    row_dict = {col:value for col,value in zip(colnames,row)}
                    res.append(row_dict)
                return giveSuccess(payload['user_id'],role_access_status,res)

        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure('Invalid Credentials',payload['user_id'],role_access_status)

@app.post("/getVendorPayment")
async def get_vendor_payment(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    payload['table_name'] = 'get_vendor_payment_view'
    return await runInTryCatch(
        conn = conn,
        fname = 'get_vendor_payment',
        payload=payload,
        isPaginationRequired=True,
        whereinquery=True,
        formatData=True,
        isdeleted=True
    )

@app.post('/addVendorPayment')
async def add_vendor_payment(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"add_vendor_payment:received payload <{payload}>")
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'INSERT INTO order_payment (paymentby,amount,paymentdate,orderid,vendorid,mode,description,tds,servicetaxamount,entityid,officeid,dated,createdby,isdeleted,createdon) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id'
                msg = logMessage(cursor,query,[
                    payload["paymentby"],payload["amount"],payload["paymentdate"],payload["orderid"],
                    payload["vendorid"],payload["mode"],payload["description"],payload["tds"],
                    payload["servicetaxamount"],payload["entityid"],payload["officeid"],givenowtime(),payload['user_id'],
                    False,datetime.date.today()
                ])
                logging.info(msg)
                id = cursor.fetchone()[0]
                conn[0].commit()
                return giveSuccess(payload['user_id'],role_access_status,{"Inserted Payment":id})
        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure('Invalid Credentials',payload['user_id'],role_access_status)
    
@app.post('/editVendorPayment')
async def edit_vendor_payment(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"edit_vendor_payment:received payload <{payload}>")
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'UPDATE order_payment SET paymentby=%s,amount=%s,paymentdate=%s,orderid=%s,vendorid=%s,mode=%s,description=%s,tds=%s,servicetaxamount=%s,entityid=%s,officeid=%s,dated=%s,createdby=%s,isdeleted=%s,createdon=%s WHERE id=%s'
                msg = logMessage(cursor,query,[
                    payload["paymentby"],payload["amount"],payload["paymentdate"],payload["orderid"],
                    payload["vendorid"],payload["mode"],payload["description"],payload["tds"],
                    payload["servicetaxamount"],payload["entityid"],payload["officeid"],givenowtime(),payload['user_id'],
                    False,datetime.date.today(),payload['id']
                ])
                logging.info(msg)
                conn[0].commit()
                return giveSuccess(payload['user_id'],role_access_status,{"Edited Payment":payload['id']})
        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure('Invalid Credentials',payload['user_id'],role_access_status)
    
@app.post('/deleteVendorPayment')
async def delete_vendor_payment(payload: dict,conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f"delete_vendor_payment:received payload <{payload}>")
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'UPDATE order_payment SET isdeleted=true WHERE id=%s'
                msg = logMessage(cursor,query,[payload['id']])
                if cursor.statusmessage == "UPDATE 0":
                    return giveFailure(f"No Order Payment with id {payload['id']}",payload['user_id'],role_access_status)
                logging.info(msg)
                conn[0].commit()
                return giveSuccess(payload['user_id'],role_access_status,{"Deleted Payment":payload['id']})
        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure('Invalid Credentials',payload['user_id'],role_access_status)

@app.post('/forgotPasswordEmail')
async def forgot_password_email(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        with conn[0].cursor() as cursor:
            query = 'SELECT email1 FROM usertable where username = %s'
            msg = logMessage(cursor,query,[payload['username']])
            logging.info(msg)
            email = cursor.fetchone()

            #SEND EMAIL HERE
            logging.info(email)
            if email is None:
                return giveFailure("No user",None,None)
            else:
                return giveSuccess(None,None,{"Email ID":email[0]})

    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure('Invalid Credentials',None,None)

@app.post("/resetPassword")
async def reset_password(payload: dict,conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        with conn[0].cursor() as cursor:
            #hashing to be done here, using bcrypt for now.
            newp = bcrypt.hashpw(bytes(payload['password'],'ascii'),bcrypt.gensalt()).decode('utf-8')
            logging.info(newp)
            #update part
            query = 'UPDATE usertable SET password = %s WHERE username = %s'
            # msg = logMessage(cursor,query,[newp,payload['username']])
            #logging.info(msg)
            logging.info(cursor.mogrify(query,[newp,payload['username']]))
            return giveSuccess(None,None,{"Change PW for":payload['username']})
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure('Invalid Credentials',None,None)
        
@app.post('/editBuilderContact')
async def add_new_builder_contact(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'add_new_builder_contact: received payload <{payload}>')
    try:
        if 'builderid' not in payload:
            return {
                "result": "error",
                "message": "Missing 'builderid' in payload",
                "user_id": payload.get('user_id', None),
                "data": {}
            }
        
        role_access_status = check_role_access(conn, payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = '''
                    INSERT INTO builder_contacts (
                        builderid=%s, contactname=%s, email1=%s, jobtitle=%s,
                        businessphone=%s, homephone=%s, mobilephone=%s, addressline1=%s,
                        addressline2=%s, suburb=%s, city=%s, state=%s, country=%s,
                        zip=%s, notes=%s, dated=%s, createdby=%s, isdeleted=%s WHERE id=%s
                '''
                msg = logMessage(cursor,query, (
                    payload['builderid'],
                    payload['contactname'],
                    payload['email1'],
                    payload['jobtitle'],
                    payload['businessphone'],
                    payload['homephone'],
                    payload.get('mobilephone', None),
                    payload['addressline1'],
                    payload['addressline2'],
                    payload['suburb'],
                    payload['city'],
                    payload['state'],
                    payload['country'],
                    payload['zip'],
                    payload['notes'],
                    givenowtime(),
                    payload['user_id'],
                    False,
                    payload['id']
                ))
                logging.info(msg)
                # Commit changes to the database
                conn[0].commit()
            data= {
                    "entered": payload['contactname']
                } 
            return giveSuccess(payload['user_id'],role_access_status,data)
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        print(traceback.format_exc())
        return giveFailure(str(e),payload['user_id'],0)

@app.post('/deleteBuilderContact')
async def delete_builder_contact(payload: dict,conn :psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status==1:
            with conn[0].cursor() as cursor:
                query = 'UPDATE builder_contact SET isdeleted = true'
                msg = logMessage(cursor,query,[payload['id']])
                logging.info(msg)
                conn[0].commit()
            return giveSuccess(payload['user_id'],role_access_status,{"deleted data":payload['id']})
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)        
    except Exception as e:
        return giveFailure("Invalid Credentials",0,0)

@app.post('/addLLTenant')
async def add_ll_tenant(payload :dict,conn :psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                for tenant in payload['tenants']:
                    query = 'INSERT INTO clientleavelicensetenant (leavelicenseid,tenantid,dated,createdby,isdeleted) VALUES (%s,%s,%s,%s,%s)'
                    msg = logMessage(cursor,query,[
                            payload['leavelicenseid'],
                            tenant['tenantid'],
                            givenowtime(),
                            payload['user_id'],
                            False
                        ]
                    )
                    logging.info(msg)
                conn[0].commit()
                return giveSuccess(payload['user_id'],role_access_status,{"added ids are":[dct['tenantid'] for dct in payload['tenants']]})
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)        
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure("Invalid Credentials",0,0)  

@app.post('/deleteLLTenant')
async def delete_ll_tenant(payload :dict,conn :psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'UPDATE clientleavelicensetenant SET isdeleted=true WHERE leavelicenseid=%s and isdeleted=false'
                msg = logMessage(cursor,query,[
                        payload['leavelicenseid']
                    ]
                )
                logging.info(msg)
                conn[0].commit()
                return giveSuccess(payload['user_id'],role_access_status,{"delete ll tenants from are":payload['leavelicenseid']})
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)        
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure("Invalid Credentials",0,0)  


@app.post('/getLLTenant')
async def get_ll_tenant(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'SELECT * FROM lltenant_view WHERE leavelicenseid = %s AND isdeleted=false'
                msg = logMessage(cursor,query,[payload['leavelicenseid']])
                logging.info(msg)
                _data = cursor.fetchall()
                colnames = [desc[0] for desc in cursor.description]
                arr = []
                for data in _data:
                    arr.append({colname:val for colname,val in zip(colnames,data)})
            return giveSuccess(payload['user_id'],role_access_status,arr)

        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)        
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure("Invalid Credentials",0,0)

@app.post("/getPMABilling")
async def get_pma_billing(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    tbl=False
    try:
        role_access_status = check_role_access(conn,payload)
        pid = uuid.uuid4()
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                tbl = f'get_pma_billing_view_{pid.hex}'
                query =  f'''CREATE VIEW {tbl} AS
                                SELECT DISTINCT
                                    a.id,
                                    b.clientid,
                                    d.id AS leavelicenseid,
                                    CONCAT_WS(' ', c.firstname, c.lastname) AS clientname,
                                    d.orderid,
                                    CONCAT(' ',e.briefdescription,' {month_map[payload["month"]]}-{payload["year"]} Charges') as briefdescription,
                                    EXTRACT(DAY FROM d.startdate) AS start_day,
                                    d.vacatingdate,
                                    d.rentamount,
                                    a.rented,
                                    a.rentedtax,
                                    a.fixed,
                                    a.fixedtax,
                                    e.entityid,
                                    CASE 
                                        WHEN a.rented IS NULL THEN NULL 
                                        ELSE (d.rentamount * COALESCE(a.rented, 0)/100 * (31-EXTRACT(DAY FROM d.startdate))/30) 
                                    END AS rentedamt,
                                    a.fixed AS fixedamt,
                                    st.rate,
                                    CASE 
                                        WHEN a.rented IS NULL THEN NULL 
                                        ELSE ((d.rentamount * COALESCE(a.rented, 0) / 100) * st.rate / 100 * (31-EXTRACT(DAY FROM d.startdate))/30) 
                                    END AS rentedtaxamt,
                                    (a.fixed * st.rate / 100) AS fixedtaxamt,
                                    COALESCE((d.rentamount * COALESCE(a.rented, 0)/100 * (31-EXTRACT(DAY FROM d.startdate))/30),0) + COALESCE(a.fixed,0) as totalbaseamt,
                                    COALESCE((a.fixed * st.rate / 100),0) + COALESCE((d.rentamount * COALESCE(a.rented, 0) / 100) * st.rate / 100 * (31-EXTRACT(DAY FROM d.startdate))/30,0) AS totaltaxamt,
                                    ((d.rentamount * COALESCE(a.rented, 0) / 100 * (31-EXTRACT(DAY FROM d.startdate))/30) + COALESCE((d.rentamount * COALESCE(a.rented, 0) / 100) * st.rate / 100 * (31-EXTRACT(DAY FROM d.startdate))/30, 0) + COALESCE(a.fixed,0) + (COALESCE(a.fixed,0) * st.rate / 100)) AS totalamt
                                FROM 
                                    client_property_caretaking_agreement a
                                LEFT JOIN
                                    client_property b ON a.clientpropertyid = b.id
                                LEFT JOIN
                                    client c ON b.clientid = c.id
                                LEFT JOIN
                                    client_property_leave_license_details d ON a.clientpropertyid = d.clientpropertyid AND d.active = true
                                LEFT JOIN
                                    orders e ON a.orderid=e.id
                                LEFT JOIN
                                    servicetax st ON '{payload['year']}-{payload['month']}-01' >= st.fromdate AND '{payload['year']}-{payload['month']}-01' <= st.todate
                                WHERE
                                    (d.clientpropertyid, d.startdate) IN (
                                        SELECT 
                                            clientpropertyid,
                                            MAX(startdate) AS max_startdate
                                        FROM 
                                            client_property_leave_license_details
                                        GROUP BY 
                                            clientpropertyid
                                    )
                                AND
                                    a.active = true
                                AND 
                                    a.isdeleted=false
                                AND
                                    e.service = 62;


'''
                cursor.execute(query)
                logging.info(cursor.statusmessage)
                conn[0].commit()
                payload['rows'] = ['*']
                payload['table_name'] = tbl
                data = await runInTryCatch(conn,fname='pma_billing',payload=payload,isPaginationRequired=True,whereinquery=False,formatData=True,isdeleted=False)
                for row in data['data']:
                    row['invoicedate'] = f"01-{month_map[payload['month']]}-{payload['year']}"
                if not payload['insertIntoDB']:
                    return data
                else:
                    cursor.execute(f'select * from {tbl}')
                    _rows = cursor.fetchall()

                    colnames = [desc[0] for desc in cursor.description]
                    rows = []
                    for row in _rows:
                        rows.append({colname:val for colname,val in zip(colnames,row)})
                    
                    for row in rows:
                        query = 'INSERT INTO order_invoice (clientid,orderid,estimatedate,estimateamount,invoicedate,invoiceamount,quotedescription,createdon,baseamount,tax,entityid,dated,createdby,isdeleted) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                        msg = logMessage(cursor,query,[
                            row["clientid"],row["orderid"],None,row["totalamt"],
                            datetime.date.today(),row["totalamt"],row["briefdescription"],datetime.date.today(),
                            row["totalbaseamt"],row["totaltaxamt"],row["entityid"],givenowtime(),payload['user_id'],False
                        ])
                    #---Only enable when not testing
                    conn[0].commit()
                    return giveSuccess(payload['user_id'],role_access_status,len(_rows))
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)        
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure("Invalid Credentials",0,0)
    finally:
        if tbl:
            cursor = conn[0].cursor()
            cursor.execute(f'drop view {tbl}')
            conn[0].commit()

@app.post("/getOrderPending")
async def get_order_pending(payload: dict, conn :psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status:
            with conn[0].cursor() as cursor:
                logMessage(cursor,f"SELECT sum(a.invoiceamount)-sum(b.amount) FROM order_invoice a LEFT JOIN order_receipt b ON a.orderid = b.orderid WHERE a.orderid = {payload['orderid']}")
                pending = cursor.fetchone()[0]
                logMessage(cursor,f"SELECT orderstatus,orderdate FROM get_orders_view WHERE id={payload['orderid']}")
                orderstatus,orderdate = cursor.fetchone()
            data = {
                "pending":0 if pending is None else pending,
                "orderstatus":orderstatus,
                "orderdate":orderdate
            }
            return giveSuccess(payload['user_id'],role_access_status,data)
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)
    except KeyError as ke:
        logging.info(traceback.print_exc())
        return giveFailure(f"Key error{ke}",0,0)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure("Invalid Credentials",0,0)
    
@app.post("/getUserInfo")
async def get_user(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    payload['table_name'] = 'get_users_view'
    return await runInTryCatch(
        conn = conn,
        fname="add_user",
        payload=payload,
        isPaginationRequired=True,
        whereinquery=True,
        formatData=True,
        isdeleted=True
    )

@app.post("/addUser")
async def add_user(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                payload['password'] = bcrypt.hashpw(base64.b64decode(payload['password']),bcrypt.gensalt(12)).decode("utf-8")
                query = "INSERT INTO usertable (username,roleid,password,officeid,lobid,usercode,firstname,lastname,status,effectivedate,homephone,workphone,email1,email2,addressline1,addressline2,suburb,city,state,country,zip,dated,createdby,isdeleted,entityid) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id"
                msg = logMessage(cursor,query,(payload['username'],payload['roleid'],payload['password'],payload['officeid'],payload['lobid'],payload['usercode'],payload['firstname'],payload['lastname'],payload['status'],payload['effectivedate'],payload['homephone'],payload['workphone'],payload['email1'],payload['email2'],payload['addressline1'],payload['addressline2'],payload['suburb'],payload['city'],payload['state'],payload['country'],payload['zip'],givenowtime(),payload['user_id'],False,payload['entityid']))
                logging.info(msg)
                id = cursor.fetchone()[0]
                conn[0].commit()
                return giveSuccess(payload['user_id'],role_access_status,{"Inserted User ID":id})
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)
    except KeyError as ke:
        logging.info(traceback.print_exc())
        return giveFailure(f"{ke} is missing",0,0)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure("Invalid Credentials",0,0)

@app.post("/editUser")
async def edit_user(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                payload['password'] = bcrypt.hashpw(base64.b64decode(payload['password']),bcrypt.gensalt(12)).decode("utf-8")
                query = "UPDATE usertable SET username=%s,roleid=%s,password=%s,officeid=%s,lobid=%s,usercode=%s,firstname=%s,lastname=%s,status=%s,effectivedate=%s,homephone=%s,workphone=%s,email1=%s,email2=%s,addressline1=%s,addressline2=%s,suburb=%s,city=%s,state=%s,country=%s,zip=%s,dated=%s,createdby=%s,isdeleted=%s,entityid=%s WHERE id=%s"
                msg = logMessage(cursor,query,(payload['username'],payload['roleid'],payload['password'],payload['officeid'],payload['lobid'],payload['usercode'],payload['firstname'],payload['lastname'],payload['status'],payload['effectivedate'],payload['homephone'],payload['workphone'],payload['email1'],payload['email2'],payload['addressline1'],payload['addressline2'],payload['suburb'],payload['city'],payload['state'],payload['country'],payload['zip'],givenowtime(),payload['user_id'],False,payload['entityid'],payload['id']))
                logging.info(msg)
                conn[0].commit()
                return giveSuccess(payload['user_id'],role_access_status,{"Edited User ID":payload['id']})
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)
    except KeyError as ke:
        logging.info(traceback.print_exc())
        return giveFailure(f"{ke} is missing",0,0)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure("Invalid Credentials",0,0)
    
@app.post("/deleteUser")
async def delete_user(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = f"UPDATE usertable SET isdeleted=true WHERE id={payload['id']} and isdeleted=false"
                cursor.execute(query)
                if cursor.statusmessage == "UPDATE 0":
                    return giveFailure(f"No User with id {payload['id']}",payload['user_id'],role_access_status)
                conn[0].commit()
                return giveSuccess(payload['user_id'],role_access_status,{"Deleted User ID":payload['id']})
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)
    except KeyError as ke:
        logging.info(traceback.print_exc())
        return giveFailure(f"{ke} is missing",0,0)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure("Invalid Credentials",0,0)

@app.post("/getServices")
async def get_services(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    payload['table_name'] = 'get_services_view'
    return await runInTryCatch(
        conn = conn,
        fname="get_services",
        payload=payload,
        isPaginationRequired=True,
        whereinquery=False,
        formatData=True,
        isdeleted=False
    )

@app.post('/addService')
async def add_services(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = """INSERT INTO services (lob,service,active,dated,createdby,isdeleted,servicetype,category2,tallyledgerid)
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id"""
                msg = logMessage(cursor,query,(payload['lob'],payload['service'],payload['active'],givenowtime(),payload['user_id'],False,payload['servicetype'],payload['category2'],payload['tallyledgerid']))
                logging.info(msg)
                id = cursor.fetchone()[0]
                conn[0].commit()
                return giveSuccess(payload['user_id'],role_access_status,{"Inserted Service ID":id})
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)
    except KeyError as ke:
        logging.info(traceback.print_exc())
        return giveFailure(f"Missing key {ke}",0,0)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure(f"Invalid Credentials",0,0)
    
@app.post('/editService')
async def edit_services(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = """UPDATE services SET lob=%s,service=%s,active=%s,dated=%s,createdby=%s,isdeleted=%s,servicetype=%s,category2=%s,tallyledgerid=%s WHERE id=%s"""
                msg = logMessage(cursor,query,(payload['lob'],payload['service'],payload['active'],givenowtime(),payload['user_id'],False,payload['servicetype'],payload['category2'],payload['tallyledgerid'],payload['id']))
                logging.info(msg)
                conn[0].commit()
                return giveSuccess(payload['user_id'],role_access_status,{"Edited Service ID":payload['id']})
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)
    except KeyError as ke:
        logging.info(traceback.print_exc())
        return giveFailure(f"Missing key {ke}",0,0)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure(f"Invalid Credentials",0,0)
    
    
@app.post('/deleteService')
async def delete_services(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = """DELETE FROM services WHERE id=%s"""
                msg = logMessage(cursor,query,(payload['id'],))
                logging.info(msg)
                conn[0].commit()
                return giveSuccess(payload['user_id'],role_access_status,{"Deleted Service ID":payload['id']})
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)
    except KeyError as ke:
        logging.info(traceback.print_exc())
        return giveFailure(f"Missing key {ke}",0,0)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure(f"Invalid Credentials",0,0)

@app.post('/getReportOrderPayment')
async def get_report_order_payment(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        payload['table_name'] = 'orderpaymentview'
        payload['filters'].append(['paymentdate','between',[payload['startdate'],payload['enddate']],'Date'])
        
        res = await runInTryCatch(
            conn = conn,
            payload=payload,
            fname='get_report_order_payment',
            isPaginationRequired=True,
            whereinquery=True,
            formatData=True,
            isdeleted=True
        )
        return res
    except KeyError as ke:
        logging.info(traceback.print_exc())
        return giveFailure(f'Missing key {ke}',0,0)


@app.post('/getResearchEmployer')
async def get_research_employer(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
        payload['table_name'] = 'get_research_employer_view'
        return await runInTryCatch(
            conn = conn,
            fname='get_reseatch_employer',
            payload=payload,
            isPaginationRequired=True,
            whereinquery=True,
            formatData=True,
            isdeleted=True
        )

@app.post('/addResearchEmployer')
async def add_research_employer(payload:dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = """INSERT INTO research_employer (country,onsiteopportunity,city,state,admincontactmail,zip,hc,website,
                admincontactphone,contactname1,contactmail1,contactphone1,contactname2,contactmail2,contactphone2,
                hrcontactname,hrcontactmail,hrcontactphone,admincontactname,employername,industry,addressline1,addressline2,suburb,
                dated,createdby,isdeleted) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id"""
                msg = logMessage(cursor,query,[
                    payload["country"],payload["onsiteopportunity"],payload["city"],payload["state"],payload["admincontactmail"],
                    payload["zip"],payload["hc"],payload["website"],payload["admincontactphone"],payload["contactname1"],
                    payload["contactmail1"],payload["contactphone1"],payload["contactname2"],payload["contactmail2"],payload["contactphone2"],
                    payload["hrcontactname"],payload["hrcontactmail"],payload["hrcontactphone"],payload["admincontactname"],payload["employername"],
                    payload["industry"],payload["addressline1"],payload["addressline2"],payload["suburb"],givenowtime(),payload['user_id'],False
                ])
                logging.info(msg)
                id = cursor.fetchone()[0]
                conn[0].commit()
            return giveSuccess(payload['user_id'],role_access_status,{"Inserted Employer":id})
        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except KeyError as ke:
        logging.info(traceback.print_exc())
        return giveFailure(f"Missing key {ke}",0,0)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure(f"Invalid Credentials",0,0)

@app.post('/editResearchEmployer')
async def edit_research_employer(payload:dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = """UPDATE research_employer SET country=%s,onsiteopportunity=%s,city=%s,state=%s,admincontactmail=%s,zip=%s,hc=%s,website=%s,
                admincontactphone=%s,contactname1=%s,contactmail1=%s,contactphone1=%s,contactname2=%s,contactmail2=%s,contactphone2=%s,
                hrcontactname=%s,hrcontactmail=%s,hrcontactphone=%s,admincontactname=%s,employername=%s,industry=%s,addressline1=%s,addressline2=%s,suburb=%s,
                dated=%s,createdby=%s,isdeleted=%s WHERE id=%s"""
                msg = logMessage(cursor,query,[
                    payload["country"],payload["onsiteopportunity"],payload["city"],payload["state"],payload["admincontactmail"],
                    payload["zip"],payload["hc"],payload["website"],payload["admincontactphone"],payload["contactname1"],
                    payload["contactmail1"],payload["contactphone1"],payload["contactname2"],payload["contactmail2"],payload["contactphone2"],
                    payload["hrcontactname"],payload["hrcontactmail"],payload["hrcontactphone"],payload["admincontactname"],payload["employername"],
                    payload["industry"],payload["addressline1"],payload["addressline2"],payload["suburb"],givenowtime(),payload['user_id'],False,payload['id']
                ])
                logging.info(msg)
                conn[0].commit()
            if cursor.statusmessage == "UPDATE 0":
                return giveFailure('No Record Available',payload['user_id'],role_access_status)
            else:
                return giveSuccess(payload['user_id'],role_access_status,{"Edited Employer":payload['id']})
        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except KeyError as ke:
        logging.info(traceback.print_exc())
        return giveFailure(f"Missing key {ke}",0,0)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure(f"Invalid Credentials",0,0)

@app.post('/deleteResearchEmployer')
async def delete_research_employer(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'UPDATE research_employer SET isdeleted=true WHERE id=%s and isdeleted=false'
                msg = logMessage(cursor,query,[payload['id']])
                logging.info(msg)
                conn[0].commit()
            if cursor.statusmessage == "UPDATE 0":
                return giveFailure('No Record Available',payload['user_id'],role_access_status)
            else:
                return giveSuccess(payload['user_id'],role_access_status,{"Deleted Employer":payload['id']})
        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except KeyError as ke:
        logging.info(traceback.print_exc())
        return giveFailure(f"Missing key {ke}",0,0)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure(f"Invalid Credentials",0,0)

@app.post('/getResearchAgents')
async def get_research_agents(payload: dict,conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    payload['table_name'] = 'get_research_realestate_agents_view'
    return await runInTryCatch(
        conn = conn,
        fname = 'get_research_agents',
        payload=payload,
        isPaginationRequired=True,
        whereinquery=True,
        formatData=True,
        isdeleted=True
    )

@app.post('/addResearchAgents')
async def add_research_agents(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = """INSERT INTO realestateagents (nameofagent,agencyname,emailid,phoneno,phoneno2,localitiesdealing,nameofpartners,registered,dated,createdby,isdeleted) 
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id"""
                msg = logMessage(cursor,query,[
                    payload["nameofagent"],payload["agencyname"],payload["emailid"],payload["phoneno"],payload["phoneno2"],
                    payload["localitiesdealing"],payload["nameofpartners"],payload["registered"],givenowtime(),payload['user_id'],False
                ])
                logging.info(msg)
                id = cursor.fetchone()[0]
                conn[0].commit()
            return giveSuccess(payload['user_id'],role_access_status,{"Inserted Agent":id})
        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except KeyError as ke:
        logging.info(traceback.print_exc())
        return giveFailure(f"Missing key {ke}",0,0)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure(f"Invalid Credentials",0,0)

@app.post('/editResearchAgents')
async def edit_research_agents(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = """UPDATE realestateagents SET nameofagent=%s,agencyname=%s,emailid=%s,phoneno=%s,phoneno2=%s,localitiesdealing=%s,nameofpartners=%s,registered=%s,dated=%s,createdby=%s,isdeleted=%s 
                           WHERE id=%s"""
                msg = logMessage(cursor,query,[
                    payload["nameofagent"],payload["agencyname"],payload["emailid"],payload["phoneno"],payload["phoneno2"],
                    payload["localitiesdealing"],payload["nameofpartners"],payload["registered"],givenowtime(),payload['user_id'],
                    False,payload['id']
                ])
                logging.info(msg)
                conn[0].commit()
            return giveSuccess(payload['user_id'],role_access_status,{"Edited Agent":payload['id']})
        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except KeyError as ke:
        logging.info(traceback.print_exc())
        return giveFailure(f"Missing key {ke}",0,0)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure(f"Invalid Credentials",0,0)

@app.post('/deleteResearchAgents')
async def delete_research_agents(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'UPDATE realestateagents SET isdeleted=true WHERE id=%s and isdeleted=false'
                msg = logMessage(cursor,query,[payload['id']])
                logging.info(msg)
                conn[0].commit()
            if cursor.statusmessage == "UPDATE 0":
                return giveFailure('No Record Available',payload['user_id'],role_access_status)
            else:
                return giveSuccess(payload['user_id'],role_access_status,{"Deleted Agent":payload['id']})
        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except KeyError as ke:
        logging.info(traceback.print_exc())
        return giveFailure(f"Missing key {ke}",0,0)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure(f"Invalid Credentials",0,0)

@app.post('/getResearchCOCAndBusinessGroup')
async def get_research_coc_and_business_group(payload: dict,conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    payload['table_name'] = 'get_cocandbusinessgroup_view'
    return await runInTryCatch(
        conn = conn,
        payload=payload,
        fname = 'get_research_COC_and_business_group',
        isPaginationRequired=True,
        whereinquery=True,
        isdeleted=True,
        formatData=True
    )

@app.post('/addResearchCOCAndBusinessGroup')
async def add_research_coc_and_business_group(payload: dict,conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = '''INSERT INTO cocandbusinessgroup (name,suburb,phoneno,contactperson1,emailid,contactperson2,email1,email2,contactname1,
                contactname2,city,state,country,groupid,address,excludefrommailinglist,dated,createdby,isdeleted) VALUES 
                (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id'''
                msg = logMessage(cursor,query,[
                    payload["name"],payload["suburb"],payload["phoneno"],payload["contactperson1"],payload["emailid"],payload["contactperson2"],
                    payload["email1"],payload["email2"],payload["contactname1"],payload["contactname2"],payload["city"],payload["state"],payload["country"],
                    payload["groupid"],payload["address"],payload["excludefrommailinglist"],givenowtime(),payload['user_id'],False
                ])
                logging.info(msg)
                id = cursor.fetchone()[0]
                conn[0].commit()
                return giveSuccess(payload['user_id'],role_access_status,{"Inserted Group":id})
        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except KeyError as ke:
        logging.info(traceback.print_exc())
        return giveFailure(f"Missing key {ke}",0,0)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure(f"Invalid Credentials",0,0)

@app.post('/editResearchCOCAndBusinessGroup')
async def edit_research_coc_and_business_group(payload: dict,conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = '''UPDATE cocandbusinessgroup SET name=%s,suburb=%s,phoneno=%s,contactperson1=%s,emailid=%s,contactperson2=%s,email1=%s,email2=%s,contactname1=%s,
                contactname2=%s,city=%s,state=%s,country=%s,groupid=%s,address=%s,excludefrommailinglist=%s,dated=%s,createdby=%s,isdeleted=%s WHERE id=%s'''
                msg = logMessage(cursor,query,[
                    payload["name"],payload["suburb"],payload["phoneno"],payload["contactperson1"],payload["emailid"],payload["contactperson2"],
                    payload["email1"],payload["email2"],payload["contactname1"],payload["contactname2"],payload["city"],payload["state"],payload["country"],
                    payload["groupid"],payload["address"],payload["excludefrommailinglist"],givenowtime(),payload['user_id'],False,payload['id']
                ])
                logging.info(msg)
                if cursor.statusmessage == 'UPDATE 0':
                    return giveFailure("No Record Available",payload['user_id'],role_access_status)
                else:
                    conn[0].commit()
                    return giveSuccess(payload['user_id'],role_access_status,{"Edited Group":payload['id']})
        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except KeyError as ke:
        logging.info(traceback.print_exc())
        return giveFailure(f"Missing key {ke}",0,0)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure(f"Invalid Credentials",0,0)

@app.post('/deleteResearchCOCAndBusinessGroup')
async def edit_research_coc_and_business_group(payload: dict,conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = '''UPDATE cocandbusinessgroup SET isdeleted=true WHERE id=%s and isdeleted=false'''
                msg = logMessage(cursor,query,[
                    payload['id']
                ])
                logging.info(msg)
                if cursor.statusmessage == 'UPDATE 0':
                    return giveFailure("No Record Available",payload['user_id'],role_access_status)
                else:
                    conn[0].commit()
                    return giveSuccess(payload['user_id'],role_access_status,{"Deleted Group":payload['id']})
        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except KeyError as ke:
        logging.info(traceback.print_exc())
        return giveFailure(f"Missing key {ke}",0,0)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure(f"Invalid Credentials",0,0)
    
@app.post('/getGroupsAdmin')
async def get_payment_status_admin(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'SELECT DISTINCT id,name from z_cocbusinessgroup order by name'
                msg = logMessage(cursor,query)
                _data = cursor.fetchall()
                logging.info(msg)
                
                colnames = [desc[0] for desc in cursor.description]
                res = []
                for data in _data:
                    res.append({colname:val for colname,val in zip(colnames,data)})
                if not data:
                    res = {colname:None for colname in colnames}
            return giveSuccess(payload['user_id'],role_access_status,res)
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure("Invalid Credentials",0,0)

@app.post('/getResearchProfessional')
async def get_research_professional(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    payload['table_name'] = 'get_professionals_view'
    return await runInTryCatch(
        conn = conn,
        fname = 'get_research_professionals',
        payload=payload,
        isPaginationRequired=True,
        whereinquery=True,
        formatData=True,
        isdeleted=True
    )

@app.post('/addResearchProfessional')
async def add_research_professional(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = '''INSERT INTO professionals (typeid,dated,createdby,isdeleted,city,country,excludefrommailinglist,name,
                suburb,emailid,phoneno,website,state,phoneno1) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id'''
                msg = logMessage(cursor,query,[
                                    payload['typeid'],
                                    givenowtime(),
                                    payload['user_id'],
                                    False,
                                    payload['city'],
                                    payload['country'],
                                    payload['excludefrommailinglist'],
                                    payload['name'],
                                    payload['suburb'],
                                    payload['emailid'],
                                    payload['phoneno'],
                                    payload['website'],
                                    payload['state'],
                                    payload['phoneno1']
                                    ]
                                 )
                logging.info(msg)
                id = cursor.fetchone()[0]
                conn[0].commit()
                return giveSuccess(payload['user_id'],role_access_status,{"Inserted Professional":id})
        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except KeyError as ke:
        logging.info(traceback.print_exc())
        return giveFailure(f"Missing key {ke}",0,0)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure(f"Invalid Credentials",0,0)

@app.post('/editResearchProfessional')
async def edit_research_professional(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = '''UPDATE professionals SET typeid=%s,dated=%s,createdby=%s,isdeleted=%s,city=%s,country=%s,excludefrommailinglist=%s,name=%s,
                suburb=%s,emailid=%s,phoneno=%s,website=%s,state=%s,phoneno1=%s WHERe id=%s'''
                msg = logMessage(cursor,query,[
                                    payload['typeid'],
                                    givenowtime(),
                                    payload['user_id'],
                                    False,
                                    payload['city'],
                                    payload['country'],
                                    payload['excludefrommailinglist'],
                                    payload['name'],
                                    payload['suburb'],
                                    payload['emailid'],
                                    payload['phoneno'],
                                    payload['website'],
                                    payload['state'],
                                    payload['phoneno1'],
                                    payload['id']
                                    ]
                                 )
                logging.info(msg)
                if cursor.statusmessage == 'UPDATE 0':
                    return giveFailure("No Record Available",payload['user_id'],role_access_status)
                else:
                    conn[0].commit()
                    return giveSuccess(payload['user_id'],role_access_status,{"Edited Professional":payload['id']})
        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except KeyError as ke:
        logging.info(traceback.print_exc())
        return giveFailure(f"Missing key {ke}",0,0)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure(f"Invalid Credentials",0,0)
    
@app.post('/deleteResearchProfessional')
async def delete_research_professional(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = '''UPDATE professionals SET isdeleted=true WHERe id=%s and isdeleted=false'''
                msg = logMessage(cursor,query,[
                                        payload['id']
                                    ]
                                 )
                logging.info(msg)
                if cursor.statusmessage == 'UPDATE 0':
                    return giveFailure("No Record Available",payload['user_id'],role_access_status)
                else:
                    conn[0].commit()
                    return giveSuccess(payload['user_id'],role_access_status,{"Deleted Professional":payload['id']})
        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except KeyError as ke:
        logging.info(traceback.print_exc())
        return giveFailure(f"Missing key {ke}",0,0)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure(f"Invalid Credentials",0,0)

@app.post('/getProfessionalTypesAdmin')
async def get_payment_status_admin(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'SELECT DISTINCT professionalid,name from professionaltypes order by name'
                msg = logMessage(cursor,query)
                _data = cursor.fetchall()
                logging.info(msg)
                
                colnames = [desc[0] for desc in cursor.description]
                res = []
                for data in _data:
                    res.append({colname:val for colname,val in zip(colnames,data)})
                if not data:
                    res = {colname:None for colname in colnames}
            return giveSuccess(payload['user_id'],role_access_status,res)
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure("Invalid Credentials",0,0)

@app.post('/getReportOrderReceipt')
async def get_report_order_receipt(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        payload['table_name'] = 'orderreceiptview'
        payload['filters'].append(['recddate','between',[payload['startdate'],payload['enddate']],'Date'])
        
        res = await runInTryCatch(
            conn = conn,
            payload=payload,
            fname='get_report_order_payment',
            isPaginationRequired=True,
            whereinquery=True,
            formatData=True,
            isdeleted=True
        )
        return res
    except KeyError as ke:
        logging.info(traceback.print_exc())
        return giveFailure(f'Missing key {ke}',0,0)

@app.post('/getResearchGovtAgencies')
async def get_research_govt_agencies(payload: dict,conn:psycopg2.extensions.connection = Depends(get_db_connection)):
    payload['table_name'] = 'get_research_govt_agencies_view'
    return await runInTryCatch(
        conn = conn,
        fname = 'get_research_govt_agencies',
        payload=payload,
        isPaginationRequired=True,
        whereinquery=True,
        formatData=True,
        isdeleted=True
    )

@app.post('/addResearchGovtAgencies')
async def add_research_govt_agencies(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = '''INSERT INTO research_government_agencies (agencyname,addressline1,addressline2,suburb,
                            city,state,country,zip,agencytype,details,contactname,contactmail,contactphone,
                            maplink,dated,createdby,isdeleted) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id'''
                msg = logMessage(cursor,query,[
                                    payload['agencyname'],
                                    payload['addressline1'],
                                    payload['addressline2'],
                                    payload['suburb'],
                                    payload['city'],
                                    payload['state'],
                                    payload['country'],
                                    payload['zip'],
                                    payload['agencytype'],
                                    payload['details'],
                                    payload['contactname'],
                                    payload['contactmail'],
                                    payload['contactphone'],
                                    payload['maplink'],
                                    givenowtime(),
                                    payload['user_id'],
                                    False
                                ])
                logging.info(msg)
                id = cursor.fetchone()[0]
                conn[0].commit()
                return giveSuccess(payload['user_id'],role_access_status,{"Inserted Agency":id})
        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except KeyError as ke:
        logging.info(traceback.print_exc())
        return giveFailure(f"Missing key {ke}",0,0)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure(f"Invalid Credentials",0,0)

@app.post('/editResearchGovtAgencies')
async def edit_research_govt_agencies(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = '''UPDATE research_government_agencies SET agencyname=%s,addressline1=%s,addressline2=%s,suburb=%s,
                            city=%s,state=%s,country=%s,zip=%s,agencytype=%s,details=%s,contactname=%s,contactmail=%s,contactphone=%s,
                            maplink=%s,dated=%s,createdby=%s,isdeleted=%s WHERE id=%s'''
                msg = logMessage(cursor,query,[
                                    payload['agencyname'],
                                    payload['addressline1'],
                                    payload['addressline2'],
                                    payload['suburb'],
                                    payload['city'],
                                    payload['state'],
                                    payload['country'],
                                    payload['zip'],
                                    payload['agencytype'],
                                    payload['details'],
                                    payload['contactname'],
                                    payload['contactmail'],
                                    payload['contactphone'],
                                    payload['maplink'],
                                    givenowtime(),
                                    payload['user_id'],
                                    False,
                                    payload['id']
                                ])
                logging.info(msg)
                conn[0].commit()
                return giveSuccess(payload['user_id'],role_access_status,{"Edited Agency":payload['id']})
        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except KeyError as ke:
        logging.info(traceback.print_exc())
        return giveFailure(f"Missing key {ke}",0,0)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure(f"Invalid Credentials",0,0)
    

@app.post('/deleteResearchGovtAgencies')
async def delete_research_govt_agencies(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = '''UPDATE research_government_agencies SET isdeleted=true WHERE id=%s and isdeleted=false'''
                msg = logMessage(cursor,query,[
                                    payload['id']
                                ])
                logging.info(msg)
                conn[0].commit()
                return giveSuccess(payload['user_id'],role_access_status,{"Deleted Agency":payload['id']})
        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except KeyError as ke:
        logging.info(traceback.print_exc())
        return giveFailure(f"Missing key {ke}",0,0)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure(f"Invalid Credentials",0,0)

@app.post('/getAgencyTypeAdmin')
async def get_agency_type_admin(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'SELECT id,name from agencytype order by name'
                msg = logMessage(cursor,query)
                _data = cursor.fetchall()
                logging.info(msg)
                
                colnames = [desc[0] for desc in cursor.description]
                res = []
                for data in _data:
                    res.append({colname:val for colname,val in zip(colnames,data)})
                if not data:
                    res = {colname:None for colname in colnames}
            return giveSuccess(payload['user_id'],role_access_status,res)
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure("Invalid Credentials",0,0)

@app.post('/getResearchFriends')
async def get_research_friends(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    payload['table_name'] = 'get_research_friends_view'
    return await runInTryCatch(
        conn = conn,
        fname = 'get_research_friends',
        isPaginationRequired=True,
        whereinquery=True,
        formatData=True,
        isdeleted=True,
        payload=payload
    )

@app.post('/addResearchFriends')
async def add_research_friends(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = '''INSERT INTO friends (name,emailid,phoneno,contactname,societyname,employer,suburb,city,state,country,notes,excludefrommailinglist
                ,dated,createdby,isdeleted) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id'''
                msg = logMessage(cursor,query,[payload["name"],payload["emailid"],payload["phoneno"],payload["contactname"],payload["societyname"],payload["employer"],
                                               payload["suburb"],payload["city"],payload["state"],payload["country"],payload["notes"],payload["excludefrommailinglist"],
                                               givenowtime(),payload['user_id'],False
                                ])
                logging.info(msg)
                id = cursor.fetchone()[0]
                conn[0].commit()
                return giveSuccess(payload['user_id'],role_access_status,{"Inserted Friend":id})
        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except KeyError as ke:
        logging.info(traceback.print_exc())
        return giveFailure(f"Missing key {ke}",0,0)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure(f"Invalid Credentials",0,0)

@app.post('/editResearchFriends')
async def edit_research_friends(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = '''UPDATE friends SET name=%s,emailid=%s,phoneno=%s,contactname=%s,societyname=%s,employer=%s,suburb=%s,city=%s,state=%s,country=%s,notes=%s,excludefrommailinglist=%s
                ,dated=%s,createdby=%s,isdeleted=%s WHERe id=%s'''
                msg = logMessage(cursor,query,[payload["name"],payload["emailid"],payload["phoneno"],payload["contactname"],payload["societyname"],payload["employer"],
                                               payload["suburb"],payload["city"],payload["state"],payload["country"],payload["notes"],payload["excludefrommailinglist"],
                                               givenowtime(),payload['user_id'],False,payload['id']
                                ])
                logging.info(msg)
                conn[0].commit()
                return giveSuccess(payload['user_id'],role_access_status,{"Edited Friend":payload['id']})
        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except KeyError as ke:
        logging.info(traceback.print_exc())
        return giveFailure(f"Missing key {ke}",0,0)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure(f"Invalid Credentials",0,0)

@app.post('/deleteResearchFriends')
async def delete_research_friends(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = '''UPDATE friends SET isdeleted=true WHERe id=%s AND isdeleted=false'''
                msg = logMessage(cursor,query,[
                                    payload['id']
                                ])
                logging.info(msg)
                conn[0].commit()
                return giveSuccess(payload['user_id'],role_access_status,{"Deleted Friend":payload['id']})
        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except KeyError as ke:
        logging.info(traceback.print_exc())
        return giveFailure(f"Missing key {ke}",0,0)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure(f"Invalid Credentials",0,0)

@app.post('/getResearchBanksAndBranches')
async def get_research_banks_and_branches(payload: dict,conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    payload['table_name'] = 'banksandbranches'
    return await runInTryCatch(
        conn = conn,
        payload=payload,
        fname='get_research_banks_and_branches',
        isPaginationRequired=True,
        whereinquery=True,
        formatData=True,
        isdeleted=True
    )

@app.post('/addResearchBanksAndBranches')
async def add_research_banks_and_branches(payload: dict,conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = """INSERT INTO banksandbranches (name,emailid,phoneno,website,
                    contact,dated,createdby,isdeleted,excludefrommailinglist) VALUES (%s,
                    %s,%s,%s,%s,%s,%s,%s,%s) RETURNING id"""
                msg = logMessage(cursor,query,[
                    payload['name'],
                    payload['emailid'],
                    payload['phoneno'],
                    payload['website'],
                    payload['contact'],
                    givenowtime(),
                    payload['user_id'],
                    False,
                    payload['excludefrommailinglist']
                ])
                id = cursor.fetchone()[0]
                logging.info(msg)
                conn[0].commit()
                return giveSuccess(payload['user_id'],role_access_status,{"Inserted Bank":id})
        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except KeyError as ke:
        logging.info(traceback.print_exc())
        return giveFailure(f"Missing key {ke}",0,0)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure(f"Invalid Credentials",0,0)
    
@app.post('/editResearchBanksAndBranches')
async def edit_research_banks_and_branches(payload: dict,conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = """UPDATE banksandbranches SET name=%s,emailid=%s,phoneno=%s,website=%s,
                    contact=%s,dated=%s,createdby=%s,isdeleted=%s,excludefrommailinglist=%s WHERE id=%s"""
                msg = logMessage(cursor,query,[
                    payload['name'],
                    payload['emailid'],
                    payload['phoneno'],
                    payload['website'],
                    payload['contact'],
                    givenowtime(),
                    payload['user_id'],
                    False,
                    payload['excludefrommailinglist'],
                    payload['id']
                ])
                logging.info(msg)
                conn[0].commit()
                return giveSuccess(payload['user_id'],role_access_status,{"Edited Bank":payload['id']})
        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except KeyError as ke:
        logging.info(traceback.print_exc())
        return giveFailure(f"Missing key {ke}",0,0)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure(f"Invalid Credentials",0,0)

@app.post('/deleteResearchBanksAndBranches')
async def delete_research_banks_and_branches(payload: dict,conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = """UPDATE banksandbranches SET isdeleted=true WHERE id=%s AND isdeleted=false"""
                msg = logMessage(cursor,query,[
                    payload['id']
                ])
                logging.info(msg)
                conn[0].commit()
                return giveSuccess(payload['user_id'],role_access_status,{"Deleted Bank":payload['id']})
        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except KeyError as ke:
        logging.info(traceback.print_exc())
        return giveFailure(f"Missing key {ke}",0,0)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure(f"Invalid Credentials",0,0)

@app.post("/download/{file_name}")
def download_file(payload: dict,conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'got download file request with payload <{payload}>')
    try:
        file_name = payload['filename']
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            file_path = os.path.join(FILE_DIRECTORY, file_name)
            # Security check - only allow filenames, no paths
            if "/" in file_name or "\\" in file_name:
                logging.info(f'invalid filepath <{file_path}')
                return {"error": "Invalid file path"}
            if os.path.exists(file_path):
                logging.info(f'downloading file <{file_path}')
                return FileResponse(path=file_path, filename=file_name, media_type='application/octet-stream')
            return giveFailure(f'file <{file_name}> not found',payload['user_id'],role_access_status)
        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except KeyError as ke:
        logging.info(traceback.print_exc())
        return giveFailure(f"Missing key {ke}",0,0)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure(f"Invalid Credentials",0,0)


logger.info("program_started")


@app.post('/getResearchMandals')
async def get_research_mandals(payload: dict,conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    payload['table_name'] = 'get_research_mandalas_view'
    return await runInTryCatch(
        conn = conn,
        payload=payload,
        fname='get_research_mandals',
        isPaginationRequired=True,
        whereinquery=True,
        formatData=True,
        isdeleted=True
    )

@app.post('/getReportOrderInvoice')
async def get_report_order_invoice(payload: dict,conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    payload['filters'].append(['invoicedate','between',[payload['startdate'],payload['enddate']],'Date'])
    payload['table_name'] = 'orderinvoicelistview'
    return await runInTryCatch(
        conn = conn,
        payload=payload,
        fname='get_report_order_invoice',
        isPaginationRequired=True,
        whereinquery=True,
        formatData=True,
        isdeleted=True
    )

@app.post('/addResearchMandals')
async def add_research_mandals(payload: dict,conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = """INSERT INTO banksandbranches (name,typeid,emailid,phoneno,
                    suburb,city,state,country,website,email,email2,
                     contactname1,contactname2,phoneno1,phoneno2,dated
                    createdby,isdeleted,excludefrommailinglist) VALUES (%s,
                    %s,%s,%s,%s,%s,%s,%s,%s,%s,
                    %s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id"""
                msg = logMessage(cursor,query,[
                    payload['name'],
                    payload['typeid'],
                    payload['emailid'],
                    payload['phoneno'],
                    payload['suburb'],
                    payload['city'],
                    payload['state'],
                    payload['country'],
                    payload['website'],
                    payload['email1'],
                    payload['email2'],
                    payload['contactname1'],
                    payload['contactname2'],
                    payload['phoneno1'],
                    payload['phoneno2'],
                    givenowtime(),
                    payload['user_id'],
                    False,
                    payload['excludefrommailinglist']
                ])
                id = cursor.fetchone()[0]
                logging.info(msg)
                conn[0].commit()
                return giveSuccess(payload['user_id'],role_access_status,{"Inserted Mandala":id})
        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except KeyError as ke:
        logging.info(traceback.print_exc())
        return giveFailure(f"Missing key {ke}",0,0)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure(f"Invalid Credentials",0,0)
    
@app.post('/editResearchMandals')
async def edit_research_mandals(payload: dict,conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = """UPDATE mandalas SET name=%s,typeid=%s,emailid=%s,phoneno=%s,
                    suburb=%s,city=%s,state=%s,country=%s,website=%s,email1=%s,email2=%s,
                     contactname1=%s,contactname2=%s,phoneno1=%s,phoneno2=%s,dated=%s
                    createdby=%s,isdeleted=%s,excludefrommailinglist=%s WHERE id=%s"""
                msg = logMessage(cursor,query,[
                    payload['name'],
                    payload['typeid'],
                    payload['emailid'],
                    payload['phoneno'],
                    payload['suburb'],
                    payload['city'],
                    payload['state'],
                    payload['country'],
                    payload['website'],
                    payload['email1'],
                    payload['email2'],
                    payload['contactname1'],
                    payload['contactname2'],
                    payload['phoneno1'],
                    payload['phoneno2'],
                    givenowtime(),
                    payload['user_id'],
                    False,
                    payload['excludefrommailinglist'],
                    payload['id']
                ])
                logging.info(msg)
                conn[0].commit()
                return giveSuccess(payload['user_id'],role_access_status,{"Edited Mandala":payload['id']})
        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except KeyError as ke:
        logging.info(traceback.print_exc())
        return giveFailure(f"Missing key {ke}",0,0)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure(f"Invalid Credentials",0,0)

@app.post('/deleteResearchMandals')
async def delete_research_mandals(payload: dict,conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = """UPDATE mandalas SET isdeleted=true WHERE id=%s AND isdeleted=false"""
                msg = logMessage(cursor,query,[
                    payload['id']
                ])
                logging.info(msg)
                conn[0].commit()
                return giveSuccess(payload['user_id'],role_access_status,{"Deleted Mandala":payload['id']})
        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except KeyError as ke:
        logging.info(traceback.print_exc())
        return giveFailure(f"Missing key {ke}",0,0)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure(f"Invalid Credentials",0,0)

@app.post('/getResearchArchitect')
async def get_research_architect(payload: dict,conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    payload['table_name'] = 'get_research_architect_view'
    return await runInTryCatch(
        conn = conn,
        payload=payload,
        fname='get_research_architech',
        isPaginationRequired=True,
        whereinquery=True,
        formatData=True,
        isdeleted=True
    )

@app.post("/addResearchArchitect")
async def add_research_architect(payload:dict,conn:psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = """INSERT INTO architech (name,emailid,phoneno,
                    project,societyname,dated,createdby,isdeleted,suburb,city,
                     state,country,excludefrommailinglist) VALUES (
                    %s,%s,%s,%s,%s,%s,%s,%s,%s,
                    %s,%s,%s,%s) RETURNING id"""
                msg = logMessage(cursor,query,[
                    payload['name'],
                    payload['emailid'],
                    payload['phoneno'],
                    payload['project'],
                    payload['societyname'],
                    givenowtime(),
                    payload['user_id'],
                    False,
                    payload['suburb'],
                    payload['city'],
                    payload['state'],
                    payload['country'],
                    payload['excludefrommailinglist']
                ])
                id = cursor.fetchone()[0]
                logging.info(msg)
                conn[0].commit()
                return giveSuccess(payload['user_id'],role_access_status,{"Inserted Architect":id})
        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except KeyError as ke:
        logging.info(traceback.print_exc())
        return giveFailure(f"Missing key {ke}",0,0)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure(f"Invalid Credentials",0,0)

@app.post('/editResearchArchitect')
async def edit_research_architect(payload:dict,conn:psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = """UPDATE banksandbranches SET name=%s,emailid=%s,phoneno=%s,
                    project=%s,societyname=%s,dated=%s,createdby=%s,isdeleted=%s,suburb=%s,city=%s,
                     state=%s,country=%s,excludefrommailinglist=%s WHERE id=%s"""
                msg = logMessage(cursor,query,[
                    payload['name'],
                    payload['emailid'],
                    payload['phoneno'],
                    payload['project'],
                    payload['societyname'],
                    givenowtime(),
                    payload['user_id'],
                    False,
                    payload['suburb'],
                    payload['city'],
                    payload['state'],
                    payload['country'],
                    payload['excludefrommailinglist'],
                    payload["id"]
                ])
                logging.info(msg)
                conn[0].commit()
                return giveSuccess(payload['user_id'],role_access_status,{"Edited Architect":payload['id']})
        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except KeyError as ke:
        logging.info(traceback.print_exc())
        return giveFailure(f"Missing key {ke}",0,0)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure(f"Invalid Credentials",0,0)

@app.post('/deleteResearchArchitect')
async def delete_research_architect(payload:dict,conn:psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = """UPDATE banksandbranches SET isdeleted=true WHERE id=%s AND isdeleted=False"""
                msg = logMessage(cursor,query,[
                    payload["id"]
                ])
                logging.info(msg)
                conn[0].commit()
                return giveSuccess(payload['user_id'],role_access_status,{"Edited Architect":payload['id']})
        else:
            return giveFailure('Access Denied',payload['user_id'],role_access_status)
    except KeyError as ke:
        logging.info(traceback.print_exc())
        return giveFailure(f"Missing key {ke}",0,0)
    except Exception as e:
        logging.info(traceback.print_exc())
        return giveFailure(f"Invalid Credentials",0,0)

def send_email(subject, body, to_email):
    # SMTP server configuration
    smtp_server = 'smtpout.secureserver.net'  # Example: 'smtp.gmail.com'
    smtp_port = 587  # For SSL, use 465; for TLS/StartTLS, use 587
    smtp_username = 'admin@mycuraservices.com'
    smtp_password = 'Cura@123456'

    # Create MIME message
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = to_email
    msg['Subject'] = subject

    # Add body to the email
    msg.attach(MIMEText(body, 'plain'))

    # Connect to the SMTP server
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Enable security
        server.login(smtp_username, smtp_password)
        text = msg.as_string()
        server.sendmail(smtp_username, to_email, text)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

def create_token(payload: dict,expires:timedelta|None = None):
    key = secrets.token_hex(4)
    to_encode = payload.copy()
    if expires:
        expire = datetime.datetime.now(timezone.utc) + expires
    else:
        expire = datetime.datetime.now(timezone.utc) + timedelta(minutes=10)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,key=key,algorithm=ALG)
    return encoded_jwt,key

async def gentoken(payload:dict,conn: psycopg2.extensions.connection = Depends(get_db_connection),email=False):
    try:
        with conn[0].cursor() as cursor:
            access_token_expires = timedelta(minutes=100)
            access_token,key = create_token(payload,access_token_expires)
            cursor.execute(f"""INSERT INTO tokens (token,key,active) VALUES ('{access_token}','{key}',true)""")
            conn[0].commit()
            return access_token
    except Exception as e:
        raise HTTPException(status_code=401,detail="Invalid Payload")

@app.post("/token")
async def login_for_token(payload:dict,conn: psycopg2.extensions.connection = Depends(get_db_connection),):
    try:
        with conn[0].cursor() as cursor:
            cursor.execute("SELECT email1 FROM usertable WHERE username = %s",(payload["username"],))
            email = cursor.fetchone()

            if email:
                access_token_expires = timedelta(minutes=100)
                access_token,key = create_token(payload,access_token_expires)
                cursor.execute(f"""INSERT INTO tokens (token,key,active) VALUES ('{access_token}','{key}',true)""")
                if email:
                    send_email("Reset Password",f"""Reset password at 20.197.13.140:5173/reset/{access_token}""",email[0])
                    logging.info(f"""Reset password at 20.197.13.140:5173/reset/{access_token}""")
                    # print(access_token)
                    conn[0].commit()
                    return giveSuccess(0,0,email[0])
                return access_token
            else:
                raise HTTPException(status_code=401,detail="No username")
    except Exception as e:
        raise HTTPException(status_code=401,detail="Invalid Payload")

@app.post("/reset")
async def getdata(payload:dict,request : Request,conn: psycopg2.extensions.connection = Depends(get_db_connection),):
    try:
        #header derive
        headers = request.headers
        logging.info(headers)
        if 'authorization' not in headers:
            return giveFailure("No token from user",0,0)
        token = headers['authorization'][7:]
        with conn[0].cursor() as cursor:
            query = 'SELECT key FROM tokens where token = %s'
            message = logMessage(cursor,query,[token])
            
            logging.info(message)
            key = cursor.fetchone()[0]
            # logging.info(type(key))
        username = jwt.decode(token,key,algorithms=ALG)['username']
        try:
            with conn[0].cursor() as cursor:
                #hashing to be done here, using bcrypt for now.
                newp = bcrypt.hashpw(payload['password'].encode('ascii'),bcrypt.gensalt()).decode('utf-8')
                logging.info(newp)
                #update part
                query = 'UPDATE usertable SET password = %s WHERE username = %s'
                # msg = logMessage(cursor,query,[newp,payload['username']])
                #logging.info(msg
                logging.info(logMessage(cursor,query,[newp,username]))
                logging.info(cursor.statusmessage)
            conn[0].commit()
            return giveSuccess(None,None,{"Change PW for":username})
        except Exception as e:
            logging.info(traceback.print_exc())
            raise HTTPException(status_code=401,detail="Invalid Payload")
    except jwt.exceptions.ExpiredSignatureError as e:
        logging.info(traceback.print_exc())
        raise HTTPException(status_code=401,detail="Expired Token")
    except Exception as e:
        logging.info(traceback.print_exc())
        raise HTTPException(status_code=403,detail = "Invalid Credentials")


@app.post('/getReportClientReceipt')
async def report_client_receipt(payload: dict,conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    payload['table_name'] = 'clientreceiptlistview'
    payload['filters'].append(['recddate','between',[payload['startdate'],payload['enddate']],'Date'])

    return await runInTryCatch(
        conn = conn,
        fname = 'report_client_receipt',
        payload=payload,
        isPaginationRequired=True,
        whereinquery=True,
        isdeleted=True,
        formatData=True
    )

@app.post('/getReportVendorInvoice')
async def report_vendor_invoice(payload:dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    payload['table_name'] = 'ordervendorestimatelistview'
    payload['filters'].append(['invoicedate','between',[payload['startdate'],payload['enddate']],'Date'])
    return await runInTryCatch(
        conn = conn,
        fname = 'report_client_receipt',
        payload=payload,
        isPaginationRequired=True,
        whereinquery=True,
        isdeleted=True,
        formatData=True
    )

@app.post('/getItemIDBySearch')
async def get_client_id_by_search(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    query = f'SELECT {",".join(payload["rows"])} FROM {payload["table_name"]} WHERE id::text LIKE \'%{payload["id"]}%\''
    
    return await runInTryCatch(
        conn = conn,
        payload=payload,
        fname = 'get_item_id_by_search',
        query = query,
        isPaginationRequired=True,
        formatData=True,
        isdeleted=True
    )

@app.post('/reportMonthlyMarginLOBReceiptPayments')
async def report_monthly_margin_lob_receipt_payments(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):

    payload['table_name'] = 'datewiselobserviceview'
    payload['filters'].append(['date','between',[payload['startdate'],payload['enddate']],'Date'])
    logging.info("Here")
    logging.info('lobName' in payload and payload['lobName'] != 'all')
    if 'lobName' in payload and payload['lobName'] != 'all':
        payload['filters'].append(['lobname','equalTo',payload['lobName'].lower(),"String"])
    logging.info(payload['filters'])
    data =  await runInTryCatch(
        conn = conn,
        fname = 'report_monthly_margin_lob_receipt_payments',
        payload=payload,
        isPaginationRequired=True,
        whereinquery=False,
        formatData=True
    )
    total = {'totalreceipt':0,'totalpayment':0,'total_diff':0}
    payload['pg_no'] = 0
    payload['pg_size'] = 0
    forSum =  await runInTryCatch(
        conn = conn,
        fname = 'report_monthly_margin_lob_receipt_payments',
        payload=payload,
        isPaginationRequired=True,
        whereinquery=False,
        formatData=True
    )
    for i in forSum['data']:
        total['totalreceipt'] += i['orderreceiptamount']
        total['totalpayment'] += i['paymentamount']
        total['total_diff'] += i['diff']
    data['total'] = total
    logging.info(total)
    # logging.info(data)

    return data

@app.post('/reportMonthlyMarginEntityReceiptPayments')
async def report_monthly_margin_entity_receipt_payments(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    payload['table_name'] = 'datewiselobentityview'
    payload['filters'].append(['date','between',[payload['startdate'],payload['enddate']],'Date'])
    if 'entityName' in payload:
        payload['filters'].append(['entityname','equalTo',payload['entityName'],"String"])
    
    data = await runInTryCatch(
        conn = conn,
        fname = 'report_monthly_margin_entity_receipt_payments',
        payload=payload,
        isPaginationRequired=True,
        whereinquery=False,
        formatData=True
    )
    query = f'''SELECT SUM(orderreceiptamount) AS totalreceipt,SUM(paymentamount) AS totalpayment,SUM(orderreceiptamount - paymentamount)
      AS total_diff FROM datewiselobentityview'''
    payload['sort_by'] = []
    payload['filters'] = [['date','between',[payload['startdate'],payload['enddate']],'Date'],['entityname','equalTo',payload['entityName'].lower(),"String"]]
    payload['search_key'] = ''
    payload['pg_no'] = 1
    payload['pg_size'] = 15
    res = await runInTryCatch(
        conn = conn,
        fname='total_calc',
        query = query,
        payload=payload,
        whereinquery=False,
        formatData=True,
        isdeleted=False,
        isPaginationRequired=True
    )
    if not res['data']:
        data['total'] = res['data']
    data['total'] = res['data'][0]
    return data

@app.post('/reportMonthlyMarginLOBReceiptPaymentsConsolidated')
async def report_monthly_margin_lob_receipt_payments_consolidated(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    payload['table_name'] = 'datewiselobserviceview'
    payload['static'] = True
    query = """ select zz.lobname, zz.total_orderreceiptamount, zz.total_paymentamount, zz.total_diff from
(SELECT
    lobname,
    SUM(orderreceiptamount) AS total_orderreceiptamount,
    SUM(paymentamount) AS total_paymentamount,
    SUM(orderreceiptamount - paymentamount) AS total_diff,
    max(date) AS date
        FROM     datewiselobserviceview group by lobname
) as zz"""
    payload['filters'].append(['date','between',[payload['startdate'],payload['enddate']],'Date'])
    if 'lobName' in payload and payload['lobName'] != 'all':
        payload['filters'].append(['lobname','equalTo',payload['lobName'].lower(),"String"])
    data = await runInTryCatch(
        conn = conn,
        fname = 'report_monthly_margin_entity_receipt_payments',
        query=query,
        isPaginationRequired=True,
        payload=payload,
        whereinquery=False,
        formatData=True
    )
    query = """ select zz.lobname, zz.total_orderreceiptamount, zz.total_paymentamount, zz.total_diff from
(SELECT
    lobname,
    SUM(orderreceiptamount) AS total_orderreceiptamount,
    SUM(paymentamount) AS total_paymentamount,
    SUM(orderreceiptamount - paymentamount) AS total_diff,
    max(date) AS date
        FROM     datewiselobserviceview group by lobname
) as zz"""
    payload['pg_size'] = 0
    payload['pg_no'] = 0
    payload['filters'].append(['date','between',[payload['startdate'],payload['enddate']],'Date'])
    if 'lobName' in payload and payload['lobName'] != 'all':
        payload['filters'].append(['lobname','equalTo',payload['lobName'].lower(),"String"])
    dt = await runInTryCatch(
        conn = conn,
        fname = 'report_monthly_margin_entity_receipt_payments',
        query=query,
        isPaginationRequired=True,
        payload=payload,
        whereinquery=False,
        formatData=True
    )
    total = {}
    total_orderreceiptamount = 0
    total_paymentamount = 0
    total_diff = 0
    for i in dt['data']:
        total_orderreceiptamount += i['total_orderreceiptamount']
        total_paymentamount += i['total_paymentamount']
        total_diff += i['total_diff']
    total['total_orderreceiptamount'] = total_orderreceiptamount
    total['total_paymentamount'] = total_paymentamount
    total['total_diff'] = total_diff
#     query = f'''SELECT SUM(zz.total_orderreceiptamount) AS total_orderreceiptamount,SUM(zz.total_paymentamount) AS total_paymentamount,SUM(zz.total_diff) as total_diff,max(zz.date) FROM (SELECT
#     lobname,
#     SUM(orderreceiptamount) AS total_orderreceiptamount,
#     SUM(paymentamount) AS total_paymentamount,
#     SUM(orderreceiptamount - paymentamount) AS total_diff,
#     max(date) AS date
#         FROM     datewiselobserviceview group by lobname
# ) as zz '''
#     payload['pg_size'] = 0
#     payload['pg_no'] = 0
#     res = await runInTryCatch(
#         conn = conn,
#         fname='total_calc',
#         query = query,
#         payload=payload,
#         whereinquery=False,
#         formatData=True,
#         isdeleted=False,
#         isPaginationRequired=True
#     )
    # if not res['data']:
    #     data['total'] = res['data']
    #     return data
    data['total'] = total
    return data
    
@app.post('/reportPMABillingListView')
async def report_PMA_Billing_List_View(payload:dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    payload['table_name'] = 'PMABillingListView'
    return await runInTryCatch(
        conn = conn,
        fname = 'report_pma_billing_list_view',
        payload=payload,
        whereinquery=True,
        isdeleted=True,
        formatData=True,
        isPaginationRequired=True
    )

@app.post('/reportPMABillingTrendView')
async def report_PMA_Billing_Trend_View(payload:dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    payload['table_name'] = 'PMABillingTrendView'
    payload['filters'].append(["fy","equalTo",payload['fy'],"String"])
    data = await runInTryCatch(
        conn = conn,
        fname = 'report_pma_billing_trend_view',
        payload=payload,
        whereinquery=False,
        isdeleted=False,
        formatData=True,
        isPaginationRequired=True
    )
    query = f"""SELECT
    SUM(COALESCE(jan, 0)) AS jan_sum,
    SUM(COALESCE(feb, 0)) AS feb_sum,
    SUM(COALESCE(mar, 0)) AS mar_sum,
    SUM(COALESCE(apr, 0)) AS apr_sum,
    SUM(COALESCE(may, 0)) AS may_sum,
    SUM(COALESCE(jun, 0)) AS jun_sum,
    SUM(COALESCE(jul, 0)) AS jul_sum,
    SUM(COALESCE(aug, 0)) AS aug_sum,
    SUM(COALESCE(sep, 0)) AS sep_sum,
    SUM(COALESCE(oct, 0)) AS oct_sum,
    SUM(COALESCE(nov, 0)) AS nov_sum,
    SUM(COALESCE(dec, 0)) AS dec_sum
FROM pmabillingtrendview
WHERE fy = '{payload['fy']}';"""
    with conn[0].cursor() as cursor:
        msg = logMessage(cursor,query)
        logging.info(msg)
        colnames = [col[0] for col in cursor.description]
        data['total'] = dict(zip(colnames, cursor.fetchone()))
    return data

@app.post('/reportPMAClientPortalReport')
async def report_PMA_Client_Portal_Report(payload:dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    payload['table_name'] = 'PMAClientPortalReport'
    return await runInTryCatch(
        conn = conn,
        fname = 'report_pma_client_portal',
        payload=payload,
        whereinquery=False,
        isdeleted=False,
        formatData=True,
        isPaginationRequired=True
    )

@app.post('/reportPMAClientReceivable')
async def report_PMA_Client_Receivables(payload:dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    payload['table_name'] = 'rpt_pmaclient_receivables'
    data =  await runInTryCatch(
        conn = conn,
        fname = 'report_pma_client_receivable',
        payload=payload,
        whereinquery=False,
        isdeleted=False,
        formatData=True,
        isPaginationRequired=True
    )
    payload['pg_size'] = 0
    payload['pg_no'] = 0
    dt = await runInTryCatch(
        conn = conn,
        fname = 'rpt_pma_client_receivables',
        payload=payload,
        isPaginationRequired=True,
        formatData=True,
        whereinquery=False,
        isdeleted=False
    )
    total = {'total_amount':0}
    if dt['data']:
        for i in dt['data']:
            total['total_amount'] += i['amount']
    data['total'] = total
    return data

@app.post('/getResearchColleges')
async def get_research_colleges(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    payload['table_name'] = 'get_research_colleges_view'
    return await runInTryCatch(
        conn = conn,
        fname = 'get_research_colleges',
        payload=payload,
        isPaginationRequired=True,
        whereinquery=True,
        formatData=True,
        isdeleted=True
    )
        
@app.post('/addResearchColleges')
async def add_research_colleges(payload: dict, conn : psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                payload['dated'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                query = 'INSERT INTO colleges (name,typeid,emailid,phoneno,dated,createdby,isdeleted,suburb,city,state,country,website,email1,email2,contactname1,contactname2,phoneno1,phoneno2,excludefrommailinglist) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id'
                msg =logMessage(cursor,query,(payload['name'],payload['typeid'],payload['emailid'],payload['phoneno'],givenowtime(),payload['user_id'],False,payload['suburb'],payload['city'],payload['state'],payload['country'],payload['website'],payload['email1'],payload['email2'],payload['contactname1'],payload['contactname2'],payload['phoneno1'],payload['phoneno2'],payload['excludefrommailinglist']))
                logging.info(msg)
                id = cursor.fetchone()[0]
                conn[0].commit()
            data = {
                "added_data":id
            }
            return giveSuccess(payload['user_id'],role_access_status,data)
        else:
            giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        print(traceback.print_exc())
        giveFailure("Invalid Credentials",payload['user_id'],0)

@app.post('/editResearchColleges')
async def edit_research_prospect(payload: dict, conn : psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'edit_research_prospect: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                payload['dated'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                query = 'UPDATE colleges SET name=%s,typeid=%s,emailid=%s,phoneno=%s,dated=%s,createdby=%s,isdeleted=%s,suburb=%s,city=%s,state=%s,country=%s,website=%s,email1=%s,email2=%s,contactname1=%s,contactname2=%s,phoneno1=%s,phoneno2=%s,excludefrommailinglist=%s WHERE id=%s'
                msg =logMessage(cursor,query,(payload['name'],payload['typeid'],payload['emailid'],payload['phoneno'],givenowtime(),payload['user_id'],False,payload['suburb'],payload['city'],payload['state'],payload['country'],payload['website'],payload['email1'],payload['email2'],payload['contactname1'],payload['contactname2'],payload['phoneno1'],payload['phoneno2'],payload['excludefrommailinglist'],payload['id']))
                logging.info(msg)
                if cursor.statusmessage == "UPDATE 0":
                    return giveFailure("No College available",payload['user_id'],role_access_status)
                conn[0].commit()
            data = {
                "edited_data":payload['id']
            }
            return giveSuccess(payload['user_id'],role_access_status,data)
        else:
            giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        print(traceback.print_exc())
        giveFailure("Invalid Credentials",payload['user_id'],0)

@app.post('/deleteResearchColleges')
async def delete_research_colleges(payload: dict, conn : psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'delete_colleges: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'UPDATE colleges SET isdeleted=true WHERE id=%s AND isdeleted=false'
                msg = logMessage(cursor,query,(payload['id'],))
                logging.info(msg)
                if cursor.statusmessage == "UPDATE 0":
                    return giveFailure("No College available",payload['user_id'],role_access_status)
            conn[0].commit()
            data = {
                "deleted_data":payload['id']
            }
            return giveSuccess(payload['user_id'],role_access_status,data)
        else:
            giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        print(traceback.print_exc())
        giveFailure("Invalid Credentials",payload['user_id'],0)

@app.post('/getResearchOwners')
async def get_research_colleges(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    payload['table_name'] = 'owners'
    return await runInTryCatch(
        conn = conn,
        fname = 'get_research_owners',
        payload=payload,
        isPaginationRequired=True,
        whereinquery=True,
        formatData=True,
        isdeleted=True
    )
        
@app.post('/addResearchOwners')
async def add_research_colleges(payload: dict, conn : psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                payload['dated'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                query = 'INSERT INTO owners (societyname, name, propertytaxno, address, phoneno, emailid, corporation, dated, createdby, isdeleted, suburb, city, state, country, isexcludedmailinglist, propertydetails, propertyfor, phoneno1, phoneno2, source) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id'
                msg =logMessage(cursor,query,(payload['societyname'],payload['name'],payload['propertytaxno'],payload['address'],payload['phoneno'],payload['emailid'],payload['corporation'],givenowtime(),payload['user_id'],False,payload['suburb'],payload['city'],payload['state'],payload['country'],payload['isexcludedmailinglist'],payload['propertydetails'],payload['propertyfor'],payload['phoneno1'],payload['phoneno2'],payload['source']))
                logging.info(msg)
                id = cursor.fetchone()[0]
                conn[0].commit()
            data = {
                "added_data":id
            }
            return giveSuccess(payload['user_id'],role_access_status,data)
        else:
            giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        print(traceback.print_exc())
        giveFailure("Invalid Credentials",payload['user_id'],0)

@app.post('/editResearchOwners')
async def edit_research_prospect(payload: dict, conn : psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'edit_research_prospect: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                payload['dated'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                query = 'UPDATE owners SET societyname = %s, name = %s, propertytaxno = %s, address = %s, phoneno = %s, emailid = %s, corporation = %s, dated = %s, createdby = %s, isdeleted = %s, suburb = %s, city = %s, state = %s, country = %s, isexcludedmailinglist = %s, propertydetails = %s, propertyfor = %s, phoneno1 = %s, phoneno2 = %s, source = %s WHERE id = %s;'
                msg =logMessage(cursor,query,(payload['societyname'],payload['name'],payload['propertytaxno'],payload['address'],payload['phoneno'],payload['emailid'],payload['corporation'],givenowtime(),payload['user_id'],False,payload['suburb'],payload['city'],payload['state'],payload['country'],payload['isexcludedmailinglist'],payload['propertydetails'],payload['propertyfor'],payload['phoneno1'],payload['phoneno2'],payload['source'],payload['id']))
                logging.info(msg)
                if cursor.statusmessage == "UPDATE 0":
                    return giveFailure("No owners available",payload['user_id'],role_access_status)
                conn[0].commit()
            data = {
                "edited_data":payload['id']
            }
            return giveSuccess(payload['user_id'],role_access_status,data)
        else:
            giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        print(traceback.print_exc())
        giveFailure("Invalid Credentials",payload['user_id'],0)

@app.post('/deleteResearchOwners')
async def delete_research_colleges(payload: dict, conn : psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'delete_colleges: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'UPDATE owners SET isdeleted=true WHERE id=%s AND isdeleted=false'
                msg = logMessage(cursor,query,(payload['id'],))
                logging.info(msg)
                if cursor.statusmessage == "UPDATE 0":
                    return giveFailure("No owners available",payload['user_id'],role_access_status)
            conn[0].commit()
            data = {
                "deleted_data":payload['id']
            }
            return giveSuccess(payload['user_id'],role_access_status,data)
        else:
            giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        print(traceback.print_exc())
        giveFailure("Invalid Credentials",payload['user_id'],0)


logger.info("program_started")
