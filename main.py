import psycopg2
import bcrypt
from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# PostgreSQL database URL
DATABASE_URL = "postgresql://postgres:cura123@192.168.10.133:5432/cura_db"

# # Connect to the database using databases library
# db_params = {
#     "host": "192.168.10.133",
#     "database": "cura_db",
#     "user": "postgres",
#     "password": "cura123",
#     "port": "5432"
# }

# try:
#     # Establishing a connection to the database
#     connection = psycopg2.connect(**db_params)
#     # Creating a cursor object to interact with the database
#     cursor = connection.cursor()
#     print('done')
#     # Performing database operations here...
# except (Exception, psycopg2.Error) as error:
#     print(f"Error connecting to the database: {error}")

# Connect to the database using psycopg2
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

# # Define the /addCountry route
# @app.post("/addCountry")
# async def add_country(payload: AddCountryPayload, db: Database = Depends(get_db)):
#     # Check if the user exists
#     query = f"SELECT * FROM users WHERE id = {payload.user_id}"
#     user = await db.fetch_one(query)

#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")

#     # return a simple response
#     return {"message": f"Added {payload.new_country} for user {user['username']}"}
# Define the payload model
@app.get('/validateCredentials')
async def validate_credentials(username: int, password: str, company_key: int, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        with conn[0].cursor() as cursor:
            query = 'SELECT * FROM login WHERE user_id = %s' 
            #todo : change table
            cursor.execute(query, (username,))
            userdata = cursor.fetchone()

            if userdata and password == userdata[1] and company_key == userdata[2]:
                return giveSuccess(username)
            else:
                return giveFailure("Invalid credentials")

    except Exception as e:
        return giveFailure(f'{e} ab')

def giveSuccess(user_id: int):
    return {"result": "success", "user_id": user_id}

def giveFailure(message: str):
    return {"result": "failure", "message": message}

@app.get('/getRoleID')
async def get_role_id(user_id: int, db_params: tuple = Depends(get_db_connection)):
    #todo : add username access
    conn, cursor = db_params
    try:
        # Fetch role_id from the "users" table in the "cura_db" database using psycopg2
        query = "SELECT role_id FROM login WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        role_id = cursor.fetchone()

        if role_id is None:
            raise HTTPException(status_code=404, detail="User not found")

        # Return success with user role_id
        return {
            "role_id": role_id[0]
        }
    except HTTPException as e:
        # Catch and re-raise HTTPException to preserve the HTTP status code
        raise
    except Exception as e:
        return {
            "result": "error",
            "message": f'{e}',
        }

def role_id(user_id: int, db_params: tuple = Depends(get_db_connection)):
    conn, cursor = db_params
    try:
        # Fetch role_id from the "users" table in the "cura_db" database using psycopg2
        query = "SELECT role_id FROM login WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        role_id = cursor.fetchone()

        if role_id is None:
            raise HTTPException(status_code=404, detail="User not found")

        # Return success with user role_id
        return {
            "role_id": role_id[0]
        }
    except HTTPException as e:
        # Catch and re-raise HTTPException to preserve the HTTP status code
        raise
    except Exception as e:
        return {
            "result": "error",
            "message": f'{e}',
        }


@app.post('/addCountry')
async def add_country(user_id: int,name :str, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        with conn[0].cursor() as cursor:
            # Check if the user exists
            query_user = 'SELECT * FROM usertable WHERE id = %s'
            cursor.execute(query_user, (user_id,))
            user_data = cursor.fetchone()

            if user_data is None:
                raise HTTPException(status_code=404, detail="User not found")
            id = cursor.execute('SELECT COUNT(*) FROM country')
            id = cursor.fetchone()
            id = id[0]+1
            # Insert new country data into the database
            query_insert = 'INSERT INTO country (id,name) VALUES (%s,%s)'
            cursor.execute(query_insert, (id, name))

            # Commit the transaction
            conn[0].commit()

            return {
                "result": "success",
                "role_id": user_data[1],  # Assuming role_id is in the users table
                "user_id": user_id
            }
    except Exception as e:
        return giveFailure(f'{e}')

@app.post("/editCountry")
async def edit_country(user_id: str, name: str, country_name: str, conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        # Check user role
        role = role_id(user_id, conn)
        if role['role_id'] == 1:
            with conn[0].cursor() as cursor:
                # Update country name in the database
                query_update = "UPDATE country SET name = %s WHERE name = %s"
                cursor.execute(query_update, (name, country_name))

                # Commit the transaction
                conn[0].commit()

            return {
                "result": "success",
                "user_id": user_id
            }

    except HTTPException as e:
        # Catch and re-raise HTTPException to preserve the HTTP status code
        raise "error"

    except Exception as e:
        return {
            "result": "error",
            "message": f'{e}',
            "role_id": 1,  # Default role_id in case of an error
            "user_id": user_id
        }
        
@app.delete('/deleteCountry')
async def delete_country(user_id: int, country: str , conn: psycopg2.extensions.connection = Depends(get_db_connection)):
    try:
        with conn[0].cursor() as cursor:
            # Check if the user exists
            query_user = 'SELECT * FROM usertable WHERE id = %s'
            cursor.execute(query_user, (user_id,))
            user_data = cursor.fetchone()

            if user_data is None:
                raise HTTPException(status_code=404, detail="User not found")

            # Delete country data from the database
            query_delete = 'DELETE FROM country WHERE name = %s'
            cursor.execute(query_delete, (country,))

            # Commit the transaction
            conn[0].commit()

            return {
                "result": "success",
                "user_id": user_id
            }

    except HTTPException as e:
        # Catch and re-raise HTTPException to preserve the HTTP status code
        raise

    except Exception as e:
        return giveFailure(f'{e}')

@app.post('/addNewUser')
async def add_new_user(payload):
    try:
        #==========logic========
        return {{
            "result":"success",
            "role_id":1,
            "user_id":payload['user_id']} 
        }
    except Exception as e:
        return {
            "result" : "error",
            "message" : f'{e}',
            "role_id" : 1, #===return value of user role===
            "user_id" : payload['user_id']
        }

@app.delete('/deleteUser')
async def delete_user(payload):
    try:
        #==========logic========
        return {{
            "result":"success",
            "role_id":1,
            "user_id":payload['user_id']} 
        }
    except Exception as e:
        return {
            "result" : "error",
            "message" : f'{e}',
            "role_id" : 1, #===return value of user role===
            "user_id" : payload['user_id']
        }

@app.post('/editUser')
async def edit_user(payload):
    try:
        #==========logic========
        return {{
            "result":"success",
            "role_id":1,
            "user_id":payload['user_id']} 
        }
    except Exception as e:
        return {
            "result" : "error",
            "message" : f'{e}',
            "role_id" : 1, #===return value of user role===
            "user_id" : payload['user_id']
        }

@app.post('/addLob')
async def add_lob(payload):
    try:
        #==========logic========
        return {{
            "result":"success",
            "role_id":1,
            "user_id":payload['user_id']} 
        }
    except Exception as e:
        return {
            "result" : "error",
            "message" : f'{e}',
            "role_id" : 1, #===return value of user role===
            "user_id" : payload['user_id']
        }

@app.post('/editLob')
async def edit_lob(payload):
    try:
        #==========logic========
        return {{
            "result":"success",
            "role_id":1,
            "user_id":payload['user_id']} 
        }
    except Exception as e:
        return {
            "result" : "error",
            "message" : f'{e}',
            "role_id" : 1, #===return value of user role===
            "user_id" : payload['user_id']
        }

@app.delete('/deleteLob')
async def delete_Lob(payload):
    try:
        #==========logic========
        return {{
            "result":"success",
            "role_id":1,
            "user_id":payload['user_id']} 
        }
    except Exception as e:
        return {
            "result" : "error",
            "message" : f'{e}',
            "role_id" : 1, #===return value of user role===
            "user_id" : payload['user_id']
        }

@app.post('/addState')
async def add_state(payload):
    try:
        #==========logic========
        return {{
            "result":"success",
            "role_id":1,
            "user_id":payload['user_id']} 
        }
    except Exception as e:
        return {
            "result" : "error",
            "message" : f'{e}',
            "role_id" : 1, #===return value of user role===
            "user_id" : payload['user_id']
        }

@app.post('/editState')
async def edit_state(payload):
    try:
        #==========logic========
        return {{
            "result":"success",
            "role_id":1,
            "user_id":payload['user_id']} 
        }
    except Exception as e:
        return {
            "result" : "error",
            "message" : f'{e}',
            "role_id" : 1, #===return value of user role===
            "user_id" : payload['user_id']
        }


@app.delete('/deleteState')
async def delete_state(payload):
    try:
        #==========logic========
        return {{
            "result":"success",
            "role_id":1,
            "user_id":payload['user_id']} 
        }
    except Exception as e:
        return {
            "result" : "error",
            "message" : f'{e}',
            "role_id" : 1, #===return value of user role===
            "user_id" : payload['user_id']
        }


@app.post('/addService')
async def add_service(payload):
    try:
        #==========logic========
        return {{
            "result":"success",
            "role_id":1,
            "user_id":payload['user_id']} 
        }
    except Exception as e:
        return {
            "result" : "error",
            "message" : f'{e}',
            "role_id" : 1, #===return value of user role===
            "user_id" : payload['user_id']
        }


@app.post('editService')
async def edit_service(payload):
    try:
        #==========logic========
        return {{
            "result":"success",
            "role_id":1,
            "user_id":payload['user_id']} 
        }
    except Exception as e:
        return {
            "result" : "error",
            "message" : f'{e}',
            "role_id" : 1, #===return value of user role===
            "user_id" : payload['user_id']
        }


@app.delete('/deleteService')
async def delete_service(payload):
    try:
        #==========logic========
        return {{
            "result":"success",
            "role_id":1,
            "user_id":payload['user_id']} 
        }
    except Exception as e:
        return {
            "result" : "error",
            "message" : f'{e}',
            "role_id" : 1, #===return value of user role===
            "user_id" : payload['user_id']
        }

@app.post('/addLocality')
async def add_locality(payload):
    try:
        #==========logic========
        return {{
            "result":"success",
            "role_id":1,
            "user_id":payload['user_id']} 
        }
    except Exception as e:
        return {
            "result" : "error",
            "message" : f'{e}',
            "role_id" : 1, #===return value of user role===
            "user_id" : payload['user_id']
        }

@app.post('editLocality')
async def edit_locality(payload):
    try:
        #==========logic========
        return {{
            "result":"success",
            "role_id":1,
            "user_id":payload['user_id']} 
        }
    except Exception as e:
        return {
            "result" : "error",
            "message" : f'{e}',
            "role_id" : 1, #===return value of user role===
            "user_id" : payload['user_id']
        }

@app.delete('/deleteLocality')
async def delete_locality(payload):
    try:
        #==========logic========
        return {{
            "result":"success",
            "role_id":1,
            "user_id":payload['user_id']} 
        }
    except Exception as e:
        return {
            "result" : "error",
            "message" : f'{e}',
            "role_id" : 1, #===return value of user role===
            "user_id" : payload['user_id']
        }


@app.post('/addEmployee')
async def add_employee(payload):
    try:
        #==========logic========
        return {{
            "result":"success",
            "role_id":1,
            "user_id":payload['user_id']} 
        }
    except Exception as e:
        return {
            "result" : "error",
            "message" : f'{e}',
            "role_id" : 1, #===return value of user role===
            "user_id" : payload['user_id']
        }

@app.post('/editEmployee')
async def edit_employee(payload):
    try:
        #==========logic========
        return {{
            "result":"success",
            "role_id":1,
            "user_id":payload['user_id']} 
        }
    except Exception as e:
        return {
            "result" : "error",
            "message" : f'{e}',
            "role_id" : 1, #===return value of user role===
            "user_id" : payload['user_id']
        }

@app.delete('/deleteEmployee')
async def delete_employee(payload):
    try:
        #==========logic========
        return {{
            "result":"success",
            "role_id":1,
            "user_id":payload['user_id']} 
        }
    except Exception as e:
        return {
            "result" : "error",
            "message" : f'{e}',
            "role_id" : 1, #===return value of user role===
            "user_id" : payload['user_id']
        }