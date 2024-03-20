import psycopg2
import bcrypt
from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
import traceback
logger = logging.getLogger(__name__)

# PostgreSQL database URL
#todo : need to source user, password and ip port from variables
DATABASE_URL = "postgresql://postgres:cura123@192.168.10.133:5432/cura_db"

def getFilteredAndPaginatedDataFromDatabaseTable(db_config,
                                                 required_columns,
                                                 table_name,
                                                 filters=None,
                                                 sort_column=None,
                                                 sort_order='asc',
                                                 page_number=1,
                                                 page_size=10,
                                                 query = None):
    try:
        # Base query
        if query is None:
            query = f"SELECT {','.join(required_columns)} FROM {table_name}"
        # Adding filters
        print(f'Query is {query}')
        where_clauses = []
        for column, filter_type, value in (filters or []):
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
        print(query)
        # handle where clause and sorting
        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)
        if sort_column:
            query += f" ORDER BY {sort_column} {sort_order}"
        # Calculate OFFSET
        offset = (page_number - 1) * page_size
        # Adding pagination
        query += f" LIMIT {page_size} OFFSET {offset}"
        print(f'Prepared final query [{query}]')
        # fetch results and return to caller
        conn = psycopg2.connect(db_config)
        cur = conn.cursor()
        cur.execute(query)
        print(cur.statusmessage)

        rows = cur.fetchall()
        print(rows)
        cur.close()
        conn.close()
        return {'data':rows, 'message':'success'}
    except Exception as e:
        print(traceback.print_exc())
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
        print(traceback.print_exc())
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
        print(traceback.print_exc())
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
            print("Here")
            res = {}
            for row in data:
                res[row[0]] = row[1:]
            return res
    except:
        print(traceback.print_exc())
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
    try:
        with conn[0].cursor() as cursor:
            query = 'SELECT password,id,roleid FROM usertable where username = %s'
            query2 = "SELECT EXISTS (SELECT 1 FROM companykey WHERE companycode = %s);"
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
            print(company_key)
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
        print(traceback.print_exc())
        return {
            "result" : "Error",
            "message":"Wrong input",
            "data":{}
            }

def giveSuccess(uid,rid,data=[]):
    return {
        "result":"success",
        "user_id":uid,
        "role_id":rid,
        "data":data
    }

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
        print(traceback.print_exc())
    finally:
        cursor.close()

# FastAPI route to get roleid based on id or username
@app.post("/getRoleID")
async def get_role_id(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    role_id = check_role_access(conn, payload)
    print('There')
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
    try:
        role_access_status = check_role_access(conn,payload)
        print(role_access_status)
        if role_access_status is not None:
            if role_access_status == 1:
                with conn[0].cursor() as cursor:
                    query = "SELECT * FROM country ORDER BY id;"
                    cursor.execute(query)
                    data = cursor.fetchall()
                return giveSuccess(payload['user_id'],role_access_status,data)
            else:
                return giveFailure("Access Denied",payload["user_id"],role_access_status)
        else:
            return giveFailure("User does not exist",payload["user_id"],role_access_status)

    except Exception as e:
        # print(traceback.print_exc())
        return giveFailure(f"error {e} found",payload['user_id'],0)

@app.post('/addCountry')
async def add_country(payload:dict,conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        with conn[0].cursor() as cursor:
            role_access_status = check_role_access(conn,payload)
            print(role_access_status)
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
        print(traceback.print_exc())
        return False

@app.post("/editCountry")
async def edit_country(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        # Check user role
        role_access_status = check_role_access(conn,payload)
        print(role_access_status)
        
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
    print(payload)
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
                print("Inserted row ID:", last_row_id)
                data= {
                    "entered": payload["buildername"]
                }
            return giveSuccess(payload['user_id'],role_access_status,data,data)
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        print(traceback.print_exc())
        return giveFailure("Invalid Credentials",payload['user_id'],0)

#BUILDER UPDATED
@app.post('/getBuilderInfo')
def getBuilderInfo(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    countries = get_countries_from_id(conn=conn)
    cities = get_city_from_id(conn=conn)
    try:
        role_access_status = check_role_access(conn, payload)

        if role_access_status == 1:  
            with conn[0].cursor() as cursor:
                query = "SELECT a.id,a.buildername,a.phone1,a.phone2,a.email1,a.email2,a.addressline1,a.addressline2,a.suburb,b.city,a.state,c.name as country,a.zip,a.website,a.comments,a.dated,a.createdby,a.isdeleted FROM builder a,cities b,country c WHERE a.city = b.id AND a.country = c.id ORDER BY id;"
                cursor.execute(query)
                data = cursor.fetchall()

                colnames = [desc[0] for desc in cursor.description]
                
                res = []
                for row in data:
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
        print(traceback.print_exc())
        return giveFailure("Invalid Credentials",payload['user_id'],0)

@app.post("/editBuilder")
async def edit_builder(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
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
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status==1:
            with conn[0].cursor() as cursor:
                query = 'SELECT * FROM builder where id=%s'
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
        print(traceback.print_exc())
        return giveFailure("Invalid Credentials",payload['user_id'],0)

#STATES UPDATED
@app.post('/getStatesAdmin')
async def get_states_admin(payload:dict,conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status==1:
            with conn[0].cursor() as cursor:
                query = "SELECT DISTINCT a.state,b.name FROM cities a,country b WHERE a.countryid=b.id"
                cursor.execute(query)
                data = cursor.fetchall()
            return giveSuccess(payload["user_id"],role_access_status,data)
        else:
            return giveFailure("Invalid Credentials",payload['user_id'],role_access_status)
    except Exception as e:
        print(traceback.print_exc())
        return giveFailure("Invalid Credentials",payload['user_id'],0)

@app.post('/getStates')
async def get_states(payload : dict,conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    # logger.info(f'get_States: payload <{payload}>', flush=True)
    try:
        role_access_status = check_role_access(conn,payload)
        print(role_access_status)
        if role_access_status != 0:
            if role_access_status == 1:
                with conn[0].cursor() as cursor:
                    query = "SELECT DISTINCT state FROM cities WHERE countryid = %s" 
                    cursor.execute(query,(payload['country_id'],))
                    data = [i[0] for i in cursor.fetchall()]
                
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
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status==1:
            with conn[0].cursor() as cursor:
                query = "SELECT id,city FROM cities where state=%s"
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
    try:
        role_access_status = check_role_access(conn,payload)
        cities = get_city_from_id(conn)
        country = get_countries_from_id(conn)
        if role_access_status==1:
            table_name = 'cities'
            data = getFilteredAndPaginatedDataFromDatabaseTable(DATABASE_URL,payload['rows'],table_name,payload['filters'],payload['sort_by'],payload['order'],payload["pg_no"],payload["pg_size"])
            print(data['data'])
            colnames = payload['rows']
            print(colnames)
            res = []
            for row in data['data']:
                row_dict = {}
                print(row)
                for i,colname in enumerate(colnames):
                    row_dict[colname] = row[i]
                res.append(row_dict)
            for i in res:
                if 'countryid' in i:
                    i['countryid'] = country[i['countryid']]
                if 'city' in i:
                    i['city'] = cities[i['id']]
            return giveSuccess(payload["user_id"],role_access_status,res)
        else:
            return giveFailure("Invalid Credentials",payload['user_id'],role_access_status)
    except Exception as e:
        print(traceback.print_exc())
        return giveFailure(f"{e} error found",payload['user_id'],0)

@app.post('/getProjects')
async def get_projects(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    print("here")
    try:
        role_access_status = check_role_access(conn, payload)

        if role_access_status == 1:
            table_name = 'project'
            data = getFilteredAndPaginatedDataFromDatabaseTable(DATABASE_URL,payload['rows'],table_name,payload['filters'],payload['sort_by'],payload['order'],payload["pg_no"],payload["pg_size"])
            print(data['data'])
            colnames = payload['rows']
            print(colnames)
            res = []
            for row in data['data']:
                row_dict = {}
                print(row)
                for i,colname in enumerate(colnames):
                    row_dict[colname] = row[i]
                res.append(row_dict)
            return giveSuccess(payload["user_id"],role_access_status,res)
        else:
            return giveFailure( "Username or User ID not found",payload['user_id'],role_access_status)
    except Exception as e:
        return giveFailure("Username or User ID not found",payload["user_id"],0)

@app.post('/getProjectsByBuilder')
async def get_projects_builder(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    print("here")
    try:
        role_access_status = check_role_access(conn, payload)

        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = "SELECT a.id,a.builderid,a.addressline1,a.addressline2,a.suburb,b.city as city,a.state,c.name as country,a.zip,a.nearestlandmark, a.project_type, a.rules,a.completionyear,a.jurisdiction,a.taluka,a.corporationward,a.policechowkey,a.policestation,a.maintenance_details,a.numberoffloors,a.numberofbuildings,a.approxtotalunits,a.tenantstudentsallowed,a.tenantworkingbachelorsallowed,a.tenantforeignersallowed,a.otherdetails,a.duespayablemonth,a.dated,a.createdby,a.isdeleted FROM project a,cities b, country c where a.city = b.id and a.country = c.id and builderid=%s ORDER BY id;"
                cursor.execute(query,(payload['builder_id'],))
                data = cursor.fetchall()

                colnames = [desc[0] for desc in cursor.description]

                res = []
                for row in data:
                    row_dict = {}
                    for i, colname in enumerate(colnames):
                        row_dict[colname] = row[i]
                    res.append(row_dict)
                data= {
                        "project_info": res
                    }
                return giveSuccess(payload['user_id'],role_access_status,data)
        else:
            return giveFailure("Username or User ID not found",payload["user_id"],role_access_status)
    except Exception as e:
        print(traceback.print_exc())
        return giveFailure("Username or User ID not found",payload['user_id'],0)

@app.post("/addNewProject")
async def add_new_project(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
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
                        otherdetails, duespayablemonth, dated, createdby
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
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
                ))
                
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

@app.post('/addNewBuilderContact')
async def add_new_builder_contact(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
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
    try:
        cities = get_city_from_id(conn)
        role_access_status = check_role_access(conn,payload)
        if role_access_status==1:
            table_name = 'locality'
            query = 'SELECT DISTINCT a.id,a.locality,b.city,b.state,c.name as country from locality a, cities b, country c where a.cityid=b.id and b.countryid = c.id'
            data = getFilteredAndPaginatedDataFromDatabaseTable(DATABASE_URL,payload['rows'],table_name,payload['filters'],payload['sort_by'],payload['order'],payload["pg_no"],payload["pg_size"],query)
            print(data['data'])
            colnames = payload['rows']
            print(colnames)
            res = []
            for row in data['data']:
                row_dict = {}
                print(row)
                for i,colname in enumerate(colnames):
                    row_dict[colname] = row[i]
                res.append(row_dict)
            return giveSuccess(payload["user_id"],role_access_status,res)
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        print(traceback.print_exc())
        return giveFailure("Invalid Credentials",payload['user_id'],0)

@app.post('/addLocality')
async def add_localities(payload: dict, conn : psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'INSERT INTO locality VALUES (%s,%s,%s)'
                cursor.execute(query,(payload['id'],payload['locality'],payload['cityid']))
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
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status==1:
            table_name = 'bankst'
            data = getFilteredAndPaginatedDataFromDatabaseTable(DATABASE_URL,payload['rows'],table_name,payload['filters'],payload['sort_by'],payload['order'],payload["pg_no"],payload["pg_size"])
            print(data['data'])
            colnames = payload['rows']
            print(colnames)
            res = []
            for row in data['data']:
                row_dict = {}
                print(row)
                for i,colname in enumerate(colnames):
                    row_dict[colname] = row[i]
                res.append(row_dict)
            return giveSuccess(payload["user_id"],role_access_status,res)
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)        
    except Exception as e:
        giveFailure("Invalid Credentials",payload['user_id'],0)

@app.post('/addBankSt')
async def add_bank_statement(payload : dict, conn : psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'INSERT INTO bankst (id,modeofpayment,date,amount,particulars,crdr,chequeno,availablebalance,dateadded,clientid,orderid,receivedby,details,vendorid,createdby) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                cursor.execute(query,(payload['id'],payload['modeofpayment'],payload['date'],payload['amount'],payload['particulars'],payload['crdr'],payload['chequeno'],payload['availablebalance'],payload['dateadded'],payload['clientid'],payload['orderid'],payload['receivedby'],payload['details'],payload['vendorid'],payload['createdby']))
                conn[0].commit()
            data = {
                "added_data":payload['id']
            }
            return giveSuccess(payload['user_id'],role_access_status,data)
        else:
            giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        print(traceback.print_exc())
        giveFailure("Invalid Credentials",payload['user_id'],0)

@app.post('/editBankSt')
async def edit_bank_statement(payload : dict, conn : psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'UPDATE bankst SET modeofpayment=%s,date=%s,amount=%s,particulars=%s,crdr=%s,chequeno=%s,availablebalance=%s,dateadded=%s,clientid=%s,orderid=%s,receivedby=%s,details=%s,vendorid=%s,createdby=%s WHERE id=%s'
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
    cities = get_city_from_id(conn)
    countries = get_countries_from_id(conn)
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status==1:
            table_name = 'employee'
            data = getFilteredAndPaginatedDataFromDatabaseTable(DATABASE_URL,payload['rows'],table_name,payload['filters'],payload['sort_by'],payload['order'],payload["pg_no"],payload["pg_size"])
            print(data['data'])
            colnames = payload['rows']
            print(colnames)
            res = []
            for row in data['data']:
                row_dict = {}
                print(row)
                for i,colname in enumerate(colnames):
                    row_dict[colname] = row[i]
                res.append(row_dict)
            for i in res:
                if 'country' in i:
                    i['country'] = countries[i['country']]
                if 'city' in i:
                    i['city'] = cities[i['city']]
            
            return giveSuccess(payload["user_id"],role_access_status,res)
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)        
    except Exception as e:
        print(traceback.print_exc())
        giveFailure("Invalid Credentials",payload['user_id'],0)

@app.post('/getlob')
async def get_lob(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status==1:
            table_name = 'lob'
            data = getFilteredAndPaginatedDataFromDatabaseTable(DATABASE_URL,payload['rows'],table_name,payload['filters'],payload['sort_by'],payload['order'],payload["pg_no"],payload["pg_size"])
            print(data['data'])
            colnames = payload['rows']
            print(colnames)
            res = []
            for row in data['data']:
                row_dict = {}
                print(row)
                for i,colname in enumerate(colnames):
                    row_dict[colname] = row[i]
                res.append(row_dict)
            return giveSuccess(payload["user_id"],role_access_status,res)
        else:
            return giveFailure("Access Denied",payload['user_id'],role_access_status)        
    except Exception as e:
        print(traceback.print_exc())
        giveFailure("Invalid Credentials",payload['user_id'],0)    

@app.post('/addLob')
async def add_lob(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'INSERT INTO lob (id,name,lob_head,company,entityid) VALUES (%s,%s,%s,%s,%s)'
                cursor.execute(query,(payload['id'],payload['name'],payload['lob_head'],payload['company'],payload['entityid']))
                conn[0].commit()
            data = {
                "added_data":payload['id']
            }
            return giveSuccess(payload['user_id'],role_access_status,data)
        else:
            giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        print(traceback.print_exc())
        giveFailure("Invalid Credentials",payload['user_id'],0)

@app.post('/editLob')
async def edit_lob(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'UPDATE lob SET name=%s,lob_head=%s,company=%s,entityid=%s WHERE id=%s'
                cursor.execute(query,(payload['name'],payload['lob_head'],payload['company'],payload['entityid'],payload['id']))
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

@app.post('/deleteLob')
async def delete_lob(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = 'DELETE FROM lob WHERE id=%s'
                cursor.execute(query,(payload['id'],))
                if cursor.statusmessage == "DELETE 0":
                    return giveFailure("No LOB available",payload['user_id'],role_access_status)
                conn[0].commit()
            data = {
                "deleted_lob":payload['id']
            }
            return giveSuccess(payload['user_id'],role_access_status,data)
        else:
            giveFailure("Access Denied",payload['user_id'],role_access_status)
    except Exception as e:
        print(traceback.print_exc())
        giveFailure("Invalid Credentials",payload['user_id'],0)  
logger.info("program_started")
