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
            print(data)
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

# Create a FastAPI app
app = FastAPI()

# CORS Middleware for handling Cross-Origin Resource Sharing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
def giveSuccess(id):
    return {
        'result':'success',
        'user_id': id
    }
    
def giveFailure(msg):
    return {
        'result' : 'failure',
        'message' : msg
    }

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
                resp = giveSuccess(userdata[1])
                resp['role_id'] = userdata[2]
                return resp
            else:
                return giveFailure("Invalid credentials")
    except KeyError as ke:
        return {
            "result": "error",
            "message": f"key {ke} not found",
            "user_id": payload['user_id']
        }
    except Exception as e:
        print(traceback.print_exc())
        return {
            "result" : "Error",
            "message":"Wrong input",
            "data":{}
            }

def giveSuccess(user_id: int):
    return {"result": "success", "user_id": user_id}

def giveFailure(message: str):
    return {"result": "failure", "message": message}


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
    print(payload)
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
                return {
                    "result": "success",
                    "user_id": payload['user_id'],
                    "role_id": role_access_status,
                    "data":data
                }
            else:
                return {
                    "result": "error",
                    "message": "Access denied",
                    "role_id": role_access_status,  # Assuming role_id is in the users table
                    "user_id": payload['user_id'],
                    "data":{}      
                }
        else:
            return {
                "result": "error",
                "message": "User doesn't exist",
                "role_id": 0,  # Assuming role_id is in the users table
                "user_id": payload['user_id'],
                "data":{}      
                }
    except Exception as e:
        # print(traceback.print_exc())
        return {
            "result": "error",
            "message": "f'{e} error found",
            "role_id": role_access_status,  # Assuming role_id is in the users table
            "user_id": payload['user_id'],
            "data":{}
        }

@app.post('/addCountry')
async def add_country(payload:dict,conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        with conn[0].cursor() as cursor:
            role_access_status = check_role_access(conn,payload)
            print(role_access_status)
            if role_access_status == 1:
                id = cursor.execute('SELECT COUNT(*) FROM country')
                id = cursor.fetchone()
                id = id[0]+1
                print(id)
            # Insert new country data into the database
                query_insert = 'INSERT INTO country (id,name) VALUES (%s,%s)'
                cursor.execute(query_insert, (id, payload['country_name']))

            # Commit the transaction
                conn[0].commit()

                return {
                    "result": "success",
                    "role_id": role_access_status,  # Assuming role_id is in the users table
                    "user_id": payload['user_id'],
                    "data":{"added":payload['country_name']}
                }
            elif role_access_status!=1:
                return {
                    "result": "error",
                    "message": "Access denied",
                    "role_id": role_access_status,  # Assuming role_id is in the users table
                    "user_id": payload['user_id'],
                    "data":{}
                }
            else:
                return {
                    "result": "error",
                    "message": "Invalid credentials",
                    "user_id": payload['user_id'],
                    "data":{}
                }
    except KeyError as ke:
        return {
            "result": "error",
            "message": f"key {ke} not found",
            "user_id": payload['user_id'],
            "data":{}
        }  
    except Exception as e:
        return {
            "result": "error",
            "message": "Invalid credentials",
            "user_id": payload['user_id'],
            "data":{}
        }
    

    
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

            return {
                "result": "success",
                "user_id": payload['user_id'],
                "role_id": role_access_status,
                "data":{
                    "original":payload['old_country_name'],
                    "new country":payload['new_country_name']
                }
            }
        elif not checkcountry(payload['old_country_name'],conn):
            return {
                "result":"error",
                "message":"Does not exist",
                "role_id": role_access_status,
                "data":{}
            }
        elif role_access_status!=1:
            return {
                    "result": "error",
                    "message": "Access denied",
                    "role_id": role_access_status,  # Assuming role_id is in the users table
                    "user_id": payload['user_id'],
                    "data":{}
                }
        
        else:
            return {
                    "result": "error",
                    "message": "Invalid credentials",
                    "user_id": payload['user_id'],
                    "data":{}
                }
    except KeyError as ke:
        return {
            "result": "error",
            "message": f"key {ke} not found",
            "user_id": payload['user_id'],
            "data":{}
        }     
    except Exception as e:
        return {
            "result": "error", 
            "message": "Invalid credentials",
            "user_id": payload['user_id'],
            "data":{}
        }
    

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

                return {
                    "result": "success",
                    "user_id": payload['user_id'],
                    "role_id": role_access_status,
                    "data":{
                        "deleted":payload["country_name"]
                        }
                    }
            elif role_access_status!=1:
                return {
                    "result": "error",
                    "message": "Access denied",
                    "role_id": role_access_status,  # Assuming role_id is in the users table
                    "user_id": payload['user_id'],
                    "data":{}
                }
            elif not checkcountry(payload['name'],conn):
                return {
                    "result": "error",
                    "message": "Does not exist",
                    "role_id": role_access_status,  # Assuming role_id is in the users table
                    "user_id": payload['user_id'],
                    "data":{}
                }
            else:
                return {
                    "result": "error",
                    "message": "Invalid credentials",
                    "user_id": payload['user_id'],
                    "data":{}
                }
    except KeyError as ke:
        return {
            "result": "error",
            "message": f"Country {payload['country_name']} not found",
            "user_id": payload['user_id'],
            "data":{}
        }  
    except Exception as e:
        return {
            "result": "error",
            "message": "Invalid credentials",
            "user_id": payload['user_id'],
            "data":{}
        }

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
            return {
                "result": "success",
                "user_id": payload['user_id'],
                "role_id": role_access_status,
                "data": {
                    "entered": payload["buildername"]
                }
            }
        else:
            return {
                "result": "error",
                "message": "Access Denied",
                "user_id": payload['user_id'],
                "data": {}
            }
    except Exception as e:
        print(traceback.print_exc())
        return {
            "result": "error",
            "message": str(e),
            "user_id": payload['user_id'],
            "data": {}
        }


@app.post('/getBuilderInfo')
def getBuilderInfo(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    countries = get_countries_from_id(conn=conn)
    cities = get_city_from_id(conn=conn)
    try:
        role_access_status = check_role_access(conn, payload)

        if role_access_status == 1:  
            with conn[0].cursor() as cursor:
                query = "SELECT * FROM builder ORDER BY id;"
                cursor.execute(query)
                data = cursor.fetchall()

                colnames = [desc[0] for desc in cursor.description]
                
                res = []
                for row in data:
                    row_dict = {}
                    for i,colname in enumerate(colnames):
                        row_dict[colname] = row[i]
                    row_dict['country'] = get_name(row_dict['country'],countries)
                    row_dict['city'] = get_name(row_dict['city'],cities)
                    res.append(row_dict)
                
                return {
                    "result": "success",
                    "user_id": payload['user_id'],
                    "role_id": role_access_status,
                    "data":{
                        "builder_info":res
                    }
                }
        else:
            return {
                "result": "error",
                "message": "Access Denied",
                "user_id": payload['user_id'],
                "data":{}
            }
    except Exception as e:
        print(traceback.print_exc())
        return {
            "result": "error",
            "message": f"Invalid credentials {e}",
            "user_id": payload['user_id'],
            "data":{}
        }

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

            return {
                "result": "success",
                "user_id": payload['user_id'],
                "role_id": role_access_status,
                "data": payload  # Return the updated payload
            }
        elif not builder_exists:
            return {
                "result": "error",
                "message": "Builder does not exist",
                "role_id": role_access_status,
                "user_id": payload['user_id'],
                "data": {}
            }
        elif role_access_status != 1:
            return {
                "result": "error",
                "message": "Access denied",
                "role_id": role_access_status,
                "user_id": payload['user_id'],
                "data": {}
            }
        else:
            return {
                "result": "error",
                "message": "Invalid credentials",
                "user_id": payload['user_id'],
                "data": {}
            }
    except KeyError as ke:
        return {
            "result": "error",
            "message": f"key {ke} not found",
            "user_id": payload['user_id'],
            "data": {}
        }
    except Exception as e:
        return {
            "result": "error",
            "message": str(e),
            "user_id": payload['user_id'],
            "data": {}
        }



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
                    return {
                    "result": "success",
                    "user_id": payload['user_id'],
                    "role_id": role_access_status,
                    "data" : {
                        "deleted_user":payload['builder_id']
                        }
                    }
                else:
                    return {
                        "result":"failure",
                        "message":"No Builder with given ID"
                        }
        else:
            return {"result":"failure",
                    "message":"Access Denied"}
    except Exception as e:
        print(traceback.print_exc())
        return {
            "result":"failure",
            "message":"Invalid UserName or UserID"
        }
@app.post('/getStatesAdmin')
async def get_states_admin(payload:dict,conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status==1:
            with conn[0].cursor() as cursor:
                query = "SELECT DISTINCT state,countryid FROM cities"
                cursor.execute(query)
                data = cursor.fetchall()
            return {
                "result": "success",
                "user_id": payload['user_id'],
                "role_id": role_access_status,
                "data": data
            }
        else:
            return {
                "result": "error",
                "message":"Invalid Credentials",
                "user_id": payload['user_id'],
                "role_id": role_access_status,
                "data": data
            }
    except Exception as e:
        print(traceback.print_exc())
        return {
            "result": "error",
            "message": f"{e} error found",
            "role_id": role_access_status,
            "user_id": payload['user_id'],
            "data": {}
        }

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
                
                return {
                    "result": "success",
                    "user_id": payload['user_id'],
                    "role_id": role_access_status,
                    "data": data
                }
            else:
                return {
                    "result": "error",
                    "message": "Access denied",
                    "role_id": role_access_status,
                    "user_id": payload['user_id'],
                    "data": {}
                }
        else:
            return {
                "result": "error",
                "message": "User doesn't exist",
                "role_id": 0,
                "user_id": payload['user_id'],
                "data": {}
            }
    except ValueError as ve:
        print(traceback.print_exc())
        return {
            "result": "error",
            "message": f"{ve} error found",
            "role_id": role_access_status,
            "user_id": payload['user_id'],
            "data": {}
        }
    except Exception as e:
        print(traceback.print_exc())
        return {
            "result": "error",
            "message": f"{e} error found",
            "role_id": role_access_status,
            "user_id": payload['user_id'],
            "data": {}
        }
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
            return {
                "result": "success",
                "user_id": payload['user_id'],
                "role_id": role_access_status,
                "data": res
            }
        else:
            return {
                "result": "error",
                "message":"Invalid Credentials",
                "user_id": payload['user_id'],
                "role_id": role_access_status,
                "data": data
            }
    except Exception as e:
        print(traceback.print_exc())
        return {
            "result": "error",
            "message": f"{e} error found",
            "role_id": role_access_status,
            "user_id": payload['user_id'],
            "data": {}
        }
@app.post('/getCitiesAdmin')
async def get_cities_admin(payload:dict,conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        role_access_status = check_role_access(conn,payload)
        if role_access_status==1:
            with conn[0].cursor() as cursor:
                query = "SELECT id,city,state,countryid FROM cities"
                cursor.execute(query)
                data = cursor.fetchall()
            colnames = [desc[0] for desc in cursor.description]
                
            res = []
            for row in data:
                row_dict = {}
                for i,colname in enumerate(colnames):
                    row_dict[colname] = row[i]
                res.append(row_dict)
            return {
                "result": "success",
                "user_id": payload['user_id'],
                "role_id": role_access_status,
                "data": res
            }
        else:
            return {
                "result": "error",
                "message":"Invalid Credentials",
                "user_id": payload['user_id'],
                "role_id": role_access_status,
                "data": data
            }
    except Exception as e:
        print(traceback.print_exc())
        return {
            "result": "error",
            "message": f"{e} error found",
            "role_id": role_access_status,
            "user_id": payload['user_id'],
            "data": {}
        }

@app.post('/getProjects')
async def get_projects(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    print("here")
    try:
        role_access_status = check_role_access(conn, payload)

        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = "SELECT * FROM project ORDER BY id;"
                cursor.execute(query)
                data = cursor.fetchall()

                colnames = [desc[0] for desc in cursor.description]

                res = []
                for row in data:
                    row_dict = {}
                    for i, colname in enumerate(colnames):
                        row_dict[colname] = row[i]
                    res.append(row_dict)
                return {
                    "result": "success",
                    "user_id": payload['user_id'],
                    "role_id": role_access_status,
                    "data": {
                        "project_info": res
                    }
                }
        else:
            return {
            "result": "error",
            "message": "Username or User ID not found",
            "role_id": role_access_status,
            "user_id": payload['user_id'],
            "data": {}
        }
    except Exception as e:
        return {
            "result": "error",
            "message": "Username or User ID not found",
            "role_id": role_access_status,
            "user_id": payload['user_id'],
            "data": {}
        }
    

@app.post('/getProjectsByBuilder')
async def get_projects(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    print("here")
    try:
        role_access_status = check_role_access(conn, payload)

        if role_access_status == 1:
            with conn[0].cursor() as cursor:
                query = "SELECT * FROM project where builderid=%s ORDER BY id;"
                cursor.execute(query,(payload['builder_id'],))
                data = cursor.fetchall()

                colnames = [desc[0] for desc in cursor.description]

                res = []
                for row in data:
                    row_dict = {}
                    for i, colname in enumerate(colnames):
                        row_dict[colname] = row[i]
                    res.append(row_dict)
                return {
                    "result": "success",
                    "user_id": payload['user_id'],
                    "role_id": role_access_status,
                    "data": {
                        "project_info": res
                    }
                }
        else:
            return {
            "result": "error",
            "message": "Username or User ID not found",
            "role_id": role_access_status,
            "user_id": payload['user_id'],
            "data": {}
            }
    except Exception as e:
        print(traceback.print_exc())
        return {
            "result": "error",
            "message": "Username or User ID not found",
            "role_id": role_access_status,
            "user_id": payload['user_id'],
            "data": {}
        }

@app.post("/addNewProject")
async def add_new_project(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
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

                return {
                    "result": "success",
                    "user_id": payload['user_id'],
                    "role_id": role_access_status,
                    "data": {
                        "entered": payload['projectname'],
                        "project_id": last_row_id
                    }
                }
        else:
            return {
                "result": "error",
                "message": "Access Denied",
                "user_id": payload['user_id'],
                "data": {}
            }
    except Exception as e:
        print(traceback.format_exc())
        return {
            "result": "error",
            "message": str(e),
            "user_id": payload['user_id'],
            "data": {}
        }


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
                
            return {
                "result": "success",
                "user_id": payload['user_id'],
                "role_id": role_access_status,
                "data": {
                    "entered": payload['contactname']
                }
            }
        else:
            return {
                "result": "error",
                "message": "Access Denied",
                "user_id": payload['user_id'],
                "data": {}
            }
    except Exception as e:
        print(traceback.format_exc())
        return {
            "result": "error",
            "message": str(e),
            "user_id": payload['user_id'],
            "data": {}
        }




logger.info("program_started")
