import psycopg2
import bcrypt
from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
import traceback

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
            cursor.execute(query2, (payload['company_key'],))
            key = cursor.fetchone()
            print(userdata,key)
            if userdata is None:
                return giveFailure("User does not exist")
            if userdata and userdata[0]==payload['password'] and key[0]:
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
    

@app.delete('/deleteCountry')
async def delete_country(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        with conn[0].cursor() as cursor:
            # Check if the user exists
            query_user = 'SELECT * FROM usertable WHERE id = %s'
            cursor.execute(query_user, (payload['user_id'],))
            user_data = cursor.fetchone()

            if user_data is None:
                raise HTTPException(status_code=404, detail="User not found")
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
 
@app.post('/getBuilderInfo')
def getBuilderInfo(payload: dict, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    print("here")
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
            return {"result":"failure",
                    "message":"Access Denied"}  # Return an empty list if access is denied
    except Exception as e:
        return {"result":"failure",
                "message":"Invalid credentials"}
