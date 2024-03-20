import pytest
from fastapi.testclient import TestClient
from main import app
import psycopg2
import asyncio

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

@pytest.fixture(scope='module')
def init_database(db_connection):
    try:
        print("Debug: Initializing database...")
        cursor = db_connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS country (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) UNIQUE NOT NULL
            )
        """)
        cursor.execute("SELECT COUNT(*) FROM country")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO country (name) VALUES ('TestCountry')")
        db_connection.commit()
        yield
        # cursor.execute("DROP TABLE IF EXISTS country")
        db_connection.commit()
    except Exception as e:
        print("Error initializing database:", e)
        raise




def test_add_country_route(test_client, init_database, db_connection):
    try:
        print("Debug: Starting test_add_country_route...")
        print("Debug: Initializing test data...")
        test_payload = {
            'country_name': 'test_country1',
            'user_id': 1,
            'role_id': 1
        }
        response = test_client.post('/addCountry', json=test_payload)
        assert response.status_code == 200
        country_exists = check_existing_entity(db_connection, 'country', test_payload['country_name'])
        if country_exists:
            assert response.json() == {
                "result": "success",
                "role_id": test_payload['role_id'],
                "user_id": test_payload['user_id'],
                "data": {"added": test_payload['country_name']}
            }
        else:
            assert response.json() == {
                "result": "success",
                "role_id": test_payload['role_id'],
                "user_id": test_payload['user_id'],
                "data": {"added": test_payload['country_name']}
            }

    except Exception as e:
        print("Error in test_add_country_route:", e)
        raise

def test_edit_country_route(test_client, init_database, db_connection):
    try:
        print("Debug: Starting test_edit_country_route...")
        print("Debug: Initializing test data...")
        test_payload = {
            'user_id': 1,
            'old_country_name': 'some_country',
            'new_country_name': 'edited_country',
            'role_id': 1
        }
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
        elif not old_country_exists:
            assert response.json() == {
                "result": "error",
                "message": "Does not exist",
                "role_id": test_payload['role_id'],
                "data": {}
            }
        elif test_payload['role_id'] != 1:
            assert response.json() == {
                "result": "error",
                "message": "Access denied",
                "user_id": test_payload['user_id'],
                "role_id": test_payload['role_id'],
                "data": {}
            }
        else:
            assert response.json() == {
                "result": "error",
                "message": "Invalid credentials",
                "user_id": test_payload['user_id'],
                "data": {}
            }

    except Exception as e:
        print("Error in test_edit_country_route:", e)
        raise

def test_add_builder_info_route(test_client, init_database, db_connection):
    try:
        existing_builder = check_existing_entity(db_connection, 'builder', 'Rudra')
        if existing_builder:
            assert False, "Builder already exists in the database"

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
        response = test_client.post('/addBuilderInfo', json=test_payload)
        assert response.status_code == 200
        assert response.json() == {
            "result": "success",
            "user_id": 1,
            "role_id": 1,
            "data": {"entered": "Rudra"}
        }

    except Exception as e:
        print("Error in test_add_builder_info_route:", e)
        raise

def test_edit_country_route(test_client, init_database, db_connection):
    try:
        print("Debug: Starting test_edit_country_route...")
        print("Debug: Initializing test data...")
        test_payload = {
            'user_id': 1,
            'old_country_name': 'some_country',
            'new_country_name': 'edited_country',
            'role_id': 1
        }
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
        elif not old_country_exists:
            assert response.json() == {
                "result": "error",
                "message": "Does not exist",
                "role_id": test_payload['role_id'],
                "data": {}
            }
        elif test_payload['role_id'] != 1:
            assert response.json() == {
                "result": "error",
                "message": "Access denied",
                "user_id": test_payload['user_id'],
                "role_id": test_payload['role_id'],
                "data": {}
            }
        else:
            assert response.json() == {
                "result": "error",
                "message": "Invalid credentials",
                "user_id": test_payload['user_id'],
                "data": {}
            }

    except Exception as e:
        print("Error in test_edit_country_route:", e)
        raise

def test_add_builder_info_route(test_client, init_database, db_connection):
    try:
        existing_builder = check_existing_entity(db_connection, 'builder', 'Rudra')
        if existing_builder:
            assert False, "Builder already exists in the database"

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
        response = test_client.post('/addBuilderInfo', json=test_payload)
        assert response.status_code == 200
        assert response.json() == {
            "result": "success",
            "user_id": 1,
            "role_id": 1,
            "data": {"entered": "Rudra"}
        }

    except Exception as e:
        print("Error in test_add_builder_info_route:", e)
        raise

def test_edit_builder_route_success(test_client, init_database, db_connection):
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
    response = test_client.post('/editBuilder', json=test_payload)
    assert response.status_code == 200
    assert response.json() == {
        "result": "success",
        "user_id": test_payload['user_id'],
        "role_id": 1,
        "data": test_payload
    }

def test_edit_builder_route_failure_no_builder(test_client, init_database, db_connection):
    test_payload = {
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
    response = test_client.post('/editBuilder', json=test_payload)
    assert response.status_code == 200
    assert response.json() == {
        "result": "error",
        "message": "Builder does not exist",
        "role_id": 1,
        "user_id": test_payload['user_id'],
        "data": {}
    }

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


def test_get_countries_access_granted(test_client, init_database, db_connection):
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

def test_get_countries_access_denied(test_client, init_database, db_connection):
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

def test_get_countries_user_not_exist(test_client, init_database, db_connection):
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

def test_get_states_access_granted(test_client, init_database, db_connection):
    try:
        test_payload = {
            'user_id': 1,
            'role_id': 1,
            'country_id': 1  
        }
        
        response = test_client.post('/getStates', json=test_payload)
        
        assert response.status_code == 200
        assert response.json()['result'] == 'success'
        assert 'data' in response.json()
        
    except Exception as e:
        print(f"Exception occurred: {e}")

def test_get_states_access_denied(test_client, init_database, db_connection):
    try:
        test_payload = {
            'user_id': 1,
            'role_id': 2,  
            'country_id': 1
        }
        
        response = test_client.post('/getStates', json=test_payload)
    
        assert response.status_code == 200
        assert response.json()['result'] == 'error'
        assert response.json()['message'] == 'Access denied'
        
    except Exception as e:
        print(f"Exception occurred: {e}")

def test_get_states_user_not_exist(test_client, init_database, db_connection):
    try:
        test_payload = {
            'user_id': 1000,  
            'role_id': 1,
            'country_id': 1
        }
        
        response = test_client.post('/getStates', json=test_payload)
        
        assert response.status_code == 200
        assert response.json()['result'] == 'error'
        assert response.json()['message'] == 'User doesn\'t exist'
        
    except Exception as e:
        print(f"Exception occurred: {e}")

def test_get_cities_access_granted(test_client, init_database, db_connection):
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

def test_get_cities_invalid_credentials(test_client, init_database, db_connection):
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

def test_get_cities_state_not_found(test_client, init_database, db_connection):
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

def test_get_builder_info_access_granted(test_client, init_database, db_connection):
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

def test_get_builder_info_invalid_credentials(test_client, init_database, db_connection):
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

def test_get_builder_info_user_not_exist(test_client, init_database, db_connection):
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


def test_add_new_project_not_existing(test_client, init_database, db_connection):
    try:
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
        
        # Check if the project already exists in the database
        with db_connection.cursor() as cursor:
            cursor.execute("SELECT id FROM project WHERE projectname = %s", (test_payload['projectname'],))
            existing_project = cursor.fetchone()
        
        # project already exists
        assert existing_project is None, f"Project '{test_payload['projectname']}' already exists in the database"
        
        response = test_client.post('/addNewProject', json=test_payload)
        
        assert response.status_code == 200
        assert response.json()['result'] == 'success'
        assert 'data' in response.json()
        assert 'project_id' in response.json()['data']
        
        # Checking if project has been added to the database
        with db_connection.cursor() as cursor:
            cursor.execute("SELECT * FROM project WHERE id = %s", (response.json()['data']['project_id'],))
            project_data = cursor.fetchone()
            assert project_data is not None 
        
    except Exception as e:
        print(f"Exception occurred: {e}")


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

def test_get_role_id_endpoint(test_client, init_database, db_connection):
    #  Valid payload with existing role ID using user_id
    valid_payload_user_id = {"user_id": 1234,"username":"rudra"}
    response = test_client.post('/getRoleID', json=valid_payload_user_id)
    assert response.status_code == 200
    assert response.json()['result'] == 'Success'
    assert 'data' in response.json()
    assert 'role id' in response.json()['data']
    
    # Test case: Valid payload with existing role ID using username
    # valid_payload_username = {"username": "rudra"}
    # response = test_client.post('/getRoleID', json=valid_payload_username)
    # assert response.status_code == 200
    # assert response.json()['result'] == 'Success'
    # assert 'data' in response.json()
    # assert 'role id' in response.json()['data']
    
    
    invalid_payload_user_id = {"user_id": 5678}
    response = test_client.post('/getRoleID', json=invalid_payload_user_id)
    assert response.status_code == 200
    assert response.json()['result'] == 'error'
    assert response.json()['message'] == 'role_id not obtainable'  # Fix typo here
    assert 'data' in response.json()
    

    invalid_payload_username = {"username": "nonexistent_username"}
    response = test_client.post('/getRoleID', json=invalid_payload_username)
    assert response.status_code == 200
    assert response.json()['result'] == 'error'
    assert response.json()['message'] == 'role_id not obtainable'  # Fix typo here
    assert 'data' in response.json()
    
    #  Payload with role ID not found 
    invalid_payload_user_id = {"user_id": 9999} 
    response = test_client.post('/getRoleID', json=invalid_payload_user_id)
    assert response.status_code == 200
    assert response.json()['result'] == 'error'
    assert response.json()['message'] == 'role_id not obtainable'  
    assert 'data' in response.json()
    
    # (role_id=None) using username
    invalid_payload_username = {"username": "nonexistent_username"}
    response = test_client.post('/getRoleID', json=invalid_payload_username)
    assert response.status_code == 200
    assert response.json()['result'] == 'error'
    assert response.json()['message'] == 'role_id not obtainable'  
    assert 'data' in response.json()

def test_get_states_admin_success(test_client, init_database, db_connection):
    # Test case: Valid payload with admin role
    valid_payload = {"user_id": 1234}  # Assuming user_id of an admin
    response = test_client.post('/getStatesAdmin', json=valid_payload)
    assert response.status_code == 200
    assert response.json()['result'] == 'success'
    assert 'data' in response.json()
    assert 'user_id' in response.json()
    assert 'role_id' in response.json()

def test_get_states_admin_failure_invalid_credentials(test_client, init_database, db_connection):
    # Test case: Payload with non-admin role
    invalid_payload = {"user_id": 5678}  # Assuming user_id of a non-admin
    response = test_client.post('/getStatesAdmin', json=invalid_payload)
    assert response.status_code == 200
    assert response.json()['result'] == 'error'
    assert response.json()['message'] == 'Invalid Credentials'
    assert 'data' in response.json()
    assert 'user_id' in response.json()
    assert 'role_id' in response.json()

def test_get_states_admin_failure_missing_user_id(test_client, init_database, db_connection):
    # Test case: Missing user_id in payload
    invalid_payload = {}  # Empty payload
    response = test_client.post('/getStatesAdmin', json=invalid_payload)
    assert response.status_code == 200
    assert response.json()['result'] == 'error'
    assert response.json()['message'] == 'Invalid Payload'
    assert 'data' in response.json()
    assert 'user_id' not in response.json()
    assert 'role_id' not in response.json()




# def test_get_states_admin_exception(test_client, init_database, db_connection):
#     # Test case: Exception occurred
#     invalid_payload = {"user_id": 9999}  # Assuming user_id of a non-existent user
#     response = test_client.post('/getStatesAdmin', json=invalid_payload)
#     assert response.status_code == 200
#     assert response.json()['result'] == 'error'
#     assert response.json()['message'] == 'Exception occurred'
#     assert 'data' in response.json()
#     assert 'user_id' in response.json()
#     assert 'role_id' in response.json()







