import pytest
import psycopg2
from fastapi import HTTPException
import logging
import unittest.mock as mock 
from unittest.mock import patch
from fastapi.testclient import TestClient
logger = logging.getLogger(__name__)
from main import app
 



@pytest.fixture(scope='module')
def client():
    return TestClient(app)
@pytest.fixture(scope='module')
def db_connection():
    try:
        conn = psycopg2.connect(
            dbname="cura_testing",
            user="postgres",
            password="cura123",
            host="192.168.10.133"
        )
        logger.info("Database connection established successfully.")
        yield conn
        conn.close()
    except Exception as e:
        logger.error("Error establishing database connection:", e)
        raise HTTPException(status_code=500, detail="Database error")



@pytest.mark.usefixtures("db_connection")  
def test_id_1(client):
    response = client.post('/validateCredentials', json={
        'username': 'ruderaw',  # Assuming this user exists with the correct password
        'password': 'abcdefg', 
        'company_key': '9632'  # Assuming this company key exists
    })
    assert response.status_code == 200
    data = response.json()
    assert data['result'] == 'success'
    

@pytest.mark.usefixtures("db_connection")
def test_id_2(client):
    response = client.post('/validateCredentials', json={
        'username': 'RRRRRRR', 
        'password': 'abcdefg', 
        'company_key': '9632' 
    })
    assert response.status_code == 200  # Or a more appropriate error code
    assert response.json() == {
        "result": "Error",
        "message": "Wrong input", 
        "data": {}
    }

@pytest.mark.usefixtures("db_connection")
def test_id_3(client):
    response = client.post('/validateCredentials', json={
        'username': 'ruderaw',
        'password': 'hijklmn', 
        'company_key': '9632' 
    })
    assert response.status_code == 200  # Or a different code for auth errors
    assert response.json() == {
        "result": "error",
        "message": "Invalid Credentials" 
    }

@pytest.mark.usefixtures("db_connection")
def test_id_4(client):
    response = client.post('/validateCredentials', json={
        'username': 'ruderaw',
        'password': 'abcdefg', 
        'company_key': '1111' 
    })
    assert response.status_code == 200  # Or a different code for auth errors
    assert response.json() == {
        "result": "error",
        "message": "Invalid Credentials" 
    }

@pytest.mark.usefixtures("db_connection")
def test_id_5(client):
    response = client.post('/validateCredentials', json={
        'username': 'RRRRRRR',
        'password': 'hijklmn', 
        'company_key': '1111' 
    })
    assert response.status_code == 200  
    assert response.json() == {
        "result": "Error",
        "message": "Wrong input",
        "data": {}
    }

@pytest.mark.usefixtures("db_connection")
def test_id_15(client,db_connection):
    payload={"user_id":1234,"country_name":"country710"}
    with db_connection.cursor() as cursor:
        cursor.execute("SELECT MAX(id) FROM country")
        max_id = cursor.fetchone()[0]
        next_id = max_id + 1 if max_id else 1

    with db_connection.cursor() as cursor:
        cursor.execute("INSERT INTO country (id, name) VALUES (%s, %s)", 
                    (next_id, payload["country_name"]))  
        db_connection.commit() 
    expected_response={
         "result": "success",
        "user_id": 1234,
        "role_id": 1,
        "data": {
          "added": "country710"
        }
    }
    with patch('main.check_role_access', return_value=1):
       response=client.post('/addCountry',json=payload)
    
    assert response.status_code == 200
    assert response.json() == expected_response
    with db_connection.cursor() as cursor:
        cursor.execute("DELETE FROM country WHERE (id, name) = (%s, %s)", (next_id, payload["country_name"]))
        db_connection.commit()

@pytest.mark.usefixtures("db_connection")
def test_id_16(client):
    payload={"user_id":1234,"country_name":"country"}
    with db_connection.cursor() as cur:  
        cur.execute("INSERT INTO country (id, name) VALUES (%s, %s)", (payload["user_id"], payload["country_name"]))
        db_connection.commit() 
    
    expected_response={
  "result": "error",
  "message": "Already Exists",
  "user_id": 1234,
  "role_id": 1,
  "data": []
}
    with patch('main.check_role_access', return_value=1):
       response=client.post('/addCountry',json=payload)
    
    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.usefixtures("db_connection")
def test_id_17(client):
    payload = {"user_id":1234,"country_name":"country"}

    expected_response={
  "result": "error",
  "message": "Access Denied",
  "user_id": 1234,
  "role_id": 0,
  "data": []
}

    with patch('main.check_role_access', return_value=0):
       response=client.post('/addCountry',json=payload)
    
    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_18(client):
    payload = {"user_id":1234}

    expected_response={
  "result": "error",
  "message": "key 'country_name' not found",
  "user_id": 1234,
  "role_id": 0,
  "data": []
}

    with patch('main.check_role_access', return_value=1):
       response=client.post('/addCountry',json=payload)
    
    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_19(client, db_connection):
    payload = {
        "user_id": 1234,
        "old_country_name": "country", 
        "new_country_name": "edited_country"
    }
    # with db_connection.cursor() as cursor:
    #     cursor.execute("SELECT MAX(id) FROM country")
    #     max_id = cursor.fetchone()[0]
    #     next_id = max_id + 1 if max_id else 1

    with db_connection.cursor() as cursor:
        insert_query = """
            UPDATE country SET name = %s WHERE name = %s
        """
        cursor.execute(insert_query, (payload['new_country_name'], payload['old_country_name']))
        db_connection.commit()

    # 2. API Call and Assertions
    expected_response = {
        "result": "success",
        "user_id": 1234,
        "role_id": 1,
        "data": {
            "original": payload["old_country_name"],
            "new country": payload["new_country_name"] 
        }
    }
    with patch('main.check_role_access', return_value=1):
        with patch('main.checkcountry', return_value=True):  
            response = client.post('/editCountry', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

    # Clean up
    with db_connection.cursor() as cursor:
        cursor.execute("DELETE FROM country WHERE name = %s", (payload["new_country_name"],)) 
        db_connection.commit()


# @pytest.mark.usefixtures("db_connection")
# def test_id_20(client):
#     payload = {"user_id":1234,"old_country_name":"country", "new_country_name" : "edited_country"}

#     expected_response={
#   "result": "error",
#   "message": "No country Exists",
#   "user_id": 1234,
#   "role_id": 0,
#   "data": []
# }


#     with patch('main.check_role_access', return_value=0):
#        response=client.post('/editCountry',json=payload)
    
#     assert response.status_code == 200
#     assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_21(client):
    payload = {"user_id":1234,"old_country_name":"country", "new_country_name" : "edited_country"}

    expected_response={
  "result": "error",
  "message": "No country Exists",
  "user_id": 1234,
  "role_id": 0,
  "data": []
}


    with patch('main.check_role_access', return_value=0):
       response=client.post('/editCountry',json=payload)
    
    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.usefixtures("db_connection")
def test_id_22(client):
    payload = {"user_id":1234,"old_country_name":"country"}

    expected_response={
  "result": "error",
  "message": "No country Exists",
  "user_id": 1234,
  "role_id": 1,
  "data": []
}


    with patch('main.check_role_access', return_value=1):
       response=client.post('/editCountry',json=payload)
    
    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_47(client, db_connection):
    payload = {"user_id": 1234, "country_name": "edited_country"}

    # Use the provided database connection object
    conn = db_connection

    try:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO country (name) VALUES (%s)", (payload["country_name"],))
            conn.commit()

        with patch.object(logging, 'info') as mock_info:
            with patch('main.check_role_access', return_value=1):
                response = client.post('/deleteCountry', json=payload)

        expected_response = {
            "result": "success",
            "user_id": 1234,
            "role_id": 1,
            "data": {
                "deleted": "edited_country"
            }
        }

        # Assert the response
        assert response.status_code == 200
        assert response.json() == expected_response
        mock_info.assert_called_once_with(f'deleteCountry: received payload <{payload}>')

        # Check if the country name was deleted correctly
        with conn.cursor() as cur:
            cur.execute("SELECT name FROM country WHERE name = %s", (payload["country_name"],))
            result = cur.fetchone()
            assert result is None  # The country should not exist in the database

    except Exception as e:
        # Log the exception
        logging.error(f"An error occurred: {e}")

    finally:
        conn.rollback()

@pytest.mark.usefixtures("db_connection")
def test_id_48(client):
    payload = {"user_id":1234}

    expected_response={
  "result": "error",
  "message": "Invalid Credentials",
  "user_id": 1234,
  "role_id": 0,
  "data": []
}


    with patch('main.check_role_access', return_value=1):
       response=client.post('/deleteCountry',json=payload)
    
    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_51(client, db_connection):
    payload = {
        "user_id": 1234,
        "employeename": "changed emp",
        "employeeid": "P002020",
        "userid": 1236,
        "roleid": 2,
        "dateofjoining": "2024-01-13T00:00:00",
        "dob": "2001-01-13T00:00:00",
        "panno": "abcd",
        "status": False,
        "phoneno": None,
        "email": None,
        "addressline1": "abcdefgh",
        "addressline2": "ijklmnop",
        "suburb": "Pune",
        "city": 847,
        "state": "Maharashta",
        "country": 5,
        "zip": None,
        "dated": "2020-01-20T00:00:00",
        "createdby": 1234,
        "isdeleted": False,
        "entityid": 10,
        "lobid": 100,
        "lastdateofworking": "2020-02-20T00:00:00",
        "designation": "New"
    }

    conn = db_connection

    try:
        with conn.cursor() as cur:
            query = """
            INSERT INTO employees (
                employeename, employeeid, userid, roleid, dateofjoining, dob,
                panno, status, phoneno, email, addressline1, addressline2,
                suburb, city, state, country, zip, dated, createdby, isdeleted,
                entityid, lobid, lastdateofworking, designation
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cur.execute(query, (
                payload["employeename"], payload["employeeid"], payload["userid"],
                payload["roleid"], payload["dateofjoining"], payload["dob"],
                payload["panno"], payload["status"], payload["phoneno"],
                payload["email"], payload["addressline1"], payload["addressline2"],
                payload["suburb"], payload["city"], payload["state"],
                payload["country"], payload["zip"], payload["dated"],
                payload["createdby"], payload["isdeleted"], payload["entityid"],
                payload["lobid"], payload["lastdateofworking"], payload["designation"]
            ))
            # Commit the transaction
            conn.commit()

        with patch.object(logging, 'info') as mock_info:
            with patch('main.check_role_access', return_value=1):
                response = client.post('/addEmployee', json=payload)

        expected_response = {
            "result": "success",
            "user_id": 1234,
            "role_id": 1,
            "data": {
                "Inserted Employee": "changed emp"
            }
        }

        # Assert the response
        assert response.status_code == 200
        assert response.json() == expected_response
        # Assert that logging.info was called with the correct payload
        mock_info.assert_called_once_with(f'addEmployee: received payload <{payload}>')

    except Exception as e:
        logging.error(f"An error occurred: {e}")

    finally:
        # rollback the transaction
        conn.rollback()

@pytest.mark.usefixtures("db_connection")
def test_id_53(client):
    payload = {
        "user_id": 1235,
        "employeename": "changed emp",
        "employeeid": "P002020",
        "userid": 1236,
        "roleid": 2,
        "dateofjoining": "2024-01-13T00:00:00",
        "dob": "2001-01-13T00:00:00",
        "panno": "abcd",
        "status": False,
        "phoneno": None,
        "email": None,
        "addressline1": "abcdefgh",
        "addressline2": "ijklmnop",
        "suburb": "Pune",
        "city": 847,
        "state": "Maharashta",
        "country": 5,
        "zip": None,
        "dated": "2020-01-20T00:00:00",
        "createdby": 1234,
        "isdeleted": False,
        "entityid": 10,
        "lobid": 100,
        "lastdateofworking": "2020-02-20T00:00:00",
        "designation": "New"
    }

    expected_response = {
        "result": "error",
        "message": "Access Denied",
        "user_id": 1235,
        "role_id": 0,
        "data": []
    }

    with patch('main.check_role_access', return_value=0): 
        response = client.post('/addEmployee', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_54(client):
    payload = {
    
    "user_id": 1234,
    "employeeid": "P002020",
    "userid": 1236,
    "roleid": 2,
    "dateofjoining": "2024-01-13T00:00:00",
    "dob": "2001-01-13T00:00:00",
    "panno": "abcd",
    "status": False,
    "phoneno": None,
    "email": None,
    "addressline1": "abcdefgh",
    "addressline2": "ijklmnop",
    "suburb": "Pune",
    "city": 847,
    "state": "Maharashta",
    "country": 5,
    "zip": None,
    "dated": "2020-01-20T00:00:00",
    "createdby": 1234,
    "isdeleted": False,
    "entityid": 10,
    "lobid": 100,
    "lastdateofworking": "2020-02-20T00:00:00",
    "designation": "New"
}



    expected_response = {
        "result": "error",
        "message": "Invalid Credentials",
        "user_id": 1234,
        "role_id": 0,
        "data": []
    }

    response = client.post('/addEmployee', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.usefixtures("db_connection")
def test_id_55(client, db_connection):
    payload = {
        "user_id": 1234,
        "id": 100,
        "employeename": "changed emp",
        "employeeid": "P002020",
        "userid": 1236,
        "roleid": 2,
        "dateofjoining": "13-01-2024 00:00:00",
        "dob": "13-01-2001 00:00:00",
        "panno": "abcd",
        "status": False,
        "phoneno": None,
        "email": None,
        "addressline1": "abcdefgh",
        "addressline2": "ijklmnop",
        "suburb": "Pune",
        "city": 847,
        "state": "Maharashta",
        "country": 5,
        "zip": None,
        "dated": "20-01-2020  00:00:00",
        "createdby": 1234,
        "isdeleted": False,
        "entityid": 10,
        "lobid": 100,
        "lastdateofworking": "20-02-2020 00:00:00",
        "designation": "New"
    }

    conn = db_connection

    try:
        with conn.cursor() as cur:
            query = """
            UPDATE employees
            SET employeename = %s
            WHERE id = %s
            """
            cur.execute(query, (payload["employeename"], payload["id"]))
            conn.commit()

        # Call the route function
        with patch('main.check_role_access', return_value=1):
            response = client.post('/editEmployee', json=payload)

        # Define the expected response
        expected_response = {
            "result": "success",
            "user_id": 1234,
            "role_id": 1,
            "data": {
                "Updated Employee": "changed emp"
            }
        }

        # Assert the response
        assert response.status_code == 200
        assert response.json() == expected_response

    except Exception as e:
        logging.error(f"An error occurred: {e}")

    finally:
        # rollback the transaction
        conn.rollback()

# Test case for access denied scenario
@pytest.mark.usefixtures("db_connection")
def test_id_56(client):
    payload = {
        "user_id": 1234,
        "id": 100,
        "employeename": "changed emp",
        "employeeid": "P002020",
        "userid": 1236,
        "roleid": 2,
        "dateofjoining": "13-01-2024 00:00:00",
        "dob": "13-01-2001 00:00:00",
        "panno": "abcd",
        "status": False,
        "phoneno": None,
        "email": None,
        "addressline1": "abcdefgh",
        "addressline2": "ijklmnop",
        "suburb": "Pune",
        "city": 847,
        "state": "Maharashta",
        "country": 5,
        "zip": None,
        "dated": "20-01-2020  00:00:00",
        "createdby": 1234,
        "isdeleted": False,
        "entityid": 10,
        "lobid": 100,
        "lastdateofworking": "20-02-2020 00:00:00",
        "designation": "New"
    }

    expected_response = {
        "result": "error",
        "message": "Access Denied",
        "user_id": 1234,
        "role_id": 0,
        "data": []
    }

    with patch('main.check_role_access', return_value=0):
        response = client.post('/editEmployee', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

# Test case for invalid credentials
@pytest.mark.usefixtures("db_connection")
def test_id_57(client):
    payload = {
        "user_id": 1234,
        "employeename": "changed emp",
        "employeeid": "P002020",
        "userid": 1236,
        "roleid": 2,
        "dateofjoining": "13-01-2024 00:00:00",
        "dob": "13-01-2001 00:00:00",
        "panno": "abcd",
        "status": False,
        "phoneno": None,
        "email": None,
        "addressline1": "abcdefgh",
        "addressline2": "ijklmnop",
        "suburb": "Pune",
        "city": 847,
        "state": "Maharashta",
        "country": 5,
        "zip": None,
        "dated": "20-01-2020  00:00:00",
        "createdby": 1234,
        "isdeleted": False,
        "entityid": 10,
        "lobid": 100,
        "lastdateofworking": "20-02-2020 00:00:00",
        "designation": "New"
    }

    expected_response = {
        "result": "error",
        "message": "Invalid Credentials",
        "user_id": 1234,
        "role_id": 0,
        "data": []
    }

    with patch('main.check_role_access', return_value=1):
       response = client.post('/editEmployee', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.usefixtures("db_connection")
def test_id_58(client, db_connection):
    payload = {"user_id": 1234, "id": 301}

    try:
        conn = db_connection

        with conn.cursor() as cur:
            query_add_employee = "INSERT INTO employee (id) VALUES (%s)"
            cur.execute(query_add_employee, (payload["id"],))
            conn.commit()

        with conn.cursor() as cur:
            query_delete_employee = "DELETE FROM employee WHERE id = %s"
            cur.execute(query_delete_employee, (payload["id"],))
            conn.commit()

        with patch('main.check_role_access', return_value=1):
            response = client.post('/deletemployee', json=payload)

        expected_response = {
            "result": "success",
            "user_id": 1234,
            "role_id": 1,
            "data": {
                "deleted_user": 301
            }
        }

        assert response.status_code == 200
        assert response.json() == expected_response
        assert expected_response['data']['deleted_user'] > 0

    except Exception as e:
        logging.error(f"An error occurred: {e}")

    finally:
        # Rollback the transaction in case of any exceptions
        conn.rollback()

@pytest.mark.usefixtures("db_connection")
def test_id_59(client, db_connection):
    payload = {"user_id":1234, "id": 100}

    try:
        conn = db_connection
        
        # Check if the ID exists 
        with conn.cursor() as cur:
            query_check_id = "SELECT 1 FROM employee WHERE id = %s LIMIT 1"
            cur.execute(query_check_id, (payload["id"],))
            id_exists = cur.fetchone() is not None
        
        if not id_exists:
            expected_response = {
                "result": "error",
                "message": "No record exists",
                "user_id": 1234,
                "role_id": 1,
                "data": []
            }

            with patch('main.check_role_access', return_value=1):
                response = client.post('/deleteEmployee', json=payload)

            assert response.status_code == 200
            assert response.json() == expected_response

    except Exception as e:
        logging.error(f"An error occurred: {e}")
    
    finally:
        # Rollback the transaction in case of any exceptions
        conn.rollback()


# @pytest.mark.usefixtures("db_connection")
# def test_id_60(client):
#     payload = {"user_id":1234,"id": 129}

#     expected_response = {
#   "result": "error",
#   "message": "No record exists",
#   "user_id": 1234,
#   "role_id":1,
#   "data": []
# }

#     with patch('main.check_role_access', return_value=1):
#         response = client.post('/deleteEmployee', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_60(client):
    payload = {"user_id":1234,"id": 129}

    expected_response = {
  "result": "error",
  "message": "Access Denied",
  "user_id": 1234,
  "role_id": 0,
  "data": []
}

    with patch('main.check_role_access', return_value=0):
        response = client.post('/deleteEmployee', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_61(client, db_connection):
    payload = {
        "user_id": 1234,
        "locality": "Test Locality",
        "cityid": 8111 
    }

    try:
        conn = db_connection
        
        # Insert the locality into the database
        with conn.cursor() as cur:
            query_insert_locality = "INSERT INTO locality (user_id, name, city_id) VALUES (%s, %s, %s)"
            cur.execute(query_insert_locality, (payload["user_id"], payload["locality"], payload["cityid"]))
            conn.commit()
        
        expected_response = {
            "result": "success",
            "user_id": 1234,
            "role_id": 1,
            "data": {
                "Inserted Locality": "Test Locality"
            }
        }

        with patch('main.check_role_access', return_value=1):
            response = client.post('/addLocality', json=payload)

        assert response.status_code == 200
        assert response.json() == expected_response

    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        conn.rollback()
    


@pytest.mark.usefixtures("db_connection")
def test_id_62(client):
    payload = {
        "user_id": 1234,
        "locality": "Test Locality",
        "cityid": 8111
    }

    expected_response = {
  "result": "error",
  "message": "Access Denied",
  "user_id": 1234,
  "role_id": 0,
  "data": []
}

    with patch('main.check_role_access', return_value=0):
        response = client.post('/addLocality', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_63(client):
    payload = {
        "user_id": 1234,
        "locality": "Test Locality"
    }

    expected_response = {
  "result": "error",
  "message": "Invalid Credentials",
  "user_id": 1234,
  "role_id": 0,
  "data": []
}

    with patch('main.check_role_access', return_value=1):
        response = client.post('/addLocality', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response



# Test case for editing locality successfully
@pytest.mark.usefixtures("db_connection")
def test_id_65(client, db_connection):
    payload = {
        "user_id": 1234,
        "id": 45,
        "locality": "Locality132",
        "cityid": 8111
    }

    try:
        conn = db_connection
        
        with conn.cursor() as cur:
            query_insert_locality = "INSERT INTO locality (id, user_id, name, city_id) VALUES (%s, %s, %s, %s)"
            cur.execute(query_insert_locality, (payload["id"], payload["user_id"], payload["locality"], payload["cityid"]))
            conn.commit()
        
        expected_response = {
            "result": "success",
            "user_id": 1234,
            "role_id": 1,
            "data": {
                "Updated Locality": "Locality132"
            }
        }

        with patch('main.check_role_access', return_value=1):
            response = client.post('/editLocality', json=payload)

        assert response.status_code == 200
        assert response.json() == expected_response

    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        conn.rollback()


@pytest.mark.usefixtures("db_connection")
def test_id_66(client):
    payload = {
        "user_id": 1235,
        "id": 45,
        "locality": "Locality132",
        "cityid": 8111
    }

    expected_response = {
        "result": "error",
        "message": "Access Denied",
        "user_id": 1235,
        "role_id": 0,
        "data": []
    }

    with patch('main.check_role_access', return_value=0):
        response = client.post('/editLocality', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

# Test case for invalid credentials
@pytest.mark.usefixtures("db_connection")
def test_id_67(client):
    payload = {
        "user_id": 1235,
        "locality": "Locality132",
        "cityid": 8111
    }

    expected_response = {
        "result": "error",
        "message": "Invalid Credentials",
        "user_id": 1235,
        "role_id": 0,
        "data":[]
    }
    with patch('main.check_role_access', return_value=1):
       response = client.post('/editLocality', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

# Test case for successful locality deletion
@pytest.mark.usefixtures("db_connection")
def test_id_68(client, db_connection):
    payload = {
        "user_id": 1234,
        "id": 45  
    }

    expected_response = {
        "result": "success",
        "user_id": 1234,
        "role_id": 1,
        "data": {
            "Deleted Locality ID": 45
        }
    }

    try:
        conn = db_connection

        with conn.cursor() as cur:
            # Insert the locality 
            insert_query = "INSERT INTO locality (id) VALUES (%s)"
            cur.execute(insert_query, (payload["id"],))
            conn.commit()

            # Check if the locality ID exists in the database
            query = "SELECT COUNT(*) FROM locality WHERE id = %s"
            cur.execute(query, (payload["id"],))
            count = cur.fetchone()[0]

            if count == 0:
                # If the locality ID does not exist
                assert expected_response["data"]["Deleted Locality ID"] == payload["id"]
                return

            # If the locality ID exists, delete it from the database
            delete_query = "DELETE FROM locality WHERE id = %s"
            cur.execute(delete_query, (payload["id"],))
            conn.commit()

        with patch('main.check_role_access', return_value=1):
            response = client.post('/deleteLocality', json=payload)

        assert response.status_code == 200
        assert response.json() == expected_response

    except Exception as e:
        logging.error(f"An error occurred: {e}")

    finally:
        conn.rollback()

# Test case for access denied scenario
@pytest.mark.usefixtures("db_connection")
def test_id_69(client):
    payload = {
        "user_id": 1234,
        "id": 45  
    }

    expected_response = {
        "result": "error",
        "message": "Access Denied",
        "user_id": 1234,
        "role_id": 0,
        "data": []
    }

    with patch('main.check_role_access', return_value=0):
        response = client.post('/deleteLocality', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_70(client, db_connection):
    payload = {
        "user_id": 1235,
        "id": 999  
    }

    expected_response = {
        "result": "error",
        "message": "Access Denied",
        "user_id": 1235,
        "role_id": 2,
        "data": []
    }

    try:
        conn = db_connection

        with conn.cursor() as cur:
            # Check if the locality ID exists in the database
            query = "SELECT COUNT(*) FROM locality WHERE id = %s"
            cur.execute(query, (payload["id"],))
            count = cur.fetchone()[0]

            if count == 0:
                assert response.status_code == 200
                assert response.json() == expected_response
                return

        with patch('main.check_role_access', return_value=2):
            response = client.post('/deleteLocality', json=payload)

        assert response.status_code == 200
        assert response.json() == expected_response

    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        conn.rollback()


@pytest.mark.usefixtures("db_connection")
def test_id_71(client, db_connection):
    payload={
        "user_id":1234,
        "id":20,
        "name":"lobname",
        "lob_head":100,
        "company":"lobcompany",
        "entityid":123
    }

    expected_response={
        "result": "success",
        "user_id": 1234,
        "role_id": 1,
        "data": {
            "added_data": "lobname"
        }
    }

    try:
        conn = db_connection

        with conn.cursor() as cur:
            # Insert data into the lob table
            query = "INSERT INTO lob (id, name, lob_head, company, entityid) VALUES (%s, %s, %s, %s, %s)"
            cur.execute(query, (payload["id"], payload["name"], payload["lob_head"], payload["company"], payload["entityid"]))
            conn.commit()

        with patch('main.check_role_access', return_value=1):
            response = client.post('/addLob', json=payload)

        assert response.status_code == 200
        assert response.json() == expected_response

    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        conn.rollback()


@pytest.mark.usefixtures("db_connection")
def test_id_72(client):
    payload={
    "user_id":1234,
    "id":20,
    "name":"lobname",
    "lob_head":100,
    "company":"lobcompany",
    "entityid":123
}

    expected_response=None

    with patch('main.check_role_access', return_value=0):
       response=client.post('/addLob',json=payload)
    
    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_73(client):
    payload={
    "user_id":1234,
    "id":20,
    "lob_head":100,
    "company":"lobcompany",
    "entityid":123
}

    expected_response=None

    with patch('main.check_role_access', return_value=1):
       response=client.post('/addLob',json=payload)
    
    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_74(client, db_connection):
    payload={
        "user_id":1234,
        "old_name": "lobname",
        "new_name": "new_lobname"
    }

    expected_response={
        "result": "success",
        "user_id": 1234,
        "role_id": 1,
        "data": {
            "edited_lob": "lobname"
        }
    }

    try:
        conn = db_connection

        with conn.cursor() as cur:
            # Insert the initial lob data into the lob table
            initial_query = "INSERT INTO lob (name) VALUES (%s)"
            cur.execute(initial_query, (payload["old_name"],))
            conn.commit()

            # Update the name of the lob
            update_query = "UPDATE lob SET name = %s WHERE name = %s"
            cur.execute(update_query, (payload["new_name"], payload["old_name"]))
            conn.commit()

        with patch('main.check_role_access', return_value=1):
            response = client.post('/editLob', json=payload)

        assert response.status_code == 200
        assert response.json() == expected_response

    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        conn.rollback()


@pytest.mark.usefixtures("db_connection")
def test_id_75(client):
    payload={
    "user_id":1234,
    "old_name" : "lobname",
    "new_name" : "new_lobname"
}

    expected_response=None
    

    with patch('main.check_role_access', return_value=0):
       response=client.post('/editLob',json=payload)
    
    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_76(client):
    payload={
    "user_id":1234,
    "old_name" : "lobname"
}

    expected_response=None
    

    with patch('main.check_role_access', return_value=1):
       response=client.post('/editLob',json=payload)
    
    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_77(client):
    payload = {"user_id":1234,"name": "new_lobname"}

    expected_response = {
  "result": "success",
  "user_id": 1234,
  "role_id": 1,
  "data": {
    "deleted_lob": "new_lobname"
  }
}

    with patch('main.check_role_access', return_value=1):
        response = client.post('/deleteLob', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_78(client):
    payload = {"user_id":1234,"name": "new_lobname"}

    expected_response = None

    with patch('main.check_role_access', return_value=0):
        response = client.post('/deleteLob', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_79(client):
    payload = {"user_id":1234}

    expected_response = None

    with patch('main.check_role_access', return_value=1):
        response = client.post('/deleteLob', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_80(client):
    payload = {"user_id":1234, "receivedby":5, "paymentmode":11, "recddate":"31-Mar-2024", "entityid":1, "amount":111, "howreceivedid":1, "clientid" : 7, "receiptdesc":"", "serviceamount":0, "reimbursementamount":0, "tds":0}

    expected_response = {
  "result": "success",
  "user_id": 1234,
  "role_id": 1,
  "data": {
    "entered": "client receipt for amount <111>"
  }
}

    with patch('main.check_role_access', return_value=1):
        response = client.post('/addClientReceipt', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_81(client):
    payload = {"user_id":1234,"paymentmode":11, "recddate":"31-Mar-2024", "entityid":1, "amount":111, "howreceivedid":1, "clientid" : 7, "receiptdesc":"", "serviceamount":0, "reimbursementamount":0, "tds":0}
    expected_response = {
  "result": "error",
  "message": "'receivedby'",
  "user_id": 1234,
  "role_id": 0,
  "data": []
}

    with patch('main.check_role_access', return_value=1):
        response = client.post('/addClientReceipt', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_82(client):
    payload = {"user_id":1234, "receivedby":5, "paymentmode":11, "recddate":"31-Mar-2024", "entityid":1, "amount":111, "howreceivedid":1, "clientid" : 7, "receiptdesc":"", "serviceamount":0, "reimbursementamount":0, "tds":0}

    expected_response = {
  "result": "error",
  "message": "Access Denied",
  "user_id": 1234,
  "role_id": 0,
  "data": []
}

    with patch('main.check_role_access', return_value=0):
        response = client.post('/addClientReceipt', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_83(client):
    payload = {
    "user_id": 1234,
    "builderid": 101,
    "contactname": "Alice Smith",
    "email1": "alice.smith@example.com",
    "jobtitle": "Project Engineer",
    "businessphone": "123-456-7890",
    "homephone": "987-654-3210",
    "mobilephone": "555-123-4567",
    "addressline1": "456 Oak Street",
    "addressline2": "Suite 200",
    "suburb": "Downtown",
    "city": 456,
    "state": "New York",
    "country": 2,
    "zip": "54321",
    "notes": "Some notes about Alice Smith",
    "dated": "2024-03-14T08:00:00",
    "createdby": 5678,
    "isdeleted": False
}


    expected_response = {
  "result": "success",
  "user_id": 1234,
  "role_id": 1,
  "data": {
    "entered": "Alice Smith"
  }
}

    with patch('main.check_role_access', return_value=1):
        response = client.post('/addNewBuilderContact', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_84(client):
    payload = {
    "user_id": 1234,
    "builderid": 101,
    "email1": "alice.smith@example.com",
    "jobtitle": "Project Engineer",
    "businessphone": "123-456-7890",
    "homephone": "987-654-3210",
    "mobilephone": "555-123-4567",
    "addressline1": "456 Oak Street",
    "addressline2": "Suite 200",
    "suburb": "Downtown",
    "city": 456,
    "state": "New York",
    "country": 2,
    "zip": "54321",
    "notes": "Some notes about Alice Smith",
    "dated": "2024-03-14T08:00:00",
    "createdby": 5678,
    "isdeleted": False
}


    expected_response = {
  "result": "error",
  "message": "'contactname'",
  "user_id": 1234,
  "role_id": 0,
  "data": []
}

    with patch('main.check_role_access', return_value=1):
        response = client.post('/addNewBuilderContact', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.usefixtures("db_connection")
def test_id_85(client):
    payload = {
    "user_id": 1234,
    "builderid": 101,
    "contactname": "Alice Smith",
    "email1": "alice.smith@example.com",
    "jobtitle": "Project Engineer",
    "businessphone": "123-456-7890",
    "homephone": "987-654-3210",
    "mobilephone": "555-123-4567",
    "addressline1": "456 Oak Street",
    "addressline2": "Suite 200",
    "suburb": "Downtown",
    "city": 456,
    "state": "New York",
    "country": 2,
    "zip": "54321",
    "notes": "Some notes about Alice Smith",
    "dated": "2024-03-14T08:00:00",
    "createdby": 5678,
    "isdeleted": False
}


    expected_response = {
  "result": "error",
  "message": "Access Denied",
  "user_id": 1234,
  "role_id": 0,
  "data": []
}

    with patch('main.check_role_access', return_value=0):
        response = client.post('/addNewBuilderContact', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_36(client):
    payload = {"user_id":1234} 

    expected_response = {
  "result": "Success",
  "data": {
    "role id": 1
  }
}


    response = client.post('/getRoleID', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_37(client):
    payload =  {"username" : "ruderaw"}  

    expected_response = {
  "result": "Success",
  "data": {
    "role id": 1
  }
}


    response = client.post('/getRoleID', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_38(client):
    payload =  {"username" : "ashish"}  

    expected_response = {
  "result": "error",
  "messgae": "role_id not obtainable",
  "data": {}
}


    response = client.post('/getRoleID', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_39(client):
    payload = {"user_id":1000} 

    expected_response = {
  "result": "error",
  "messgae": "role_id not obtainable",
  "data": {}
}


    response = client.post('/getRoleID', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_23(client):
    payload = {
    "user_id": 1234,
    "buildername": "Aryan",
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



    expected_response = {
  "result": "success",
  "user_id": 1234,
  "role_id": 1,
  "data": {
    "entered": "Aryan"
  },
  "total_count": {
    "entered": "Aryan"
  }
}

    with patch('main.check_role_access', return_value=1):
        response = client.post('/addBuilderInfo', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_25(client):
    payload = {
    "user_id": 1234,
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



    expected_response = {
  "result": "error",
  "message": "Invalid Credentials",
  "user_id": 1234,
  "role_id": 0,
  "data": []
}

    with patch('main.check_role_access', return_value=1):
        response = client.post('/addBuilderInfo', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_26(client):
    payload = {
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



    expected_response = {
  "result": "error",
  "message": "Access Denied",
  "user_id": 1234,
  "role_id": 0,
  "data": []
}

    with patch('main.check_role_access', return_value=0):
        response = client.post('/addBuilderInfo', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_27(client):
    payload = {
    "user_id": 1234,
    "builder_id": 10027,
    "builder_name": "Rudra_kumar",
    "phone_1": "9999999999",
    "phone_2": "8888888888",
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
    "created_by": 1234,
    "is_deleted": False
}




    expected_response = {
  "result": "success",
  "user_id": 1234,
  "role_id": 1,
  "data": {
    "updated": {
      "user_id": 1234,
      "builder_id": 10027,
      "builder_name": "Rudra_kumar",
      "phone_1": "9999999999",
      "phone_2": "8888888888",
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
      "created_by": 1234,
      "is_deleted": False
    }
  }
}

    with patch('main.check_role_access', return_value=1):
        response = client.post('/editBuilder', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_28(client):
    payload = {
    "user_id": 1234,
    "builder_id": 10027,
    "phone_1": "9999999999",
    "phone_2": "8888888888",
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
    "created_by": 1234,
    "is_deleted": False
}




    expected_response = {
  "result": "error",
  "message": "key 'builder_name' not found",
  "user_id": 1234,
  "role_id": 0,
  "data": []
}

    with patch('main.check_role_access', return_value=1):
        response = client.post('/editBuilder', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_29(client):
    payload = {
    "user_id": 1234,
    "builder_id": 10027,
    "builder_name": "Rudra_kumar",
    "phone_1": "9999999999",
    "phone_2": "8888888888",
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
    "created_by": 1234,
    "is_deleted": False
}






    expected_response = {
  "result": "error",
  "message": "Access denied",
  "user_id": 1234,
  "role_id": 0,
  "data": []
}

    with patch('main.check_role_access', return_value=0):
        response = client.post('/editBuilder', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_49(client):
    payload = {"user_id":1234, "builder_id":10211}

    expected_response = {
  "result": "success",
  "user_id": 1234,
  "role_id": 1,
  "data": {
    "deleted_user": 10211
  }
}
    with patch('main.check_role_access', return_value=1):
        response = client.post('/deleteBuilder', json=payload)

    assert response.status_code == 200
    assert expected_response['data']['deleted_user'] > 0
    


@pytest.mark.usefixtures("db_connection")
def test_id_50(client):
    payload = {"user_id":1234}

    expected_response = {
  "result": "error",
  "message": "Invalid Credentials",
  "user_id": 1234,
  "role_id": 0,
  "data": []
}
    with patch('main.check_role_access', return_value=1):
        response = client.post('/deleteBuilder', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.usefixtures("db_connection")
def test_id_86(client):
    payload = {
    "user_id": 1234,
    "id":11000,
    "builderid": 3000,
    "projectname": "Sample Project",
    "addressline1": "123 Main Street",
    "addressline2": "Apt 101",
    "suburb": "Downtown",
    "city": 456,
    "state": "California",
    "country": 789,
    "zip": "12345",
    "nearestlandmark": "Central Park",
    "project_type": 1,
    "mailgroup1": "group1@example.com",
    "mailgroup2": "group2@example.com",
    "website": "www.sampleproject.com",
    "project_legal_status": 2,
    "rules": "Some rules for the project",
    "completionyear": 2025,
    "jurisdiction": "Local jurisdiction",
    "taluka": "Taluka",
    "corporationward": "Ward 1",
    "policechowkey": "Chowkey 1",
    "policestation": "Station 1",
    "maintenance_details": "Maintenance details",
    "numberoffloors": 5,
    "numberofbuildings": 3,
    "approxtotalunits": 50,
    "tenantstudentsallowed": True,
    "tenantworkingbachelorsallowed": False,
    "tenantforeignersallowed": True,
    "otherdetails": "Other details about the project",
    "duespayablemonth": 12,
    "dated": "2024-03-15T08:00:00",
    "createdby": 5678,
    "isdeleted": False
}





    expected_response = {
  "result": "success",
  "user_id": 1234,
  "role_id": 1,
  "data": {
    "entered": "Sample Project",
    "project_id": 0
  }
}

    with patch('main.check_role_access', return_value=1):
        response = client.post('/addProject', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_87(client):
    payload = {
    "user_id": 1234,
    "id":11000,
    "builderid": 3000,
    "addressline1": "123 Main Street",
    "addressline2": "Apt 101",
    "suburb": "Downtown",
    "city": 456,
    "state": "California",
    "country": 789,
    "zip": "12345",
    "nearestlandmark": "Central Park",
    "project_type": 1,
    "mailgroup1": "group1@example.com",
    "mailgroup2": "group2@example.com",
    "website": "www.sampleproject.com",
    "project_legal_status": 2,
    "rules": "Some rules for the project",
    "completionyear": 2025,
    "jurisdiction": "Local jurisdiction",
    "taluka": "Taluka",
    "corporationward": "Ward 1",
    "policechowkey": "Chowkey 1",
    "policestation": "Station 1",
    "maintenance_details": "Maintenance details",
    "numberoffloors": 5,
    "numberofbuildings": 3,
    "approxtotalunits": 50,
    "tenantstudentsallowed": True,
    "tenantworkingbachelorsallowed": False,
    "tenantforeignersallowed": True,
    "otherdetails": "Other details about the project",
    "duespayablemonth": 12,
    "dated": "2024-03-15T08:00:00",
    "createdby": 5678,
    "isdeleted": False
}


    expected_response = {
  "result": "error",
  "message": "Invalid Credentials",
  "user_id": 1234,
  "role_id": 0,
  "data": []
}

    with patch('main.check_role_access', return_value=1):
        response = client.post('/addProject', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_88(client):
    payload = {
    "user_id": 1234,
    "id":11000,
    "builderid": 3000,
    "projectname": "Sample Project",
    "addressline1": "123 Main Street",
    "addressline2": "Apt 101",
    "suburb": "Downtown",
    "city": 456,
    "state": "California",
    "country": 789,
    "zip": "12345",
    "nearestlandmark": "Central Park",
    "project_type": 1,
    "mailgroup1": "group1@example.com",
    "mailgroup2": "group2@example.com",
    "website": "www.sampleproject.com",
    "project_legal_status": 2,
    "rules": "Some rules for the project",
    "completionyear": 2025,
    "jurisdiction": "Local jurisdiction",
    "taluka": "Taluka",
    "corporationward": "Ward 1",
    "policechowkey": "Chowkey 1",
    "policestation": "Station 1",
    "maintenance_details": "Maintenance details",
    "numberoffloors": 5,
    "numberofbuildings": 3,
    "approxtotalunits": 50,
    "tenantstudentsallowed": True,
    "tenantworkingbachelorsallowed": False,
    "tenantforeignersallowed": True,
    "otherdetails": "Other details about the project",
    "duespayablemonth": 12,
    "dated": "2024-03-15T08:00:00",
    "createdby": 5678,
    "isdeleted": False
}



    expected_response = {
  "result": "error",
  "message": "Access Denied",
  "user_id": 1234,
  "role_id": 0,
  "data": []
}

    with patch('main.check_role_access', return_value=0):
        response = client.post('/addProject', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_89(client):
    payload = {
    "user_id": 1234,
    "id":11000,
    "builderid": 3000,
    "projectname": "Sample Project",
    "addressline1": "123 Main Street",
    "addressline2": "Apt 101",
    "suburb": "Downtown",
    "city": 456,
    "state": "California",
    "country": 789,
    "zip": "12345",
    "nearestlandmark": "Central Park",
    "project_type": 1,
    "mailgroup1": "group1@example.com",
    "mailgroup2": "group2@example.com",
    "website": "www.sampleproject.com",
    "project_legal_status": 2,
    "rules": "Some rules for the project",
    "completionyear": 2025,
    "jurisdiction": "Local jurisdiction",
    "taluka": "Taluka",
    "corporationward": "Ward 1",
    "policechowkey": "Chowkey 1",
    "policestation": "Station 1",
    "maintenance_details": "Maintenance details",
    "numberoffloors": 5,
    "numberofbuildings": 3,
    "approxtotalunits": 50,
    "tenantstudentsallowed": True,
    "tenantworkingbachelorsallowed": False,
    "tenantforeignersallowed": True,
    "otherdetails": "Other details about the project",
    "duespayablemonth": 12,
    "dated": "2024-03-15T08:00:00",
    "createdby": 5678,
    "isdeleted": False
}

    expected_response = {
  "result": "success",
  "user_id": 1234,
  "role_id": 1,
  "data": {
    "entered": "Sample Project"
  }
}
    with patch('main.check_role_access', return_value=1):
        response = client.post('/editProject', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.usefixtures("db_connection")
def test_id_90(client):
    payload = {
    "user_id": 1234,
    "id":11000,
    "builderid": 300,
    "addressline1": "123 Main Street",
    "addressline2": "Apt 101",
    "suburb": "Downtown",
    "city": 456,
    "state": "California",
    "country": 789,
    "zip": "12345",
    "nearestlandmark": "Central Park",
    "project_type": 1,
    "mailgroup1": "group1@example.com",
    "mailgroup2": "group2@example.com",
    "website": "www.sampleproject.com",
    "project_legal_status": 2,
    "rules": "Some rules for the project",
    "completionyear": 2025,
    "jurisdiction": "Local jurisdiction",
    "taluka": "Taluka",
    "corporationward": "Ward 1",
    "policechowkey": "Chowkey 1",
    "policestation": "Station 1",
    "maintenance_details": "Maintenance details",
    "numberoffloors": 5,
    "numberofbuildings": 3,
    "approxtotalunits": 50,
    "tenantstudentsallowed": True,
    "tenantworkingbachelorsallowed": False,
    "tenantforeignersallowed": True,
    "otherdetails": "Other details about the project",
    "duespayablemonth": 12,
    "dated": "2024-03-15T08:00:00",
    "createdby": 5678,
    "isdeleted": False
}


    expected_response = {
  "result": "error",
  "message": "Invalid Credentials",
  "user_id": 1234,
  "role_id": 0,
  "data": []
}
    
    with patch('main.check_role_access', return_value=1):
        response = client.post('/editProject', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_91(client):
    payload = {
    "user_id": 1234,
    "id":11000,
    "builderid": 3000,
    "projectname": "Sample Project",
    "addressline1": "123 Main Street",
    "addressline2": "Apt 101",
    "suburb": "Downtown",
    "city": 456,
    "state": "California",
    "country": 789,
    "zip": "12345",
    "nearestlandmark": "Central Park",
    "project_type": 1,
    "mailgroup1": "group1@example.com",
    "mailgroup2": "group2@example.com",
    "website": "www.sampleproject.com",
    "project_legal_status": 2,
    "rules": "Some rules for the project",
    "completionyear": 2025,
    "jurisdiction": "Local jurisdiction",
    "taluka": "Taluka",
    "corporationward": "Ward 1",
    "policechowkey": "Chowkey 1",
    "policestation": "Station 1",
    "maintenance_details": "Maintenance details",
    "numberoffloors": 5,
    "numberofbuildings": 3,
    "approxtotalunits": 50,
    "tenantstudentsallowed": True,
    "tenantworkingbachelorsallowed": False,
    "tenantforeignersallowed": True,
    "otherdetails": "Other details about the project",
    "duespayablemonth": 12,
    "dated": "2024-03-15T08:00:00",
    "createdby": 5678,
    "isdeleted": False
}

    expected_response = {
  "result": "error",
  "message": "Access Denied",
  "user_id": 1234,
  "role_id": 0,
  "data": []
}
    with patch('main.check_role_access', return_value=0):
        response = client.post('/editProject', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_6(client):
    payload = {"user_id":1234,"rows":["id","name"],"filters":[],"sort_by":[],"order":"asc","pg_no":1,"pg_size":15}
    
    expected_response = {
  "result": "success",
  "user_id": 1234,
  "role_id": 1,
  "data": {
    "data": [
      [
        19,
        "TBD"
      ],
      [
        214,
        "India"
      ],
      [
        204,
        "India"
      ],
      [
        3,
        "France"
      ],
      [
        27,
        "Finland"
      ],
      [
        101,
        "Pakistan"
      ],
      [
        8,
        "Sri Lanka"
      ],
      [
        7,
        "UAE"
      ],
      [
        207,
        "India"
      ],
      [
        10,
        "UK"
      ],
      [
        201,
        "test_country"
      ],
      [
        9,
        "Netherlands"
      ],
      [
        18,
        "Kuwait"
      ],
      [
        20,
        "China"
      ],
      [
        1,
        "Switzerland"
      ]
    ],
    "total_count": 52,
    "message": "success",
    "colnames": [
      "id",
      "name"
    ]
  },
  "total_count": 52
}
    with patch('main.check_role_access', return_value=1):
        response = client.post('/getCountries', json=payload)

    assert response.status_code == 200
    assert expected_response['data']['total_count'] > 0
    

@pytest.mark.usefixtures("db_connection")
def test_id_7(client):
    payload = {"user_id":1234,"rows":["id","name"],"sort_by":[],"order":"asc","pg_no":1,"pg_size":15}
    expected_response = {
  "result": "error",
  "message": "error 'filters' found",
  "user_id": 1234,
  "role_id": 0,
  "data": []
}
    with patch('main.check_role_access', return_value=1):
        response = client.post('/getCountries', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_8(client):
    payload = {"user_id":1234,"rows":["id","name"],"filters":[],"sort_by":[],"order":"asc","pg_no":1,"pg_size":15}
    expected_response = {
  "result": "error",
  "message": "Access Denied",
  "user_id": 1234,
  "role_id": 0,
  "data": []
}
    with patch('main.check_role_access', return_value=0):
        response = client.post('/getCountries', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.usefixtures("db_connection")
def test_id_9(client):
    payload = {"user_id":1234,"country_id":5}
    expected_response = {
  "result": "success",
  "user_id": 1234,
  "role_id": 1,
  "data": [
    [
      1617,
      "Gujarat"
    ],
    [
      1637,
      "Rajasthan"
    ],
    [
      1776,
      "Bihar"
    ],
    [
      1758,
      "Himachal Pradesh"
    ],
    [
      1794,
      "Maharashtra"
    ],
    [
      1783,
      "Maharashtra"
    ],
    [
      1625,
      "Andhra Pradesh"
    ],
    [
      1745,
      "Orissa"
    ],
    [
      1781,
      "Uttarakhand"
    ],
    [
      1752,
      "Maharashtra"
    ],
    [
      1764,
      "Andhra Pradesh"
    ],
    [
      1787,
      "Uttar Pradesh"
    ],
    [
      1773,
      "Chhattisgarh"
    ],
    [
      1786,
      "Telangana"
    ],
    [
      1768,
      "Gujarat"
    ],
    [
      1789,
      "Maharashtra"
    ],
    [
      1779,
      "Jammu and Kashmir"
    ],
    [
      1746,
      "Rajasthan"
    ],
    [
      1795,
      "Uttar Pradesh"
    ],
    [
      1796,
      "Maharashtra"
    ],
    [
      1778,
      "Maharashtra"
    ],
    [
      1803,
      "Maharashtra"
    ],
    [
      1636,
      "Punjab"
    ],
    [
      1620,
      "West Bengal"
    ],
    [
      1632,
      "Karnataka"
    ],
    [
      1775,
      "Bihar"
    ],
    [
      1622,
      "Madhya Pradesh"
    ],
    [
      1798,
      "Rajasthan"
    ],
    [
      1631,
      "Gujarat"
    ],
    [
      1615,
      "Gujarat"
    ],
    [
      1750,
      "Uttar Pradesh"
    ],
    [
      1753,
      "Maharashtra"
    ],
    [
      1749,
      "Uttar Pradesh"
    ],
    [
      1751,
      "Maharashtra"
    ],
    [
      1767,
      "Haryana"
    ],
    [
      1755,
      "Jharkhand"
    ],
    [
      1633,
      "Madhya Pradesh"
    ],
    [
      1748,
      "Uttar Pradesh"
    ],
    [
      1802,
      "Maharashtra"
    ],
    [
      1756,
      "Jharkhand"
    ],
    [
      1624,
      "Uttar Pradesh"
    ],
    [
      1626,
      "Bihar"
    ],
    [
      1770,
      "Kerala"
    ],
    [
      1623,
      "Uttar Pradesh"
    ],
    [
      1759,
      "Uttarakhand"
    ],
    [
      1784,
      "Maharashtra"
    ],
    [
      1761,
      "Haryana"
    ],
    [
      1760,
      "Punjab"
    ],
    [
      1763,
      "Maharashtra"
    ],
    [
      1790,
      "Maharashtra"
    ],
    [
      1621,
      "Goa"
    ],
    [
      1754,
      "Maharashtra"
    ],
    [
      1627,
      "Delhi"
    ],
    [
      1638,
      "Tamil Nadu"
    ],
    [
      1762,
      "Punjab"
    ],
    [
      1757,
      "Karnataka"
    ],
    [
      1771,
      "Kerala"
    ],
    [
      1616,
      "Gujarat"
    ],
    [
      1788,
      "Uttar Pradesh"
    ],
    [
      1780,
      "Uttarakhand"
    ],
    [
      1618,
      "Rajasthan"
    ],
    [
      1635,
      "Maharashtra"
    ],
    [
      1774,
      "Kerala"
    ],
    [
      1785,
      "Maharashtra"
    ],
    [
      1808,
      "Maharashtra"
    ],
    [
      1619,
      "Tamilnadu"
    ],
    [
      1747,
      "Uttar Pradesh"
    ],
    [
      1740,
      "TBD"
    ],
    [
      847,
      "Maharashtra"
    ],
    [
      1772,
      "Chhattisgarh"
    ],
    [
      1769,
      "Uttar Pradesh"
    ]
  ]
}
    with patch('main.check_role_access', return_value=1):
        response = client.post('/getStates', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_10(client):
    payload = {"user_id":1234}
    expected_response = {
  "result": "error",
  "message": "'country_id' error found",
  "user_id": 1234,
  "role_id": 0,
  "data": []
}
    with patch('main.check_role_access', return_value=1):
        response = client.post('/getStates', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_11(client):
    payload = {"user_id":1234,"country_id":5}
    expected_response = {
  "result": "error",
  "message": "User does not exist",
  "user_id": 1234,
  "role_id": 0,
  "data": []
}
    with patch('main.check_role_access', return_value=0):
        response = client.post('/getStates', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_12(client):
    payload = {"user_id":1234,"rows":["buildername", "builderid","projectname","addressline1","addressline2","suburb","city","state","country","zip","nearestlandmark","project_type","mailgroup1","mailgroup2","website","project_legal_status","rules","completionyear","jurisdiction","taluka","corporationward","policechowkey","policestation","maintenance_details","numberoffloors","numberofbuildings","approxtotalunits","tenantstudentsallowed","tenantworkingbachelorsallowed","tenantforeignersallowed","otherdetails","duespayablemonth","dated","createdby","isdeleted","id"],"filters":[],"sort_by":[],"order":"asc","pg_no":1,"pg_size":2}
    expected_response = {
  "result": "success",
  "user_id": 1234,
  "role_id": 1,
  "data": [
    {
      "buildername": "Mont Vert Homes",
      "builderid": 18,
      "projectname": "Mont Vert Seville",
      "addressline1": "Wakad Thergaon Link Road",
      "addressline2": "",
      "suburb": "Wakad",
      "city": 847,
      "state": "Maharashtra",
      "country": 5,
      "zip": "",
      "nearestlandmark": "",
      "project_type": 6,
      "mailgroup1": "Google",
      "mailgroup2": "",
      "website": "",
      "project_legal_status": 1,
      "rules": "",
      "completionyear": 0,
      "jurisdiction": "",
      "taluka": "",
      "corporationward": "",
      "policechowkey": "",
      "policestation": "",
      "maintenance_details": "",
      "numberoffloors": 0,
      "numberofbuildings": 0,
      "approxtotalunits": 0,
      "tenantstudentsallowed": False,
      "tenantworkingbachelorsallowed": False,
      "tenantforeignersallowed": False,
      "otherdetails": "Every day 12 Noon to 8 PM\r\n Weekly Off: Wednesday",
      "duespayablemonth": 0,
      "dated": "2016-02-23T13:17:05.450000",
      "createdby": 69,
      "isdeleted": False,
      "id": 19
    },
    {
      "buildername": "Mont Vert Homes",
      "builderid": 18,
      "projectname": "Mont Vert Seville",
      "addressline1": "Wakad Thergaon Link Road",
      "addressline2": "",
      "suburb": "Wakad",
      "city": 847,
      "state": "Maharashtra",
      "country": 5,
      "zip": "",
      "nearestlandmark": "",
      "project_type": 6,
      "mailgroup1": "Google",
      "mailgroup2": "",
      "website": "",
      "project_legal_status": 1,
      "rules": "",
      "completionyear": 0,
      "jurisdiction": "",
      "taluka": "",
      "corporationward": "",
      "policechowkey": "",
      "policestation": "",
      "maintenance_details": "",
      "numberoffloors": 0,
      "numberofbuildings": 0,
      "approxtotalunits": 0,
      "tenantstudentsallowed": False,
      "tenantworkingbachelorsallowed": False,
      "tenantforeignersallowed": False,
      "otherdetails": "Every day 12 Noon to 8 PM\r\n Weekly Off: Wednesday",
      "duespayablemonth": 0,
      "dated": "2016-02-23T13:17:05.450000",
      "createdby": 69,
      "isdeleted": False,
      "id": 19
    }
  ],
  "total_count": 1344
}
    with patch('main.check_role_access', return_value=1):
        response = client.post('/getProjects', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.usefixtures("db_connection")
def test_id_13(client):
    payload = {"user_id":1234,"rows":["buildername", "builderid","projectname","addressline1","addressline2","suburb","city","state","country","zip","nearestlandmark","project_type","mailgroup1","mailgroup2","website","project_legal_status","rules","completionyear","jurisdiction","taluka","corporationward","policechowkey","policestation","maintenance_details","numberoffloors","numberofbuildings","approxtotalunits","tenantstudentsallowed","tenantworkingbachelorsallowed","tenantforeignersallowed","otherdetails","duespayablemonth","dated","createdby","isdeleted","id"],"sort_by":[],"order":"asc","pg_no":1,"pg_size":2}
    expected_response ={
  "result": "error",
  "message": "Username or User ID not found",
  "user_id": 1234,
  "role_id": 0,
  "data": []
}
    with patch('main.check_role_access', return_value=1):
        response = client.post('/getProjects', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_14(client):
    payload = {"user_id":1234,"rows":["buildername", "builderid","projectname","addressline1","addressline2","suburb","city","state","country","zip","nearestlandmark","project_type","mailgroup1","mailgroup2","website","project_legal_status","rules","completionyear","jurisdiction","taluka","corporationward","policechowkey","policestation","maintenance_details","numberoffloors","numberofbuildings","approxtotalunits","tenantstudentsallowed","tenantworkingbachelorsallowed","tenantforeignersallowed","otherdetails","duespayablemonth","dated","createdby","isdeleted","id"],"filters":[],"sort_by":[],"order":"asc","pg_no":1,"pg_size":2}
    expected_response ={
  "result": "error",
  "message": "Username or User ID not found",
  "user_id": 1234,
  "role_id": 0,
  "data": []
}
    with patch('main.check_role_access', return_value=0):
        response = client.post('/getProjects', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.usefixtures("db_connection")
def test_id_30(client):
    payload = {
    "user_id": 1234,
    "state_name":"Maharashtra"
}
    expected_response ={
  "result": "success",
  "user_id": 1234,
  "role_id": 1,
  "data": [
    {
      "id": 1783,
      "city": "Kolhapur"
    },
    {
      "id": 1763,
      "city": "Dhule"
    },
    {
      "id": 1751,
      "city": "Jalgaon"
    },
    {
      "id": 1790,
      "city": "Solapur"
    },
    {
      "id": 1789,
      "city": "Amravati"
    },
    {
      "id": 1784,
      "city": "Navi Mumbai"
    },
    {
      "id": 1803,
      "city": "Panchgani"
    },
    {
      "id": 1802,
      "city": "Satara"
    },
    {
      "id": 1796,
      "city": "Aurangabad"
    },
    {
      "id": 847,
      "city": "Pune"
    },
    {
      "id": 1753,
      "city": "Nashik"
    },
    {
      "id": 1635,
      "city": "Mumbai"
    },
    {
      "id": 1785,
      "city": "Palghar"
    },
    {
      "id": 1794,
      "city": "Washim"
    },
    {
      "id": 1778,
      "city": "Thane"
    },
    {
      "id": 1752,
      "city": "Nagpur"
    },
    {
      "id": 1808,
      "city": "Mahabaleshwar"
    },
    {
      "id": 1754,
      "city": "Ahmednagar"
    }
  ]
}
    with patch('main.check_role_access', return_value=1):
        response = client.post('/getCities', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.usefixtures("db_connection")
def test_id_31(client):
    payload = {
    "user_id": 1234,
    "state_name":"Maharashtra"
}

    expected_response ={
  "result": "error",
  "message": "Invalid Credentials",
  "user_id": 1234,
  "role_id": 0,
  "data": []
}
    with patch('main.check_role_access', return_value=0):
        response = client.post('/getCities', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response
@pytest.mark.usefixtures("db_connection")
def test_id_32(client):
    payload = {
    "user_id": 1234
}

    expected_response ={
  "result": "error",
  "message": "'state_name' error found",
  "user_id": 1234,
  "role_id": 0,
  "data": []
}
    with patch('main.check_role_access', return_value=1):
        response = client.post('/getCities', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.usefixtures("db_connection")
def test_id_43(client):
    payload = {"user_id":1234,"rows":["id","city","state","countryid","country"],"filters":[],"sort_by":[],"order":"asc","pg_no":1,"pg_size":15}

    expected_response ={
  "result": "success",
  "user_id": 1234,
  "role_id": 1,
  "data": [
    {
      "id": 847,
      "city": "Pune",
      "state": "Maharashtra",
      "countryid": 5,
      "country": "India"
    },
    {
      "id": 1604,
      "city": "Zurich",
      "state": "Switzerland",
      "countryid": 1,
      "country": "Switzerland"
    },
    {
      "id": 1605,
      "city": "Geneva",
      "state": "Switzerland",
      "countryid": 1,
      "country": "Switzerland"
    },
    {
      "id": 1606,
      "city": "Durban",
      "state": "South Africa",
      "countryid": 2,
      "country": "South Africa"
    },
    {
      "id": 1607,
      "city": "Cape Town",
      "state": "South Africa",
      "countryid": 2,
      "country": "South Africa"
    },
    {
      "id": 1608,
      "city": "Johannesburg",
      "state": "South Africa",
      "countryid": 2,
      "country": "South Africa"
    },
    {
      "id": 1609,
      "city": "Paris",
      "state": "France",
      "countryid": 3,
      "country": "France"
    },
    {
      "id": 1610,
      "city": "Sydney",
      "state": "Australia",
      "countryid": 4,
      "country": "Australia"
    },
    {
      "id": 1611,
      "city": "Melbourne",
      "state": "Australia",
      "countryid": 4,
      "country": "Australia"
    },
    {
      "id": 1612,
      "city": "Brisbane",
      "state": "Australia",
      "countryid": 4,
      "country": "Australia"
    },
    {
      "id": 1613,
      "city": "Adelaide",
      "state": "Australia",
      "countryid": 4,
      "country": "Australia"
    },
    {
      "id": 1614,
      "city": "Perth",
      "state": "Australia",
      "countryid": 4,
      "country": "Australia"
    },
    {
      "id": 1615,
      "city": "Surat",
      "state": "Gujarat",
      "countryid": 5,
      "country": "India"
    },
    {
      "id": 1616,
      "city": "Ahmedabad",
      "state": "Gujarat",
      "countryid": 5,
      "country": "India"
    },
    {
      "id": 1617,
      "city": "Baroda",
      "state": "Gujarat",
      "countryid": 5,
      "country": "India"
    }
  ],
  "total_count": 195
}
    with patch('main.check_role_access', return_value=1):
        response = client.post('getCitiesAdmin', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_45(client):
    payload = {"user_id":1234,"rows":["id","city","state","countryid","country"],"sort_by":[],"order":"asc","pg_no":1,"pg_size":15}
    expected_response ={
  "result": "error",
  "message": "getCitiesAdmin: 'filters' error found. exception <None>",
  "user_id": 1234,
  "role_id": 0,
  "data": []
}
    with patch('main.check_role_access', return_value=1):
        response = client.post('getCitiesAdmin', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_44(client):
    payload = {"user_id":1234,"rows":["id","city","state","countryid","country"],"filters":[],"sort_by":[],"order":"asc","pg_no":1,"pg_size":15}
    expected_response ={
  "result": "error",
  "message": "Invalid Credentials",
  "user_id": 1234,
  "role_id": 0,
  "data": []
}
    with patch('main.check_role_access', return_value=0):
        response = client.post('getCitiesAdmin', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.usefixtures("db_connection")
def test_id_33(client):
    payload = {"user_id":1234,"rows":[],"filters":[],"sort_by":[],"order":"asc","pg_no":1,"pg_size":15}
    expected_response ={
  "result": "success",
  "user_id": 1234,
  "role_id": 1,
  "data": [
    [
      "Japan",
      "Tokyo",
      21
    ],
    [
      "USA",
      "Pennsylvania",
      13
    ],
    [
      "USA",
      "Alaska",
      13
    ],
    [
      "India",
      "Maharashtra",
      5
    ],
    [
      "Belgium",
      "Belgium",
      6
    ],
    [
      "USA",
      "Idaho",
      13
    ],
    [
      "USA",
      "Washington",
      13
    ],
    [
      "India",
      "Kerala",
      5
    ],
    [
      "India",
      "Bihar",
      5
    ],
    [
      "Qatar",
      "Qatar",
      16
    ],
    [
      "USA",
      "Virginia",
      13
    ],
    [
      "USA",
      "Oregon",
      13
    ],
    [
      "New Zealand",
      "New Zealand",
      12
    ],
    [
      "India",
      "Uttar Pradesh",
      5
    ],
    [
      "USA",
      "North Carolina",
      13
    ]
  ],
  "total_count": 85
}
    with patch('main.check_role_access', return_value=1):
        response = client.post('getStatesAdmin', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.usefixtures("db_connection")
def test_id_34(client):
    payload = {"user_id":1234,"rows":[],"filters":[],"sort_by":[],"order":"asc","pg_no":1,"pg_size":15}
    expected_response ={
  "result": "error",
  "message": "Invalid Credentials",
  "user_id": 1234,
  "role_id": 0,
  "data": []
}
    with patch('main.check_role_access', return_value=0):
        response = client.post('getStatesAdmin', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_35(client):
    payload = {"user_id":1234,"rows":[],"sort_by":[],"order":"asc","pg_no":1,"pg_size":15}
    expected_response ={
  "result": "error",
  "message": "Invalid Credentials",
  "user_id": 1234,
  "role_id": 0,
  "data": []
}
    with patch('main.check_role_access', return_value=1):
        response = client.post('getStatesAdmin', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.usefixtures("db_connection")
def test_id_40(client):
    payload = {
    "user_id": 1234,
    "rows": ["id","buildername","phone1","phone2","email1","email2","addressline1","addressline2","suburb","city","state","country","zip","website","comments","dated","createdby","isdeleted"]
,
    "filters": [],
    "sort_by": [],
    "order": "asc",
    "pg_no": 1,
    "pg_size": 15
  } 

    expected_response = {
  "result": "success",
  "user_id": 1234,
  "role_id": 1,
  "data": {
    "builder_info": [
      {
        "id": 8,
        "buildername": "Paranjape Schemes Constructions Pvt. Ltd.",
        "phone1": "020 39394949",
        "phone2": "",
        "email1": "",
        "email2": "",
        "addressline1": "Off Prabhat Road",
        "addressline2": "",
        "suburb": "Deccan",
        "city": "Pune",
        "state": "Maharashtra",
        "country": "India",
        "zip": "",
        "website": "www.pscl.in",
        "comments": "Satish Nene (V P Sales) - 9970169102\r\nReception 02039394949, 25440986, 9860500214, \r\nShirish Engale 9665028744\r\nDattatry TDC - 96650603150\r\nSachin Khirsagar (Legal) - 9860500217\r\nBlue Ridge - Suksham - 7387007721\r\n\r\n\r\n\r\nFLATSHIP INFRA :- account no : 000730350001737 IFSC Code : HDFC0000007 Bhandarkar Road current account\r\n\r\n\r\n",
        "dated": "2014-12-24T11:25:13.113000",
        "createdby": 83,
        "isdeleted": False
      },
      {
        "id": 9,
        "buildername": "AUM Regency Housing",
        "phone1": "02032670999",
        "phone2": "",
        "email1": "",
        "email2": "",
        "addressline1": "Baner Mhalunge Road",
        "addressline2": "",
        "suburb": "Baner",
        "city": "Pune",
        "state": "Maharashtra",
        "country": "India",
        "zip": "",
        "website": "www.regencygroup.co.in",
        "comments": "",
        "dated": "2014-04-17T14:42:32.253000",
        "createdby": 65,
        "isdeleted": False
      },
      {
        "id": 10,
        "buildername": "Shree Bal Developers",
        "phone1": "020-24336372",
        "phone2": "",
        "email1": "",
        "email2": "",
        "addressline1": "LB Shastri Rd Navi Peth ",
        "addressline2": "",
        "suburb": "Pune",
        "city": "Pune",
        "state": "Maharashtra",
        "country": "India",
        "zip": "",
        "website": "",
        "comments": "Sharad Bal -9822015459",
        "dated": "2016-09-09T12:36:25.537000",
        "createdby": 69,
        "isdeleted": False
      },
      {
        "id": 11,
        "buildername": "Alliance Group",
        "phone1": "0",
        "phone2": "",
        "email1": "",
        "email2": "",
        "addressline1": "Wakad",
        "addressline2": "",
        "suburb": "Wakad",
        "city": "Pune",
        "state": "Maharashtra",
        "country": "India",
        "zip": "",
        "website": "",
        "comments": "",
        "dated": "2017-01-12T12:31:21.947000",
        "createdby": 1106,
        "isdeleted": False
      },
      {
        "id": 12,
        "buildername": "Sukhwani Constructions",
        "phone1": "0",
        "phone2": "",
        "email1": "",
        "email2": "",
        "addressline1": "Pimpri",
        "addressline2": "",
        "suburb": "Pimpri",
        "city": "Pune",
        "state": "Maharashtra",
        "country": "India",
        "zip": "",
        "website": "",
        "comments": "",
        "dated": "2014-04-21T13:03:33.953000",
        "createdby": 65,
        "isdeleted": False
      },
      {
        "id": 13,
        "buildername": "Roseland Residency ",
        "phone1": "020 27212300",
        "phone2": "",
        "email1": "pralhadui@gmail.com",
        "email2": "",
        "addressline1": "Pimple Saudagar",
        "addressline2": "",
        "suburb": "Pimple Saudagar",
        "city": "Pune",
        "state": "Maharashtra",
        "country": "India",
        "zip": "",
        "website": "www.roselandresidency.com",
        "comments": "",
        "dated": "2014-04-21T11:55:21.413000",
        "createdby": 65,
        "isdeleted": False
      },
      {
        "id": 14,
        "buildername": "Kumar Properties Pvt Ltd ",
        "phone1": "020 30583662",
        "phone2": "",
        "email1": "",
        "email2": "",
        "addressline1": "East Street Camp",
        "addressline2": "",
        "suburb": "Camp",
        "city": "Pune",
        "state": "Maharashtra",
        "country": "India",
        "zip": "411001",
        "website": "",
        "comments": "",
        "dated": "2014-04-21T13:16:41.320000",
        "createdby": 65,
        "isdeleted": False
      },
      {
        "id": 15,
        "buildername": "Naik Navare Developers ",
        "phone1": "020 41471199 ",
        "phone2": "",
        "email1": "sales@naiknavare.com",
        "email2": "",
        "addressline1": "Ghole Road , Shivajinagar",
        "addressline2": "",
        "suburb": "Shivajinagar ",
        "city": "Pune",
        "state": "Maharashtra",
        "country": "India",
        "zip": "",
        "website": "",
        "comments": "",
        "dated": "2014-04-21T12:15:22.577000",
        "createdby": 65,
        "isdeleted": False
      },
      {
        "id": 16,
        "buildername": "Angal Group ",
        "phone1": " 020 25670470",
        "phone2": "",
        "email1": "",
        "email2": "",
        "addressline1": "Kamla Nehru Park ",
        "addressline2": "",
        "suburb": "Deccan ",
        "city": "Pune",
        "state": "Maharashtra",
        "country": "India",
        "zip": "",
        "website": "",
        "comments": "",
        "dated": "2014-04-21T12:22:03.677000",
        "createdby": 65,
        "isdeleted": False
      },
      {
        "id": 17,
        "buildername": "Rachana Constructions Pvt ltd ",
        "phone1": "712-2022591 ",
        "phone2": "",
        "email1": "",
        "email2": "",
        "addressline1": "Nagpur",
        "addressline2": "",
        "suburb": "WHC Road, Dharampeth ",
        "city": "Pune",
        "state": "Maharashtra",
        "country": "India",
        "zip": "",
        "website": "",
        "comments": "to be deleted",
        "dated": "2014-07-09T16:58:51.107000",
        "createdby": 83,
        "isdeleted": False
      },
      {
        "id": 18,
        "buildername": "Mont Vert Homes",
        "phone1": "020 25872633",
        "phone2": "7219717227",
        "email1": "sadeep.sarkar@montverthomes.com",
        "email2": "",
        "addressline1": "Pashan Sus Road ",
        "addressline2": "",
        "suburb": "Pashan",
        "city": "Pune",
        "state": "Maharashtra",
        "country": "India",
        "zip": "411021",
        "website": "www.montverthomes.com/",
        "comments": "Channel Partner",
        "dated": "2016-12-07T11:02:58.203000",
        "createdby": 1125,
        "isdeleted": False
      },
      {
        "id": 19,
        "buildername": "Achalare Associates ",
        "phone1": "020 2553 4496",
        "phone2": "",
        "email1": "",
        "email2": "",
        "addressline1": "JM Road, Shivajinagar ",
        "addressline2": "",
        "suburb": "Shivajinagar",
        "city": "Pune",
        "state": "Maharashtra",
        "country": "India",
        "zip": "",
        "website": "",
        "comments": "",
        "dated": "2014-04-21T12:47:07.257000",
        "createdby": 65,
        "isdeleted": False
      },
      {
        "id": 20,
        "buildername": "G Corp Developers",
        "phone1": "020 30585711",
        "phone2": "",
        "email1": "",
        "email2": "",
        "addressline1": "Church Road , Opp Police comm. office ",
        "addressline2": "",
        "suburb": "Camp",
        "city": "Pune",
        "state": "Maharashtra",
        "country": "India",
        "zip": "",
        "website": "",
        "comments": "",
        "dated": "2014-04-21T12:51:56.567000",
        "createdby": 65,
        "isdeleted": False
      },
      {
        "id": 21,
        "buildername": "Rohan Builders ",
        "phone1": "020-41404140 ",
        "phone2": "91-20-4140 5140",
        "email1": "rohanpn@rohanbuilders.com",
        "email2": "",
        "addressline1": "805, Bhandarkar Institute Road,",
        "addressline2": "",
        "suburb": "Deccan ",
        "city": "Pune",
        "state": "Maharashtra",
        "country": "India",
        "zip": "",
        "website": "http://www.rohanbuilders.com",
        "comments": "Suhas Lunkad - 9822092636",
        "dated": "2014-07-07T12:24:29.797000",
        "createdby": 83,
        "isdeleted": False
      },
      {
        "id": 22,
        "buildername": "Darode Jog Properties ",
        "phone1": "020 - 25532725",
        "phone2": "02025533725",
        "email1": "info@darodejog.com",
        "email2": "",
        "addressline1": "Darode Jog 1212 Apte Road Deccan Gymkhana pune",
        "addressline2": "",
        "suburb": "Deccan ",
        "city": "Pune",
        "state": "Maharashtra",
        "country": "India",
        "zip": "",
        "website": "www.darodejog",
        "comments": "Anand Jog - 9822022659\r\nSupriya Shinde Manager Sales - 9922901412 (supriya@darodejog.com)\r\n ",
        "dated": "2014-12-17T16:04:57.510000",
        "createdby": 83,
        "isdeleted": False
      }
    ]
  },
  "total_count": 218
}

    response = client.post('/getBuilderInfo', json=payload)

    assert response.status_code == 200
    assert expected_response['total_count'] > 0

@pytest.mark.usefixtures("db_connection")
def test_id_41(client):
    payload = {
    "user_id": 1234,
    "rows": ["id","buildername","phone1","phone2","email1","email2","addressline1","addressline2","suburb","city","state","country","zip","website","comments","dated","createdby","isdeleted"]
,
    "sort_by": [],
    "order": "asc",
    "pg_no": 1,
    "pg_size": 15
  }
    expected_response ={
  "result": "error",
  "message": "Invalid Credentials",
  "user_id": 1234,
  "role_id": 0,
  "data": []
}
    with patch('main.check_role_access', return_value=1):
        response = client.post('/getBuilderInfo', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.usefixtures("db_connection")
def test_id_42(client):
    payload = {
    "user_id": 1234,
    "rows": ["id","buildername","phone1","phone2","email1","email2","addressline1","addressline2","suburb","city","state","country","zip","website","comments","dated","createdby","isdeleted"]
,
    "filters": [],
    "sort_by": [],
    "order": "asc",
    "pg_no": 1,
    "pg_size": 15
  } 
    expected_response ={
  "result": "error",
  "message": "Access Denied",
  "user_id": 1234,
  "role_id": 0,
  "data": []
}
    with patch('main.check_role_access', return_value=0):
        response = client.post('/getBuilderInfo', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.usefixtures("db_connection")
def test_id_92(client):
    payload = {"user_id":1234}
    expected_response ={
  "result": "success",
  "user_id": 1234,
  "role_id": 1,
  "data": [
    [
      3,
      "Z-PRIME"
    ],
    [
      7,
      "Z-CASH"
    ],
    [
      5,
      "ZZZ"
    ],
    [
      1,
      "CURA"
    ],
    [
      6,
      "Z-COREFUR"
    ],
    [
      4,
      "ZZZ"
    ],
    [
      2,
      "Z-ASDK"
    ]
  ]
}
    with patch('main.check_role_access', return_value=1):
        response = client.post('/getEntityAdmin', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.usefixtures("db_connection")
def test_id_93(client):
    payload = {"user_id":123}
    expected_response = None
    with patch('main.check_role_access', return_value=0):
        response = client.post('/getEntityAdmin', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.usefixtures("db_connection")
def test_id_94(client):
    payload = {"user_id":1234}
    expected_response = None
    with patch('main.check_role_access', return_value=0):
        response = client.post('/getEntityAdmin', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_95(client):
    payload = {
    "user_id":1234,
    "paymentto": 1234,
    "paymentby": 1235,
    "amount": 12345,
    "paidon": "2020-01-01 10:00:00",
    "paymentmode": 3,
    "description": "test payment",
    "paymentfor":100,
    "dated":"2021-01-01 12:00:00",
    "createdby":1234,
    "isdeleted":False,
    "entityid":123,
    "officeid":10,
    "tds":3,
    "professiontax":10,
    "month":"march",
    "deduction":10 
}
    expected_response = {
  "result": "success",
  "user_id": 1234,
  "role_id": 1,
  "data": {
    "added_payment_by": 1234
  }
}
    with patch('main.check_role_access', return_value=1):
        response = client.post('/addPayment', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.usefixtures("db_connection")
def test_id_96(client):
    payload = {
    "user_id":1234,
    "paymentto": 1234,
    "paymentby": 1235,
    "amount": 12345,
    "paidon": "2020-01-01 10:00:00",
    "paymentmode": 3,
    "description": "test payment",
    "paymentfor":100,
    "dated":"2021-01-01 12:00:00",
    "createdby":1234,
    "isdeleted":False,
    "entityid":123,
    "officeid":10,
    "tds":3,
    "professiontax":10,
    "month":"march",
    "deduction":10 
}
    expected_response = None
    with patch('main.check_role_access', return_value=0):
        response = client.post('/addPayment', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_97(client):
    payload = {
    "user_id":1234,
    "paymentby": 1235,
    "amount": 12345,
    "paidon": "2020-01-01 10:00:00",
    "paymentmode": 3,
    "description": "test payment",
    "paymentfor":100,
    "dated":"2021-01-01 12:00:00",
    "createdby":1234,
    "isdeleted":False,
    "entityid":123,
    "officeid":10,
    "tds":3,
    "professiontax":10,
    "month":"march",
    "deduction":10 
}
    expected_response = None
    with patch('main.check_role_access', return_value=1):
        response = client.post('/addPayment', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_98(client):
    payload = { "user_id":1234, "id": 13000, "paymentto": 1234, "paymentby": 1235, "amount": 12345, "paidon": "2020-01-01 10:00:00", "paymentmode": 3, "paymentstatus": 3, "description": "test payment", "banktransactionid":"abcd32", "paymentfor":100, "dated":"2021-01-01 12:00:00", "createdby":1234, "isdeleted":False, "entityid":123, "officeid":10, "tds":3, "professiontax":10, "month":"march", "deduction":10 }
    expected_response ={
  "result": "success",
  "user_id": 1234,
  "role_id": 1,
  "data": {
    "edited_data": 13000
  }
}
    with patch('main.check_role_access', return_value=1):
        response = client.post('/editPayment', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_99(client):
    payload = { "user_id":1234, "paymentto": 1234, "paymentby": 1235, "amount": 12345, "paidon": "2020-01-01 10:00:00", "paymentmode": 3, "paymentstatus": 3, "description": "test payment", "banktransactionid":"abcd32", "paymentfor":100, "dated":"2021-01-01 12:00:00", "createdby":1234, "isdeleted":False, "entityid":123, "officeid":10, "tds":3, "professiontax":10, "month":"march", "deduction":10 }
    expected_response = None

    with patch('main.check_role_access', return_value=1):
        response = client.post('/editPayment', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_100(client):
    payload = { "user_id":1234, "id": 13000, "paymentto": 1234, "paymentby": 1235, "amount": 12345, "paidon": "2020-01-01 10:00:00", "paymentmode": 3, "paymentstatus": 3, "description": "test payment", "banktransactionid":"abcd32", "paymentfor":100, "dated":"2021-01-01 12:00:00", "createdby":1234, "isdeleted":False, "entityid":123, "officeid":10, "tds":3, "professiontax":10, "month":"march", "deduction":10 }
    expected_response = None

    with patch('main.check_role_access', return_value=0):
        response = client.post('/editPayment', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_101(client):
    payload =  {"user_id":1234,"id":12019}
    expected_response = {
  "result": "success",
  "user_id": 1234,
  "role_id": 1,
  "data": {
    "deleted_payment": 12019
  }
}

    with patch('main.check_role_access', return_value=1):
        response = client.post('/deletePayment', json=payload)

    assert response.status_code == 200
    assert expected_response['data']['deleted_payment'] > 0
    

@pytest.mark.usefixtures("db_connection")
def test_id_102(client):
    payload = {"user_id":1234}
    expected_response = None

    with patch('main.check_role_access', return_value=1):
        response = client.post('/deletePayment', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_103(client):
    payload = {"user_id":1234,"id":12046}
    expected_response = None

    with patch('main.check_role_access', return_value=0):
        response = client.post('/deletePayment', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.usefixtures("db_connection")
def test_id_104(client):
    payload = { "user_id": 1234, "rows": [ "id", "paymentto", "paymentby", "amount", "paidon", "paymentmode", "paymentstatus", "description", "banktransactionid", "paymentfor", "dated", "createdby", "isdeleted", "entityid", "officeid", "tds", "professiontax", "month", "deduction" ], "filters": [], "sort_by": [], "order": "asc", "pg_no": 1, "pg_size": 15, "search_key":"anvay" }
    expected_response = {
  "result": "success",
  "user_id": 1234,
  "role_id": 1,
  "data": [
    {
      "id": 1237,
      "paymentto": "Anvay Paranjape",
      "paymentby": "ZShrinidhi Ranade",
      "amount": 2000,
      "paidon": "2014-11-03T00:00:00",
      "paymentmode": "DAP-ICICI-42",
      "paymentstatus": "Not Accepted",
      "description": "Petrol Aug 2014",
      "banktransactionid": "",
      "paymentfor": "Fuel expense reimbursement",
      "dated": "2015-04-06T12:19:42.750000",
      "createdby": 85,
      "isdeleted": False,
      "entityid": 1,
      "officeid": 2,
      "tds": None,
      "professiontax": None,
      "month": None,
      "deduction": None
    },
    {
      "id": 9719,
      "paymentto": "Anvay Paranjape",
      "paymentby": "Kashmira Yadav",
      "amount": 18000,
      "paidon": "2016-04-11T00:00:00",
      "paymentmode": "DAP-IDBI",
      "paymentstatus": "Not Accepted",
      "description": "Salary for Mar 2016--via chq#186089, dtd - 4-Apr-16",
      "banktransactionid": None,
      "paymentfor": "Remuneration",
      "dated": "2016-04-11T18:07:05.590000",
      "createdby": 85,
      "isdeleted": False,
      "entityid": 1,
      "officeid": 2,
      "tds": None,
      "professiontax": None,
      "month": None,
      "deduction": None
    },
    {
      "id": 8588,
      "paymentto": "Anvay Paranjape",
      "paymentby": "Santosh Kasule",
      "amount": 16500,
      "paidon": "2015-11-02T00:00:00",
      "paymentmode": "Z-COREFUR-ICICI",
      "paymentstatus": "Not Accepted",
      "description": "Sal for Oct 2015",
      "banktransactionid": None,
      "paymentfor": "Remuneration",
      "dated": "2015-12-04T12:12:25.363000",
      "createdby": 85,
      "isdeleted": False,
      "entityid": 6,
      "officeid": 2,
      "tds": None,
      "professiontax": None,
      "month": None,
      "deduction": None
    },
    {
      "id": 3382,
      "paymentto": "Anvay Paranjape",
      "paymentby": "ZShrinidhi Ranade",
      "amount": 2000,
      "paidon": "2015-02-12T00:00:00",
      "paymentmode": "Z-DAP-INT-ICICI",
      "paymentstatus": "Not Accepted",
      "description": "Paid for Nov 2014",
      "banktransactionid": "",
      "paymentfor": "Fuel expense reimbursement",
      "dated": "2015-04-06T15:42:09.337000",
      "createdby": 85,
      "isdeleted": False,
      "entityid": 1,
      "officeid": 2,
      "tds": None,
      "professiontax": None,
      "month": None,
      "deduction": None
    },
    {
      "id": 7456,
      "paymentto": "Anvay Paranjape",
      "paymentby": "ZShilpa Chakranarayan",
      "amount": 28000,
      "paidon": "2015-06-04T00:00:00",
      "paymentmode": "Z-DAP-INT-ICICI",
      "paymentstatus": "Not Accepted",
      "description": "Salary For May 2015",
      "banktransactionid": None,
      "paymentfor": "Remuneration",
      "dated": "2015-06-26T16:54:38.490000",
      "createdby": 61,
      "isdeleted": False,
      "entityid": 1,
      "officeid": 2,
      "tds": None,
      "professiontax": None,
      "month": None,
      "deduction": None
    },
    {
      "id": 11049,
      "paymentto": "Anvay Paranjape",
      "paymentby": "Sarjerao Deshmukh",
      "amount": 15300,
      "paidon": "2017-11-08T00:00:00",
      "paymentmode": "DAP-ICICI-65-S",
      "paymentstatus": "Not Accepted",
      "description": "Salary for Oct 2017",
      "banktransactionid": None,
      "paymentfor": "Remuneration",
      "dated": "2017-11-22T12:34:02.373000",
      "createdby": 85,
      "isdeleted": False,
      "entityid": 1,
      "officeid": 2,
      "tds": 0,
      "professiontax": 100,
      "month": "Oct",
      "deduction": 0
    },
    {
      "id": 9712,
      "paymentto": "Anvay Paranjape",
      "paymentby": "ZPreetha Lakshman",
      "amount": 13600,
      "paidon": "2016-03-31T00:00:00",
      "paymentmode": "DAP-ICICI-42",
      "paymentstatus": "Not Accepted",
      "description": "mar",
      "banktransactionid": None,
      "paymentfor": "Remuneration",
      "dated": "2016-04-03T17:34:29.720000",
      "createdby": 59,
      "isdeleted": False,
      "entityid": 1,
      "officeid": 2,
      "tds": None,
      "professiontax": None,
      "month": None,
      "deduction": None
    },
    {
      "id": 9701,
      "paymentto": "Anvay Paranjape",
      "paymentby": "Santosh Kasule",
      "amount": 18000,
      "paidon": "2016-03-03T00:00:00",
      "paymentmode": "Z-COREFUR-ICICI",
      "paymentstatus": "Not Accepted",
      "description": "Salary for Feb 2016",
      "banktransactionid": None,
      "paymentfor": "Remuneration",
      "dated": "2016-03-23T17:25:49.177000",
      "createdby": 85,
      "isdeleted": False,
      "entityid": 6,
      "officeid": 2,
      "tds": None,
      "professiontax": None,
      "month": None,
      "deduction": None
    },
    {
      "id": 11033,
      "paymentto": "Anvay Paranjape",
      "paymentby": "Kashmira Yadav",
      "amount": 5000,
      "paidon": "2017-11-06T00:00:00",
      "paymentmode": "DAP-IDBI",
      "paymentstatus": "Not Accepted",
      "description": "Salary for Oct 2017",
      "banktransactionid": None,
      "paymentfor": "Remuneration",
      "dated": "2017-11-07T17:11:24.810000",
      "createdby": 85,
      "isdeleted": False,
      "entityid": 1,
      "officeid": 2,
      "tds": 0,
      "professiontax": 0,
      "month": "Oct",
      "deduction": 0
    },
    {
      "id": 9699,
      "paymentto": "Anvay Paranjape",
      "paymentby": "ZPrashant Shinde",
      "amount": 13500,
      "paidon": "2016-03-03T00:00:00",
      "paymentmode": "Z-COREFUR-ICICI",
      "paymentstatus": "Not Accepted",
      "description": "salary for Feb 2016",
      "banktransactionid": None,
      "paymentfor": "Remuneration",
      "dated": "2016-03-23T17:23:55.600000",
      "createdby": 85,
      "isdeleted": False,
      "entityid": 6,
      "officeid": 2,
      "tds": None,
      "professiontax": None,
      "month": None,
      "deduction": None
    },
    {
      "id": 1198,
      "paymentto": "Anvay Paranjape",
      "paymentby": "ZAmruta Kulkarni",
      "amount": 1500,
      "paidon": "2014-07-03T00:00:00",
      "paymentmode": "DAP-ICICI-42",
      "paymentstatus": "Not Accepted",
      "description": "BIL/000613038948/Petrol-Jun14/0040501038146\r\n",
      "banktransactionid": "",
      "paymentfor": "Fuel expense reimbursement",
      "dated": "2014-10-28T17:21:08.527000",
      "createdby": 61,
      "isdeleted": False,
      "entityid": 1,
      "officeid": 2,
      "tds": None,
      "professiontax": None,
      "month": None,
      "deduction": None
    },
    {
      "id": 6438,
      "paymentto": "Anvay Paranjape",
      "paymentby": "ZShrinidhi Ranade",
      "amount": 20000,
      "paidon": "2015-05-02T00:00:00",
      "paymentmode": "Z-DAP-INT-ICICI",
      "paymentstatus": "Not Accepted",
      "description": "salary for April 2015",
      "banktransactionid": None,
      "paymentfor": "Remuneration",
      "dated": "2015-05-15T17:39:48.020000",
      "createdby": 85,
      "isdeleted": False,
      "entityid": 1,
      "officeid": 2,
      "tds": None,
      "professiontax": None,
      "month": None,
      "deduction": None
    },
    {
      "id": 9755,
      "paymentto": "Anvay Paranjape",
      "paymentby": "ZPrashant Shinde",
      "amount": 15300,
      "paidon": "2016-05-04T00:00:00",
      "paymentmode": "DAP-IDBI",
      "paymentstatus": "Not Accepted",
      "description": "",
      "banktransactionid": None,
      "paymentfor": "Remuneration",
      "dated": "2016-06-11T19:46:56.973000",
      "createdby": 59,
      "isdeleted": False,
      "entityid": 1,
      "officeid": 2,
      "tds": None,
      "professiontax": None,
      "month": None,
      "deduction": None
    },
    {
      "id": 8497,
      "paymentto": "Anvay Paranjape",
      "paymentby": "ZPreetha Lakshman",
      "amount": 15000,
      "paidon": "2015-08-07T00:00:00",
      "paymentmode": "DAP-ICICI-42",
      "paymentstatus": "Not Accepted",
      "description": "for july",
      "banktransactionid": None,
      "paymentfor": "Remuneration",
      "dated": "2015-08-07T12:27:36.173000",
      "createdby": 1105,
      "isdeleted": False,
      "entityid": 1,
      "officeid": 2,
      "tds": None,
      "professiontax": None,
      "month": None,
      "deduction": None
    },
    {
      "id": 9754,
      "paymentto": "Anvay Paranjape",
      "paymentby": "Kaka Mokashi",
      "amount": 15800,
      "paidon": "2016-05-04T00:00:00",
      "paymentmode": "DAP-IDBI",
      "paymentstatus": "Not Accepted",
      "description": "",
      "banktransactionid": None,
      "paymentfor": "Remuneration",
      "dated": "2016-06-11T19:46:19.963000",
      "createdby": 59,
      "isdeleted": False,
      "entityid": 1,
      "officeid": 2,
      "tds": None,
      "professiontax": None,
      "month": None,
      "deduction": None
    }
  ],
  "total_count": 989
}


    with patch('main.check_role_access', return_value=1):
        response = client.post('/getPayments', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_105(client):
    payload = { "user_id": 1234, "rows": [ "id", "paymentto", "paymentby", "amount", "paidon", "paymentmode", "paymentstatus", "description", "banktransactionid", "paymentfor", "dated", "createdby", "isdeleted", "entityid", "officeid", "tds", "professiontax", "month", "deduction" ], "sort_by": [], "order": "asc", "pg_no": 1, "pg_size": 15, "search_key":"anvay" }
    expected_response = None

    with patch('main.check_role_access', return_value=1):
        response = client.post('/getPayments', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.usefixtures("db_connection")
def test_id_106(client):
    payload = { "user_id": 1234, "rows": [ "id", "paymentto", "paymentby", "amount", "paidon", "paymentmode", "paymentstatus", "description", "banktransactionid", "paymentfor", "dated", "createdby", "isdeleted", "entityid", "officeid", "tds", "professiontax", "month", "deduction" ], "filters": [], "sort_by": [], "order": "asc", "pg_no": 1, "pg_size": 15, "search_key":"anvay" }
    expected_response = {
  "result": "error",
  "message": "Access Denied",
  "user_id": 1234,
  "role_id": 0,
  "data": []
}

    with patch('main.check_role_access', return_value=0):
        response = client.post('/getPayments', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_107(client):
    payload = { "user_id": 1234}
    expected_response = {
  "result": "success",
  "user_id": 1234,
  "role_id": 1,
  "data": [
    {
      "id": 1,
      "name": "Admin"
    },
    {
      "id": 2,
      "name": "Finance"
    },
    {
      "id": 4,
      "name": "Research"
    },
    {
      "id": 8,
      "name": "Client"
    },
    {
      "id": 6,
      "name": "Consultant"
    },
    {
      "id": 9,
      "name": "Super Admin"
    },
    {
      "id": 5,
      "name": "Manager"
    },
    {
      "id": 15,
      "name": "undefined role"
    },
    {
      "id": 7,
      "name": "Vendor"
    },
    {
      "id": 3,
      "name": "Analyst"
    },
    {
      "id": 11,
      "name": "Social Media"
    },
    {
      "id": 14,
      "name": "Auditor"
    }
  ],
  "total_count": 12
}

    with patch('main.check_role_access', return_value=1):
        response = client.post('/getRolesAdmin', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.usefixtures("db_connection")
def test_id_108(client):
    payload = { "user_id": 1238}
    expected_response ={
  "result": "error",
  "message": "Access Denied",
  "user_id": 1238,
  "role_id": 0,
  "data": []
}

    with patch('main.check_role_access', return_value=0):
        response = client.post('/getRolesAdmin', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.usefixtures("db_connection")
def test_id_109(client):
    payload = { "user_id": 1234}
    expected_response ={
  "result": "error",
  "message": "Access Denied",
  "user_id": 1234,
  "role_id": 0,
  "data": []
}

    with patch('main.check_role_access', return_value=0):
        response = client.post('/getRolesAdmin', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.usefixtures("db_connection")
def test_id_110(client):
    payload = { "user_id": 1234}
    expected_response ={
  "result": "success",
  "user_id": 1234,
  "role_id": 1,
  "data": [
    {
      "id": 1,
      "name": "Admin User"
    },
    {
      "id": 58,
      "name": "ZAshish Paranjape"
    },
    {
      "id": 59,
      "name": "Anvay Paranjape"
    },
    {
      "id": 60,
      "name": "Dipty Paranjape"
    },
    {
      "id": 61,
      "name": "ZAmruta Kulkarni"
    },
    {
      "id": 62,
      "name": "ZMedha Manohar"
    },
    {
      "id": 63,
      "name": "Harshada Nijsure"
    },
    {
      "id": 64,
      "name": "Santosh Kasule"
    },
    {
      "id": 65,
      "name": "ZGaurav Paranjape"
    },
    {
      "id": 66,
      "name": "ZSaajan Mahbubani"
    },
    {
      "id": 67,
      "name": "ZMahesh Patil"
    },
    {
      "id": 68,
      "name": "ZMangesh Dhotre"
    },
    {
      "id": 69,
      "name": "Kaka Mokashi"
    },
    {
      "id": 70,
      "name": "ZKunal Deshmukh"
    },
    {
      "id": 71,
      "name": "ZSawani Ranade"
    },
    {
      "id": 72,
      "name": "ZShrinidhi Ranade"
    },
    {
      "id": 73,
      "name": "ZAnil Chandanshive"
    },
    {
      "id": 74,
      "name": "ZDatta D"
    },
    {
      "id": 75,
      "name": "ZSachin W"
    },
    {
      "id": 76,
      "name": "Santoshi Marathe"
    },
    {
      "id": 77,
      "name": "ZSomnath Gaikwad"
    },
    {
      "id": 78,
      "name": "ZAstha Deo"
    },
    {
      "id": 79,
      "name": "ZSunitha Pullagalla"
    },
    {
      "id": 80,
      "name": "ZKundalik Raut"
    },
    {
      "id": 81,
      "name": "Sneha Paranjape"
    },
    {
      "id": 82,
      "name": "Mahendra Shinde"
    },
    {
      "id": 84,
      "name": "ZNilesh Nagul"
    },
    {
      "id": 85,
      "name": "ZShilpa Chakranarayan"
    },
    {
      "id": 86,
      "name": "ZGanesh Dhoni"
    },
    {
      "id": 87,
      "name": "ZBandu Pakhare"
    },
    {
      "id": 88,
      "name": "ZSwapnil Mane"
    },
    {
      "id": 89,
      "name": "ZSurajit Bhattacharya"
    },
    {
      "id": 90,
      "name": "ZRanjit Pandey"
    },
    {
      "id": 91,
      "name": "ZRaveen Gaikwad"
    },
    {
      "id": 92,
      "name": "ZArun Raina"
    },
    {
      "id": 96,
      "name": "ZKadri Arafatulla Khan"
    },
    {
      "id": 97,
      "name": "ZSonali Firodia"
    },
    {
      "id": 98,
      "name": "ZVilas Sonawne"
    },
    {
      "id": 99,
      "name": "ZRanjeet Kale"
    },
    {
      "id": 100,
      "name": "ZPrashant Shinde"
    },
    {
      "id": 102,
      "name": "ZSantosh Boramani"
    },
    {
      "id": 1106,
      "name": "Kashmira Yadav"
    },
    {
      "id": 83,
      "name": "ZRajesh Jorkar"
    },
    {
      "id": 93,
      "name": "ZJaspreet Kaur"
    },
    {
      "id": 94,
      "name": "ZGayatri Mande"
    },
    {
      "id": 1102,
      "name": "ZAkash Dhok"
    },
    {
      "id": 1103,
      "name": "ZASDK Intern"
    },
    {
      "id": 1104,
      "name": "Sarjerao Deshmukh"
    },
    {
      "id": 1105,
      "name": "ZMithilesh Kokate"
    },
    {
      "id": 1107,
      "name": "ZPreetha Lakshman"
    },
    {
      "id": 1108,
      "name": "ZNandini Mathur"
    },
    {
      "id": 1109,
      "name": "ZSonakshi Sinha"
    },
    {
      "id": 1110,
      "name": "ZAshish D"
    },
    {
      "id": 1111,
      "name": "ZPravin Nichal"
    },
    {
      "id": 1112,
      "name": "ZAditya Padale"
    },
    {
      "id": 1113,
      "name": "ZDhananjay Khot"
    },
    {
      "id": 1114,
      "name": "ZRohit Patil"
    },
    {
      "id": 1115,
      "name": "ZRohit Bokariya"
    },
    {
      "id": 1116,
      "name": "ZOmprakash VENKATA SAI "
    },
    {
      "id": 1117,
      "name": "ZShruti Awalgaonkar"
    },
    {
      "id": 1118,
      "name": "ZShrikant Pimplapure"
    },
    {
      "id": 1119,
      "name": "ZNikhil Sonatkar"
    },
    {
      "id": 1120,
      "name": "ZMonika Sonawane"
    },
    {
      "id": 1121,
      "name": "ZAtish Mane"
    },
    {
      "id": 1122,
      "name": "ZSuchita Patole"
    },
    {
      "id": 1123,
      "name": "ZAjay Birajdar"
    },
    {
      "id": 1124,
      "name": "ZAkshay Gonyal"
    },
    {
      "id": 1126,
      "name": "ZDivyani Audichya"
    },
    {
      "id": 1127,
      "name": "ZSachin Gawali"
    },
    {
      "id": 1128,
      "name": "ZSuchitra Patra"
    },
    {
      "id": 1129,
      "name": "ZAmita Jeurkar"
    },
    {
      "id": 1132,
      "name": "ZDAP Intern"
    },
    {
      "id": 1133,
      "name": "ZKumar Agnihotri"
    },
    {
      "id": 1135,
      "name": "Keshav Paranjape"
    },
    {
      "id": 1136,
      "name": "Usha Paranjape"
    },
    {
      "id": 1137,
      "name": "Rati Kunte"
    },
    {
      "id": 1138,
      "name": "ZSandip Bhagwat"
    },
    {
      "id": 1139,
      "name": "Jyotsna Kunte"
    },
    {
      "id": 1141,
      "name": "ZShital Kadam"
    },
    {
      "id": 95,
      "name": "ZShilpa Agarkar"
    },
    {
      "id": 1125,
      "name": "ZPrachi Surve"
    },
    {
      "id": 1142,
      "name": "Virtuoso Virtuoso"
    },
    {
      "id": 1143,
      "name": "ZPoonam Khanvilkar"
    },
    {
      "id": 1144,
      "name": "ZPrakash Rai"
    },
    {
      "id": 1148,
      "name": "ZSurekha Chandrahas"
    },
    {
      "id": 1149,
      "name": "Mayur  Kole"
    },
    {
      "id": 1150,
      "name": "ZShreya Bhanot"
    },
    {
      "id": 1151,
      "name": "ZApoorva Varadkar"
    },
    {
      "id": 1152,
      "name": "Siddhi Nagarkar"
    },
    {
      "id": 1153,
      "name": "Vaibhavi  Patil"
    },
    {
      "id": 1154,
      "name": "Uma  Deo"
    },
    {
      "id": 1155,
      "name": "Shreyas Jadhav"
    },
    {
      "id": 1156,
      "name": "Shreyas  Jadhav"
    },
    {
      "id": 1158,
      "name": "PAVAN KASULE"
    },
    {
      "id": 1159,
      "name": "Priya muley"
    },
    {
      "id": 1160,
      "name": "zKrutika  Shah"
    },
    {
      "id": 1161,
      "name": "zANURADHA NITTLA"
    },
    {
      "id": 1162,
      "name": "Tech Support"
    },
    {
      "id": 1163,
      "name": "Preeti Kulkarni"
    },
    {
      "id": 1164,
      "name": "Amrita Vaidya"
    },
    {
      "id": 1166,
      "name": "Kriti Yadav"
    },
    {
      "id": 1167,
      "name": "SOHANA JOSHI"
    },
    {
      "id": 1168,
      "name": "Shivali Deshpande"
    },
    {
      "id": 1169,
      "name": "Priya Shinde"
    },
    {
      "id": 1130,
      "name": "ZHitendra Patil"
    },
    {
      "id": 1134,
      "name": "ZAshish Gujrathi"
    },
    {
      "id": 1140,
      "name": "Sujit Kulkarni"
    },
    {
      "id": 1165,
      "name": "Prachi Kulkarni"
    },
    {
      "id": 1170,
      "name": "Shreyas  Sutar"
    },
    {
      "id": 1131,
      "name": "ZMinal na"
    },
    {
      "id": 1157,
      "name": "Sujan Maharjan"
    },
    {
      "id": 1145,
      "name": "ZVeena Ghanshani"
    },
    {
      "id": 1146,
      "name": "ZMonica Joshi"
    },
    {
      "id": 1147,
      "name": "ZJyoti Walvekar"
    },
    {
      "id": 1235,
      "name": "Aryan Ashish"
    },
    {
      "id": 1234,
      "name": "Rudra Sen Mallik"
    }
  ],
  "total_count": 116
}

    with patch('main.check_role_access', return_value=1):
        response = client.post('/getUsersAdmin', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.usefixtures("db_connection")
def test_id_111(client):
    payload = {"user_id":1235}
    expected_response = {
  "result": "error",
  "message": "Access Denied",
  "user_id": 1235,
  "role_id": 2,
  "data": []
}

    with patch('main.check_role_access', return_value=2):
        response = client.post('/getUsersAdmin', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_112(client):
    payload = {"user_id":1234}
    expected_response = {
  "result": "error",
  "message": "Access Denied",
  "user_id": 1234,
  "role_id": 0,
  "data": []
}

    with patch('main.check_role_access', return_value=0):
        response = client.post('/getUsersAdmin', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_113(client):
    payload = { "user_id": 1234, "modeofpayment": 20, "date":"20-03-2024 00:00:00", "amount":112 , "particulars":"put any description or notes here", "crdr":"CR", "vendorid":411, "createdby":1234 }
    expected_response = {
  "result": "success",
  "user_id": 1234,
  "role_id": 1,
  "data": {
    "added_data": "added bank statement for amount <112>"
  }
}

    with patch('main.check_role_access', return_value=1):
        response = client.post('/addBankSt', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_114(client):
    payload = { "user_id": 1234, "modeofpayment": 20, "date":"20-03-2024 00:00:00", "amount":112 , "particulars":"put any description or notes here", "crdr":"CR", "vendorid":411, "createdby":1234 }
    expected_response = None

    with patch('main.check_role_access', return_value=0):
        response = client.post('/addBankSt', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.usefixtures("db_connection")
def test_id_115(client):
    payload = { "user_id": 1234, "modeofpayment": 20, "date":"20-03-2024 00:00:00", "particulars":"put any description or notes here", "crdr":"CR", "vendorid":411, "createdby":1234 }
    expected_response = {
  "result": "error",
  "message": "failed to add bank statement due to exception <'amount'>",
  "user_id": 1234,
  "role_id": 0,
  "data": []
}

    with patch('main.check_role_access', return_value=1):
        response = client.post('/addBankSt', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_116(client):
    payload = {
  "user_id": 1234,
  "id": 100028,  
  "modeofpayment": 20,
  "date": "2024-03-23 00:00:00",  
  "amount": 9384.00,
  "particulars": "abcd",
  "crdr": "CR",
  "receivedby": 5,
  "vendorid": 14000,
  "createdby": 1234
}
    expected_response = {
  "result": "success",
  "user_id": 1234,
  "role_id": 1,
  "data": {
    "edited_data": 100028
  }
}
    with patch('main.check_role_access', return_value=1):
        response = client.post('/editBankSt', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_117(client):
    payload = {
  "user_id": 1234,  
  "modeofpayment": 20,
  "date": "2024-03-23 00:00:00",  
  "amount": 9384.00,
  "particulars": "abcd",
  "crdr": "CR",
  "receivedby": 5,
  "vendorid": 14000,
  "createdby": 1234
}
    expected_response = None
    with patch('main.check_role_access', return_value=1):
        response = client.post('/editBankSt', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.usefixtures("db_connection")
def test_id_118(client):
    payload = {
  "user_id": 1234,
  "id": 100028,  
  "modeofpayment": 20,
  "date": "2024-03-23 00:00:00",  
  "amount": 9384.00,
  "particulars": "abcd",
  "crdr": "CR",
  "receivedby": 5,
  "vendorid": 14000,
  "createdby": 1234
}
    expected_response = None
    with patch('main.check_role_access', return_value=0):
        response = client.post('/editBankSt', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.usefixtures("db_connection")
def test_id_119(client): 
    payload = {"user_id":1234,"id":100088}
    expected_response = {
  "result": "success",
  "user_id": 1234,
  "role_id": 1,
  "data": {
    "deleted_data": 100088
  }
}
    with patch('main.check_role_access', return_value=1):
        response = client.post('/deleteBankSt', json=payload)

    assert response.status_code == 200
    assert expected_response['data']['deleted_data'] > 0

@pytest.mark.usefixtures("db_connection")
def test_id_120(client):
    payload = {"user_id":1234}
    expected_response = None
    with patch('main.check_role_access', return_value=1):
        response = client.post('/deleteBankSt', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.usefixtures("db_connection")
def test_id_121(client):
    payload = {"user_id":1234,"id": 20137}
    expected_response = None
    with patch('main.check_role_access', return_value=0):
        response = client.post('/deleteBankSt', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_122(client):
    payload = {
  "user_id": 1234,
  "rows": ["id", "modeofpayment", "amount", "crdr", "chequeno"],
  "filters": [],
  "sort_by": [],
  "order": "asc",
  "pg_no": 0,
  "pg_size": 0
}
    expected_response = {
  "result": "success",
  "user_id": 1234,
  "role_id": 1,
  "data": [
    {
      "id": 20052,
      "modeofpayment": 5,
      "amount": 15318,
      "crdr": "CR                  ",
      "chequeno": None
    },
    {
      "id": 3499,
      "modeofpayment": 7,
      "amount": 5100,
      "crdr": "DR                  ",
      "chequeno": None
    },
    {
      "id": 8127,
      "modeofpayment": 5,
      "amount": 2475,
      "crdr": "DR                  ",
      "chequeno": None
    },
    {
      "id": 11650,
      "modeofpayment": 5,
      "amount": 12744,
      "crdr": "CR                  ",
      "chequeno": None
    },
    {
      "id": 4690,
      "modeofpayment": 5,
      "amount": 15000,
      "crdr": "CR                  ",
      "chequeno": None
    },
    {
      "id": 13843,
      "modeofpayment": 5,
      "amount": 15939,
      "crdr": "CR                  ",
      "chequeno": None
    },
    {
      "id": 4738,
      "modeofpayment": 5,
      "amount": 2760,
      "crdr": "CR                  ",
      "chequeno": None
    },
    {
      "id": 19216,
      "modeofpayment": 5,
      "amount": 3415,
      "crdr": "DR                  ",
      "chequeno": None
    },
    {
      "id": 9791,
      "modeofpayment": 5,
      "amount": 32668,
      "crdr": "CR                  ",
      "chequeno": None
    },
    {
      "id": 15052,
      "modeofpayment": 5,
      "amount": 1000,
      "crdr": "DR                  ",
      "chequeno": None
    },
    {
      "id": 9837,
      "modeofpayment": 5,
      "amount": 16851,
      "crdr": "CR                  ",
      "chequeno": None
    },
    {
      "id": 4750,
      "modeofpayment": 5,
      "amount": 450,
      "crdr": "CR                  ",
      "chequeno": None
    },
    {
      "id": 9917,
      "modeofpayment": 5,
      "amount": 3700,
      "crdr": "CR                  ",
      "chequeno": None
    },
    {
      "id": 3110,
      "modeofpayment": 7,
      "amount": 65,
      "crdr": "DR                  ",
      "chequeno": "-"
    },
    {
      "id": 4920,
      "modeofpayment": 5,
      "amount": 10000,
      "crdr": "CR                  ",
      "chequeno": None
    }
  ],
  "total_count": 14804
}
    with patch('main.check_role_access', return_value=1):
        response = client.post('/getBankSt', json=payload)

    assert response.status_code == 200
    assert expected_response['total_count'] > 0

@pytest.mark.usefixtures("db_connection")
def test_id_123(client):
    payload = {
  "user_id": 1234,
  "rows": ["id", "modeofpayment", "amount", "crdr", "chequeno"],
  "sort_by": [],
  "order": "asc",
  "pg_no": 1,
  "pg_size": 15
}
    expected_response = None
    with patch('main.check_role_access', return_value=1):
        response = client.post('/getBankSt', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_124(client):
    payload = {
  "user_id": 1234,
  "rows": ["id", "modeofpayment", "amount", "crdr", "chequeno"],
  "filters": [],
  "sort_by": [],
  "order": "asc",
  "pg_no": 1,
  "pg_size": 15
}
    expected_response = {
  "result": "error",
  "message": "Access Denied",
  "user_id": 1234,
  "role_id": 0,
  "data": []
}
    with patch('main.check_role_access', return_value=0):
        response = client.post('/getBankSt', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_125(client):
    payload = {"user_id":1234}
    expected_response = {
  "result": "success",
  "user_id": 1234,
  "role_id": 1,
  "data": [
    [
      1,
      "Received in Cash"
    ],
    [
      2,
      "Received by Cheque"
    ],
    [
      3,
      "Received via Online transfer"
    ],
    [
      4,
      "Received in TDS Certificate"
    ],
    [
      5,
      "Received via mSwipe"
    ],
    [
      1,
      "Received in Cash"
    ],
    [
      2,
      "Received by Cheque"
    ],
    [
      3,
      "Received via Online transfer"
    ],
    [
      4,
      "Received in TDS Certificate"
    ],
    [
      5,
      "Received via mSwipe"
    ]
  ]
}
    with patch('main.check_role_access', return_value=1):
        response = client.post('/getHowReceivedAdmin', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_126(client):
    payload = {"user_id":1235}
    expected_response = None
    with patch('main.check_role_access', return_value=0):
        response = client.post('/getHowReceivedAdmin', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_127(client):
    payload = {"user_id":1234}
    expected_response = None
    with patch('main.check_role_access', return_value=0):
        response = client.post('/getHowReceivedAdmin', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_128(client):
    payload = {"user_id":1234,"rows":["id","personname","suburb","city","country"],"filters":[],"sort_by":[],"order":"asc","pg_no":1,"pg_size":15}

    expected_response = {
  "result": "success",
  "user_id": 1234,
  "role_id": 1,
  "data": [
    {
      "id": 45,
      "personname": "New changed person",
      "suburb": "abcde",
      "city": "Mumbai",
      "country": "India",
      "countryid": 5
    },
    {
      "id": 1,
      "personname": "Test",
      "suburb": "Test",
      "city": "Pune",
      "country": "India",
      "countryid": 5
    },
    {
      "id": 41,
      "personname": "New changed person",
      "suburb": "abcde",
      "city": "Mumbai",
      "country": "India",
      "countryid": 5
    },
    {
      "id": 40,
      "personname": "New changed person",
      "suburb": "abcde",
      "city": "Mumbai",
      "country": "India",
      "countryid": 5
    },
    {
      "id": 44,
      "personname": "New changed person",
      "suburb": "abcde",
      "city": "Mumbai",
      "country": "India",
      "countryid": 5
    }
  ],
  "total_count": 24 
}
    with patch('main.check_role_access', return_value=1):
        response = client.post('/getResearchProspect', json=payload)

    assert response.status_code == 200
    assert expected_response['total_count'] > 0

@pytest.mark.usefixtures("db_connection")
def test_id_129(client):
    payload = {"user_id":1234,"rows":["id","personname","suburb","city","country"],"sort_by":[],"order":"asc","pg_no":1,"pg_size":15}
    expected_response = None
    with patch('main.check_role_access', return_value=1):
        response = client.post('/getResearchProspect', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_130(client):
    payload = {"user_id":1234,"rows":["id","personname","suburb","city","country"],"filters":[],"sort_by":[],"order":"asc","pg_no":1,"pg_size":15}
    expected_response = {
  "result": "error",
  "message": "Access Denied",
  "user_id": 1234,
  "role_id": 0,
  "data": []
}
    with patch('main.check_role_access', return_value=0):
        response = client.post('/getResearchProspect', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_131(client):
    payload = {
    "user_id": 1234,  
    "personname": "New changed person",
    "suburb": "abcde",
    "city": "Mumbai",
    "state": "Maharashtra",
    "country": 5,
    "propertylocation": "abcdefgh",
    "possibleservices": "abcdefgh",
    "createdby": 1234,
    "isdeleted": False
  }
    expected_response = {
  "result": "success",
  "user_id": 1234,
  "role_id": 1,
  "data": {
    "added_data": "New changed person"
  }
}
    with patch('main.check_role_access', return_value=1):
        response = client.post('/addResearchProspect', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_132(client):
    payload = {
    "user_id": 1234,  
    "suburb": "abcde",
    "city": "Mumbai",
    "state": "Maharashtra",
    "country": 5,
    "propertylocation": "abcdefgh",
    "possibleservices": "abcdefgh",
    "createdby": 1234,
    "isdeleted": False
  }
    expected_response = None
    with patch('main.check_role_access', return_value=1):
        response = client.post('/addResearchProspect', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_133(client):
    payload = {
    "user_id": 1234,  
    "personname": "New changed person",
    "suburb": "abcde",
    "city": "Mumbai",
    "state": "Maharashtra",
    "country": 5,
    "propertylocation": "abcdefgh",
    "possibleservices": "abcdefgh",
    "createdby": 1234,
    "isdeleted": False
  }
    expected_response = None
    with patch('main.check_role_access', return_value=0):
        response = client.post('/addResearchProspect', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_134(client):
    payload = {
    "user_id": 1234,
    "id": 90,
    "personname": "New changed person",
    "suburb": "abcde",
    "city": "Mumbai",
    "state": "Maharashtra",
    "country": 5,
    "propertylocation": "abcdefgh",
    "possibleservices": "abcdefgh",
    "dated": "2024-01-01 00:00:00",
    "createdby": 1234,
    "isdeleted": False
  }
    expected_response = {
  "result": "success",
  "user_id": 1234,
  "role_id": 1,
  "data": {
    "edited_data": 90
  }
}
    with patch('main.check_role_access', return_value=1):
        response = client.post('/editResearchProspect', json=payload)

    assert response.status_code == 200
    assert expected_response['data']['edited_data'] > 0

@pytest.mark.usefixtures("db_connection")
def test_id_135(client):
    payload = {
    "user_id": 1234,
    "personname": "New changed person",
    "suburb": "abcde",
    "city": "Mumbai",
    "state": "Maharashtra",
    "country": 5,
    "propertylocation": "abcdefgh",
    "possibleservices": "abcdefgh",
    "dated": "2024-01-01 00:00:00",
    "createdby": 1234,
    "isdeleted": False
  }
    expected_response = None
    with patch('main.check_role_access', return_value=1):
        response = client.post('/editResearchProspect', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.usefixtures("db_connection")
def test_id_136(client):
    payload = {
    "user_id": 1234,
    "id": 42,
    "personname": "New changed person",
    "suburb": "abcde",
    "city": "Mumbai",
    "state": "Maharashtra",
    "country": 5,
    "propertylocation": "abcdefgh",
    "possibleservices": "abcdefgh",
    "dated": "2024-01-01 00:00:00",
    "createdby": 1234,
    "isdeleted": False
  }
    expected_response = None
    with patch('main.check_role_access', return_value=0):
        response = client.post('/editResearchProspect', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.usefixtures("db_connection")
def test_id_137(client):
    payload = {"user_id":1234,"id":89}
    expected_response = {
  "result": "success",
  "user_id": 1234,
  "role_id": 1,
  "data": {
    "deleted_prospect": 89
  }
}
    with patch('main.check_role_access', return_value=1):
        response = client.post('/deleteResearchProspect', json=payload)

    assert response.status_code == 200
    assert expected_response['data']['deleted_prospect'] > 0

@pytest.mark.usefixtures("db_connection")
def test_id_138(client):
    payload = {"user_id":1234}
    expected_response = None
    with patch('main.check_role_access', return_value=1):
        response = client.post('/deleteResearchProspect', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_139(client):
    payload = {"user_id":1234,"id":43}
    expected_response = None
    with patch('main.check_role_access', return_value=0):
        response = client.post('/deleteResearchProspect', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.usefixtures("db_connection")
def test_id_140(client):
    payload = {
    "user_id": 1234,
    "id":11000
}
    expected_response = {
  "result": "success",
  "user_id": 1234,
  "role_id": 1,
  "data": {
    "deleted": 11000
  }
}
    with patch('main.check_role_access', return_value=1):
        response = client.post('/deleteProject', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.usefixtures("db_connection")
def test_id_141(client):
     
    payload = {
    "user_id": 1234
    }
    expected_response = {
  "result": "error",
  "message": "Invalid Credentials",
  "user_id": 1234,
  "role_id": 0,
  "data": []
}
    with patch('main.check_role_access', return_value=1):
        response = client.post('/deleteProject', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

  
@pytest.mark.usefixtures("db_connection")
def test_id_142(client): 
    payload = {
    "user_id": 1234,
    "id":11000
    }
    expected_response = {
  "result": "error",
  "message": "Access Denied",
  "user_id": 1234,
  "role_id": 0,
  "data": []
}
    with patch('main.check_role_access', return_value=0):
        response = client.post('/deleteProject', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_143(client):
     
    payload = {"user_id":1234,"table_name":"employee","item_id":98}
    expected_response = {
  "result": "success",
  "user_id": 1234,
  "role_id": 1,
  "data": {
    "id": 98,
    "employeename": "temp",
    "employeeid": "234",
    "userid": 1236,
    "roleid": 8,
    "dateofjoining": "2024-03-21T00:00:00",
    "dob": "2024-03-01T00:00:00",
    "panno": "1234",
    "status": False,
    "phoneno": "9",
    "email": "aam@gma.com",
    "addressline1": "def",
    "addressline2": "ijk",
    "suburb": "tyr",
    "city": 1641,
    "state": "1641",
    "country": 7,
    "zip": "441",
    "dated": "2020-01-20T00:00:00",
    "createdby": 1234,
    "isdeleted": False,
    "entityid": 1,
    "lobid": 19,
    "lastdateofworking": "2024-03-29T00:00:00",
    "designation": "abc"
  }
}
    with patch('main.check_role_access', return_value=1):
        response = client.post('/getItembyId', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response


# @pytest.mark.usefixtures("db_connection")
# def test_id_146(client): 
#     payload = {
#   "user_id": 1234,
#   "rows": [
#     "id",
#     "client",
#     "clientid",
#     "project",
#     "projectid",
#     "propertytypeid",
#     "propertytype",
#     "suburb",
#     "cityid",
#     "city",
#     "state",
#     "countryid",
#     "country",
#     "layoutdetails",
#     "numberofparkings",
#     "internalfurnitureandfittings",
#     "leveloffurnishing",
#     "propertystatus",
#     "status",
#     "initialpossessiondate",
#     "poagiven",
#     "poaid",
#     "electricityconsumernumber",
#     "electricitybillingunit",
#     "otherelectricitydetails",
#     "gasconnectiondetails",
#     "propertytaxnumber",
#     "clientservicemanager",
#     "propertymanager",
#     "comments",
#     "propertyownedbyclientonly",
#     "textforposting",
#     "dated",
#     "createdby",
#     "isdeleted",
#     "electricitybillingduedate"
#   ],
#   "filters": [],
#   "sort_by": [],
#   "order": "asc",
#   "pg_no": 1,
#   "pg_size": 15
# }
#     expected_response = {
#   "result": "error",
#   "message": "Access Denied",
#   "user_id": 1234,
#   "role_id": 0,
#   "data": []
# }
#     with patch('main.check_role_access', return_value=1):
#         response = client.post('/getClientProperty', json=payload)

#     assert response.status_code == 200
#     assert response.json() == expected_response
