import pytest
from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.testclient import TestClient
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from main import app
import psycopg2
import traceback
import logging
logger = logging.getLogger(__name__)


def execute_query(cursor, query, *args):
    try:
        cursor.execute(query, args)
        return cursor.fetchone()
    except Exception as e:
        print("Error executing query:", e)
        raise

def check_existing_entity(db_connection, entity_type, entity_name):
    try:
        cursor = db_connection.cursor()
        result = execute_query(cursor, f"SELECT id FROM {entity_type} WHERE name = %s", entity_name)
        cursor.close()
        return result
    except Exception as e:
        print(f"Error checking existing {entity_type}:", e)
        raise

@pytest.fixture(scope='module')
def db_connection():
    try:
        conn = psycopg2.connect(
            dbname="cura_testing",
            user="postgres",
            password="cura123",
            host="192.168.10.133"
        )
        print("Database connection established successfully.")
        yield conn
        conn.close()
    except Exception as e:
        print("Error establishing database connection:", e)
        raise

@pytest.fixture(scope='module')
def test_client():
    return TestClient(app)

def check_role_access(conn,db_connection, payload):
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
    pass
def test_id_15(test_client, db_connection, test_payload):
    try:
        # Check role access before adding country
        assert check_role_access(db_connection, test_payload)

        # Send request to add country
        response = test_client.post('/addCountry', json=test_payload)
        
        # Assert response status and content
        assert response.status_code == 200
        assert response.json()['result'] == 'success'
        assert response.json()['role_id'] == test_payload['role_id']
        assert response.json()['user_id'] == test_payload['user_id']
        assert response.json()['data']['added'] == test_payload['country_name']

        # Check if country exists in the database
        country_exists = check_existing_entity(db_connection, 'country', test_payload['country_name'])
        assert country_exists

        return response
    except Exception as e:
        print(f"Error adding country successfully: {e}")
        raise

def test_id_16(test_client, db_connection, test_payload):
    try:
        # Send request to add existing country
        response = test_client.post('/addCountry', json=test_payload)
        
        # Assert response status and content
        assert response.status_code == 200
        assert response.json()['result'] == 'error'
        assert response.json()['role_id'] == test_payload['role_id']
        assert response.json()['user_id'] == test_payload['user_id']
        assert response.json()['message'] == 'Country already exists'

    except Exception as e:
        print(f"Error adding existing country: {e}")
        raise

def test_id_17(test_client, db_connection, test_payload):
    try:
        # Modify payload to have invalid role ID
        test_payload['role_id'] = 2

        # Send request with invalid role ID
        response = test_client.post('/addCountry', json=test_payload)
        
        # Assert response status and content
        assert response.status_code == 200
        assert response.json()['result'] == 'error'
        assert response.json()['role_id'] == test_payload['role_id']
        assert response.json()['user_id'] == test_payload['user_id']
        assert response.json()['message'] == 'Access denied'

    except Exception as e:
        print(f"Error giving unauthorized access: {e}")
        raise

def test_id_18(test_client, db_connection, test_payload):
    try:
        # Modify payload to have invalid user ID
        test_payload['user_id'] = 1000

        # Send request with invalid user ID
        response = test_client.post('/addCountry', json=test_payload)
        
        # Assert response status and content
        assert response.status_code == 200
        assert response.json()['result'] == 'error'
        assert response.json()['user_id'] == test_payload['user_id']
        assert response.json()['message'] == f"User {test_payload['user_id']} not found"

    except Exception as e:
        print(f"Error validating error response: {e}")
        raise



def test_id_19(test_client, init_database, db_connection):
    try:
        print("Debug: Starting test_edit_country_successfully...")
        print("Debug: Initializing test data...")
        test_payload = {
            'user_id': 1,
            'old_country_name': 'existing_country',
            'new_country_name': 'edited_country',
            'role_id': 1
        }

        # Checking role access
        assert check_role_access(db_connection, test_payload)

        response = test_client.post('/editCountry', json=test_payload)
        assert response.status_code == 200
        old_country_exists = check_existing_entity(db_connection, 'country', test_payload['old_country_name'])
        new_country_exists = check_existing_entity(db_connection, 'country', test_payload['new_country_name'])
        if old_country_exists and new_country_exists:
            assert response.json() == {
                "result": "success",
                "user_id": test_payload['user_id'],
                "role_id": test_payload['role_id'],
                "data": {
                    "original": test_payload['old_country_name'],
                    "new_country": test_payload['new_country_name']
                }
            }
        else:
            raise AssertionError("Error editing country: Country not successfully updated or not found")

    except Exception as e:
        print("Error in test_edit_country_successfully:", e)
        raise


def test_id_20(test_client, init_database, db_connection):
    try:
        print("Debug: Starting test_edit_non_existent_country...")
        print("Debug: Initializing test data...")
        test_payload = {
            'user_id': 1,
            'old_country_name': 'non_existent_country',
            'new_country_name': 'edited_country',
            'role_id': 1
        }

        # Checking role access
        assert check_role_access(db_connection, test_payload)

        response = test_client.post('/editCountry', json=test_payload)
        assert response.status_code == 200
        assert response.json() == {
            "result": "error",
            "message": "Does not exist",
            "role_id": test_payload['role_id'],
            "data": {}
        }

    except Exception as e:
        print("Error in test_edit_non_existent_country:", e)
        raise


def test_id_21(test_client, init_database, db_connection):
    try:
        print("Debug: Starting test_access_denied_role_id...")
        print("Debug: Initializing test data...")
        test_payload = {
            'user_id': 1,
            'old_country_name': 'existing_country',
            'new_country_name': 'edited_country',
            'role_id': 2  # Unauthorized role ID
        }

        # Checking role access
        assert check_role_access(db_connection, test_payload)

        response = test_client.post('/editCountry', json=test_payload)
        assert response.status_code == 200
        assert response.json() == {
            "result": "error",
            "message": "Access denied",
            "user_id": test_payload['user_id'],
            "role_id": test_payload['role_id'],
            "data": {}
        }

    except Exception as e:
        print("Error in test_access_denied_role_id:", e)
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

        # Modify payload to trigger invalid credentials scenario
        test_payload['role_id'] = 0

        # Checking role access
        assert check_role_access(db_connection, test_payload)

        response = test_client.post('/editCountry', json=test_payload)
        assert response.status_code == 200
        assert response.json() == {
            "result": "error",
            "message": "Invalid credentials",
            "user_id": test_payload['user_id'],
            "data": {}
        }

    except Exception as e:
        print("Error in test_invalid_credentials:", e)
        raise

def add_test_country(db_connection, country_name):
    try:
        with db_connection.cursor() as cursor:
            cursor.execute("INSERT INTO country (name) VALUES (%s)", (country_name,))
            db_connection.commit()
    except Exception as e:
        print(f"Error adding test country to the database: {e}")
        raise

def test_id_47(test_client, db_connection, test_payload):
    try:
        response = test_client.post('/deleteCountry', json=test_payload)
        
        assert response.status_code == 200
        assert response.json()['result'] == 'success'
        assert response.json()['data']['deleted'] == test_payload['country_name']
        
        return response
    except Exception as e:
        print(f"Error deleting country and verifying response: {e}")
        raise

def test_id_48(db_connection, country_name):
    try:
        with db_connection.cursor() as cursor:
            cursor.execute("SELECT * FROM country WHERE name = %s", (country_name,))
            deleted_country = cursor.fetchone()
            assert deleted_country is None
    except Exception as e:
        print(f"Error checking if country is deleted from the database: {e}")
        raise

@pytest.mark.parametrize("country_name", ['TestCountry1', 'TestCountry2'])
def test_delete_country_route(test_client, init_database, db_connection, country_name):
    try:
        # Test data
        test_payload = {
            'user_id': 1,
            'country_name': country_name,
            'role_id': 1
            
        }

        # Add test country to the database
        add_test_country(db_connection, test_payload['country_name'])

        # Send request to delete country and verify response
        response = test_id_47(test_client, db_connection, test_payload)

        # Check if country is deleted from the database
        test_id_48(db_connection, test_payload['country_name'])

    except Exception as e:
        print(f"Error in test_delete_country_route: {e}")
        raise

def test_id_23(test_client, db_connection, test_payload):
    try:
        # Checking if the builder already exists in the database
        existing_builder = check_existing_entity(db_connection, 'builder', test_payload['buildername'])
        assert not existing_builder, "Builder already exists in the database"

        # Checking role_access
        role_access_status = check_role_access(db_connection, test_payload)
        assert role_access_status == 1  

        # Sending request to add the builder
        response = test_client.post('/addBuilderInfo', json=test_payload)
        
        # Asserting response status and content
        assert response.status_code == 200
        assert response.json() == {
            "result": "success",
            "user_id": 1,  
            "role_id": 1,  
            "data": {"entered": test_payload['buildername']}
        }

    except Exception as e:
        print("Error in add_builder_successfully:", e)
        raise

def test_id_24(test_client, db_connection, test_payload):
    try:
        # Checking if the builder already exists in the database
        existing_builder = check_existing_entity(db_connection, 'builder', test_payload['buildername'])
        assert existing_builder, "Builder does not exist in the database"

        # Sending request to add the builder which already exists
        response = test_client.post('/addBuilderInfo', json=test_payload)
        
        # Asserting response status and content
        assert response.status_code == 200
        assert response.json() == {
            "result": "error",
            "message": "Builder already exists in the database",
            "role_id": 1,  
            "user_id": test_payload['user_id'],  
            "data": {}
        }

    except Exception as e:
        print("Error in handle_existing_builder:", e)
        raise

def test_id_25(test_client, db_connection):
    try:
        # Payload missing required field 'buildername'
        test_payload = {
    "user_id": 1234,
    "buildername": "Rudra",
    "phone1": "9999999999",
    "phone2": "8888888888",
    "email1": "abc@def.com",
    "addressline1": "abc area, def house",
    "addressline2": "ghi locality",
    "suburb": "ijkl",
    "city": 360,
    "state": "Maharashtra",
    "country": 5,
    "zip": "1234",
    "website": "www.abc.example.com",
    "comments": "comment1\ncomment2\ncomment3",
    "dated": "10-03-2024 08:29:00",
    "createdby": 1234,
    "isdeleted": False
}


        # Sending request with invalid payload
        response = test_client.post('/addBuilderInfo', json=test_payload)
        
        # Asserting response status
        assert response.status_code == 422  # Unprocessable Entity
        # Add more assertions for specific error handling if needed

    except Exception as e:
        print("Error in handle_invalid_payload:", e)
        raise

def test_id_26(test_client, db_connection):
    try:
        # Triggering an exception in the test case
        1 / 0

    except Exception as e:
        print("Exception occurred:", e)
        # Add assertions or error reporting for proper exception handling

    finally:
        # Clean-up code if any
        pass



def test_id_27(test_client, init_database, db_connection):
    try:
        # Prepare test payload
        test_payload = {
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

        # Check role access before editing builder info
        role_access_status = check_role_access(db_connection, test_payload)
        assert role_access_status == 1  # Assuming role access status 1 means access granted

        # Make the request to edit the builder info
        response = test_client.post('/editBuilder', json=test_payload)

        # Assertions
        assert response.status_code == 200
        assert response.json() == {
            "result": "success",
            "user_id": test_payload['user_id'],
            "role_id": 1,  # Assuming the role_id in the response should be 1
            "data": test_payload
        }

    except Exception as e:
        print("Error in test_edit_builder_route_success:", e)
        raise

def test_id_28(test_client, init_database, db_connection):
    try:
        # Prepare test payload
        test_payload = {
            "user_id": 1234,
            "builder_id": 1000,  # Assuming this builder ID doesn't exist
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

        # Checking role access
        role_access_status = check_role_access(db_connection, test_payload)
        assert role_access_status == 1  

        # Make the request to edit the builder info
        response = test_client.post('/editBuilder', json=test_payload)

        # Assertions
        assert response.status_code == 200
        assert response.json() == {
            "result": "error",
            "message": "Builder does not exist",
            "role_id": 1,  
            "user_id": test_payload['user_id'],
            "data": {}
        }

    except Exception as e:
        print("Error in test_edit_builder_route_failure_no_builder:", e)
        raise

def test_id_29(test_client, init_database, db_connection):
    try:
        # Prepare test payload
        test_payload = {
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

        # Assume role access status 0 means unauthorized access
        # Check role access before editing builder info
        role_access_status = check_role_access(db_connection, test_payload)
        assert role_access_status == 0  

        # Make the request to edit the builder info
        response = test_client.post('/editBuilder', json=test_payload)

        # Assertions
        assert response.status_code == 200
        assert response.json() == {
            "result": "error",
            "message": "Access denied",
            "role_id": 0,  # Assuming the role_id in the response should be 0 for unauthorized access
            "user_id": test_payload['user_id'],
            "data": {}
        }

    except Exception as e:
        print("Error in test_edit_builder_route_failure_unauthorized_access:", e)
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

def test_delete_builder_info_route_success(test_client, init_database, db_connection):
    test_payload = {
        "user_id": 1234,
        "builder_id": 1
    }
    response = test_client.post('/deleteBuilderInfo', json=test_payload)
    assert response.status_code == 200
    assert response.json() == {
        "result": "success",
        "user_id": test_payload['user_id'],
        "role_id": 1,
        "data": {
            "deleted_user": test_payload['builder_id']
        }
    }

def test_delete_builder_info_route_failure_no_builder(test_client, init_database, db_connection):
    test_payload = {
        "user_id": 1234,
        "builder_id": 1000
    }
    response = test_client.post('/deleteBuilderInfo', json=test_payload)
    assert response.status_code == 200
    assert response.json() == {
        "result": "failure",
        "message": "No Builder with given ID",
        "role_id": 1,
        "user_id": test_payload['user_id']
    }

def test_delete_builder_info_route_failure_access_denied(test_client, init_database, db_connection):
    test_payload = {
        "user_id": 1234,
        "builder_id": 1
    }
    response = test_client.post('/deleteBuilderInfo', json=test_payload)
    assert response.status_code == 200
    assert response.json() == {
        "result": "failure",
        "message": "Access Denied",
        "role_id": 2,  
        "user_id": test_payload['user_id']
    }


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
        assert response.json()['message'] == 'State not found'
        
    except Exception as e:
        print(f"Exception occurred: {e}")

def test_id_40(test_client, init_database, db_connection):
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

def test_id_41(test_client, init_database, db_connection):
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

def test_id_42(test_client, init_database, db_connection):
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
    invalid_payload_username = {"username": "nonexistent_username"}
    response = test_client.post('/getRoleID', json=invalid_payload_username)
    assert response.status_code == 200
    assert response.json()['result'] == 'error'
    assert response.json()['message'] == 'role_id not obtainable'
    assert 'data' in response.json()


def test_id_40(test_client, init_database, db_connection):
    invalid_payload_user_id = {"user_id": 9999}
    response = test_client.post('/getRoleID', json=invalid_payload_user_id)
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

def test_id_43(test_client):
    # Valid payload with admin role
    payload = {"user_id": 1234}
    role_access_status = check_role_access(None, payload)
    
    response = test_client.post('/getCitiesAdmin', json=payload)
    
    assert response.status_code == 200
    assert response.json()['result'] == 'success'
    assert 'data' in response.json()
    assert 'user_id' in response.json()
    assert 'role_id' in response.json()
    assert response.json()['role_id'] == role_access_status

def test_id_44(test_client):
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

def test_id_45(test_client):
    # Missing user ID in payload
    payload = {}
    role_access_status = check_role_access(None, payload)
    
    response = test_client.post('/getCitiesAdmin', json=payload)
    
    assert response.status_code == 200
    assert response.json()['result'] == 'error'
    assert response.json()['message'] == 'Invalid Payload'
    assert 'data' in response.json()
    assert response.json()['role_id'] == role_access_status

def test_id_46(test_client):
    # Valid payload that raises an exception
    payload = {"user_id": 9999}
    role_access_status = check_role_access(None, payload)
    
    response = test_client.post('/getCitiesAdmin', json=payload)
    
    assert response.status_code == 200
    assert response.json()['result'] == 'error'
    assert 'message' in response.json()
    assert 'data' in response.json()
    assert response.json()['role_id'] == role_access_status

def test_id_49(test_client, init_database, db_connection):
    try:
        # Test data
        test_payload = {
            'user_id': 1,
            'builder_id': 1,
            'role_id': 1
        }

        # Get role access status
        role_access_status = check_role_access(db_connection, test_payload)

        # Send request to delete builder info
        response = test_client.post('/deleteBuilderInfo', json=test_payload)

        # Assertions
        assert response.status_code == 200
        assert response.json()['result'] == 'success'
        assert 'data' in response.json()
        assert 'deleted_user' in response.json()['data']
        assert response.json()['data']['deleted_user'] == test_payload['builder_id']
        assert 'role_access_status' in response.json()
        assert response.json()['role_access_status'] == role_access_status

        # Check if builder is deleted from the database
        test_id_50(db_connection, test_payload['builder_id'])

    except Exception as e:
        print(f"Error in test_delete_builder_success: {e}")
        raise

def test_id_50(db_connection, builder_id):
    try:
        with db_connection.cursor() as cursor:
            query = "SELECT * FROM builder WHERE id = %s"
            cursor.execute(query, (builder_id,))
            deleted_builder = cursor.fetchone()
            assert deleted_builder is None
    except Exception as e:
        print(f"Error checking if builder is deleted from the database: {e}")
        raise








