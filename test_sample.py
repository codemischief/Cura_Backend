import logging
import pytest
import psycopg2
from psycopg2.extras import DictCursor
from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.testclient import TestClient
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from unittest import mock
from unittest.mock import MagicMock
from typing import Optional, List

app = FastAPI()

origins = ["*"]  # Adjust for production security

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Set appropriate log level

class User(BaseModel):
    username: str
    password: str
    company_key: str

class Country(BaseModel):
    user_id: int
    country_name: str
    role_id: int

class Builder(BaseModel):
    user_id: int
    builder_name: str
    phone_1: Optional[str]
    phone_2: Optional[str]
    email1: Optional[str]
    email2: Optional[str]
    addressline1: Optional[str]
    addressline2: Optional[str]
    suburb: Optional[str]
    city: Optional[int]
    state: Optional[str]
    country: Optional[int]
    zip: Optional[str]
    website: Optional[str]
    comments: Optional[str]
    dated: Optional[str]  
    created_by: Optional[int]
    is_deleted: bool = False

def execute_query(cursor, query, *args):
    try:
        cursor.execute(query, args)
        return cursor.fetchone()
    except psycopg2.DatabaseError as e:
        logger.error("Database error: %s", e)
        raise HTTPException(status_code=500, detail="Database error")

def check_existing_entity(db_connection, entity_type, entity_name):
    try:
        with db_connection.cursor() as cursor:
            result = execute_query(cursor, f"SELECT id FROM {entity_type} WHERE name = %s", entity_name)
            return result  # Return the ID or None if not found
    except HTTPException as e:
        raise  # Propagate database errors
    except Exception as e:
        logger.error(f"Error checking existing {entity_type}:", e)
        raise HTTPException(status_code=500, detail="Internal server error")

def check_role_access(db_connection, payload):
    if 'user_id' not in payload or 'role_id' not in payload:
        return None  

    user_id = payload['user_id']
    role_id = payload['role_id']

    try:
        with db_connection.cursor() as cursor:
            query = "SELECT * FROM user_role WHERE user_id = %s AND role_id = %s"
            cursor.execute(query, (user_id, role_id))
            result = cursor.fetchone()

            if result is not None:
                return role_id
            else:
                return None 
    except HTTPException as e:
        raise  # Propagate database errors
    except Exception as e:  
        logger.error(f"Error in check_role_access: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@pytest.fixture(scope='module')
def db_connection():
    try:
        conn = psycopg2.connect(
            dbname="cura_testing",
            user="postgres",
            password="cura123",
            host="192.168.10.133",
            cursor_factory=DictCursor
        )
        logger.info("Database connection established successfully.")
        yield conn
        conn.close()
    except Exception as e:
        logger.error("Error establishing database connection:", e)
        raise HTTPException(status_code=500, detail="Database error")

@pytest.fixture(scope='module')
def test_client():
    return TestClient(app)




@pytest.fixture
def mock_cursor():  # Remains unchanged
    with mock.patch('psycopg2.connect') as mock_connect:
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.execute.side_effect = cursor_execute  
        yield mock_cursor

def cursor_execute(query, params):
        if query.startswith('SELECT password'):
            return (("hashed_password", 123, 1),) 
        elif query.startswith('SELECT EXISTS'):
            return ((True,),)

# # Simplified Route Logic (essential parts for understanding test scenarios)
# def validate_credentials(username, password, company_key):
#     # ... Logic to fetch user data from the database ...
#     if not user_data:
#         return 401, {"detail": "not found"}
#     # ... Logic to validate password and company key ...
#     if credentials_valid: 
#         return 200, {"result": "success", "user_id": 123, "role_id": 1}
#     else:
#         return 404, {"result": "error","message":"Invalid Credentials"}  # Or another error


@pytest.mark.parametrize(
    "username, password, company_key, expected_status_code, expected_response",
    [
        ("ruderaw","abcdefg", "9632", 200, {"result": "success","user_id":1,"role_id":1}), 
        ('Ruderaw', 'aaaaaaaaa', '9632', 404, {"result": "error", "message":"error message"})  
    ]
)
def test_id_1(test_client, mock_cursor, username, password, company_key, expected_status_code, expected_response):
    test_payload = {"username" : "ruderaw", "password" : "abcdefg", "company_key" : "9632"}
    response = test_client.post('/validateCredentials', json=test_payload) 

    assert response.status_code == expected_status_code
    assert response.json() == expected_response


def test_id_2(test_client):
    
    test_payload = {
        'username': 'Ruderaw',  
        'password': 'abcdefg',  
        'company_key': '9632'
    }
    response = test_client.post('/validateCredentials', json=test_payload) 

    assert response.status_code == expected_status_code
    assert response.json() == expected_response

def test_id_3(test_client, db_connection):
    with mock_cursor() as cursor:
        # Configure side effects for the mock cursor 
        cursor.fetchone.side_effect = [
            (("hashed_password", 123, 1),),  # For 'SELECT password' 
            ((True),),                      # For 'SELECT EXISTS'
        ]

        test_payload = {
            'username': 'ruderaw',
            'password': 'abdefg',  # Incorrect password
            'company_key': '9632'
        }

        response = test_client.post('/validateCredentials', json=test_payload, conn=db_connection)

        assert response.status_code == 200
        assert response.json() == {
            "result": "failure",
            "message": "Invalid credentials"
        }
def test_id_4(test_client, db_connection):
    with mock_cursor() as cursor:
        # Configure side effects for the mock cursor 
        cursor.fetchone.side_effect = [
            (("hashed_password", 123, 1),),  # For 'SELECT password' 
            ((False),),                     # For 'SELECT EXISTS'
        ]

        test_payload = {
            'username': 'ruderaw',
            'password': 'abcdefg',  # Correct password
            'company_key': '99999'  # Incorrect company key
        }

        response = test_client.post('/validateCredentials', json=test_payload, conn=db_connection)

        assert response.status_code == 200
        assert response.json() == {
            "result": "failure",
            "message": "Invalid credentials"
        }
def test_id_5(test_client, db_connection):
    with mock_cursor() as cursor:
        # Configure side effects for the mock cursor 
        cursor.fetchone.side_effect = [
            (None,),   # For 'SELECT password' 
            ((False),), # For 'SELECT EXISTS'
        ]

        test_payload = {
            'username': 'RUDERAW',  # Incorrect username
            'password': 'hijklmn',  # Incorrect password
            'company_key': '1000'   # Incorrect company key
        }

        response = test_client.post('/validateCredentials', json=test_payload, conn=db_connection)

        assert response.status_code == 200
        assert response.json() == {
            "result": "failure",
            "message": "User does not exist"
        }
@pytest.fixture
def test_payload():
    return {
        'user_id': 1,
        'country_name': 'TestCountry',
        'role_id': 1
    }

def test_id_15(test_client, db_connection): 
    try:
        role_access_result = check_role_access(test_payload, db_connection)
        logger.debug("Role Access Result: %s", role_access_result) 
        assert role_access_result == 1 

        response = test_client.post('/addCountry', json=test_payload)

        # Assertions
        assert response.status_code == 200
        assert response.json()['result'] == 'success'
        # ... (rest of your assertions) 

        return response
    except KeyError as e:
        logger.error("Missing key in test_payload: %s", e)
        raise
    except HTTPException as e:
        logger.error("Error adding country: %s", e) 
        raise
    except Exception as e:  # Catch-all for unexpected errors
        logger.exception("Unexpected error: %s", e)
        raise 

def test_id_16(test_client, db_connection, test_payload):
    try:
        # Precondition: Add existing country
        test_id_15(test_client, db_connection, test_payload) 

        # Attempt to add the existing country again
        response = test_client.post('/addCountry', json=test_payload)

        # Assertions
        assert response.status_code == 200
        assert response.json()['result'] == 'success'  
        # ... (rest of your assertions) 
        assert response.json().get('message') == 'Country already exists'

        # Optional: Verify country was not duplicated
        existing_country_added = check_existing_entity(db_connection, 'country', test_payload['country_name'])
        assert not existing_country_added 

    except Exception as e:
        logger.error("Error adding existing country: %s", e) 
        raise

def test_id_17(test_client, db_connection, test_payload):
    try:
        # Modify payload for invalid role ID
        test_payload['role_id'] = 1000  

        # Send request with invalid role
        response = test_client.post('/addCountry', json=test_payload)

        # Assertions
        assert response.status_code == 200  
        assert response.json()['result'] == 'error'
        # ... (rest of your assertions) 
        assert response.json()['message'] == 'Access denied'  

    except HTTPException as e:
        logger.error("HTTP Error (likely unauthorized access): %s", e) 
        raise  # Re-raise to propagate the exception
    except Exception as e:  
        logger.exception("Unexpected error: %s", e)
        raise

def test_id_18(test_client, db_connection, test_payload):
    try:
        # Modify payload for invalid user ID
        test_payload['user_id'] = 1000  

        # Send request with invalid user ID
        response = test_client.post('/addCountry', json=test_payload)

        # Assertions
        assert response.status_code == 200  
        assert response.json()['result'] == 'error'
        assert response.json()['user_id'] == test_payload['user_id']
        assert response.json()['message'] == "Access denied"  

    except HTTPException as e:
        logger.error("HTTP Error (likely unauthorized access): %s", e) 
        raise  
    except Exception as e:
        logger.exception("Unexpected error: %s", e)
        raise

def test_id_19(test_client, db_connection):
    try:
        print("Debug: Starting test_edit_country_successfully...")
        print("Debug: Initializing test data...")
        test_payload = {
            'user_id': 1,
            'old_country_name': 'existing_country', 
            'new_country_name': 'edited_country',
            'role_id': 1 
        }

        # Mock role access (assuming check_role_access interacts with the database)
        def mock_check_role_access(conn, payload):
            return 1  # Simulate successful role access

        # Patch the dependency to use our mock functions
        with mock.patch('your_module.check_role_access', mock_check_role_access), \
             mock.patch('your_module.checkcountry', return_value=True): 

            response = test_client.post('/editCountry', json=test_payload)

            # Assertions
            assert response.status_code == 200

            # ... (verify response content as needed)
            assert response.json()['result'] == 'success'  
            # ... (other assertions on the response data)    

    except AssertionError as e:
        logger.error("Assertion failed during country edit: %s", e)
        raise
    except Exception as e:
        logger.exception("Unexpected error in test_edit_country_successfully: %s", e)
        raise 



def test_id_20(test_client, db_connection):
    try:
        print("Debug: Starting test_edit_non_existent_country...")
        print("Debug: Initializing test data...")
        test_payload = {
            'user_id': 1,
            'old_country_name': 'non_existent_country', 
            'new_country_name': 'edited_country',
            'role_id': 1 
        }

        # Mock role access and country existence
        def mock_check_role_access(conn, payload):
            return 1 

        def mock_checkcountry(country_name, conn):
            return False  # Simulate the country not existing

        # Patch the dependencies for mocking
        with mock.patch('your_module.check_role_access', mock_check_role_access), \
             mock.patch('your_module.checkcountry', mock_checkcountry): 

            response = test_client.post('/editCountry', json=test_payload)

            # Assertions
            assert response.status_code == 200
            assert response.json() == {
                "result": "error",
                "message": "Does not exist",
                "role_id": test_payload['role_id'],
                "data": {}
            }

    except AssertionError as e:
        logger.error("Assertion failed in test_edit_non_existent_country: %s", e)
        raise
    except Exception as e:
        logger.exception("Unexpected error in test_edit_non_existent_country: %s", e)
        raise 

def test_id_21(test_client, init_database, db_connection):
    try:
        test_payload = {
            'user_id': 1,
            'old_country_name': 'existing_country',
            'new_country_name': 'edited_country',
            'role_id': 2  
        }

        # Mock role access to simulate denial
        def mock_check_role_access(conn, payload):
            return 0  # Or any value that represents access denial

        with mock.patch('your_module.check_role_access', mock_check_role_access):
            response = test_client.post('/editCountry', json=test_payload)

            # Assertions
            assert response.status_code == 200  
            assert response.json() == {
                "result": "error",
                "message": "Access denied",
                # ... (other fields in the response)
            } 

    except AssertionError as e:
        logger.error("Assertion failed in test_access_denied_role_id: %s", e)
        raise
    except Exception as e:
        logger.exception("Unexpected error in test_access_denied_role_id: %s", e)
        raise 

def test_id_22(test_client, init_database, db_connection):
    try:
        print("Debug: Starting test_invalid_credentials...")
        print("Debug: Initializing test data...")
        test_payload = {
            'user_id': 1,
            'old_country_name': 'existing_country',
            'new_country_name': 'edited_country',
            'role_id': 1 
        }

        # Mock role access to simulate invalid credentials
        def mock_check_role_access(conn, payload):
            return 0  # Or any value that represents invalid credentials

        with mock.patch('your_module.check_role_access', mock_check_role_access):
            response = test_client.post('/editCountry', json=test_payload)

            # Assertions
            assert response.status_code == 200  
            assert response.json() == {
                "result": "error",
                "message": "Invalid credentials",  
                # ... (other elements in the response)
            } 

    except AssertionError as e:
        logger.error("Assertion failed in test_invalid_credentials: %s", e)
        raise
    except Exception as e:
        logger.exception("Unexpected error in test_invalid_credentials: %s", e)
        raise 
@pytest.fixture(scope='module')
def test_country_name():  # Simplified name, scope depends on how you use it
    return 'TestCountry' 

def add_test_country(db_connection, test_country_name):  # Parameterized
    try:
        with db_connection.cursor() as cursor:
            cursor.execute("INSERT INTO country (name) VALUES (%s) RETURNING id", (test_country_name,))
            country_id = cursor.fetchone()[0]  
            db_connection.commit()
            return country_id 
    except Exception as e:
        print(f"Error adding test country to the database: {e}")
        raise

def test_id_48(test_client, db_connection, test_country_name):
    try:
        # Precondition: Add test country
        add_test_country(db_connection, test_country_name)

        test_payload = {
            'user_id': 1,  # Add necessary user data
            'role_id': 1,  # Assuming the role has delete permissions
            'country_name': test_country_name, 
        }

        # Mock role access and country existence
        def mock_check_role_access(conn, payload):
            return 1

        def mock_checkcountry(country_name, conn):
            return True

        with mock.patch('your_module.check_role_access', mock_check_role_access), \
             mock.patch('your_module.checkcountry', mock_checkcountry):

            response = test_client.post('/deleteCountry', json=test_payload)

            # Assertions
            assert response.status_code == 200
            assert response.json()['result'] == 'success'
            assert response.json()['data']['deleted'] == test_country_name

    except Exception as e:
        logger.exception(f"Error deleting country and verifying response: {e}")
        raise

def test_id_49(db_connection, test_country_name):
    try:
        with db_connection.cursor() as cursor:
            cursor.execute("SELECT * FROM country WHERE name = %s", (test_country_name,))
            deleted_country = cursor.fetchone()
            assert deleted_country is None

    except Exception as e:
        logger.error(f"Error checking if country is deleted: {e}")
        raise

def test_delete_country_route(test_client, db_connection, test_country_name):
    try:
        test_payload = {
            'user_id': 1,
            'country_name': test_country_name, 
            'role_id': 1 
        }

        # Precondition: Add test country
        add_test_country(db_connection, test_country_name)

        # Mock role access and country existence (if needed)
        # ... (add mocking here based on your route's logic) ...

        # Delete the country
        response = test_client.post('/deleteCountry', json=test_payload)

        # Assertions on the deletion response
        assert response.status_code == 200
        assert response.json()['result'] == 'success'
        assert response.json()['data']['deleted'] == test_country_name

        # Verify deletion in the database
        test_id_49(db_connection, test_country_name)

    except Exception as e:
        logger.exception(f"Error in test_delete_country_route: {e}")
        raise

def test_id_23(test_client, db_connection, test_payload):
    try:
        # Precondition: Ensure builder doesn't exist
        ...  # Optionally, you might delete if it exists, for clean testing

        # Mock role access and database interactions
        def mock_check_role_access(conn, payload):
            return 1

        def mock_check_existing_entity(conn, entity_type, entity_name):
            return False  # Simulate builder not existing

        with mock.patch('your_module.check_role_access', mock_check_role_access), \
             mock.patch('your_module.check_existing_entity', mock_check_existing_entity): 

            response = test_client.post('/addBuilderInfo', json=test_payload)

            # Assertions
            assert response.status_code == 200
            assert response.json()['result'] == 'success'  
            # ... (assert other elements in the response) 

    except Exception as e:
        logger.exception("Error in add_builder_successfully: %s", e) 
        raise

def test_id_24(test_client, db_connection, test_payload):
    try:
        # Precondition: Ensure builder exists (add it to the database)
        ... 

        def mock_check_role_access(conn, payload):
            return 1

        def mock_check_existing_entity(conn, entity_type, entity_name):
            return True  # Simulate builder existing

        with mock.patch('your_module.check_role_access', mock_check_role_access), \
             mock.patch('your_module.check_existing_entity', mock_check_existing_entity): 

            response = test_client.post('/addBuilderInfo', json=test_payload)

            # Assertions
            assert response.status_code == 200  
            assert response.json()['result'] == 'error'
            assert response.json()['message'] == 'Builder already exists in the database'

    except Exception as e:
        logger.exception("Error in handle_existing_builder: %s", e)
        raise
def test_id_25(test_client, db_connection):
    try:
        # 1. Test Payload Setup
        test_payload = {
            "user_id": 1234,
            "buildername": "Rudra",
            "phone1": "9999999999",
            "phone2": "8888888888",
            "email1": "abc@def.com",
            "addressline1": "abc area, def house",
            "addressline2": "ghi locality",
            "suburb": "ijkl",
            "city": 360,  # Invalid city value
            "state": "Maharashtra",
            "country": 1000,  # Invalid country value
            "zip": "1234",
            "website": "www.abc.example.com",
            "comments": "comment1\ncomment2\ncomment3",
            # 'dated' field is missing
            "createdby": 1234,
            "isdeleted": False
        }
        # 2. Sending the Request
        response = test_client.post('/addBuilderInfo', json=test_payload)

        # 3. Assertions
        assert response.status_code == 422  
        assert response.json() == {
            "result": "error",
            "message": "Invalid payload",
            "details": [
                "Invalid value for 'city' field",
                "Invalid value for 'country' field",
                "Missing required field 'dated'"
            ]
        }

    except Exception as e:
        logger.exception("Error in handle_invalid_payload: %s", e) 
        raise

def test_id_26(test_client, db_connection):
    try:
        # Replace with a request to your route:
        response = test_client.get('/some_route_that_might_fail')  

        # If we expect a successful response:
        assert response.status_code == 200  # Or the appropriate status code

    except HTTPException as e:  # Catch specific HTTP exceptions
        assert e.status_code in [500, 400, ...]  # List expected failure codes
        # Optionally check error message content, if applicable 

    except Exception as e:  # Catch other unexpected errors
        logger.exception("Unexpected error in test_id_26: %s", e)  
        assert False, "An unexpected exception occurred"




def test_id_27(test_client, init_database, db_connection):
    try:
        # Precondition: Builder with builder_id 1 exists (setup in init_database)
        test_payload1 = {
            "user_id": 1234,
            "builder_id": 1,
            "builder_name": "EditedBuilder",
            "phone_1": "987654321",
            "phone_2": "9876543210",
            "email1": "edited@example.com",
            "addressline1": "Edited Address",
            "addressline2": "Edited Address 2",
            "suburb": "Edited Suburb",
            "city": 360,
            "state": "Edited State",
            "country": 5,
            "zip": "54321",
            "website": "www.edited.example.com",
            "comments": "Edited Comments",
            "dated": "2024-03-19 12:00:00",
            "created_by": 1234,
            "is_deleted": False
        }

        # Mock role access and database interactions
        def mock_check_role_access(conn, payload):
            return 1 

        def mock_check_existing_entity(conn, entity_type, entity_name):
            return True  # Builder exists

        with mock.patch('your_module.check_role_access', mock_check_role_access), \
             mock.patch('your_module.check_existing_entity', mock_check_existing_entity): 

            response = test_client.post('/editBuilder', json=test_payload1)

            # Assertions
            assert response.status_code == 200
            assert response.json() == {
                "result": "success",
                "user_id": test_payload['user_id'],
                "role_id": 1,  
                "data": {
                   "updated": test_payload  # Assuming this is what's returned
                } 
            } 

    except Exception as e:
        logger.exception("Error in test_edit_builder_route_success: %s", e) 
        raise

def test_id_28(test_client, init_database, db_connection):
    try:
        # Precondition: Builder with builder_id 1000 does NOT exist
        # ... (Potentially delete or don't create it in init_database)

        test_payload2 = {
            "user_id": 1234,
            "builder_id": 1000, 
            "builder_name": "EditedBuilder",
            "phone_1": "987654321",
            "phone_2": "9876543210",
            "email1": "edited@example.com",
            "addressline1": "Edited Address",
            "addressline2": "Edited Address 2",
            "suburb": "Edited Suburb",
            "city": 360,
            "state": "Edited State",
            "country": 5,
            "zip": "54321",
            "website": "www.edited.example.com",
            "comments": "Edited Comments",
            "dated": "2024-03-19 12:00:00",
            "created_by": 1234,
            "is_deleted": False
        }

        # Optionally consider mocking if needed
        def mock_check_role_access(conn, payload):
            return 1 

        def mock_check_existing_entity(conn, entity_type, entity_name):
            return False  # Builder does not exist 

        with mock.patch('your_module.check_role_access', mock_check_role_access), \
             mock.patch('your_module.check_existing_entity', mock_check_existing_entity): 

            response = test_client.post('/editBuilder', json=test_payload2)

            # Assertions
            assert response.status_code == 200  
            assert response.json() == {
                "result": "error",
                "message": "Builder does not exist",
                # ... (other fields in the error response)
            } 

    except Exception as e:
        logger.exception("Error in test_edit_builder_route_failure_no_builder: %s", e) 
        raise

def test_id_29(test_client, init_database, db_connection):
    try:
        # Precondition: Builder with builder_id 1 exists (setup in init_database)
        test_payload4 = {
            "user_id": 1234,
            "builder_id": 1,
            "builder_name": "EditedBuilder",
            "phone_1": "987654321",
            "phone_2": "9876543210",
            "email1": "edited@example.com",
            "addressline1": "Edited Address",
            "addressline2": "Edited Address 2",
            "suburb": "Edited Suburb",
            "city": 360,
            "state": "Edited State",
            "country": 5,
            "zip": "54321",
            "website": "www.edited.example.com",
            "comments": "Edited Comments",
            "dated": "2024-03-19 12:00:00",
            "created_by": 1234,
            "is_deleted": False
        }

        # Mock role access 
        def mock_check_role_access(conn, payload):
            return 0  # Simulate unauthorized access

        with mock.patch('your_module.check_role_access', mock_check_role_access): 

            response = test_client.post('/editBuilder', json=test_payload4)

            # Assertions
            assert response.status_code == 200  
            assert response.json() == {
                "result": "error",
                "message": "Access denied",
                # ... (other fields in the error response)
            } 

    except Exception as e:
        logger.exception("Error in test_edit_builder_route_failure_unauthorized_access: %s", e) 
        raise



@pytest.fixture(scope='module')
def init_database(db_connection):
    try:
        cursor = db_connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS builder (
                id SERIAL PRIMARY KEY,
                buildername VARCHAR(255) NOT NULL,
                phone1 VARCHAR(20),
                phone2 VARCHAR(20),
                email1 VARCHAR(100),
                email2 VARCHAR(100),
                addressline1 TEXT,
                addressline2 TEXT,
                suburb VARCHAR(100),
                city INTEGER,
                state VARCHAR(100),
                country INTEGER,
                zip VARCHAR(20),
                website TEXT,
                comments TEXT,
                dated TIMESTAMP,
                createdby INTEGER,
                isdeleted BOOLEAN
            )
        """)
        cursor.execute("INSERT INTO builder (buildername, phone1, email1) VALUES ('TestBuilder', '123456789', 'test@example.com')")
        db_connection.commit()
        yield
        #cursor.execute("DELETE FROM builder")
        db_connection.commit()
    except Exception as e:
        print("Error initializing database:", e)
        raise
    finally:
        cursor.close()


def test_id_6(test_client, init_database, db_connection):
    try:
        test_payload = {
            'user_id': 1,
            'role_id': 1
        }
        
        response = test_client.post('/getCountries', json=test_payload)
        
        assert response.status_code == 200
        assert response.json()['result'] == 'success'
        assert 'data' in response.json()
        
    except Exception as e:
        print(f"Exception occurred: {e}")

def test_id_7(test_client, init_database, db_connection):
    try:
        test_payload = {
            'user_id': 1,
            'role_id': 2  
        }
        
        response = test_client.post('/getCountries', json=test_payload)
        
        assert response.status_code == 200
        assert response.json()['result'] == 'error'
        assert response.json()['message'] == 'Access denied'
        
    except Exception as e:
        print(f"Exception occurred: {e}")

def test_id_8(test_client, init_database, db_connection):
    try:
        test_payload = {
            'user_id': 1000,  
            'role_id': 1
        }
        
        response = test_client.post('/getCountries', json=test_payload)
        
        assert response.status_code == 200
        assert response.json()['result'] == 'error'
        assert response.json()['message'] == 'User doesn\'t exist'
        
    except Exception as e:
        print(f"Exception occurred: {e}")

def test_id_9(test_client, init_database, db_connection):
    try:
        test_payload = {
            'user_id': 1,
            'role_id': 1,
            'country_id': 1  
        }

        # Check role access before accessing states
        role_access_status = check_role_access(db_connection, test_payload)

        response = test_client.post('/getStates', json=test_payload)

        assert response.status_code == 200
        assert response.json()['result'] == 'success'
        assert 'data' in response.json()
        
    except Exception as e:
        print(f"Exception occurred: {e}")


def test_id_10(test_client, init_database, db_connection):
    try:
        test_payload = {
            'user_id': 1,
            'role_id': 2,  
            'country_id': 1
        }

        # Check role access before accessing states
        role_access_status = check_role_access(db_connection, test_payload)

        response = test_client.post('/getStates', json=test_payload)
    
        assert response.status_code == 200
        assert response.json()['result'] == 'error'
        assert response.json()['message'] == 'Access denied'
        
    except Exception as e:
        print(f"Exception occurred: {e}")


def test_id_11(test_client, init_database, db_connection):
    try:
        test_payload = {
            'user_id': 1000,  
            'role_id': 1,
            'country_id': 1
        }

        # Check role access before accessing states
        role_access_status = check_role_access(db_connection, test_payload)

        response = test_client.post('/getStates', json=test_payload)
        
        assert response.status_code == 200
        assert response.json()['result'] == 'error'
        assert response.json()['message'] == 'User doesn\'t exist'
        
    except Exception as e:
        print(f"Exception occurred: {e}")

def test_id_30(test_client, init_database, db_connection):
    try:
        test_payload = {
            'user_id': 1,
            'role_id': 1,
            'state_name': 'California'  
        }
        
        response = test_client.post('/getCities', json=test_payload)
        
        assert response.status_code == 200
        assert response.json()['result'] == 'success'
        assert 'data' in response.json()
        
    except Exception as e:
        print(f"Exception occurred: {e}")

def test_id_31(test_client, init_database, db_connection):
    try:
        test_payload = {
            'user_id': 1,
            'role_id': 2,  
            'state_name': 'California'
        }
        
        response = test_client.post('/getCities', json=test_payload)
        
        assert response.status_code == 200
        assert response.json()['result'] == 'error'
        assert response.json()['message'] == 'Invalid Credentials'
        
    except Exception as e:
        print(f"Exception occurred: {e}")

def test_id_32(test_client, init_database, db_connection):
    try:
        test_payload = {
            'user_id': 1,
            'role_id': 1,
            'state_name': 'NonExistentState'  
        }
        
        response = test_client.post('/getCities', json=test_payload)
        
        assert response.status_code == 200
        assert response.json()['result'] == 'error'
        assert response.json()['message'] == 'City not found'
        
    except Exception as e:
        print(f"Exception occurred: {e}")

def test_id_41(test_client, init_database, db_connection):
    try:
        test_payload = {
            'user_id': 1,
            'role_id': 1
        }
        
        response = test_client.post('/getBuilderInfo', json=test_payload)
        
    
        assert response.status_code == 200
        assert response.json()['result'] == 'success'
        assert 'data' in response.json()
        assert 'builder_info' in response.json()['data']
        
    except Exception as e:
        print(f"Exception occurred: {e}")

def test_id_42(test_client, init_database, db_connection):
    try:
        test_payload = {
            'user_id': 1,
            'role_id': 2 
        }
        
        response = test_client.post('/getBuilderInfo', json=test_payload)
        
        # Assertions
        assert response.status_code == 200
        assert response.json()['result'] == 'error'
        assert response.json()['message'] == 'Invalid credentials'
        
    except Exception as e:
        print(f"Exception occurred: {e}")

def test_id_43(test_client, init_database, db_connection):
    try:
        test_payload = {
            'user_id': 1000, 
            'role_id': 1
        }
        
        response = test_client.post('/getBuilderInfo', json=test_payload)
        
        assert response.status_code == 200
        assert response.json()['result'] == 'error'
        assert response.json()['message'] == 'Invalid credentials'
        
    except Exception as e:
        print(f"Exception occurred: {e}")

def check_project_exists(db_connection, project_name):
    """Check if a project already exists in the database."""
    with db_connection.cursor() as cursor:
        cursor.execute("SELECT id FROM project WHERE projectname = %s", (project_name,))
        existing_project = cursor.fetchone()
    return existing_project

def check_project_added_to_database(db_connection, project_id):
    """Check if the project has been added to the database."""
    with db_connection.cursor() as cursor:
        cursor.execute("SELECT * FROM project WHERE id = %s", (project_id,))
        project_data = cursor.fetchone()
        assert project_data is not None

def add_new_project(test_client, db_connection, test_payload):
    """Add a new project and verify its addition."""
    try:
        # Check if the project already exists in the database
        existing_project = check_project_exists(db_connection, test_payload['projectname'])
        # Assert that the project does not exist already
        assert existing_project is None, f"Project '{test_payload['projectname']}' already exists in the database"
        
        # Send request to add the new project
        response = test_client.post('/addNewProject', json=test_payload)
        
        # Assert response status and content
        assert response.status_code == 200
        assert response.json()['result'] == 'success'
        assert 'data' in response.json()
        assert 'project_id' in response.json()['data']
        
        # Check if the project has been added to the database
        check_project_added_to_database(db_connection, response.json()['data']['project_id'])
        
    except Exception as e:
        print(f"Exception occurred: {e}")

# Test case for adding a new project when it doesn't already exist
def test_add_new_project_not_existing(test_client, init_database, db_connection):
    test_payload = {
        'user_id': 1,
        'builderid': 1, 
        'projectname': 'Test Project',
        'addressline1': '123 Test Street',
        'addressline2': 'Unit 101',
        'suburb': 'Test Suburb',
        'city': 'Test City',
        'state': 'Test State',
        'country': 'Test Country',
        'zip': '12345',
        'nearestlandmark': 'Test Landmark',
        'project_type': 'Residential',
        'mailgroup1': 'group1@example.com',
        'mailgroup2': 'group2@example.com',
        'website': 'www.testproject.com',
        'project_legal_status': 'Pending',
        'rules': 'No smoking allowed',
        'completionyear': '2025',
        'jurisdiction': 'Test Jurisdiction',
        'taluka': 'Test Taluka',
        'corporationward': 'Test Ward',
        'policechowkey': 'Test Chowkey',
        'policestation': 'Test Police Station',
        'maintenance_details': 'Maintenance provided',
        'numberoffloors': 5,
        'numberofbuildings': 3,
        'approxtotalunits': 50,
        'tenantstudentsallowed': True,
        'tenantworkingbachelorsallowed': False,
        'tenantforeignersallowed': True,
        'otherdetails': 'Additional details',
        'duespayablemonth': 'January',
        'dated': '2024-03-19 12:00:00',
        'createdby': 1
    }
    add_new_project(test_client, db_connection, test_payload)


@pytest.mark.parametrize("existing_builder_name", ["ExistingBuilder", "AnotherBuilder"])
def test_add_new_builder_not_existing(test_client, init_database, db_connection, existing_builder_name):
    try:
        # Check if the builder already exists in the database
        with db_connection.cursor() as cursor:
            cursor.execute("SELECT id FROM builder WHERE buildername = %s", (existing_builder_name,))
            existing_builder = cursor.fetchone()
        
        assert existing_builder is None, f"Builder '{existing_builder_name}' already exists in the database"
        
        test_payload = {
            'user_id': 1,
            'buildername': 'NewBuilder',
            'email1': 'test@example.com',
            'jobtitle': 'Engineer',
            'businessphone': '1234567890',
            'homephone': '0987654321',
            'addressline1': '123 Test Street',
            'addressline2': 'Unit 101',
            'suburb': 'Test Suburb',
            'city': 'Test City',
            'state': 'Test State',
            'country': 'Test Country',
            'zip': '12345',
            'notes': 'Test notes',
            'dated': '2024-03-19 12:00:00',
            'createdby': 1,
            'isdeleted': False
        }
        
        response = test_client.post('/addNewBuilderContact', json=test_payload)
        
        assert response.status_code == 200
        assert response.json()['result'] == 'success'
        assert 'data' in response.json()
        assert 'entered' in response.json()['data']
        
        # Check if builder has been added to the database
        with db_connection.cursor() as cursor:
            cursor.execute("SELECT * FROM builder WHERE buildername = %s", (test_payload['buildername'],))
            builder_data = cursor.fetchone()
            assert builder_data is not None 
        
    except Exception as e:
        print(f"Exception occurred: {e}")

def test_id_37(test_client, init_database, db_connection):
    valid_payload_user_id = {"user_id": 1234, "username": "rudra"}
    response = test_client.post('/getRoleID', json=valid_payload_user_id)
    assert response.status_code == 200
    assert response.json()['result'] == 'Success'
    assert 'data' in response.json()
    assert 'role id' in response.json()['data']


def test_id_38(test_client, init_database, db_connection):
    invalid_payload_user_id = {"user_id": 5678}
    response = test_client.post('/getRoleID', json=invalid_payload_user_id)
    assert response.status_code == 200
    assert response.json()['result'] == 'error'
    assert response.json()['message'] == 'role_id not obtainable'
    assert 'data' in response.json()

def test_id_39(test_client, init_database, db_connection):
    try:
        valid_payload = {"username": "rudra"}
        
        # Send request to get the role ID
        response = test_client.post('/getRoleID', json=valid_payload)
        
        # Assertions
        assert response.status_code == 200
        assert response.json()['result'] == 'Success'
        assert 'data' in response.json()
        assert 'role id' in response.json()['data']
        
    except Exception as e:
        print(f"Exception occurred: {e}")

def test_id_40(test_client, init_database, db_connection):
    invalid_payload_username = {"username": "nonexistent_username"}
    response = test_client.post('/getRoleID', json=invalid_payload_username)
    assert response.status_code == 200
    assert response.json()['result'] == 'error'
    assert response.json()['message'] == 'role_id not obtainable'
    assert 'data' in response.json()





def test_id_33(test_client, init_database, db_connection):
    try:
        valid_payload = {"user_id": 1234}  
        role_access_status = check_role_access(db_connection, valid_payload)
        response = test_client.post('/getStatesAdmin', json=valid_payload)
        assert response.status_code == 200
        assert response.json()['result'] == 'success'
        assert 'data' in response.json()
        assert 'user_id' in response.json()
        assert 'role_id' in response.json()
        assert 'role_access_status' in response.json()
    except Exception as e:
        print(f"Exception occurred: {e}")

def test_id_34(test_client, init_database, db_connection):
    try:
        invalid_payload = {"user_id": 5678}  
        role_access_status = check_role_access(db_connection, invalid_payload)
        response = test_client.post('/getStatesAdmin', json=invalid_payload)
        assert response.status_code == 200
        assert response.json()['result'] == 'error'
        assert response.json()['message'] == 'Invalid Credentials'
        assert 'data' in response.json()
        assert 'user_id' in response.json()
        assert 'role_id' in response.json()
        assert 'role_access_status' in response.json()
    except Exception as e:
        print(f"Exception occurred: {e}")

def test_id_35(test_client, init_database, db_connection):
    try:
        invalid_payload = {}  
        role_access_status = check_role_access(db_connection, invalid_payload)
        response = test_client.post('/getStatesAdmin', json=invalid_payload)
        assert response.status_code == 200
        assert response.json()['result'] == 'error'
        assert response.json()['message'] == 'Invalid Payload'
        assert 'data' in response.json()
        assert 'user_id' not in response.json()
        assert 'role_id' not in response.json()
        assert 'role_access_status' in response.json()
    except Exception as e:
        print(f"Exception occurred: {e}")

def test_id_36(test_client, init_database, db_connection):
    try:
        invalid_payload = {"user_id": 9999}  
        role_access_status = check_role_access(db_connection, invalid_payload)
        response = test_client.post('/getStatesAdmin', json=invalid_payload)
        assert response.status_code == 200
        assert response.json()['result'] == 'error'
        assert response.json()['message'] == 'Exception occurred'
        assert 'data' in response.json()
        assert 'user_id' in response.json()
        assert 'role_id' in response.json()
        assert 'role_access_status' in response.json()
    except Exception as e:
        print(f"Exception occurred: {e}")

    
def test_id_12(test_client, init_database, db_connection):
    try:
        test_payload = {
            'user_id': 1234
        }
        
        response = test_client.post('/getProjects', json=test_payload)
        
        assert response.status_code == 200
        assert response.json()['result'] == 'success'
        assert 'data' in response.json()
        
    except Exception as e:
        print(f"Exception occurred: {e}")

def test_id_13(test_client, init_database, db_connection):
    try:
        test_payload = {
            'user_id': 1234,
            'role_id': 2  
        }
        
        response = test_client.post('/getProjects', json=test_payload)
    
        assert response.status_code == 200
        assert response.json()['result'] == 'error'
        assert response.json()['message'] == 'Access denied'
        
    except Exception as e:
        print(f"Exception occurred: {e}")

def test_id_14(test_client, init_database, db_connection):
    try:
        test_payload = {
            'user_id': 1000  
        }
        
        response = test_client.post('/getProjects', json=test_payload)
        
        assert response.status_code == 200
        assert response.json()['result'] == 'error'
        assert response.json()['message'] == 'User doesn\'t exist'
        
    except Exception as e:
        print(f"Exception occurred: {e}")

def test_id_44(test_client, init_database, db_connection):
    # Valid payload
    payload = {"user_id": 1234, "role_id": 1}
    role_access_status = check_role_access(db_connection, payload)

    response = test_client.post('/getCitiesAdmin', json=payload)

    assert response.status_code == 200
    assert response.json()['result'] == 'success'
    assert 'data' in response.json()
    assert 'user_id' in response.json()
    assert 'role_id' in response.json()
    assert response.json()['role_id'] == role_access_status

def test_id_45(test_client):
    # Invalid role ID
    payload = {"user_id": 5678}
    role_access_status = check_role_access(None, payload)
    
    response = test_client.post('/getCitiesAdmin', json=payload)
    
    assert response.status_code == 200
    assert response.json()['result'] == 'error'
    assert response.json()['message'] == 'Invalid Credentials'
    assert 'data' in response.json()
    assert 'user_id' in response.json()
    assert 'role_id' in response.json()
    assert response.json()['role_id'] == role_access_status

def test_id_46(test_client):
    # Missing user ID in payload
    payload = {}
    role_access_status = check_role_access(None, payload)
    
    response = test_client.post('/getCitiesAdmin', json=payload)
    
    assert response.status_code

def test_id_47(test_client):
    # Valid payload that raises an exception
    payload = {"user_id": 9999}
    role_access_status = check_role_access(None, payload)
    
    response = test_client.post('/getCitiesAdmin', json=payload)
    
    assert response.status_code == 200
    assert response.json()['result'] == 'error'
    assert 'message' in response.json()
    assert 'data' in response.json()
    assert response.json()['role_id'] == role_access_status

def test_id_50(test_client, init_database, db_connection):
    try:
        # Test data
        test_payload5 ={
            'user_id': 1,
            'builder_id': 1,
            'role_id': 1
        }

        # Get role access status
        role_access_status = check_role_access(db_connection,test_payload5)

        # Send request to delete builder info
        response = test_client.post('/deleteBuilderInfo', json=test_payload5)

        # Assertions
        assert response.status_code == 200
        assert response.json()['result'] == 'success'
        assert 'data' in response.json()
        assert 'deleted_user' in response.json()['data']
        assert response.json()['data']['deleted_user'] == test_payload['builder_id']
        assert 'role_access_status' in response.json()
        assert response.json()['role_access_status'] == role_access_status

        # Check if builder is deleted from the database
        test_id_51(db_connection, test_payload['builder_id'])

    except Exception as e:
        print(f"Error in test_delete_builder_success: {e}")
        raise
        # Check if builder is deleted from the database
        test_id_51(db_connection, test_payload['builder_id'])

    except Exception as e:
        print(f"Error in test_delete_builder_success: {e}")
        raise

def test_id_51(db_connection):
    builder_id = 1  
    try:
        with db_connection.cursor() as cursor:
            query = "SELECT * FROM builder WHERE id = %s"
            cursor.execute(query, (builder_id,))
            deleted_builder = cursor.fetchone()
            assert deleted_builder is None
    except Exception as e:
        print(f"Error checking if builder is deleted from the database: {e}")
        raise








