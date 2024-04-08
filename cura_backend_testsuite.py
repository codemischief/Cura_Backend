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
            host="20.197.13.140"
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
def test_id_15(client, db_connection):
    payload={"user_id": 1234, "country_name": "country713"}


    expected_response={
        "result": "success",
        "user_id": 1234,
        "role_id": 1,
        "data": {
            "added": "country713"
        }
    }


    try:
        conn = db_connection

        with conn.cursor() as cur:
            # Insert data into the country table
            query = "INSERT INTO country (name) VALUES (%s)"
            cur.execute(query, (payload["country_name"],))
            conn.commit()

        with patch('main.check_role_access', return_value=1):
            response = client.post('/addCountry', json=payload)

        assert response.status_code == 200
        assert response.json() == expected_response

    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        conn.rollback()

@pytest.mark.usefixtures("db_connection")
def test_id_16(client, db_connection):
    payload = {"user_id": 1234, "country_name": "India"}
    with db_connection.cursor() as cursor:
        cursor.execute("SELECT id FROM country WHERE name = %s", (payload["country_name"],))
        existing_country = cursor.fetchone()

    if existing_country:
        expected_response = {
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
   
    db_connection.rollback()




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

    with db_connection.cursor() as cursor:
        insert_query = "INSERT INTO country (name) VALUES (%s)"
        cursor.execute(insert_query, (payload["old_country_name"],))
        db_connection.commit()

    with db_connection.cursor() as cursor:
        update_query = "UPDATE country SET name = %s WHERE name = %s"
        cursor.execute(update_query, (payload["new_country_name"], payload["old_country_name"]))
        db_connection.commit()

    try:
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

    finally:
        db_connection.rollback()



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
        assert response.status_code == 200
        assert response.json() == expected_response
        mock_info.assert_called_once_with(f'deleteCountry: received payload <{payload}>')
        with conn.cursor() as cur:
            cur.execute("SELECT name FROM country WHERE name = %s", (payload["country_name"],))
            result = cur.fetchone()
            assert result is None  

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
        mock_info.assert_called_once_with(f'addEmployee: received payload <{payload}>')

    except Exception as e:
        logging.error(f"An error occurred: {e}")

    finally:
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
  "message": "Already Exists",
  "user_id": 1234,
  "role_id": 1,
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
        "locality": "Test_locality_0"
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

    conn = db_connection

    try:
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

        with conn.cursor() as cur:
            query_update_locality = "UPDATE locality SET name = %s WHERE id = %s"
            cur.execute(query_update_locality, (payload["locality"], payload["id"]))
            conn.commit()

        with patch('main.check_role_access', return_value=1):
            response = client.post('/editLocality', json=payload)

        assert response.status_code == 200
        assert response.json() == expected_response

    except Exception as e:
        logging.error(f"An error occurred: {e}")
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
            insert_query = "INSERT INTO locality (id) VALUES (%s)"
            cur.execute(insert_query, (payload["id"],))
            conn.commit()

            # Check if the locality ID exists in the database
            query = "SELECT COUNT(*) FROM locality WHERE id = %s"
            cur.execute(query, (payload["id"],))
            count = cur.fetchone()[0]

            if count == 0:
                assert expected_response["data"]["Deleted Locality ID"] == payload["id"]
                return

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

    expected_response={
  "result": "error",
  "message": "Access Denied",
  "user_id": 1234,
  "role_id": 0,
  "data": []
}

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
            initial_query = "INSERT INTO lob (name) VALUES (%s)"
            cur.execute(initial_query, (payload["old_name"],))
            conn.commit()

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
def test_id_77(client, db_connection):
    payload = {"user_id":1234, "name": "new_lobname"}

    expected_response = {
        "result": "success",
        "user_id": 1234,
        "role_id": 1,
        "data": {
            "deleted_lob": "new_lobname"
        }
    }

    try:
        conn = db_connection

        with conn.cursor() as cur:
            initial_query = "INSERT INTO lob (name) VALUES (%s)"
            cur.execute(initial_query, (payload["name"],))
            conn.commit()

        with patch('main.check_role_access', return_value=1):
            response = client.post('/deleteLob', json=payload)

        assert response.status_code == 200
        assert response.json() == expected_response

    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        conn.rollback()

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
def test_id_80(client, db_connection):
    payload = {
        "user_id":1234,
        "receivedby":5,
        "paymentmode":11,
        "recddate":"31-Mar-2024",
        "entityid":1,
        "amount":111,
        "howreceivedid":1,
        "clientid": 7,
        "receiptdesc":"",
        "serviceamount":0,
        "reimbursementamount":0,
        "tds":0
    }

    expected_response = {
        "result": "success",
        "user_id": 1234,
        "role_id": 1,
        "data": {
            "entered": "client receipt for amount <111>"
        }
    }

    try:
        conn = db_connection

        with conn.cursor() as cur:
            initial_query = """
            INSERT INTO client_receipt 
            (receivedby, paymentmode, recddate, entityid, amount, howreceivedid, clientid, receiptdesc, serviceamount, reimbursementamount, tds) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cur.execute(initial_query, (
                payload["receivedby"], payload["paymentmode"], payload["recddate"], payload["entityid"],
                payload["amount"], payload["howreceivedid"], payload["clientid"], payload["receiptdesc"],
                payload["serviceamount"], payload["reimbursementamount"], payload["tds"]
            ))
            conn.commit()

        with patch('main.check_role_access', return_value=1):
            response = client.post('/addClientReceipt', json=payload)

        assert response.status_code == 200
        assert response.json() == expected_response

    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        conn.rollback()


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
def test_id_83(client, db_connection):
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

    try:
        conn = db_connection

        with conn.cursor() as cur:
            initial_query = """
            INSERT INTO builder_contacts 
            (builderid, contactname, email1, jobtitle, businessphone, homephone, mobilephone, 
            addressline1, addressline2, suburb, city, state, country, zip, notes, dated, createdby, isdeleted) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cur.execute(initial_query, (
                payload["builderid"], payload["contactname"], payload["email1"], payload["jobtitle"],
                payload["businessphone"], payload["homephone"], payload["mobilephone"],
                payload["addressline1"], payload["addressline2"], payload["suburb"], payload["city"],
                payload["state"], payload["country"], payload["zip"], payload["notes"], payload["dated"],
                payload["createdby"], payload["isdeleted"]
            ))
            conn.commit()

        with patch('main.check_role_access', return_value=1):
            response = client.post('/addNewBuilderContact', json=payload)

        assert response.status_code == 200
        assert response.json() == expected_response

    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        conn.rollback()

@pytest.mark.usefixtures("db_connection")
def test_id_84(client, db_connection):
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

    try:
        conn = db_connection

        with conn.cursor() as cur:
            initial_query = """
            INSERT INTO builder_contacts 
            (builderid, email1, jobtitle, businessphone, homephone, mobilephone, 
            addressline1, addressline2, suburb, city, state, country, zip, notes, dated, createdby, isdeleted) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cur.execute(initial_query, (
                payload["builderid"], payload["email1"], payload["jobtitle"],
                payload["businessphone"], payload["homephone"], payload["mobilephone"],
                payload["addressline1"], payload["addressline2"], payload["suburb"], payload["city"],
                payload["state"], payload["country"], payload["zip"], payload["notes"], payload["dated"],
                payload["createdby"], payload["isdeleted"]
            ))
            conn.commit()

        with patch('main.check_role_access', return_value=1):
            response = client.post('/addNewBuilderContact', json=payload)

        assert response.status_code == 200
        assert response.json() == expected_response

    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        conn.rollback()


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
def test_id_23(client, db_connection):
    payload = {
        "user_id": 1234,
        "buildername": "test_name100",
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
            "entered": "test_name100"
        },
        "total_count": {
            "entered": "test_name100"
        }
    }

    conn = db_connection
    try:
        with conn.cursor() as cursor:
            query = """
            INSERT INTO builder (buildername, phone1, phone2, email1, email2, addressline1, addressline2,
                                 suburb, city, state, country, zip, website, comments, dated, createdby, isdeleted)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                payload["buildername"], payload["phone1"], payload["phone2"],
                payload["email1"], payload.get("email2", ""), payload["addressline1"], payload["addressline2"],
                payload["suburb"], payload["city"], payload["state"], payload["country"], payload["zip"],
                payload["website"], payload["comments"], payload["dated"], payload["createdby"], payload["isdeleted"]
            ))
            conn.commit()

        with patch('main.check_role_access', return_value=1):
            response = client.post('/addBuilderInfo', json=payload)

        assert response.status_code == 200
        assert response.json() == expected_response

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise e

    finally:
        conn.rollback()
        conn.close()

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
def test_id_27(client, db_connection):
    payload = {
        "user_id": 1234,
        "builder_id": 10027,
        "buildername": "Rudra_kumar",
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
            "updated": {
                "user_id": 1234,
                "builder_id": 10027,
                "buildername": "Rudra_kumar",
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
        }
    }

    conn = db_connection
    try:
        # Insert data into the database
        with conn.cursor() as cursor:
            query = """
            INSERT INTO builder (buildername, phone1, phone2, email1, addressline1, addressline2,
                                 suburb, city, state, country, zip, website, comments, dated, createdby, isdeleted)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                payload["buildername"], payload["phone1"], payload["phone2"],
                payload["email1"], payload["addressline1"], payload["addressline2"], payload["suburb"],
                payload["city"], payload["state"], payload["country"], payload["zip"], payload["website"],
                payload["comments"], payload["dated"], payload["createdby"], payload["isdeleted"]
            ))
            conn.commit()

        # Update data in the database
        with patch('main.check_role_access', return_value=1):
            response = client.post('/editBuilder', json=payload)

        assert response.status_code == 200
        assert response.json() == expected_response

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise e
    finally:
        conn.rollback()


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
def test_id_86(client, db_connection):
    payload = {
        "user_id": 1234,
        "id": 11000,
        "builderid": 3000,
        "projectname": "aryan_project",
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

    try:
        conn = db_connection
        
        # Insert data into the database
        with conn.cursor() as cursor:
            query_insert_project = """
            INSERT INTO project (
                builderid, projectname, addressline1, addressline2, suburb, city, state, country,
                zip, nearestlandmark, project_type, mailgroup1, mailgroup2, website, project_legal_status,
                rules, completionyear, jurisdiction, taluka, corporationward, policechowkey, policestation,
                maintenance_details, numberoffloors, numberofbuildings, approxtotalunits, tenantstudentsallowed,
                tenantworkingbachelorsallowed, tenantforeignersallowed, otherdetails, duespayablemonth, dated,
                createdby, isdeleted
            ) VALUES (
                %(builderid)s, %(projectname)s, %(addressline1)s, %(addressline2)s, %(suburb)s, %(city)s,
                %(state)s, %(country)s, %(zip)s, %(nearestlandmark)s, %(project_type)s, %(mailgroup1)s, %(mailgroup2)s,
                %(website)s, %(project_legal_status)s, %(rules)s, %(completionyear)s, %(jurisdiction)s, %(taluka)s,
                %(corporationward)s, %(policechowkey)s, %(policestation)s, %(maintenance_details)s, %(numberoffloors)s,
                %(numberofbuildings)s, %(approxtotalunits)s, %(tenantstudentsallowed)s, %(tenantworkingbachelorsallowed)s,
                %(tenantforeignersallowed)s, %(otherdetails)s, %(duespayablemonth)s, %(dated)s, %(createdby)s, %(isdeleted)s
            )
            """
            cursor.execute(query_insert_project, payload)
            conn.commit()

        expected_response = {
            "result": "success",
            "user_id": 1234,
            "role_id": 1,
            "data": {
                "entered": "aryan_project",
                "project_id": 0
            }
        }

        with patch('main.check_role_access', return_value=1):
            response = client.post('/addProject', json=payload)

        assert response.status_code == 200
        assert response.json() == expected_response

    except Exception as e:
        print(f"An error occurred: {e}")
        raise e  

    finally:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM project WHERE id = %s", (payload["id"],))
            conn.commit()

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
def test_id_89(client, db_connection):
    payload = {
        "user_id": 1234,
        "id": 11000,
        "builderid": 3000,
        "projectname": "Aryan_Project",
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

    try:
        conn = db_connection
        
        with conn.cursor() as cursor:
            query_insert_project = """
            INSERT INTO project (
                builderid, projectname, addressline1, addressline2, suburb, city, state, country,
                zip, nearestlandmark, project_type, mailgroup1, mailgroup2, website, project_legal_status,
                rules, completionyear, jurisdiction, taluka, corporationward, policechowkey, policestation,
                maintenance_details, numberoffloors, numberofbuildings, approxtotalunits, tenantstudentsallowed,
                tenantworkingbachelorsallowed, tenantforeignersallowed, otherdetails, duespayablemonth, dated,
                createdby, isdeleted
            ) VALUES (
                %(builderid)s, %(projectname)s, %(addressline1)s, %(addressline2)s, %(suburb)s, %(city)s,
                %(state)s, %(country)s, %(zip)s, %(nearestlandmark)s, %(project_type)s, %(mailgroup1)s, %(mailgroup2)s,
                %(website)s, %(project_legal_status)s, %(rules)s, %(completionyear)s, %(jurisdiction)s, %(taluka)s,
                %(corporationward)s, %(policechowkey)s, %(policestation)s, %(maintenance_details)s, %(numberoffloors)s,
                %(numberofbuildings)s, %(approxtotalunits)s, %(tenantstudentsallowed)s, %(tenantworkingbachelorsallowed)s,
                %(tenantforeignersallowed)s, %(otherdetails)s, %(duespayablemonth)s, %(dated)s, %(createdby)s, %(isdeleted)s
            )
            """
            cursor.execute(query_insert_project, payload)
            conn.commit()
        
        payload["projectname"] = "Updated Sample Project"
        with conn.cursor() as cursor:
            query_update_project_name = "UPDATE project SET projectname = %s WHERE id = %s"
            cursor.execute(query_update_project_name, (payload["projectname"], payload["id"]))
            conn.commit()

        expected_response = {
            "result": "success",
            "user_id": 1234,
            "role_id": 1,
            "data": {
                "entered": "Updated Sample Project"
            }
        }

        with patch('main.check_role_access', return_value=1):
            response = client.post('/editProject', json=payload)

        assert response.status_code == 200
        assert response.json() == expected_response

    except Exception as e:
        print(f"An error occurred: {e}")
        raise e  

    finally:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM project WHERE id = %s", (payload["id"],))
            conn.commit()

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
def test_id_06(client, db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute("INSERT INTO country (name) VALUES ('country1')")
        cursor.execute("INSERT INTO country (name) VALUES ('country2')")
        db_connection.commit()

    expected_response = {
        "result": "success",
        "user_id": 1234,
        "role_id": 1,
        "data": {
            "colnames": ["id", "name"],
            "data": [
                [1, "country1"],
                [2, "country2"]
            ],
            "total_count": 2,
            "message": "success"
        },
        "total_count": 2
    }
    with patch('main.filterAndPaginate') as mock_filter:
        mock_filter.return_value = expected_response["data"]
        
        with patch('main.check_role_access', return_value=1):
            response = client.post('/getCountries', json={
                "user_id": 1234,
                "rows": ["id", "name"],
                "filters": [],
                "sort_by": None,
                "order": None,
                "pg_no": 1,
                "pg_size": 15,
                "search_key": None
            })

        assert response.status_code == 200
        assert response.json() == expected_response
    
    db_connection.rollback()

@pytest.mark.usefixtures("db_connection")
def test_id_07(client):
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
def test_id_08(client):
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
def test_id_09(client, db_connection):
    try:
        with db_connection.cursor() as cursor:
            dummy_data = [
                (1, "Netherlands", 9),
            ]
            for data in dummy_data:
                cursor.execute("INSERT INTO cities (id, state, countryid) VALUES (%s, %s, %s)", data)
            db_connection.commit()

        expected_response = {
            "result": "success",
            "user_id": 1234,
            "role_id": 1,
            "data": [
                ["Netherlands"]
            ]
        }
        with patch('main.check_role_access', return_value=1):
            response = client.post('/getStates', json={"user_id": 1234, "country_id": 9})

        assert response.status_code == 200
        assert response.json() == expected_response
    
    finally:
        with db_connection.cursor() as cursor:
            cursor.execute("DELETE FROM cities WHERE id = 1") 
        db_connection.commit()


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
def test_id_30(client, db_connection):
    try:
        with db_connection.cursor() as cursor:
            try:  # Wrap insertions in a try-except block
                cursor.execute("INSERT INTO country (id, name) VALUES (%s, %s)", (5, "India"))
                cursor.execute("INSERT INTO get_cities_view (id, city, state, countryid) VALUES (%s, %s, %s, %s)", (1620, "Kolkata", "West Bengal", 5))
            except Exception as e:  # Catch any exceptions during insertion
                print(f"Error during insertion: {e}")
                db_connection.rollback()  # Explicitly rollback on error
                raise  # Re-raise the exception to fail the test

        expected_response = {
            "result": "success",
            "user_id": 1234,
            "role_id": 1,
            "data": [
                {
                    "id": 1620,
                    "city": "Kolkata"
                }
            ]
        }

        with patch('main.check_role_access', return_value=('India', 1)):
            response = client.post('/getCities', json={"user_id": 1234,
                                                     "state_name": "West Bengal",
                                                     "country_name": "India"})

        assert response.status_code == 200
        assert response.json() == expected_response

    finally:
        with db_connection.cursor() as cursor:
            cursor.execute("DELETE FROM get_cities_view WHERE id = 1620")  # Cleanup
            cursor.execute("DELETE FROM country WHERE id = 5")   # Cleanup
        db_connection.commit()

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
def test_id_43(client, db_connection):
    # Sample data setup (if not already existing in your test database)
    with db_connection.cursor() as cursor:
        cursor.execute("INSERT INTO country (id, name) VALUES (1, 'test_country1'), (2, 'test_country2')")
        cursor.execute("INSERT INTO cities (id, city, state, countryid) VALUES (1, 'test_city1', '', 1), (2, 'test_city2', '', 1), (3, 'test_city3', '', 2), (4, 'test_city4', '', 2)")
        db_connection.commit()

    # Expected response with joined country data
    expected_response = {
        "result": "success",
        "user_id": 1234,
        "role_id": 1,
        "data": [
            {"id": 1, "city": "test_city1", "state": "", "countryid": 1, "countryname": "test_country1"},
            {"id": 2, "city": "test_city2", "state": "", "countryid": 1, "countryname": "test_country1"},
            {"id": 3, "city": "test_city3", "state": "", "countryid": 2, "countryname": "test_country2"},
            {"id": 4, "city": "test_city4", "state": "", "countryid": 2, "countryname": "test_country2"},
        ],
        "total_count": 4
    }

    # Patch dependencies
    with mock.patch('main.filterAndPaginate') as mock_filter:
        mock_filter.return_value = {"data": expected_response["data"], "total_count": expected_response["total_count"]}

        with mock.patch('main.check_role_access', return_value=1):
            response = client.post('/getCitiesAdmin', json={"user_id": 1234, "rows": ["id", "city", "state", "countryid", "countryname"], "filters": [], "sort_by": [], "order": "asc","pg_no": 1, "pg_size": 15})

            assert response.status_code == 200
            assert response.json() == expected_response
    
    db_connection.rollback()


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
def test_id_33(client, db_connection):
    with db_connection.cursor() as cursor:
        dummy_data = [
            (1, "test_country1"),
            (2, "test_country2"),
        ]
        for data in dummy_data:
            cursor.execute("INSERT INTO country (id, name) VALUES (%s, %s)", data)
        db_connection.commit()

        dummy_data = [
            (1, "test_state1", 1),
            (2, "test_state2", 1),
            (3, "test_state3", 2),
            (4, "test_state4", 2),
        ]
        for data in dummy_data:
            cursor.execute("INSERT INTO cities (id, state, countryid) VALUES (%s, %s, %s)", data)
        db_connection.commit()

    expected_response = {
        "result": "success",
        "user_id": 1234,
        "role_id": 1,
        "data": [
            {"countryname": "test_country1", "state": "test_state1", "id": 1},
            {"countryname": "test_country1", "state": "test_state2", "id": 1},
            {"countryname": "test_country2", "state": "test_state3", "id": 2},
            {"countryname": "test_country2", "state": "test_state4", "id": 2},
        ],
        "total_count": 4
    }

    with patch('main.filterAndPaginate') as mock_filter:
        mock_filter.return_value = {"data": expected_response["data"], "total_count": expected_response["total_count"]}
        
        with patch('main.check_role_access', return_value=1):
            response = client.post('/getStatesAdmin', json={"user_id": 1234, "rows": "*", "filters": [], "sort_by": [], "order": "asc", "pg_no": 1, "pg_size": 10})

        assert response.status_code == 200
        assert response.json() == expected_response
    
    db_connection.rollback()

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
        response = client.post('/getStatesAdmin', json=payload)

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
        response = client.post('/getStatesAdmin', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response



@pytest.mark.usefixtures("db_connection")
def test_id_40(client, db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO builder (
                buildername, phone1, phone2, email1, email2, addressline1, addressline2,
                suburb, city, state, country, zip, website, comments, dated, createdby, isdeleted
            ) VALUES (
                'Sample Builder 1', '1234567890', '0987654321', 'email1@example.com', 'email2@example.com', '123 Main St', 'Apt 101', 'Suburbia', 1, 'Some State', 1, '12345', 'www.samplebuilder1.com', 'Sample comments for builder 1', '2024-04-03 12:00:00', 1, false
            ), (
                'Sample Builder 2', '9876543210', '0123456789', 'email3@example.com', 'email4@example.com', '456 Elm St', 'Suite 200', 'Cityville', 2, 'Another State', 1, '54321', 'www.samplebuilder2.com', 'Sample comments for builder 2', '2024-04-03 13:00:00', 2, false
            ), (
                'Sample Builder 3', '5554443333', '', 'email5@example.com', '', '789 Oak St', '', 'Townville', 3, 'Yet Another State', 1, '67890', '', 'Sample comments for builder 3', '2024-04-03 14:00:00', 3, false
            );
        """)
        db_connection.commit()
    

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
                }
                # Add more builder_info entries as needed
            ]
        },
        "total_count": 218
    }

    with patch('main.filterAndPaginate') as mock_filter:
        mock_filter.return_value = expected_response["data"]
        
        with patch('main.check_role_access', return_value=1):
            response = client.post('/getBuilderInfo', json={
                "user_id": 1234,
                "rows": ["id", "buildername", "phone1", "phone2", "email1", "email2", "addressline1", "addressline2", "suburb", "city", "state", "country", "zip", "website", "comments", "dated", "createdby", "isdeleted"],
                "filters": [],
                "sort_by": [],
                "order": "asc",
                "pg_no": 1,
                "pg_size": 15
            })

            assert response.status_code == 200
            assert response.json() == expected_response


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
def test_id_113(client, db_connection):
    payload = {
        "user_id": 1234,
        "modeofpayment": 20,
        "date": "2024-03-20 00:00:00",
        "amount": 112,
        "particulars": "put any description or notes here",
        "crdr": "CR",
        "vendorid": 411,
        "createdby": 1234
    }

    try:
        conn = db_connection

        with conn.cursor() as cursor:
            query_insert_bank_st = "INSERT INTO bankst (modeofpayment, date, amount, particulars, crdr, vendorid, createdby) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query_insert_bank_st, (payload["modeofpayment"], payload["date"], payload["amount"], payload["particulars"], payload["crdr"], payload["vendorid"], payload["createdby"]))
            conn.commit()

        expected_response = {
            "result": "success",
            "user_id": 1234,
            "role_id": 1,
            "data": {
                "added_data": f"added bank statement for amount <{payload['amount']}>"
            }
        }

        with patch('main.check_role_access', return_value=1):
            response = client.post('/addBankSt', json=payload)

        assert response.status_code == 200
        assert response.json() == expected_response

    except Exception as e:
        print(f"An error occurred: {e}")
        raise e  

    finally:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM bankst WHERE date = %s AND amount = %s", (payload["date"], payload["amount"]))
            conn.commit()


@pytest.mark.usefixtures("db_connection")
def test_id_114(client):
    payload = { "user_id": 1234, "modeofpayment": 20, "date":"20-03-2024 00:00:00", "amount":112 , "particulars":"put any description or notes here", "crdr":"CR", "vendorid":411, "createdby":1234 }
    expected_response = {
  "result": "error",
  "message": "Access Denied",
  "user_id": 1234,
  "role_id": 0,
  "data": []
} 

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
def test_id_116(client, db_connection):
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

    try:
        conn = db_connection

        with conn.cursor() as cursor:
            query_insert_bank_st = """
                INSERT INTO bankst (id, modeofpayment, date, amount, particulars, crdr, receivedby, vendorid, createdby)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query_insert_bank_st, (
                payload["id"], payload["modeofpayment"], payload["date"], payload["amount"],
                payload["particulars"], payload["crdr"], payload["receivedby"], payload["vendorid"],
                payload["createdby"]
            ))
            conn.commit()

        with conn.cursor() as cursor:
            query_update_bank_st = """
                UPDATE bankst 
                SET id = %s
                WHERE id = %s
            """
            cursor.execute(query_update_bank_st, (payload["id"] + 1, payload["id"]))
            conn.commit()

        expected_response = {
            "result": "success",
            "user_id": 1234,
            "role_id": 1,
            "data": {
                "edited_data": payload["id"]
            }
        }

        with patch('main.check_role_access', return_value=1):
            response = client.post('/editBankSt', json=payload)

        assert response.status_code == 200
        assert response.json() == expected_response

    except Exception as e:
        print(f"An error occurred: {e}")
        raise e  

    finally:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM bankst WHERE id = %s", (payload["id"] + 1,))
            cursor.execute("DELETE FROM bankst WHERE id = %s", (payload["id"],))
            conn.commit()

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
def test_id_119(client, db_connection):
    payload = {"user_id": 1234, "id": 100028}  

    try:
        conn = db_connection

        with conn.cursor() as cursor:
            query_insert_bank_st = """
                INSERT INTO bankst (id, modeofpayment, date, amount, particulars, crdr, receivedby, vendorid, createdby)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query_insert_bank_st, (
                payload["id"], 20, "2024-03-23 00:00:00", 9384.00,
                "abcd", "CR", 5, 14000,
                1234
            ))  

            expected_response = {
            "result": "success",
            "user_id": 1234,
            "role_id": 1,
            "data": {
                "deleted_data": payload["id"]
            }
        }

        with patch('main.check_role_access', return_value=1):
            response = client.post('/deleteBankSt', json=payload)

        assert response.status_code == 200
        assert response.json() == expected_response


    except Exception as e:
        print(f"An error occurred: {e}")
        raise e 

    finally:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM bankst WHERE id = %s", (payload["id"] + 1,))
            cursor.execute("DELETE FROM bankst WHERE id = %s", (payload["id"],))
            conn.commit()

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
def test_id_122(client, db_connection):
    # Define the dummy data to insert into the bankst table
    dummy_data = [
        (20052, 5, 15318, "CR                  ", None),
        # Add more dummy data as needed
    ]

    # Insert the dummy data into the bankst table
    with db_connection.cursor() as cursor:
        for data in dummy_data:
            cursor.execute("INSERT INTO bankst (id, modeofpayment, amount, crdr, chequeno) VALUES (%s, %s, %s, %s, %s)", data)
        db_connection.commit()

    # Define the payload
    payload = {
        "user_id": 1234,
        "rows": ["id", "modeofpayment", "amount", "crdr", "chequeno"],
        "filters": [],
        "sort_by": [],
        "order": "asc",
        "pg_no": 0,
        "pg_size": 0
    }

    # Define the expected response
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
            }
        ],
        "total_count": 14818
    }

    # Mocking the filterAndPagination function to return a predefined response
    with patch('main.filterAndPaginate') as mock_filter:
        mock_filter.return_value = {
            "data": expected_response["data"],
            "total_count": expected_response["total_count"]
        }

        # Patching check_role_access function to return a role access status of 1
        with patch('main.check_role_access', return_value=1):
            # Send a request to the route
            response = client.post('/getBankSt', json=payload)

            # Assert the response status code
            assert response.status_code == 200

            # Convert the response to JSON
            response_data = response.json()

            # Assert the response data matches the expected response
            assert response_data == expected_response

            # Ensure that the response has a total_count key
            assert 'total_count' in response_data

            # Ensure that the total_count is greater than 0
            assert response_data['total_count'] > 0

            # Ensure that the data returned matches the expected data
            assert response_data['data'] == expected_response['data']

    # Delete the inserted dummy data from the bankst table
    with db_connection.cursor() as cursor:
        for data in dummy_data:
            cursor.execute("DELETE FROM bankst WHERE id = %s", (data[0],))
        db_connection.commit()
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
def test_id_140(client, db_connection):
    payload = {
        "user_id": 1234,
        "id": 11000
    }

    try:
        conn = db_connection

        with conn.cursor() as cursor:
            query_insert_project = "INSERT INTO project (id) VALUES (%s)"
            cursor.execute(query_insert_project, (payload["id"],))
            conn.commit()

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

    except Exception as e:
        print(f"An error occurred: {e}")
        raise e  

    finally:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM project WHERE id = %s", (payload["id"],))
            conn.commit()

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

@pytest.mark.usefixtures("db_connection")
def test_id_146(client, db_connection):
    expected_data = [
        {"id": 10, "name": "Agent-Broker"},
        {"id": 11, "name": "Builder-Developer"},
        {"id": 9, "name": "Buyer"},
        {"id": 6, "name": "Expat service provider"},
        {"id": 8, "name": "Office"},
        {"id": 1, "name": "Owner - Corporate"},
        {"id": 2, "name": "Owner - Individual"},
        {"id": 7, "name": "PMA - Owner"},
        {"id": 4, "name": "Tenant - Corporate"},
        {"id": 3, "name": "Tenant - Individual"},
        {"id": 5, "name": "Tenant - Service Apartment Group"}
    ]

    try:
        with db_connection.cursor() as cursor:
            for data in expected_data:
                 cursor.execute("INSERT INTO client_type (id, name) VALUES (%s, %s)", (data["id"], data["name"]))
            db_connection.commit()

        payload = {"user_id": 1234}

        expected_response = {
            "result": "success",
            "user_id": 1234,
            "role_id": 1,
            "data": expected_data
        }

        with patch('main.check_role_access', return_value=1):
            response = client.post('/getClientTypeAdmin', json=payload)

        assert response.status_code == 200
        response_data = response.json()
        assert response_data == expected_response  

    finally:
        with db_connection.cursor() as cursor:
            cursor.execute("DELETE FROM client_type")  
            db_connection.commit()


@pytest.mark.usefixtures("db_connection")
def test_id_147(client):
    payload = {"user_id":1235}

    expected_response={
  "result": "error",
  "message": "Access Denied",
  "user_id": 1235,
  "role_id": 2,
  "data": []
}


    with patch('main.check_role_access', return_value=2):
       response=client.post('/getClientTypeAdmin',json=payload)
    
    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.usefixtures("db_connection")
def test_id_148(client):
    payload = {"user_id":1234}

    expected_response={
  "result": "error",
  "message": "Access Denied",
  "user_id": 1234,
  "role_id": 0,
  "data": []
}


    with patch('main.check_role_access', return_value=0):
       response=client.post('/getClientTypeAdmin',json=payload)
    
    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.usefixtures("db_connection")
def test_id_149(client, db_connection):
    expected_data = [
        {"id": 2, "name": "Daughter of"},
        {"id": 1, "name": "Son of"},
        {"id": 3, "name": "Wife of"}
    ]

    try:
        with db_connection.cursor() as cursor:
            for data in expected_data:
                 cursor.execute("INSERT INTO relation (id, name) VALUES (%s, %s)", (data["id"], data["name"]))
            db_connection.commit()

        payload = {"user_id": 1234}

        expected_response = {
            "result": "success",
            "user_id": 1234,
            "role_id": 1,
            "data": expected_data
        }

        with patch('main.check_role_access', return_value=1):
            response = client.post('/getRelationAdmin', json=payload)

        assert response.status_code == 200
        response_data = response.json()
        assert response_data == expected_response  

    finally:
        with db_connection.cursor() as cursor:
            cursor.execute("DELETE FROM relation")  
            db_connection.commit()


@pytest.mark.usefixtures("db_connection")
def test_id_150(client):
    payload = {"user_id":1235}

    expected_response={
  "result": "error",
  "message": "Access Denied",
  "user_id": 1235,
  "role_id": 2,
  "data": []
}


    with patch('main.check_role_access', return_value=2):
       response=client.post('/getRelationAdmin',json=payload)
    
    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.usefixtures("db_connection")
def test_id_151(client):
    payload = {"user_id":1234}

    expected_response={
  "result": "error",
  "message": "Access Denied",
  "user_id": 1234,
  "role_id": 0,
  "data": []
}


    with patch('main.check_role_access', return_value=0):
       response=client.post('/getRelationAdmin',json=payload)
    
    assert response.status_code == 200
    assert response.json() == expected_response


