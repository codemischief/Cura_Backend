import psycopg2
import bcrypt
from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
import traceback
import datetime
# import os
# from dotenv import load_dotenv,find_Dotenv
logger = logging.getLogger(__name__)

# PostgreSQL database URL
#todo : need to source user, password and ip port from variables
DATABASE_URL = "postgresql://postgres:cura123@192.168.10.133:5432/cura_db"

def getdata(conn: psycopg2.extensions.connection):
    return [
        usernames(conn),
        paymentmode(conn),
        entity(conn),
        paymentfor(conn)
    ]



def usernames(conn : psycopg2.extensions.connection):
    try:
        with conn.cursor() as cursor:
            query = 'SELECT firstname,lastname,id FROM usertable'
            cursor.execute(query)
            data = cursor.fetchall()
        if data:
            res = {}
            for i in data:
                res[i[2]] = f'{i[0]} {i[1]}'
        return res
    except Exception as e:
        return None

def paymentfor(conn: psycopg2.extensions.connection):
    try:
        with conn.cursor() as cursor:
            query = 'SELECT DISTINCT id,name from payment_for'
            cursor.execute(query)
            data = cursor.fetchall()
        res = {}
        for i in data:
            res[i[0]] = i[1]
        print(res)
        return res
    except Exception as e:
        print(traceback.print_exc())
        print(f"Error is {e}")
        return None

def paymentmode(conn: psycopg2.extensions.connection):
    try:
        with conn.cursor() as cursor:
            query = 'SELECT DISTINCT id,name from mode_of_payment'
            cursor.execute(query)
            data = cursor.fetchall()
        res = {}
        for i in data:
            res[i[0]] = i[1]
        print(res)
        return res
    except Exception as e:
        print(traceback.print_exc())
        print(f"Error is {e}")
        return None
def entity(conn):
    try:
        with conn.cursor() as cursor:
            query = 'SELECT DISTINCT id,name from entity'
            cursor.execute(query)
            data = cursor.fetchall()
        res = {}
        for i in data:
            res[i[0]] = i[1]
        print(res)
        return res
    except Exception as e:
        print(traceback.print_exc())
        print(f"Error is {e}")
        return None

def roles(conn):
    try:
        with conn.cursor() as cursor:
            query = 'SELECT DISTINCT id,name from role'
            cursor.execute(query)
            data = cursor.fetchall()
        res = {}
        for i in data:
            res[i[0]] = i[1]
        print(res)
        return res
    except Exception as e:
        print(traceback.print_exc())
        print(f"Error is {e}")
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
                      search_key = None):
    try:
        # Base query
        query_frontend = False
        if query is None:
            query = f"SELECT distinct {','.join(required_columns)} FROM {table_name}"
            query_frontend = True
        # Adding filters
        where_clauses = []
        for column, filter_type, value in (filters or []):
            if value != '':
                if filter_type == 'startsWith':
                    where_clauses.append(f"{column} LIKE '{value}%'")
                elif filter_type == 'endsWith':
                    where_clauses.append(f"{column} LIKE '%{value}'")
                elif filter_type == 'contains':
                    where_clauses.append(f"{column} LIKE '%{value}%'")
                elif filter_type == 'exactMatch':
                    where_clauses.append(f"{column} = '{value}'")
                elif filter_type == 'isNull':
                    where_clauses.append(f"{column} = ''")
                elif filter_type == 'isNotNull':
                    where_clauses.append(f"{column} != ''")
        # handle where clause and sorting
        if where_clauses and query_frontend:
            query += " WHERE " + " AND ".join(where_clauses)
        elif where_clauses and not query_frontend:
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

        logging.info(f'Prepared final query [{query}]')
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
            rows = search_results[start_index:end_index]

        return {'data':rows, 'total_count' : total_count, 'message':'success', 'colnames':colnames}
    except Exception as e:
        logging.exception(traceback.print_exc())
        msg = str(e).replace("\n","")
        return {'data':None, 'message':f'exception due to <{msg}>'}


def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    try:
        cursor = conn.cursor()
        yield conn, cursor
    finally:
        cursor.close()
        conn.close()

def get_countries_from_id(conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        with conn[0].cursor() as cursor:
            query = 'SELECT * FROM country'
            cursor.execute(query)
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
            cursor.execute(query)
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
            query = 'SELECT id,city,state,countryid FROM cities'
            cursor.execute(query)
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
    logging.info(f'getCredentials: received payload <{payload}>')
    try:
        with conn[0].cursor() as cursor:
            query = 'SELECT password,id,roleid FROM usertable where username = %s'
            query2 = "SELECT EXISTS (SELECT 1 FROM companykey WHERE companycode = %s)"
            cursor.execute(query, (payload['username'],))
            userdata = cursor.fetchone()
            cursor.execute(query2, (str(payload['company_key']),))
            company_key = cursor.fetchone()
            if userdata is None:
                return giveFailure("User does not exist")
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
                    "data": {}
                }
                return resp
            else:
                return {
                    "result": "error",
                    "message": "Invalid Credentials",
                }
    except KeyError as ke:
        return {
            "result": "error",
            "message": f"key {ke} not found",
        }
    except Exception as e:
        logging.exception(traceback.print_exc())
        return {
            "result" : "Error",
            "message":"Wrong input",
            "data":{}
            }

def giveSuccess(uid,rid,data=[], total_count=None):
    final_data =  {
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
    return {
        "result":"error",
        "message":msg,
        "user_id":uid,
        "role_id":rid,
        "data":data
    }

def check_role_access(conn, payload: dict):
    if 'user_id' in payload:
        identifier_id = payload['user_id']
        identifier_name = None
    elif 'username' in payload:
        identifier_name = payload['username']
        identifier_id = None
    else:
        raise HTTPException(status_code=400, detail="Please provide either 'user_id' or 'username' in the payload")
    cursor = conn[0].cursor()
    try:
        if identifier_id:
            cursor.execute("SELECT roleid FROM usertable WHERE id = %s", (identifier_id,))
        elif identifier_name:
            cursor.execute("SELECT roleid FROM usertable WHERE username = %s", (identifier_name,))
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
async def get_role_id(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'getRoleID: received payload <{payload}>')
    role_id = check_role_access(conn, payload)
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
def getCountries(payload : dict,conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'getCountries: received payload <{payload}>')
    #todo: need to add pagination and filteration arrangement here
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status is not None:
            if role_access_status == 1:
                with conn[0].cursor() as cursor:
                    #query = "SELECT * FROM country ORDER BY id;"
                    data = filterAndPaginate(DATABASE_URL, payload['rows'], 'country', payload['filters'],
                                             payload['sort_by'], payload['order'], payload["pg_no"], payload["pg_size"],
                                             search_key = payload['search_key'] if 'search_key' in payload else None)
                    total_count = data['total_count']
                return giveSuccess(payload['user_id'],role_access_status,data, total_count=total_count)
            else:
                return giveFailure("Access Denied",payload["user_id"],role_access_status)
        else:
            return giveFailure("User does not exist",payload["user_id"],role_access_status)

    except Exception as e:
        logging.exception(traceback.print_exc())
        return giveFailure(f"error {e} found",payload['user_id'],0)

@app.post('/addCountry')
async def add_country(payload:dict,conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'addCountry: received payload <{payload}>')
    try:
        with conn[0].cursor() as cursor:
            role_access_status = check_role_access(conn,payload)
            if role_access_status == 1:
            # Insert new country data into the database
                query_insert = 'INSERT INTO country (id,name) VALUES (%s,%s)'
                cursor.execute(query_insert, (payload['country_id'], payload['country_name']))

            # Commit the transaction
                conn[0].commit()
                data = {"added":payload['country_name']}
                return giveSuccess(payload['user_id'],role_access_status,data)
            elif role_access_status!=1:
                return giveFailure("Access Denied",payload['user_id'],role_access_status)
            else:
                return giveFailure("Invalid Credentials",payload['user_id'],role_access_status)
    except KeyError as ke:
        return giveFailure(f"key {ke} not found",payload['user_id'],0)
    except Exception as e:
        return giveFailure(f"Error {e}",payload["user_id"],0)
    
def checkcountry(payload: str,conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        with conn[0].cursor() as cursor:
            query_find = "SELECT EXISTS (SELECT 1 FROM country WHERE name=%s)"
            cursor.execute(query_find, (payload,))
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
    logging.info(f'editCountry: received payload <{payload}>')
    try:
        # Check user role
        role_access_status = check_role_access(conn,payload)

        if role_access_status == 1 and checkcountry(payload['old_country_name'],conn):
            with conn[0].cursor() as cursor:
                # Update country name in the database
                query_update = "UPDATE country SET name = %s WHERE name = %s"
                cursor.execute(query_update, (payload['new_country_name'], payload['old_country_name']))

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
    logging.info(f'deleteCountry: received payload <{payload}>')
    try:
        with conn[0].cursor() as cursor:
            role_access_status = check_role_access(conn,payload)
            if role_access_status == 1 and checkcountry(payload['country_name'],conn):
            # Delete country data from the database
                query_delete = 'DELETE FROM country WHERE name = %s'
                cursor.execute(query_delete,(payload['country_name'],))
            # Commit the transaction
                conn[0].commit()
                data = {
                        "deleted":payload["country_name"]
                        }
                return giveSuccess(payload['user_id'],role_access_status,data)
            elif role_access_status!=1:
                return giveFailure("Invalid Credentials",payload['user_id'],role_access_status)

            elif not checkcountry(payload['name'],conn):
                return giveFailure("Invalid Credentials",payload['user_id'],role_access_status)

            else:
                return giveFailure("Invalid Credentials",payload['user_id'],role_access_status)

    except Exception as e:
        return giveFailure("Invalid Credentials",payload['user_id'],0)


@app.post('/addBuilderInfo')
async def add_builder_info(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'addBuilderInfo: received payload <{payload}>')
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
                    )
                '''
                cursor.execute(query, (
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
                    payload['dated'],
                    payload['createdby'],
                    payload['isdeleted']
                ))
                 # Commit the transaction
                conn[0].commit()
                
                # Get the ID of the last inserted row
                last_row_id = cursor.lastrowid
                data= {
                    "entered": payload["buildername"]
                }
            return giveSuccess(payload['user_id'],role_access_status,data,data)
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        logging.exception(traceback.print_exc())
        return giveFailure("Invalid Credentials",payload['user_id'],0)

#BUILDER UPDATED
@app.post('/getBuilderInfo')
def getBuilderInfo(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'getBuilderInfo: received payload <{payload}>')
    countries = get_countries_from_id(conn=conn)
    cities = get_city_from_id(conn=conn)
    try:
        role_access_status = check_role_access(conn, payload)

        if role_access_status == 1:  
            with conn[0].cursor() as cursor:
                query = "SELECT a.id,a.buildername,a.phone1,a.phone2,a.email1,a.email2,a.addressline1,a.addressline2,a.suburb,b.city,a.state,c.name as country,a.zip,a.website,a.comments,a.dated,a.createdby,a.isdeleted FROM builder a,cities b,country c WHERE a.city = b.id AND a.country = c.id ORDER BY id"
                data = filterAndPaginate(DATABASE_URL, payload['rows'], 'country', payload['filters'],
                                        payload['sort_by'], payload['order'], payload["pg_no"], payload["pg_size"],
                                        search_key = payload['search_key'] if 'search_key' in payload else None,query=query)

                colnames = data['colnames']
                
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
                return giveSuccess(payload['user_id'],role_access_status,data)
        else:
            return giveFailure("Access Denied",payload["user_id"],role_access_status)
    except Exception as e:
        logging.exception(traceback.print_exc())
        return giveFailure("Invalid Credentials",payload['user_id'],0)

@app.post("/editBuilder")
async def edit_builder(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'editBuilder: received payload <{payload}>')
    try:
        # Check user role
        role_access_status = check_role_access(conn, payload)

        with conn[0].cursor() as cursor:
            # Check if the builder exists
            query_check_builder = "SELECT EXISTS (SELECT 1 FROM builder WHERE id = %s)"
            cursor.execute(query_check_builder, (payload['builder_id'],))
            builder_exists = cursor.fetchone()[0]
            print(builder_exists)
        if role_access_status == 1 and builder_exists:
            with conn[0].cursor() as cursor:
                # Update builder information in the database
                query_update = """
                    UPDATE builder 
                    SET buildername = %s, phone1 = %s, phone2 = %s, email1 = %s, 
                    addressline1 = %s, addressline2 = %s, suburb = %s, city = %s, 
                    state = %s, country = %s, zip = %s, website = %s, comments = %s, 
                    dated = %s, createdby = %s, isdeleted = %s
                    WHERE id = %s
                """
                cursor.execute(query_update, (
                    payload['builder_name'],
                    payload['phone_1'],
                    payload['phone_2'],
                    payload['email1'],
                    payload['addressline1'],
                    payload['addressline2'],
                    payload['suburb'],
                    payload['city'],
                    payload['state'],
                    payload['country'],
                    payload['zip'],
                    payload['website'],
                    payload['comments'],
                    payload['dated'],
                    payload['created_by'],
                    payload['is_deleted'],
                    payload['builder_id']
                ))

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
        return giveFailure(f"key {ke} not found",payload['user_id'],0)
    except Exception as e:
        return giveFailure(str(e),payload['user_id'],0)

@app.post('/deleteBuilder')
async def deleteBuilder(payload:dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'deleteBuilder: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status==1:
            with conn[0].cursor() as cursor:
                query = 'SELECT distinct * FROM builder where id=%s'
                cursor.execute(query,(payload['builder_id'],))
                exists = cursor.fetchone()
                print(exists)
                if exists:
                    query = 'DELETE FROM builder where id = %s'
                    cursor.execute(query,(payload['builder_id'],))
                    conn[0].commit()
                    data = {
                        "deleted_user":payload['builder_id']
                        }
                    return giveSuccess(payload['user_id'],role_access_status,data)
                else:
                    return giveFailure("Invalid Credentials",payload['user_id'],0)

        else:
            return giveFailure("Access Denoed",payload['user_id'],0)

    except Exception as e:
        logging.exception(traceback.print_exc())
        return giveFailure("Invalid Credentials",payload['user_id'],0)

#STATES UPDATED
@app.post('/getStatesAdmin')
async def get_states_admin(payload:dict,conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'getStatesAdmin: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status==1:
            query = "SELECT DISTINCT  b.name as countryname, a.state, b.id as id FROM cities a,country b WHERE a.countryid=b.id"
            data = filterAndPaginate(DATABASE_URL, payload['rows'], None, payload['filters'], payload['sort_by'], payload['order'], payload["pg_no"], payload["pg_size"], query=query, search_key = payload['search_key'] if 'search_key' in payload else None)
            total_count = data['total_count']
            return giveSuccess(payload["user_id"],role_access_status,data['data'], total_count=total_count)
        else:
            return giveFailure("Invalid Credentials",payload['user_id'],role_access_status)
    except Exception as e:
        logging.exception(traceback.print_exc())
        return giveFailure("Invalid Credentials",payload['user_id'],0)

@app.post('/getStates')
async def get_states(payload : dict,conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'getStates: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn,payload)
        print(role_access_status)
        if role_access_status != 0:
            if role_access_status == 1:
                with conn[0].cursor() as cursor:
                    query = "SELECT DISTINCT id, state FROM cities WHERE countryid = %s"
                    cursor.execute(query,(payload['country_id'],))
                    #data = [i[0] for i in cursor.fetchall()]
                    data = cursor.fetchall()

                return giveSuccess(payload['user_id'],role_access_status,data)
            else:
                return giveFailure("Access denied",payload['user_id'],role_access_status)
        else:
            return giveFailure("User does not exist",payload['user_id'],role_access_status)
    except ValueError as ve:
        print(traceback.print_exc())
        return giveFailure(f"{ve} error found",payload["user_id"],0)
    except Exception as e:
        print(traceback.print_exc())
        return giveFailure(f"{e} error found",payload['user_id'],0)

@app.post('/getCities')
async def get_cities(payload : dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'getCities: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status==1:
            with conn[0].cursor() as cursor:
                query = "SELECT distinct id,city FROM cities where state=%s"
                cursor.execute(query,(payload['state_name'],))
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
        print(traceback.print_exc())
        return giveFailure(f"{e} error found",payload['user_id'],0)

#CITIES UPDATED
@app.post('/getCitiesAdmin')
async def get_cities_admin(payload:dict,conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'getCitiesAdmin: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn,payload)
        cities = get_city_from_id(conn)
        country = get_countries_from_id(conn)
        if role_access_status==1:
            table_name = 'cities'
            data = filterAndPaginate(DATABASE_URL, payload['rows'], table_name, payload['filters'], payload['sort_by'], payload['order'], payload["pg_no"], payload["pg_size"], search_key = payload['search_key'] if 'search_key' in payload else None)
            total_count = data['total_count']
            colnames = payload['rows']
            print(colnames)
            res = []
            for row in data['data']:
                row_dict = {}
                for i,colname in enumerate(colnames):
                    row_dict[colname] = row[i]
                res.append(row_dict)
            for i in res:
                if 'countryid' in i:
                    i['countryid'] = country[i['countryid']] if i['countryid'] in country else f"NA_id_{i['countryid']}"
                if 'city' in i:
                    i['city'] = cities[i['id']] if i['id'] in cities else f"NA_id_{i['id']}"
            return giveSuccess(payload["user_id"],role_access_status,res, total_count=total_count)
        else:
            return giveFailure("Invalid Credentials",payload['user_id'],role_access_status)
    except Exception as e:
        logging.exception(traceback.print_exc())
        return giveFailure(f"getCitiesAdmin: {e} error found. exception <{traceback.print_exc()}>",payload['user_id'],0)

@app.post('/getProjects')
async def get_projects(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'getProjects: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn, payload)

        if role_access_status == 1:
            table_name = 'project'
            query = ("SELECT b.buildername, a.builderid, a.projectname, a.addressline1, a.addressline2, "
                     "a.suburb, a.city, a.state, a.country, a.zip, a.nearestlandmark, "
                     "a.project_type, a.mailgroup1, a.mailgroup2, a.website, a.project_legal_status, "
                     "a.rules, a.completionyear, a.jurisdiction, a.taluka, a.corporationward, "
                     "a.policechowkey, a.policestation, a.maintenance_details, a.numberoffloors, "
                     "a.numberofbuildings, a.approxtotalunits, a.tenantstudentsallowed, "
                     "a.tenantworkingbachelorsallowed, a.tenantforeignersallowed, a.otherdetails, "
                     "a.duespayablemonth, a.dated, a.createdby, a.isdeleted, a.id from project a, builder b where a.builderid = b.id")
            data = filterAndPaginate(DATABASE_URL,
                                     payload['rows'], table_name, payload['filters'], payload['sort_by'], payload['order'], payload["pg_no"], payload["pg_size"],
                                     search_key = payload['search_key'] if 'search_key' in payload else None, query=query)
            total_count = data['total_count']
            colnames = payload['rows']
            print(colnames)
            res = []
            for row in data['data']:
                row_dict = {}
                for i,colname in enumerate(colnames):
                    row_dict[colname] = row[i]
                res.append(row_dict)
            return giveSuccess(payload["user_id"],role_access_status,res, total_count=total_count)
        else:
            return giveFailure( "Username or User ID not found",payload['user_id'],role_access_status)
    except Exception as e:
        logging.exception(f'getProjects: encountered exception <{e}>')
        return giveFailure("Username or User ID not found",payload["user_id"],0)
    
@app.post("/addProject")
async def add_project(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'addProject: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn, payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                cursor.execute("""
                    INSERT INTO project (
                        builderid, projectname, addressline1, addressline2, suburb, city, state, 
                        country, zip, nearestlandmark, project_type, mailgroup1, mailgroup2, website, 
                        project_legal_status, rules, completionyear, jurisdiction, taluka, corporationward,
                        policechowkey, policestation, maintenance_details, numberoffloors, numberofbuildings,
                        approxtotalunits, tenantstudentsallowed, tenantworkingbachelorsallowed, tenantforeignersallowed,
                        otherdetails, duespayablemonth, dated, createdby,id
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s
                    )
                """, (
                    payload['builderid'],
                    payload['projectname'],
                    payload['addressline1'],
                    payload['addressline2'],
                    payload['suburb'],
                    payload['city'],
                    payload['state'],
                    payload['country'],
                    payload['zip'],
                    payload['nearestlandmark'],
                    payload['project_type'],
                    payload['mailgroup1'],
                    payload['mailgroup2'],
                    payload['website'],
                    payload['project_legal_status'],
                    payload['rules'],
                    payload['completionyear'],
                    payload['jurisdiction'],
                    payload['taluka'],
                    payload['corporationward'],
                    payload['policechowkey'],
                    payload['policestation'],
                    payload['maintenance_details'],
                    payload['numberoffloors'],
                    payload['numberofbuildings'],
                    payload['approxtotalunits'],
                    payload['tenantstudentsallowed'],
                    payload['tenantworkingbachelorsallowed'],
                    payload['tenantforeignersallowed'],
                    payload['otherdetails'],
                    payload['duespayablemonth'],
                    payload['dated'],
                    payload['createdby'],
                    payload['id']
                ))
                print(cursor.statusmessage)
                # Commit the transaction
                conn[0].commit()
                
                # Get the ID of the last inserted row
                last_row_id = cursor.lastrowid
                print("Inserted row ID:", last_row_id)
                data= {
                        "entered": payload['projectname'],
                        "project_id": last_row_id
                    }
                return giveSuccess(payload['user_id'],role_access_status,data)
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        print(traceback.print_exc())
        return giveFailure("Invalid Credentials",payload['user_id'],0)

@app.post("/editProject")
async def edit_project(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'editProject: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn, payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                cursor.execute("""
                    UPDATE project SET 
                        builderid=%s, projectname=%s, addressline1=%s, addressline2=%s, suburb=%s, city=%s, state=%s, 
                        country=%s, zip=%s, nearestlandmark=%s, project_type=%s, mailgroup1=%s, mailgroup2=%s, website=%s, 
                        project_legal_status=%s, rules=%s, completionyear=%s, jurisdiction=%s, taluka=%s, corporationward=%s,
                        policechowkey=%s, policestation=%s, maintenance_details=%s, numberoffloors=%s, numberofbuildings=%s,
                        approxtotalunits=%s, tenantstudentsallowed=%s, tenantworkingbachelorsallowed=%s, tenantforeignersallowed=%s,
                        otherdetails=%s, duespayablemonth=%s, dated=%s, createdby=%s WHERE id=%s
                """, (
                    payload['builderid'],
                    payload['projectname'],
                    payload['addressline1'],
                    payload['addressline2'],
                    payload['suburb'],
                    payload['city'],
                    payload['state'],
                    payload['country'],
                    payload['zip'],
                    payload['nearestlandmark'],
                    payload['project_type'],
                    payload['mailgroup1'],
                    payload['mailgroup2'],
                    payload['website'],
                    payload['project_legal_status'],
                    payload['rules'],
                    payload['completionyear'],
                    payload['jurisdiction'],
                    payload['taluka'],
                    payload['corporationward'],
                    payload['policechowkey'],
                    payload['policestation'],
                    payload['maintenance_details'],
                    payload['numberoffloors'],
                    payload['numberofbuildings'],
                    payload['approxtotalunits'],
                    payload['tenantstudentsallowed'],
                    payload['tenantworkingbachelorsallowed'],
                    payload['tenantforeignersallowed'],
                    payload['otherdetails'],
                    payload['duespayablemonth'],
                    payload['dated'],
                    payload['createdby'],
                    payload['id']
                ))
                
                # Commit the transaction
                conn[0].commit()
                
                data= {
                        "entered": payload['projectname'],
                    }
                return giveSuccess(payload['user_id'],role_access_status,data)
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        print(traceback.print_exc())
        return giveFailure("Invalid Credentials",payload['user_id'],0)

@app.post('/deleteProject')
async def delete_project(payload:dict,conn : psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'deleteProject: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn, payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                cursor.execute("""DELETE FROM project WHERE id=%s""",(payload['id'],))
                
                # Commit the transaction
                conn[0].commit()
                
                # Get the ID of the last inserted row
                last_row_id = cursor.lastrowid
                print("Inserted row ID:", last_row_id)
                data= {
                        "deleted": payload['projectname']
                    }
                return giveSuccess(payload['user_id'],role_access_status,data)
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        print(traceback.print_exc())
        return giveFailure("Invalid Credentials",payload['user_id'],0)
    
@app.post('/addNewBuilderContact')
async def add_new_builder_contact(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'addNewBuilderContact: received payload <{payload}>')
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
                cursor.execute(query, (
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
                    payload['dated'],
                    payload['createdby'],
                    payload['isdeleted']
                ))
                
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
    logging.info(f'getLocalities: received payload <{payload}>')
    try:
        cities = get_city_from_id(conn)
        role_access_status = check_role_access(conn,payload)
        if role_access_status==1:
            table_name = 'locality'
            query = ' SELECT DISTINCT a.id,c.name as country,a.cityid,b.city,b.state as state, a.locality from locality a, cities b, country c where a.cityid=b.id and b.countryid = c.id '
            data = filterAndPaginate(DATABASE_URL, payload['rows'], table_name, payload['filters'], payload['sort_by'], payload['order'], payload["pg_no"], payload["pg_size"], query, search_key = payload['search_key'] if 'search_key' in payload else None)
            total_count = data['total_count']
            colnames = payload['rows']
            print(colnames)
            res = []
            for row in data['data']:
                row_dict = {}
                for i,colname in enumerate(colnames):
                    row_dict[colname] = row[i]
                res.append(row_dict)
            return giveSuccess(payload["user_id"],role_access_status,res, total_count=total_count)
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        print(traceback.print_exc())
        return giveFailure("Invalid Credentials",payload['user_id'],0)

@app.post('/addLocality')
async def add_localities(payload: dict, conn : psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'addLocality: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'INSERT INTO locality (locality,cityid) VALUES (%s,%s)'
                cursor.execute(query,(payload['locality'],payload['cityid']))
                conn[0].commit()
            data = {
                "Inserted Locality" : payload['locality']
            }
            return giveSuccess(payload['user_id'],role_access_status,data)
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        print(traceback.print_exc())
        return giveFailure("Invalid Credentials",payload['user_id'],0)

@app.post('/editLocality')
async def edit_localities(payload: dict, conn : psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'editLocality: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status==1:
            with conn[0].cursor() as cursor:
                query = 'UPDATE locality SET locality = %s,cityid = %s WHERE id=%s'
                cursor.execute(query,(payload['locality'],payload['cityid'],payload['id']))
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
    logging.info(f'deleteLocality: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'DELETE FROM locality WHERE id=%s'
                cursor.execute(query, (payload['id'],))
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
    logging.info(f'getBankSt: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status==1:
            table_name = 'bankst'
            data = filterAndPaginate(DATABASE_URL, payload['rows'], table_name, payload['filters'], payload['sort_by'], payload['order'], payload["pg_no"], payload["pg_size"], search_key = payload['search_key'] if 'search_key' in payload else None)
            total_count = data['total_count']
            colnames = payload['rows']
            print(colnames)
            res = []
            for row in data['data']:
                row_dict = {}
                for i,colname in enumerate(colnames):
                    row_dict[colname] = row[i]
                res.append(row_dict)
            return giveSuccess(payload["user_id"],role_access_status,res, total_count=total_count)
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)        
    except Exception as e:
        giveFailure("Invalid Credentials",payload['user_id'],0)

@app.post('/addBankSt')
async def add_bank_statement(payload : dict, conn : psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'addBankSt: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = (
                    'INSERT INTO bankst (modeofpayment,date,amount,particulars,crdr,vendorid,createdby) '
                    'VALUES (%s,%s,%s,%s,%s,%s,%s)'
                         )
                cursor.execute(query,(payload['modeofpayment'],payload['date'],payload['amount'],payload['particulars'],payload['crdr'],payload['vendorid'],payload['createdby']))
                conn[0].commit()
            data = {
                "added_data": f"added bank statement for amount <{payload['amount']}>"
            }
            return giveSuccess(payload['user_id'],role_access_status,data)
        else:
            giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        print(traceback.print_exc())
        return giveFailure(f"failed to add bank statement due to exception <{str(e)}>",payload['user_id'],0)

@app.post('/editBankSt')
async def edit_bank_statement(payload : dict, conn : psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'editBankSt: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = ('UPDATE bankst SET modeofpayment=%s,'
                         'date=%s,amount=%s,particulars=%s,'
                         'crdr=%s,vendorid=%s,createdby=%s WHERE id=%s')
                cursor.execute(query,(payload['modeofpayment'],payload['date'],payload['amount'],payload['particulars'],payload['crdr'],payload['chequeno'],payload['availablebalance'],payload['dateadded'],payload['clientid'],payload['orderid'],payload['receivedby'],payload['details'],payload['vendorid'],payload['createdby'],payload['id']))
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
    logging.info(f'deleteBankSt: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'DELETE FROM bankst WHERE id=%s'
                cursor.execute(query,(payload['id'],))
                if cursor.statusmessage == "DELETE 0":
                    return giveFailure("No Bank st available",payload['user_id'],role_access_status)
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
    logging.info(f'getEmployee: received payload <{payload}>')
    cities = get_city_from_id(conn)
    countries = get_countries_from_id(conn)
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status==1:
            role_cache = roles(conn[0])
            table_name = 'employee'
            data = filterAndPaginate(DATABASE_URL, payload['rows'], table_name, payload['filters'], payload['sort_by'], payload['order'], payload["pg_no"], payload["pg_size"], search_key = payload['search_key'] if 'search_key' in payload else None)
            total_count = data['total_count']
            colnames = payload['rows']
            print(colnames)
            res = []
            for row in data['data']:
                row_dict = {}
                for i,colname in enumerate(colnames):
                    row_dict[colname] = row[i]
                res.append(row_dict)
            print(res)
            for i in res:
                if 'country' in i:
                    i['country'] = countries[i['country']]
                if 'city' in i:
                    i['city'] = cities[i['city']]
                if['roleid'] in i:
                    i['roleid'] = get_name(i['roleid'],role_cache)
            return giveSuccess(payload["user_id"],role_access_status,res, total_count=total_count)
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)        
    except Exception as e:
        print(traceback.print_exc())
        giveFailure("Invalid Credentials",payload['user_id'],0)

@app.post('/addEmployee')
async def add_employee(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'addEmployee: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'INSERT INTO employee (employeename,employeeid, userid,roleid, dateofjoining, dob, panno,status, phoneno, email, addressline1, addressline2,suburb, city, state, country, zip,dated, createdby, isdeleted, entityid,lobid, lastdateofworking, designation)VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                cursor.execute(query,(  payload['employeename'],
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
                                        payload['designation']))
                conn[0].commit()
            data = {
                "Inserted Employee" : payload['employeename']
            }
            return giveSuccess(payload['user_id'],role_access_status,data)
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        print(traceback.print_exc())
        return giveFailure("Invalid Credentials",payload['user_id'],0)

@app.post('/editEmployee')
async def edit_employee(payload: dict, conn : psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'editEmployee: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status==1:
            with conn[0].cursor() as cursor:
                query = '''UPDATe employee SET employeename=%s,employeeid=%s, userid=%s,roleid=%s, dateofjoining=%s, dob=%s, panno=%s,status=%s, phoneno=%s, email=%s, addressline1=%s, addressline2=%s,suburb=%s, city=%s, state=%s, country=%s, zip=%s,dated=%s, createdby=%s, isdeleted=%s, entityid=%s,lobid=%s, lastdateofworking=%s, designation=%s WHERE id=%s'''
                cursor.execute(query,(
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
    logging.info(f'deleteEmployee: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status==1:
            with conn[0].cursor() as cursor:
                query = 'DELETE FROM employee WHERE id=%s'
                cursor.execute(query,(payload['id'],))
                conn[0].commit()
                if cursor.statusmessage == "DELETE 0":
                    return giveFailure("No record exists",payload['user_id'],role_access_status)        
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
    logging.info(f'getLob: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status==1:
            table_name = 'lob'
            data = filterAndPaginate(DATABASE_URL, payload['rows'], table_name, payload['filters'], payload['sort_by'], payload['order'], payload["pg_no"], payload["pg_size"], search_key = payload['search_key'] if 'search_key' in payload else None)
            total_count = data['total_count']
            colnames = payload['rows']
            print(colnames)
            res = []
            for row in data['data']:
                row_dict = {}
                for i,colname in enumerate(colnames):
                    row_dict[colname] = row[i]
                res.append(row_dict)
            return giveSuccess(payload["user_id"],role_access_status,res, total_count=total_count)
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)        
    except Exception as e:
        print(traceback.print_exc())
        giveFailure("Invalid Credentials",payload['user_id'],0)    

@app.post('/addLob')
async def add_lob(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'addLob: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'INSERT INTO lob (name) VALUES (%s)'
                cursor.execute("INSERT INTO lob (name) VALUES (%s)",(payload['name'],))
                conn[0].commit()
            data = {
                "added_data":payload['name']
            }
            return giveSuccess(payload['user_id'],role_access_status,data)
        else:
            giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        print(traceback.print_exc())
        giveFailure("Invalid Credentials",payload['user_id'],0)

@app.post('/editLob')
async def edit_lob(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'editLob: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'UPDATE lob SET name=%s WHERE name=%s'
                cursor.execute(query,(payload['new_name'],payload['old_name']))
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
    logging.info(f'deleteLob: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'DELETE FROM lob WHERE name=%s'
                cursor.execute(query,(payload['name'],))
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
    logging.info(f'getResearchProspect: received payload <{payload}>')
    countries = get_countries_from_id(conn)
    print(countries)
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status==1:
            table_name = 'research_prospect'
            data = filterAndPaginate(DATABASE_URL, payload['rows'], table_name, payload['filters'], payload['sort_by'], payload['order'], payload["pg_no"], payload["pg_size"], search_key = payload['search_key'] if 'search_key' in payload else None)
            total_count = data['total_count']
            colnames = payload['rows']
            print(colnames)
            res = []
            for row in data['data']:
                row_dict = {}
                for i,colname in enumerate(colnames):
                    row_dict[colname] = row[i]
                res.append(row_dict)
            for i in res:
                if 'country' in i:
                    i['countryid'] = i['country']
                    i['country'] = countries[i['country']]
            return giveSuccess(payload["user_id"],role_access_status,res, total_count=total_count)
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)        
    except Exception as e:
        print(traceback.print_exc())
        giveFailure("Invalid Credentials",payload['user_id'],0) 
        
@app.post('/addResearchProspect')
async def add_research_prospect(payload: dict, conn : psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'addResearchProspect: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'INSERT INTO research_prospect (personname,suburb,city,state,country,propertylocation,possibleservices,dated,createdby,isdeleted) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                cursor.execute(query,(payload['personname'],payload['suburb'],payload['city'],payload['state'],payload['country'],payload['propertylocation'],payload['possibleservices'],payload['dated'],payload['createdby'],payload['isdeleted']))
                conn[0].commit()
            data = {
                "added_data":payload['personname']
            }
            return giveSuccess(payload['user_id'],role_access_status,data)
        else:
            giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        print(traceback.print_exc())
        giveFailure("Invalid Credentials",payload['user_id'],0)

@app.post('/editResearchProspect')
async def edit_research_prospect(payload: dict, conn : psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'editResearchProspect: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'UPDATE research_prospect SET personname=%s,suburb=%s,city=%s,state=%s,country=%s,propertylocation=%s,possibleservices=%s,dated=%s,createdby=%s,isdeleted=%s WHERE id=%s'
                cursor.execute(query,(payload['personname'],payload['suburb'],payload['city'],payload['state'],payload['country'],payload['propertylocation'],payload['possibleservices'],payload['dated'],payload['createdby'],payload['isdeleted'],payload['id']))
                if cursor.statusmessage == "UPDATE 0":
                    return giveFailure("No Prospect available",payload['user_id'],role_access_status)
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

@app.post('/deleteResearchProspect')
async def delete_research_prospect(payload: dict, conn : psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'deleteResearchProspect: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'DELETE FROM research_prospect WHERE id=%s'
                cursor.execute(query,(payload['id'],))
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
    logging.info(f'getPayments: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status==1:
            users,paymentmodes,entities,paymentfordata = getdata(conn[0])
            # query = 'SELECT distinct a.id,concat(b.firstname,' ',b.lastname) as paymentby,concat(c.firstname,' ',c.lastname) as paymentto, a.amount,a.paidon,d.name as paymentmode,a.paymentstatus,a.description,a.banktransactionid,e.name as paymentfor,a.dated,a.createdby,a.isdeleted,a.entityid,a.officeid,a.tds,a.professiontax,a.month,a.deduction FROM ref_contractual_payments a,usertable b, usertable c, mode_of_payment d, payment_for e where a.paymentto = b.id and a.paymentby = c.id and a.paymentmode = d.id and a.paymentfor = e.id;'
            table_name = 'get_payments_view'
            # data = filterAndPaginate(DATABASE_URL, payload['rows'], table_name, payload['filters'], payload['sort_by'], payload['order'], payload["pg_no"], payload["pg_size"],query = query,search_key = payload['search_key'] if 'search_key' in payload else None)

            data = filterAndPaginate(DATABASE_URL, payload['rows'], table_name, payload['filters'], payload['sort_by'], payload['order'], payload["pg_no"], payload["pg_size"],search_key = payload['search_key'] if 'search_key' in payload else None)
            total_count = data['total_count']
            colnames = payload['rows']
            res = []
            for row in data['data']:
                row_dict = {}
                for i,colname in enumerate(colnames):
                    row_dict[colname] = row[i]
                res.append(row_dict)
            print(paymentfordata)
            # for i in res:
                # i['paymentto'] = users[i['paymentto']]
                # i['paymentby'] = users[i['paymentby']]
                # i['paymentmode'] = paymentmodes[i['paymentmode']]
                # i['entityid'] = entities.get(i['entityid'],None)
                # i['paymentfor']=paymentfordata.get(i['paymentfor'],None)
            return giveSuccess(payload["user_id"],role_access_status,res, total_count=total_count)
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)        
    except Exception as e:
        print(traceback.print_exc())
        giveFailure("Invalid Credentials",payload['user_id'],0) 

@app.post('/addPayment')
async def add_payment(payload: dict,conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'addPayment: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                payload['dated'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                query = 'INSERT INTO ref_contractual_payments (paymentto,paymentby,amount,paidon,paymentmode,description,paymentfor,dated,createdby,entityid,tds,professiontax,month) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'                
                cursor.execute(query,(payload['paymentto'],payload['paymentby'],payload['amount'],payload['paidon'],payload['paymentmode'],payload['description'],payload['paymentfor'],payload['dated'],payload['createdby'],payload['entityid'],payload['tds'],payload['professiontax'],payload['month']))
                conn[0].commit()
            data = {
                "added_payment_by":payload['createdby']
            }
            return giveSuccess(payload['user_id'],role_access_status,data)
        else:
            giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        print(traceback.print_exc())
        giveFailure("Invalid Credentials",payload['user_id'],0)

@app.post('/editPayment')
async def edit_payment(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'editPayment: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'UPDATE ref_contractual_payments SET paymentto=%s,paymentby=%s,amount=%s,paidon=%s,paymentmode=%s,description=%s,paymentfor=%s,dated=%s,createdby=%s,isdeleted=%s,entityid=%s,officeid=%s,tds=%s,professiontax=%s,month=%s,deduction=%s WHERE id=%s'
                cursor.execute(query,(payload['paymentto'],payload['paymentby'],payload['amount'],payload['paidon'],payload['paymentmode'],payload['description'],payload['paymentfor'],payload['dated'],payload['createdby'],payload['isdeleted'],payload['entityid'],payload['officeid'],payload['tds'],payload['professiontax'],payload['month'],payload['deduction'],payload['id']))
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
    logging.info(f'deletePayment: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'DELETE FROM get_payments_view WHERE id=%s'
                cursor.execute(query,(payload['id'],))
                if cursor.statusmessage == "DELETE 0":
                    return giveFailure("No Payment available",payload['user_id'],role_access_status)
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
    logging.info(f'getVendorAdmin: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'SELECT id,vendorname FROM vendor'
                cursor.execute(query)
                data = cursor.fetchall()
                return giveSuccess(payload['user_id'],role_access_status,data)
        else:
            giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        giveFailure('Invalid Credentials',payload['user_id'],0)


@app.post('/getClientAdmin')
async def get_client_admin(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'getClientAdmin: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn, payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = "select distinct id, concat_ws(' ',firstname,lastname) as client_name from client"
                cursor.execute(query)
                data = cursor.fetchall()
                return giveSuccess(payload['user_id'], role_access_status, data)
        else:
            giveFailure("Access Denied", payload['user_id'], role_access_status)
    except Exception as e:
        logging.exception(f'getClientAdmin_Exception: <{str(e)}>')
        giveFailure('Invalid Credentials', payload['user_id'], 0)

@app.post('/getModesAdmin')
async def get_modes_admin(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'getModesAdmin: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn, payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = "select distinct id, name, entityid from mode_of_payment"
                cursor.execute(query)
                data = cursor.fetchall()
                return giveSuccess(payload['user_id'], role_access_status, data)
        else:
            giveFailure("Access Denied", payload['user_id'], role_access_status)
    except Exception as e:
        logging.exception(f'getModesAdmin_Exception: <{str(e)}>')
        giveFailure('Invalid Credentials', payload['user_id'], 0)

@app.post('/getEntityAdmin')
async def get_entity_admin(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'getModesAdmin: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn, payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = "select distinct id, name from entity"
                cursor.execute(query)
                data = cursor.fetchall()
                return giveSuccess(payload['user_id'], role_access_status, data)
        else:
            giveFailure("Access Denied", payload['user_id'], role_access_status)
    except Exception as e:
        logging.exception(f'getModesAdmin_Exception: <{str(e)}>')
        giveFailure('Invalid Credentials', payload['user_id'], 0)

@app.post('/getHowReceivedAdmin')
async def get_howreceived_admin(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'getHowReceivedAdmin: received payload <{payload}>')
    try:
        role_access_status = check_role_access(conn, payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = "select id, name from howreceived"
                cursor.execute(query)
                data = cursor.fetchall()
                return giveSuccess(payload['user_id'], role_access_status, data)
        else:
            giveFailure("Access Denied", payload['user_id'], role_access_status)
    except Exception as e:
        logging.exception(f'getHowReceivedAdmin_Exception: <{str(e)}>')
        giveFailure('Invalid Credentials', payload['user_id'], 0)

@app.post('/getUsersAdmin')
async def get_users_admin(payload: dict, conn : psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status==1:
            res = usernames(conn[0])
            arr = []
            for i in res:
                arr.append({'id':i,'name':res[i]})
            return giveSuccess(payload['user_id'],role_access_status,arr,total_count=len(arr))
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        return giveFailure("Invalid Credentials",0,0)

@app.post('/getRolesAdmin')
async def get_roles(payload: dict, conn : psycopg2.extensions.connection = Depends(get_db_connection)):
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


@app.post('/addClientReceipt')
async def add_client_receipt(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    logging.info(f'addClientReceipt: received payload <{payload}>')
    try:
        # if 'builderid' not in payload:
        #     return {
        #         "result": "error",
        #         "message": "Missing 'builderid' in payload",
        #         "user_id": payload.get('user_id', None),
        #         "data": {}
        #     }
        role_access_status = check_role_access(conn, payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = '''
                    INSERT INTO client_receipt (
                        receivedby, paymentmode, recddate, entityid, amount, howreceivedid,
                        clientid, receiptdesc, serviceamount, reimbursementamount, tds 
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                '''
                cursor.execute(query, (
                    payload['receivedby'],
                    payload['paymentmode'],
                    payload['recddate'],
                    payload['entityid'],
                    payload['amount'],
                    payload['howreceivedid'],
                    payload['clientid'],
                    payload['receiptdesc'],
                    payload['serviceamount'],
                    payload['reimbursementamount'],
                    payload['tds']
                ))

                # Commit changes to the database
                conn[0].commit()
            data = { "entered": f"client receipt for amount <{payload['amount']}>"}
            return giveSuccess(payload['user_id'], role_access_status, data)
        else:
            return giveFailure("Access Denied", payload['user_id'], role_access_status)
    except Exception as e:
        logging.exception(f'addClientReceit_Exception: {traceback.format_exc()}')
        return giveFailure(str(e), payload['user_id'], 0)

    
@app.post('/getItembyId')
async def get_item_by_id(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status==1:
            with conn[0].cursor() as cursor:
                query = f"SELECT * FROM {payload['table_name']} WHERe id =%s LIMIT 1"
                cursor.execute(query,(payload['item_id'],))
                data = cursor.fetchone()
                
                colnames = [desc[0] for desc in cursor.description]
                
                res = {}
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

logger.info("program_started")
