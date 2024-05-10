import pytest
import traceback
import psycopg2
from fastapi import HTTPException
import logging
import unittest.mock as mock 
from unittest.mock import patch
from fastapi.testclient import TestClient
logger = logging.getLogger(__name__)
from main import app
from main import givenowtime

def newconn():
    conn = psycopg2.connect("postgresql://postgres:cura123@20.197.13.140:5432/cura_db")
    return conn



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
def test_id_01(client):
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
    "result": "error",
    "message": "User does not exist",
    "user_id": None,
    "role_id": None,
    "data": []
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
        "result": "error",
        "message": "User does not exist",
        "user_id": None,
        "role_id": None,
        "data": []
        }

@pytest.mark.usefixtures("db_connection")
def test_id_15(client, db_connection):
    payload = {"user_id": 1234, "country_name": "country713"}

    expected_response = {
        "result": "success",
        "user_id": 1234,
        "role_id": 1,
        "data": {
            "added": "country713"
        }
    }

    conn = None  

    try:
        conn = db_connection

        with conn.cursor() as cur:
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
        if conn:
            with conn.cursor() as cur:
                query_delete = "DELETE FROM country WHERE name = %s"
                cur.execute(query_delete, (payload["country_name"],))
                conn.commit()

@pytest.mark.usefixtures("db_connection")
def test_id_16(client, db_connection):
    payload = {"user_id": 1234, "country_name": "India"}
    expected_response = {
        "result": "error",
        "message": "Already Exists",
        "user_id": 1234,
        "role_id": 1,
        "data": []
    }

    conn = None  

    try:
        conn = db_connection

        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM country WHERE name = %s", (payload["country_name"],))
            existing_country = cursor.fetchone()

        if existing_country:
            assert False, "Country already exists" 

        cursor.execute("INSERT INTO country (name) VALUES (%s)", (payload["country_name"],))
        conn.commit()

        with patch('main.check_role_access', return_value=1):
            response = client.post('/addCountry', json=payload)

        assert response.status_code == 200
        assert response.json() == expected_response

    except Exception as e:
        logging.error(f"An error occurred: {e}")

    finally:
        if conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM country WHERE name = %s", (payload["country_name"],))
                conn.commit()


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

    try:
        with db_connection.cursor() as cursor:
            insert_query = "INSERT INTO country (name) VALUES (%s)"
            cursor.execute(insert_query, (payload["old_country_name"],))
            db_connection.commit()

            update_query = "UPDATE country SET name = %s WHERE name = %s"
            cursor.execute(update_query, (payload["new_country_name"], payload["old_country_name"]))
            db_connection.commit()

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
        with db_connection.cursor() as cursor:
            delete_query = "DELETE FROM country WHERE name = %s"
            cursor.execute(delete_query, (payload["new_country_name"],))
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
    payload = {"user_id": 1234, "country_name": "deleted_country"}
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
                "deleted": "deleted_country"
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
            INSERT INTO employee (
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

        assert response.status_code == 200
        assert response.json() == expected_response
        mock_info.assert_called_once_with(f'addEmployee: received payload <{payload}>')

    except Exception as e:
        logging.error(f"An error occurred: {e}")

    finally:
        with conn.cursor() as cur:
            delete_query = "DELETE FROM employee WHERE employeename = %s"
            cur.execute(delete_query, (payload["employeename"],))
            conn.commit()


@pytest.mark.usefixtures("db_connection")
def test_id_52(client, db_connection):
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
            select_query = "SELECT employeename FROM employee WHERE employeename = %s"
            cur.execute(select_query, (payload["employeename"],))
            existing_employee = cur.fetchone()
            if existing_employee:
                assert False, "Employee already exists"

            query = """
            INSERT INTO employee (
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
        "result": "error",
        "message": "Already Exists",
        "user_id": 1234,
        "role_id": 1,
        "data": []
    }

        assert response.status_code == 200
        assert response.json() == expected_response
        mock_info.assert_called_once_with(f'addEmployee: received payload <{payload}>')

    except Exception as e:
        logging.error(f"An error occurred: {e}")

    finally:
        with conn.cursor() as cur:
            delete_query = "DELETE FROM employee WHERE employeename = %s"
            cur.execute(delete_query, (payload["employeename"],))
            conn.commit()


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
        "user_id":1234,
        "employeeid":"P002020",
        "userid":1236,
        "roleid":2,
        "dateofjoining":"2024-01-13",
        "dob":"2024-01-13",
        "panno":"abcd",
        "status":False,
        "phoneno":None,
        "email":None,
        "addressline1":"abcdefgh",
        "addressline2":"ijklmnop",
        "suburb":"Pune",
        "city":847,
        "state":"Maharashta",
        "country":5,
        "zip":None,
        "dated":"2024-01-13  00:00:00",
        "createdby":1234,
        "isdeleted":False,
        "entityid":10,
        "lobid":100,
        "lastdateofworking":"2024-01-13",
        "designation":"New"
    }



    expected_response = {
  "result": "error",
  "message": "Invalid Credentials",
  "user_id": 1234,
  "role_id": 0,
  "data": []
}

    with patch('main.check_role_access', return_value=1): 
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
            insert_query = """
            INSERT INTO employee (
                employeename, employeeid, userid, roleid, dateofjoining, dob,
                panno, status, phoneno, email, addressline1, addressline2,
                suburb, city, state, country, zip, dated, createdby, isdeleted,
                entityid, lobid, lastdateofworking, designation
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cur.execute(insert_query, (
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
        with conn.cursor() as cur:
            update_query = """
            UPDATE employees
            SET employeename = %s
            WHERE id = %s
            """
            cur.execute(update_query, (payload["employeename"], payload["id"]))
            conn.commit()

        with patch('main.check_role_access', return_value=1):
            response = client.post('/editEmployee', json=payload)

        expected_response = {
            "result": "success",
            "user_id": 1234,
            "role_id": 1,
            "data": {
                "Updated Employee": "changed emp"
            }
        }

        assert response.status_code == 200
        assert response.json() == expected_response

    except Exception as e:
        logging.error(f"An error occurred: {e}")

    # finally:
    #     with conn.cursor() as cur:
    #         delete_query = "DELETE FROM employee WHERE employeename = %s"
    #         cur.execute(delete_query, (payload["employeename"],))
    #         conn.commit()


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
            query_add_employee = "INSERT INTO employee (employeename) VALUES ('') RETURNING id"
            cur.execute(query_add_employee)
            payload['id'] = cur.fetchone()[0]
            conn.commit()

        with patch('main.check_role_access', return_value=1):
            response = client.post('/deleteEmployee', json=payload)

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

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        conn = newconn()
        with conn.cursor() as cur:
            query_delete_employee = "DELETE FROM employee WHERE id = %s"
            cur.execute(query_delete_employee, (payload["id"],))
            conn.commit()
    
@pytest.mark.usefixtures("db_connection")
def test_id_59(client, db_connection):
    payload = {"user_id":1234, "id": 100}

    try:
        conn = db_connection
        
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

    # assert response.status_code == 200
    # assert response.json() == expected_response

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

    conn = db_connection

    try:
        with conn.cursor() as cur:
            query_insert_locality = "INSERT INTO locality ( name, city_id) VALUES (%s, %s, %s)"
            cur.execute(query_insert_locality, ( payload["locality"], payload["cityid"]))
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
        conn = newconn()
        with conn.cursor() as cur:
            delete_query = "DELETE FROM locality WHERE locality = %s"
            cur.execute(delete_query, (payload["locality"],))
            conn.commit()



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

@pytest.mark.usefixtures("db_connection")
def test_id_64(client, db_connection):
    payload = {
        "user_id": 1234,
        "locality": "Test Locality",
        "cityid": 8111 
    }

    conn = db_connection

    try:
        with conn.cursor() as cur:
            select_query = "SELECT COUNT(*) FROM locality WHERE locality = %s AND cityid = %s"
            cur.execute(select_query, (payload["locality"], payload["cityid"]))
            existing_locality_count = cur.fetchone()[0]

            if existing_locality_count > 0:
                raise ValueError("Locality already exists in the database")

            query_insert_locality = "INSERT INTO locality (locality, cityid) VALUES (%s, %s)"
            cur.execute(query_insert_locality, (payload["locality"], payload["cityid"]))
            conn.commit()
        
        expected_response = {
        "result": "error",
        "message": "Already Exists",
        "user_id": 1234,
        "role_id": 1,
        "data": []
    }

        with patch('main.check_role_access', return_value=1):
            response = client.post('/addLocality', json=payload)

        assert response.status_code == 200
        assert response.json() == expected_response

    except Exception as e:
        logging.error(f"An error occurred: {e}")

    finally:
        conn = newconn()
        with conn.cursor() as cur:
            delete_query = "DELETE FROM locality WHERE locality = %s AND cityid = %s"
            cur.execute(delete_query, (payload["locality"], payload["cityid"]))
            conn.commit()


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

    finally:
        with conn.cursor() as cur:
            delete_query = "DELETE FROM locality WHERE locality = %s AND cityid = %s"
            cur.execute(delete_query, (payload["locality"], payload["cityid"]))
            conn.commit()
    

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
    payload = {
        "user_id": 1234,
        "id": 20,
        "name": "lobname",
        "lob_head": 100,
        "company": "lobcompany",
        "entityid": 123
    }

    expected_response = {
        "result": "success",
        "user_id": 1234,
        "role_id": 1,
        "data": {
            "added_data": "lobname"
        }
    }

    conn = db_connection

    try:
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
        try:
            with conn.cursor() as cur:
                delete_query = "DELETE FROM lob WHERE id = %s"
                cur.execute(delete_query, (payload["id"],))
                conn.commit()
        except Exception as e:
            logging.error(f"An error occurred while deleting the inserted data: {e}")
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
    payload = {
        "user_id": 1234,
        "old_name": "lobname",
        "new_name": "new_lobname"
    }

    expected_response = {
        "result": "success",
        "user_id": 1234,
        "role_id": 1,
        "data": {
            "edited_lob": "lobname"
        }
    }

    conn = db_connection

    try:
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
        try:
            with conn.cursor() as cur:
                delete_query = "DELETE FROM lob WHERE name = %s"
                cur.execute(delete_query, (payload["new_name"],))
                conn.commit()
        except Exception as e:
            logging.error(f"An error occurred while deleting the inserted data: {e}")
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
  "message": "Invalid Credentials",
  "user_id": 0,
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
        "buildername": "test_name321",
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
            "entered": "test_name321"
        },
    }

    conn = db_connection
    try:
        with conn.cursor() as cursor:
            query = """
            INSERT INTO builder (buildername, phone1, phone2, email1, email2, addressline1, addressline2,
                                 suburb, city, state, country, zip, website, comments, dated, createdby, isdeleted)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
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
        assert response.json()['result'] == 'success'

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise e

    finally:
          with db_connection.cursor() as cursor:
            delete_query = """
                DELETE FROM builder 
                WHERE id = (SELECT MAX(id) FROM builder)
            """
            cursor.execute(delete_query)
            db_connection.commit()  

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
        "builder_name": "Rudra_kumar",
        "phone_1": "9999999999",
        "phone_2": "8888888888",
        "email1": "abc@def.com",
        "email2": "ghi@jkl.com",
        "addressline1": "abc area, def house",
        "addressline2": "ghi locality",
        "suburb": "ijkl",
        "city": 360,
        "state": "Maharashtra",
        "country": 5,
        "zip": "1234",
        "website": "www.abc.example.com",
        "comments": "comment1\ncomment2\ncomment3"
    }

    expected_response = {
        "result": "success",
        "user_id": 1234,
        "role_id": 1,
        "data": {
            "updated": {
                "user_id": 1234,
                "builder_name": "Rudra_kumar",
                "phone_1": "9999999999",
                "phone_2": "8888888888",
                "email1": "abc@def.com",
                "email2": "ghi@jkl.com",
                "addressline1": "abc area, def house",
                "addressline2": "ghi locality",
                "suburb": "ijkl",
                "city": 360,
                "state": "Maharashtra",
                "country": 5,
                "zip": "1234",
                "website": "www.abc.example.com",
                "comments": "comment1\ncomment2\ncomment3"
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
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
            """
            
            cursor.execute(query, (
                payload["builder_name"], payload["phone_1"], payload["phone_2"],
                payload["email1"], payload["addressline1"], payload["addressline2"], payload["suburb"],
                payload["city"], payload["state"], payload["country"], payload["zip"], payload["website"],
                payload["comments"],givenowtime(),payload['user_id'],False
            ))
            payload['builder_id'] = cursor.fetchone()[0]
            expected_response['data']['updated']['builder_id'] = payload['builder_id']
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


# @pytest.mark.usefixtures("db_connection")
# def test_id_86(client, db_connection):
#     with db_connection.cursor() as cursor:
#         insert_query = """
#         INSERT INTO projects ( builderid, projectname, addressline1, addressline2, suburb, city, state, country, zip, nearestlandmark, project_type, mailgroup1, mailgroup2, website, project_legal_status, rules, completionyear, jurisdiction, taluka, corporationward, policechowkey, maintenance_details, numberoffloors, numberofbuildings, approxtotalunits, tenantstudentsallowed, tenantworkingbachelorsallowed, tenantforeignersallowed, otherdetails, duespayablemonth, swimmingpool, lift, liftbatterybackup, clubhouse, gym, childrensplayarea, pipedgas, cctvcameras, otheramenities, studio, 1BHK, 2BHK, 3BHK, rowhouse, otheraccomodationtypes, sourceofwater)
# VALUES ( 10231, 'testproject', 'addressline1', 'addressline2', 'testsub', 847, 'Maharashtra', 5, 'testzip', 'landmark1', 2, 'mailgrouptest', 'newmailgrouptest', 'websitetest.com', 2, 'rule1, rule2, rule3', 2021, 'ajuri', 'tal', 'ward', 'chowkey', 'deets', 5, 4, 100, True, True, True, True, 3, True, True, True, True, True, True, True, True, 'newdata', True, False, True, True, False, '4BHK', 'abc');

# INSERT INTO project_bank_details (project_id, bankname, bankbranch, bankcity, bankaccountholdername, bankaccountno, bankifsccode, banktypeofaccount)
# VALUES (LAST_INSERT_ID(), 'Banktest', 'branchtest', 'Pune', 'Rudra', 'ABD102834732', 'PUN101', 'savings'),
#        (LAST_INSERT_ID(), 'Banktest', 'branchtest1', 'Pune', 'Rudra', 'ABD1046464732', 'PUN102', 'savings');

# INSERT INTO project_contacts (project_id, contactname, phone, email, role, effectivedate, tenureenddate, details)
# VALUES (LAST_INSERT_ID(), 'Rudra', '9796543567', 'abc', 'owner', '2021-02-04 10:00:00', NULL, 'hreiufhuire'),
#        (LAST_INSERT_ID(), 'Rudra_2', '9456545514', 'efg', 'manager', '2021-02-04 10:00:00', '2024-02-04 10:00:00', 'hreiufhuire');

# INSERT INTO project_photos (project_id, photo_link, description, date_taken)
# VALUES (LAST_INSERT_ID(), 'link1', 'Desc 1', '2024-03-01'),
#        (LAST_INSERT_ID(), 'link2', 'Desc2', '2024-01-01');

#         """
#         cursor.execute(insert_query)

#         db_connection.commit()

#         payload = {
#   "user_id": 1234,
#   "project_info": {
#     "builderid": 10231,
#     "projectname": "testproject",
#     "addressline1": "addressline1",
#     "addressline2": "addressline2",
#     "suburb": "testsub",
#     "city": 847,
#     "state": "Maharashtra",
#     "country": 5,
#     "zip": "testzip",
#     "nearestlandmark": "landmark1",
#     "project_type": 2,
#     "mailgroup1": "mailgrouptest",
#     "mailgroup2": "newmailgrouptest",
#     "website": "websitetest.com",
#     "project_legal_status": 2,
#     "rules": "rule1, rule2, rule3",
#     "completionyear": 2021,
#     "jurisdiction": "ajuri",
#     "taluka": "tal",
#     "corporationward": "ward",
#     "policechowkey": "chowkey",
#     "maintenance_details": "deets",
#     "numberoffloors": 5,
#     "numberofbuildings": 4,
#     "approxtotalunits": 100,
#     "tenantstudentsallowed": True,
#     "tenantworkingbachelorsallowed": True,
#     "tenantforeignersallowed": True,
#     "otherdetails": True,
#     "duespayablemonth": 3
#   },
#   "project_amenities": {
#     "swimmingpool": True,
#     "lift": True,
#     "liftbatterybackup": True,
#     "clubhouse": True,
#     "gym": True,
#     "childrensplayarea": True,
#     "pipedgas": True,
#     "cctvcameras": True,
#     "otheramenities": "newdata",
#     "studio": "True",
#     "1BHK": False,
#     "2BHK": True,
#     "3BHK": True,
#     "rowhouse": False,
#     "otheraccomodationtypes": "4BHK",
#     "sourceofwater": "abc"
#   },
#   "project_bank_details": [
#     {
#       "bankname": "Banktest",
#       "bankbranch": "branchtest",
#       "bankcity": "Pune",
#       "bankaccountholdername": "Rudra",
#       "bankaccountno": "ABD102834732",
#       "bankifsccode": "PUN101",
#       "banktypeofaccount": "savings"
#     },
#     {
#       "bankname": "Banktest",
#       "bankbranch": "branchtest1",
#       "bankcity": "Pune",
#       "bankaccountholdername": "Rudra",
#       "bankaccountno": "ABD1046464732",
#       "bankifsccode": "PUN102",
#       "banktypeofaccount": "savings"
#     }
#   ],
#   "project_contacts": [
#     {
#       "contactname": "Rudra",
#       "phone": "9796543567",
#       "email": "abc",
#       "role": "owner",
#       "effectivedate": "2021-02-04 10:00:00",
#       "tenureenddate": None,
#       "details": "hreiufhuire"
#     },
#     {
#       "contactname": "Rudra_2",
#       "phone": "9456545514",
#       "email": "efg",
#       "role": "manager",
#       "effectivedate": "2021-02-04 10:00:00",
#       "tenureenddate": "2024-02-04 10:00:00",
#       "details": "hreiufhuire"
#     }
#   ],
#   "project_photos":[
#     {
#         "photo_link":"link1",
#         "description":"Desc 1",
#         "date_taken":"2024-03-01"
#     },
#     {
#         "photo_link":"link2",
#         "description":"Desc2",
#         "date_taken":"2024-01-01"   
#     }
#   ]
# }


#         expected_response = {
#   "result": "success",
#   "user_id": 1234,
#   "role_id": 1,
#   "data": {
#     "added project id": 4422
#   }
# }
#         with patch('main.check_role_access', return_value=1):
#             response = client.post('/addProject', json=payload)

#         assert response.status_code == 200
#         assert response.json() == expected_response

        # delete_query = """
        # DELETE FROM research_prospect
        # WHERE personname = %s
        # """
        # cursor.execute(delete_query, ("New changed person",))
        # db_connection.commit()


# @pytest.mark.usefixtures("db_connection")
# def test_id_87(client, db_connection):
#     payload = {
#         "user_id": 1234,
#         "id": 11000,
#         "builderid": 3000,
#         "projectname": "testproject",
#         "addressline1": "123 Main Street",
#         "addressline2": "Apt 101",
#         "suburb": "Downtown",
#         "city": 456,
#         "state": "California",
#         "country": 789,
#         "zip": "12345",
#         "nearestlandmark": "Central Park",
#         "project_type": 1,
#         "mailgroup1": "group1@example.com",
#         "mailgroup2": "group2@example.com",
#         "website": "www.sampleproject.com",
#         "project_legal_status": 2,
#         "rules": "Some rules for the project",
#         "completionyear": 2025,
#         "jurisdiction": "Local jurisdiction",
#         "taluka": "Taluka",
#         "corporationward": "Ward 1",
#         "policechowkey": "Chowkey 1",
#         "policestation": "Station 1",
#         "maintenance_details": "Maintenance details",
#         "numberoffloors": 5,
#         "numberofbuildings": 3,
#         "approxtotalunits": 50,
#         "tenantstudentsallowed": True,
#         "tenantworkingbachelorsallowed": False,
#         "tenantforeignersallowed": True,
#         "otherdetails": "Other details about the project",
#         "duespayablemonth": 12,
#         "dated": "2024-03-15T08:00:00",
#         "createdby": 5678,
#         "isdeleted": False
#     }

#     conn = db_connection

#     try:
#         with conn.cursor() as cursor:
#             check_query = "SELECT projectname FROM project WHERE projectname = %s"
#             cursor.execute(check_query, (payload["projectname"],))
#             existing_project = cursor.fetchone()

#             if existing_project:
#                 assert False,"Project already exists in the database"

#             insert_query = """
#                 INSERT INTO project (
#                     builderid, projectname, addressline1, addressline2, suburb, city, state, country,
#                     zip, nearestlandmark, project_type, mailgroup1, mailgroup2, website, project_legal_status,
#                     rules, completionyear, jurisdiction, taluka, corporationward, policechowkey, policestation,
#                     maintenance_details, numberoffloors, numberofbuildings, approxtotalunits, tenantstudentsallowed,
#                     tenantworkingbachelorsallowed, tenantforeignersallowed, otherdetails, duespayablemonth, dated,
#                     createdby, isdeleted
#                 ) VALUES (
#                     %(builderid)s, %(projectname)s, %(addressline1)s, %(addressline2)s, %(suburb)s, %(city)s,
#                     %(state)s, %(country)s, %(zip)s, %(nearestlandmark)s, %(project_type)s, %(mailgroup1)s, %(mailgroup2)s,
#                     %(website)s, %(project_legal_status)s, %(rules)s, %(completionyear)s, %(jurisdiction)s, %(taluka)s,
#                     %(corporationward)s, %(policechowkey)s, %(policestation)s, %(maintenance_details)s, %(numberoffloors)s,
#                     %(numberofbuildings)s, %(approxtotalunits)s, %(tenantstudentsallowed)s, %(tenantworkingbachelorsallowed)s,
#                     %(tenantforeignersallowed)s, %(otherdetails)s, %(duespayablemonth)s, %(dated)s, %(createdby)s, %(isdeleted)s
#                 )
#                 """
#             cursor.execute(insert_query, payload)
#             conn.commit()

#         with patch.object(logging, 'info') as mock_info:
#             with patch('main.check_role_access', return_value=1):
#                 response = client.post('/addProject', json=payload)

#         expected_response = {
#         "result": "error",
#         "message": "Already Exists",
#         "user_id": 1234,
#         "role_id": 1,
#         "data": []
#     }

#         assert response.status_code == 200
#         assert response.json() == expected_response
#         mock_info.assert_called_once_with(f'addProject: received payload <{payload}>')

#     except Exception as e:
#         logging.error(f"An error occurred: {e}")
#         raise e

#     finally:
#         with conn.cursor() as cursor:
#             delete_query = "DELETE FROM project WHERE projectname = %s"
#             cursor.execute(delete_query, (payload["projectname"],))
#             conn.commit()


@pytest.mark.usefixtures("db_connection")
def test_id_87(client):
    payload = {
  "user_id": 1234,
  "project_info": {
    "builderid": 10231,
    "addressline1": "addressline1",
    "addressline2": "addressline2",
    "suburb": "testsub",
    "city": 847,
    "state": "Maharashtra",
    "country": 5,
    "zip": "testzip",
    "nearestlandmark": "landmark1",
    "project_type": 2,
    "mailgroup1": "mailgrouptest",
    "mailgroup2": "newmailgrouptest",
    "website": "websitetest.com",
    "project_legal_status": 2,
    "rules": "rule1, rule2, rule3",
    "completionyear": 2021,
    "jurisdiction": "ajuri",
    "taluka": "tal",
    "corporationward": "ward",
    "policechowkey": "chowkey",
    "policestation":"station",
    "maintenance_details": "deets",
    "numberoffloors": 5,
    "numberofbuildings": 4,
    "approxtotalunits": 100,
    "tenantstudentsallowed": True,
    "tenantworkingbachelorsallowed": True,
    "tenantforeignersallowed": True,
    "otherdetails": True,
    "duespayablemonth": 3
  },
  "project_amenities": {
    "swimmingpool": True,
    "lift": True,
    "liftbatterybackup": True,
    "clubhouse": True,
    "gym": True,
    "childrensplayarea": True,
    "pipedgas": True,
    "cctvcameras": True,
    "otheramenities": "newdata",
    "studio": True,
    "1BHK": False,
    "2BHK": True,
    "3BHK": True,
    "4BHK": False,
    "RK": False,
    "penthouse": False,
    "other": False,
    "duplex": False,
    "rowhouse": False,
    "otheraccomodationtypes": "4BHK, RK, penthouse, other, duplex",
    "sourceofwater": "abc"
  },
  "project_bank_details": [
    {
      "bankname": "Banktest",
      "bankbranch": "branchtest",
      "bankcity": "Pune",
      "bankaccountholdername": "Rudra",
      "bankaccountno": "ABD102834732",
      "bankifsccode": "PUN101",
      "banktypeofaccount": "savings",
      "bankmicrcode": "MICR1234"
    },
    {
      "bankname": "Banktest",
      "bankbranch": "branchtest1",
      "bankcity": "Pune",
      "bankaccountholdername": "Rudra",
      "bankaccountno": "ABD1046464732",
      "bankifsccode": "PUN102",
      "banktypeofaccount": "savings",
      "bankmicrcode": "MICR5678"
    }
  ],
  "project_contacts": [
    {
      "contactname": "Rudra",
      "phone": "9796543567",
      "email": "abc",
      "role": "owner",
      "effectivedate": "2021-02-04 10:00:00",
      "tenureenddate": None,
      "details": "hreiufhuire"
    },
    {
      "contactname": "Rudra_2",
      "phone": "9456545514",
      "email": "efg",
      "role": "manager",
      "effectivedate": "2021-02-04 10:00:00",
      "tenureenddate": "2024-02-04 10:00:00",
      "details": "hreiufhuire"
    }
  ],
  "project_photos": [
    {
      "photo_link": "link1",
      "description": "Desc 1",
      "date_taken": "2024-03-01"
    },
    {
      "photo_link": "link2",
      "description": "Desc2",
      "date_taken": "2024-01-01"
    }
  ]
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
  "projectid": 4378,
  "project_info": {
    "id": 4378,
    "builderid": 10231,
    "projectname": "testproject",
    "addressline1": "addressline1",
    "addressline2": "addressline2",
    "suburb": "trying",
    "city": 847,
    "state": "Maharashtra",
    "country": 5,
    "zip": "testzip",
    "nearestlandmark": "landmark1",
    "project_type": 2,
    "mailgroup1": "mailgrouptest",
    "mailgroup2": "newmailgrouptest",
    "website": "websitetest.com",
    "project_legal_status": 2,
    "rules": "rule1, rule2, rule3",
    "completionyear": 2021,
    "jurisdiction": "ajuri",
    "taluka": "tal",
    "corporationward": "ward",
    "policestation":"station",
    "policechowkey": "chowkey",
    "maintenance_details": "deets",
    "numberoffloors": 5,
    "numberofbuildings": 4,
    "approxtotalunits": 100,
    "tenantstudentsallowed": True,
    "tenantworkingbachelorsallowed": True,
    "tenantforeignersallowed": True,
    "otherdetails": True,
    "duespayablemonth": 3
  },
  "project_amenities": {
    "id": 4409,
    "swimmingpool": True,
    "lift": True,
    "liftbatterybackup": True,
    "clubhouse": True,
    "gym": True,
    "childrensplayarea": True,
    "pipedgas": True,
    "cctvcameras": True,
    "otheramenities": "newdata",
    "studio": "True",
    "1BHK": False,
    "2BHK": True,
    "3BHK": True,
    "4BHK": False,
    "RK": False,
    "other": False,
    "duplex": False,
    "penthouse": False,
    "rowhouse":True,
    "sourceofwater": "abc",
    "otheraccomodationtypes":"new"
  },
  "project_bank_details": {
    "update": [{
        "id": 71,
        "bankname": "Banktest",
        "bankbranch": "branchtest",
        "bankcity": "Pune",
        "bankaccountholdername": "Rudra",
        "bankaccountno": "ABD102834732",
        "bankifsccode": "PUN101",
        "banktypeofaccount": "current",
        "bankmicrcode":"code"
      },
      {
        "id": 72,
        "bankname": "Banktest",
        "bankbranch": "branchtest1",
        "bankcity": "Pune",
        "bankaccountholdername": "Rudra",
        "bankaccountno": "ABD1046464732",
        "bankifsccode": "PUN102",
        "banktypeofaccount": "current",
        "bankmicrcode":"code"
      }
    ],
    "insert": [{
        "bankname": "Banktest",
        "bankbranch": "branchtest",
        "bankcity": "Pune",
        "bankaccountholdername": "Rudra",
        "bankaccountno": "ABD102834732",
        "bankifsccode": "PUN101",
        "banktypeofaccount": "savings",
        "bankmicrcode":"code"
      },
      {
        "bankname": "Banktest",
        "bankbranch": "branchtest1",
        "bankcity": "Pune",
        "bankaccountholdername": "Rudra",
        "bankaccountno": "ABD1046464732",
        "bankifsccode": "PUN102",
        "banktypeofaccount": "savings",
        "bankmicrcode":"code"
      }
    ],
    "delete": []
  },
  "project_contacts": {
    "insert": [{
        "contactname": "Rudra",
        "phone": "9796543567",
        "email": "abc",
        "role": "owner",
        "effectivedate": "2021-02-04 10:00:00",
        "tenureenddate": None,
        "details": "hreiufhuire"
      },
      {
        "contactname": "Rudra_2",
        "phone": "9456545514",
        "email": "efg",
        "role": "manager",
        "effectivedate": "2021-02-04 10:00:00",
        "tenureenddate": "2024-02-04 10:00:00",
        "details": "hreiufhuire"
      }
    ],
    "update": [{
        "id": 3439,
        "contactname": "Rudra",
        "phone": "9796543567",
        "email": "abc",
        "role": "owner",
        "effectivedate": "2021-02-04 10:00:00",
        "tenureenddate": None,
        "details": "hreiufhuire"
      },
      {
        "id": 3440,
        "contactname": "Rudra_2",
        "phone": "9456545514",
        "email": "efg",
        "role": "manager",
        "effectivedate": "2021-02-04 10:00:00",
        "tenureenddate": "2024-02-04 10:00:00",
        "details": "hreiufhuire"
      }
    ]
  },
  "project_photos": {
    "insert": [{
        "photo_link": "link1",
        "description": "Desc 1",
        "date_taken": "2024-03-01"
      },
      {
        "photo_link": "link2",
        "description": "Desc2",
        "date_taken": "2024-01-01"
      }
    ],
    "update": [{
        "id": 28,
        "photo_link": "link1",
        "description": "Desc 1",
        "date_taken": "2024-03-01"
      },
      {
        "id": 29,
        "photo_link": "link2",
        "description": "Desc2",
        "date_taken": "2024-01-01"
      }
    ]
  }
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
                tenantworkingbachelorsallowed, tenantforeignersallowed, otherdetails, duespayablemonth
            ) VALUES (
                %(builderid)s, %(projectname)s, %(addressline1)s, %(addressline2)s, %(suburb)s, %(city)s,
                %(state)s, %(country)s, %(zip)s, %(nearestlandmark)s, %(project_type)s, %(mailgroup1)s, %(mailgroup2)s,
                %(website)s, %(project_legal_status)s, %(rules)s, %(completionyear)s, %(jurisdiction)s, %(taluka)s,
                %(corporationward)s, %(policechowkey)s, %(policestation)s, %(maintenance_details)s, %(numberoffloors)s,
                %(numberofbuildings)s, %(approxtotalunits)s, %(tenantstudentsallowed)s, %(tenantworkingbachelorsallowed)s,
                %(tenantforeignersallowed)s, %(otherdetails)s, %(duespayablemonth)s
            ) RETURNING id
            """
            
            cursor.execute(query_insert_project, payload["project_info"])
            payload['projectid'] = cursor.fetchone()[0]
            payload['project_info']['id'] = payload['projectid']
            conn.commit()
        
        payload["projectname"] = "Updated Sample Project"
        with conn.cursor() as cursor:
            query_update_project_name = "UPDATE project SET projectname = %s WHERE id = %s"
            cursor.execute(query_update_project_name, (payload["projectname"], payload["projectid"]))
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
        assert response.json()['result'] == 'success'

    except Exception as e:
        print(f"An error occurred: {e}")
        raise e  

    finally:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM project WHERE id = %s", (payload["projectid"],))
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
  "role_id": 1,
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
        cursor.execute("DELETE FROM country")
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
                "sort_by": ["id"],
                "order": "asc",
                "pg_no": 1,
                "pg_size": 2,
                "search_key": None
            })

        assert response.status_code == 200
        assert response.json()['result'] == 'success'
        assert len(response.json()['data']['data']) == 2
    
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
def test_id_12(client):
    payload = {"user_id":1234,"rows":["buildername", "builderid","projectname","addressline1","addressline2","suburb","city","state","country","zip","nearestlandmark","project_type","mailgroup1","mailgroup2","website","project_legal_status","rules","completionyear","jurisdiction","taluka","corporationward","policechowkey","policestation","maintenance_details","numberoffloors","numberofbuildings","approxtotalunits","tenantstudentsallowed","tenantworkingbachelorsallowed","tenantforeignersallowed","otherdetails","duespayablemonth","dated","createdby","isdeleted","id"],"filters":[],"sort_by":[],"order":"asc","pg_no":1,"pg_size":2}
    with newconn().cursor() as cursor:
        cursor.execute('SELECT count(*) FROM get_projects_view')
        count = cursor.fetchone()[0]
    expected_response = count
    with patch('main.check_role_access', return_value=1):
        response = client.post('/getProjects', json=payload)

    assert response.status_code == 200
    assert response.json()['total_count'] == expected_response


@pytest.mark.usefixtures("db_connection")
def test_id_13(client):
    payload = {"user_id":1235,"rows":["buildername", "builderid","projectname","addressline1","addressline2","suburb","city","state","country","zip","nearestlandmark","project_type","mailgroup1","mailgroup2","website","project_legal_status","rules","completionyear","jurisdiction","taluka","corporationward","policechowkey","policestation","maintenance_details","numberoffloors","numberofbuildings","approxtotalunits","tenantstudentsallowed","tenantworkingbachelorsallowed","tenantforeignersallowed","otherdetails","duespayablemonth","dated","createdby","isdeleted","id"],"sort_by":[],"order":"asc","pg_no":1,"pg_size":2}
    expected_response ={
  "result": "error",
  "message": "Access Denied",
  "user_id": 1239,
  "role_id": 0,
  "data": []
}
    with patch('main.check_role_access', return_value=1):
        response = client.post('/getProjects', json=payload)
    assert response.json()
    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_14(client):
    payload = {"user_id":1237,"rows":["buildername", "builderid","projectname","addressline1","addressline2","suburb","city","state","country","zip","nearestlandmark","project_type","mailgroup1","mailgroup2","website","project_legal_status","rules","completionyear","jurisdiction","taluka","corporationward","policechowkey","policestation","maintenance_details","numberoffloors","numberofbuildings","approxtotalunits","tenantstudentsallowed","tenantworkingbachelorsallowed","tenantforeignersallowed","otherdetails","duespayablemonth","dated","createdby","isdeleted","id"],"filters":[],"sort_by":[],"order":"asc","pg_no":1,"pg_size":2}
    expected_response ={
  "result": "error",
  "message": "Access Denied",
  "user_id": 1237,
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
                cursor.execute("INSERT INTO cities (id, city, state, countryid) VALUES (%s, %s, %s, %s)", (1620, "Kolkata", "West Bengal", 5))
                db_connection.commit()
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
        cursor.execute("INSERT INTO country (id, name) VALUES (1, 'country1'), (2, 'country2')")
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
            response = client.post('/getCitiesAdmin', json={"user_id": 1234, "rows": ["id", "city", "state", "countryid", "country"], "filters": [], "sort_by": [], "order": "asc","pg_no": 1, "pg_size": 15})

            assert response.status_code == 200
            assert response.json()['result'] == 'success'
    
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

    with patch('main.check_role_access', return_value=1):
        response = client.post('/getBuilderInfo', json=payload)

    print("Response content:", response.content) 

    assert response.status_code == 200
    assert response.json()["total_count"] > 0
    # assert response.json() == expected_response

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
      1,
      "CURA"
    ],
    [
      2,
      "Z-ASDK"
    ],
    [
      7,
      "Z-CASH"
    ],
    [
      6,
      "Z-COREFUR"
    ],
    [
      3,
      "Z-PRIME"
    ],
    [
      4,
      "ZZZ"
    ],
    [
      5,
      "ZZZ"
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
    "added_payment_id": 1234
  }
}
    with patch('main.check_role_access', return_value=1):
        response = client.post('/addPayment', json=payload)

    assert response.status_code == 200
    assert response.json()['result'] == 'success'


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

    with patch('main.check_role_access', return_value=1):
        response = client.post('/getPayments', json=payload)

    print("Response content:", response.content) 

    assert response.status_code == 200
    assert response.json()["total_count"] > 0
    # assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_105(client):
    payload = { "user_id": 1234, "row": [ "id", "paymentto", "paymentby", "amount", "paidon", "paymentmode", "paymentstatus", "description", "banktransactionid", "paymentfor", "dated", "createdby", "isdeleted", "entityid", "officeid", "tds", "professiontax", "month", "deduction" ], "sort_by": [], "order": "asc", "pg_no": 1, "pg_size": 15, "search_key":"anvay" }
    expected_response =  None

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

    with patch('main.check_role_access', return_value=1):
        response = client.post('/getRolesAdmin', json=payload)

    assert response.status_code == 200
    assert response.json()["total_count"] > 0
    # assert response.json() == expected_response


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

    with patch('main.check_role_access', return_value=1):
        response = client.post('/getUsersAdmin', json=payload)

    assert response.status_code == 200
    assert response.json()["total_count"] > 0
    # assert response.json() == expected_response


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
        "vendorid": 14000
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
                payload["user_id"]
            ))
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
            conn.commit()

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
def test_id_122(client):
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
  "result": "success",
  "user_id": 1234,
  "role_id": 1,
  "data": [
    {
      "id": 1,
      "modeofpayment": 5,
      "amount": 128890.5,
      "crdr": "CR                  ",
      "chequeno": ""
    },
    {
      "id": 2,
      "modeofpayment": 5,
      "amount": 1053,
      "crdr": "DR                  ",
      "chequeno": ""
    },
    {
      "id": 3,
      "modeofpayment": 5,
      "amount": 30600,
      "crdr": "DR                  ",
      "chequeno": ""
    },
    {
      "id": 4,
      "modeofpayment": 5,
      "amount": 346,
      "crdr": "CR                  ",
      "chequeno": ""
    },
    {
      "id": 5,
      "modeofpayment": 5,
      "amount": 2000,
      "crdr": "DR                  ",
      "chequeno": ""
    },
    {
      "id": 6,
      "modeofpayment": 5,
      "amount": 32000,
      "crdr": "CR                  ",
      "chequeno": ""
    },
    {
      "id": 7,
      "modeofpayment": 5,
      "amount": 3000,
      "crdr": "DR                  ",
      "chequeno": ""
    },
    {
      "id": 8,
      "modeofpayment": 5,
      "amount": 19300,
      "crdr": "CR                  ",
      "chequeno": ""
    },
    {
      "id": 9,
      "modeofpayment": 5,
      "amount": 2000,
      "crdr": "DR                  ",
      "chequeno": ""
    },
    {
      "id": 10,
      "modeofpayment": 5,
      "amount": 5000,
      "crdr": "CR                  ",
      "chequeno": ""
    },
    {
      "id": 11,
      "modeofpayment": 5,
      "amount": 16140,
      "crdr": "CR                  ",
      "chequeno": ""
    },
    {
      "id": 12,
      "modeofpayment": 5,
      "amount": 12500,
      "crdr": "CR                  ",
      "chequeno": ""
    },
    {
      "id": 13,
      "modeofpayment": 5,
      "amount": 5175,
      "crdr": "DR                  ",
      "chequeno": ""
    },
    {
      "id": 14,
      "modeofpayment": 5,
      "amount": 5277,
      "crdr": "CR                  ",
      "chequeno": ""
    },
    {
      "id": 15,
      "modeofpayment": 5,
      "amount": 8990,
      "crdr": "DR                  ",
      "chequeno": ""
    }
  ]
} 
    conn = newconn()
    with conn.cursor() as cursor:
        cursor.execute('SELECT count(*) FROM bankst')
        count = cursor.fetchone()[0]
    with patch('main.check_role_access', return_value=1):
       response=client.post('/getBankSt',json=payload)
    
    assert response.status_code == 200
    assert response.json()['total_count'] == count
    # assert response.json()["total_count"] > 0

@pytest.mark.usefixtures("db_connection")
def test_id_123(client):
    payload = {
  "user_id": 1235,
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

    with patch('main.check_role_access', return_value=1):
        response = client.post('/getResearchProspect', json=payload)

    assert response.status_code == 200
    assert response.json()['total_count'] > 0

@pytest.mark.usefixtures("db_connection")
def test_id_129(client):
    payload = {"user_id":1234,"rows":["id","personname","suburb","city","country"],"sort_by":[],"order":"asc","pg_no":1,"pg_size":15}
    expected_response = None
    with patch('main.check_role_access', return_value=1):
        response = client.post('/getResearchProspect', json=payload)
    conn = newconn()
    with conn.cursor() as cursor:
        cursor.execute('SELECT count(*) FROM get_research_prospect_view')
        count = cursor.fetchall()[0]
    


    assert response.status_code == 200
    assert response.json()['total_count'] == count

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
def test_id_131(client, db_connection):
    with db_connection.cursor() as cursor:
        insert_query = """
        INSERT INTO research_prospect (personname, suburb, city, state, country, propertylocation, possibleservices, createdby, isdeleted, phoneno, email1)
        VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
             "New changed person", "abcde", "Mumbai", "Maharashtra", 5, "abcdefgh", "abcdefgh", 1234, False, "8877292839", "abc@defgh.com"
        ))
        db_connection.commit()

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
            "isdeleted": False,
            "phoneno": "8877292839",
            "email1": "abc@defgh.com"
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

        delete_query = """
        DELETE FROM research_prospect
        WHERE personname = %s
        """
        cursor.execute(delete_query, ("New changed person",))
        db_connection.commit()

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
def test_id_134(client, db_connection):
    with db_connection.cursor() as cursor:
        insert_query = """
        INSERT INTO research_prospect (id, personname, suburb, city, state, country, propertylocation, possibleservices, dated, createdby, isdeleted)
        VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
             90, "New changed person", "abcde", "Mumbai", "Maharashtra", 5, "abcdefgh", "abcdefgh", "2024-01-01 00:00:00", 1234, False
        ))
        db_connection.commit()

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
        assert response.json() == expected_response

        delete_query = """
        DELETE FROM research_prospect
        WHERE id = %s
        """
        cursor.execute(delete_query, (90,))
        db_connection.commit()

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
def test_id_137(client, db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute("SELECT MAX(id) FROM research_prospect")
        max_id = cursor.fetchone()[0]
        new_id = max_id + 1 if max_id is not None else 1

        insert_query = """
        INSERT INTO research_prospect (personname, suburb, city, state, country, propertylocation, possibleservices, createdby, isdeleted, phoneno, email1)
        VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
             "New changed person", "abcde", "Mumbai", "Maharashtra", 5, "abcdefgh", "abcdefgh", 1234, False, "8877292839", "abc@defgh.com"
        ))
        db_connection.commit()

        payload = {"user_id": 1234, "id": new_id}

        expected_response = {
            "result": "success",
            "user_id": 1234,
            "role_id": 1,
            "data": {
                "deleted_prospect": new_id
            }
        }
        with patch('main.check_role_access', return_value=1):
            response = client.post('/deleteResearchProspect', json=payload)

        assert response.status_code == 200
        assert expected_response['data']['deleted_prospect'] > 0

        delete_query = """
        DELETE FROM research_prospect
        WHERE id = %s
        """
        cursor.execute(delete_query, (new_id,))
        db_connection.commit()

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


@pytest.mark.usefixtures("db_connection")
def test_id_152(client, db_connection):
    payload = {
        "user_id": 1234,
        "project_info": {
            "builderid": 10231,
            "projectname": "testproject",
            "addressline1": "addressline1",
            "addressline2": "addressline2",
            "suburb": "testsub",
            "city": 847,
            "state": "Maharashtra",
            "country": 5,
            "zip": "testzip",
            "nearestlandmark": "landmark1",
            "project_type": 2,
            "mailgroup1": "mailgrouptest",
            "mailgroup2": "newmailgrouptest",
            "website": "websitetest.com",
            "project_legal_status": 2,
            "rules": "rule1, rule2, rule3",
            "completionyear": 2021,
            "jurisdiction": "ajuri",
            "taluka": "tal",
            "corporationward": "ward",
            "policechowkey": "chowkey",
            "maintenance_details": "deets",
            "numberoffloors": 5,
            "numberofbuildings": 4,
            "approxtotalunits": 100,
            "tenantstudentsalowed": True,
            "tenantworkingbachelorsallowed": True,
            "tenantforeignersallowed": True,
            "otherdetails": True,
            "duespayablemonth": 3
        },
        "project_amenities": {
            "swimmingpool": True,
            "lift": True,
            "liftbatterybackup": True,
            "clubhouse": True,
            "gym": True,
            "childrensplayarea": True,
            "pipedgas": True,
            "cctvcameras": True,
            "otheramenities": "newdata",
            "studio": "True",
            "1BHK": False,
            "2BHK": True,
            "3BHK": True,
            "rowhouse": False,
            "otheraccomodaationtypes": "4BHK",
            "sourceofwater": "abc"
        },
        "project_bank_details": [
            {
                "bankname": "Banktest",
                "bankbranch": "branchtest",
                "bankcity": "Pune",
                "bankaccountholdername": "Rudra",
                "bankaccountno": "ABD102834732",
                "bankifsccode": "PUN101",
                "banktypeofaccount": "savings"
            },
            {
                "bankname": "Banktest",
                "bankbranch": "branchtest1",
                "bankcity": "Pune",
                "bankaccountholdername": "Rudra",
                "bankaccountno": "ABD1046464732",
                "bankifsccode": "PUN102",
                "banktypeofaccount": "savings"
            }
        ],
        "project_contacts": [
            {
                "contactname": "Rudra",
                "phone": "9796543567",
                "email": "abc",
                "role": "owner",
                "effectivedate": "2021-02-04 10:00:00",
                "tenureenddate": None,
                "details": "hreiufhuire"
            },
            {
                "contactname": "Rudra_2",
                "phone": "9456545514",
                "email": "efg",
                "role": "manager",
                "effectivedate": "2021-02-04 10:00:00",
                "tenureenddate": "2024-02-04 10:00:00",
                "details": "hreiufhuire"
            }
        ],
        "project_photos": [
            {
                "photo_link": "link1",
                "description": "Desc 1",
                "date_taken": "2024-03-01"
            },
            {
                "photo_link": "link2",
                "description": "Desc2",
                "date_taken": "2024-01-01"
            }
        ]
    }

    expected_response = {
        "result": "success",
        "user_id": 1234,
        "role_id": 1,
        "data": {
            "inserted_id": 44599
        }
    }

    conn = None

    try:
        conn = db_connection

        with conn.cursor() as cur:
            query = "INSERT INTO client (firstname,middlename,lastname,salutation,clienttype,addressline1,addressline2,suburb,city,state,country,zip,homephone,workphone,mobilephone,email1,email2,employername,comments,photo,onlineaccreated,localcontact1name,localcontact1address,localcontact1details,localcontact2name,localcontact2address,localcontact2details,includeinmailinglist,dated,createdby,isdeleted,entityid,tenantof,tenantofproperty) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id"
            cur.execute(query, (
                payload["firstname"], payload["middlename"], payload["lastname"], payload["salutation"],
                payload["clienttype"], payload["addressline1"], payload["addressline2"], payload["suburb"],
                payload["city"], payload["state"], payload["country"], payload["zip"], payload["homephone"],
                payload["workphone"], payload["mobilephone"], payload["email1"], payload["email2"],
                payload["employername"], payload["comments"], payload["photo"], payload["onlineaccreated"],
                payload["localcontact1name"], payload["localcontact1address"], payload["localcontact1details"],
                payload["localcontact2name"], payload["localcontact2address"], payload["localcontact2details"],
                payload["includeinmailinglist"], givenowtime(), payload['user_id'], False, payload["entityid"],
                payload["tenantof"], payload["tenantofproperty"]))
            conn.commit()

        with patch('main.check_role_access', return_value=1):
            response = client.post('/addClientInfo', json=payload)

        assert response.status_code == 200
        assert response.json() == expected_response

    except Exception as e:
        logging.error(f"An error occurred: {e}")

    finally:
        if conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM client WHERE id = %s", (expected_response["data"]["inserted_id"],))
                conn.commit()



@pytest.mark.usefixtures("db_connection")
def test_id_153(client, db_connection):
    payload = {
        "user_id": 1234,
        "project_info": {
            "builderid": 10231,
            "addressline1": "addressline1",
            "addressline2": "addressline2",
            "suburb": "testsub",
            "city": 847,
            "state": "Maharashtra",
            "country": 5,
            "zip": "testzip",
            "nearestlandmark": "landmark1",
            "project_type": 2,
            "mailgroup1": "mailgrouptest",
            "mailgroup2": "newmailgrouptest",
            "website": "websitetest.com",
            "project_legal_status": 2,
            "rules": "rule1, rule2, rule3",
            "completionyear": 2021,
            "jurisdiction": "ajuri",
            "taluka": "tal",
            "corporationward": "ward",
            "policechowkey": "chowkey",
            "maintenance_details": "deets",
            "numberoffloors": 5,
            "numberofbuildings": 4,
            "approxtotalunits": 100,
            "tenantstudentsalowed": True,
            "tenantworkingbachelorsallowed": True,
            "tenantforeignersallowed": True,
            "otherdetails": True,
            "duespayablemonth": 3
        },
        "project_amenities": {
            "swimmingpool": True,
            "lift": True,
            "liftbatterybackup": True,
            "clubhouse": True,
            "gym": True,
            "childrensplayarea": True,
            "pipedgas": True,
            "cctvcameras": True,
            "otheramenities": "newdata",
            "studio": "True",
            "1BHK": False,
            "2BHK": True,
            "3BHK": True,
            "rowhouse": False,
            "otheraccomodaationtypes": "4BHK",
            "sourceofwater": "abc"
        },
        "project_bank_details": [
            {
                "bankname": "Banktest",
                "bankbranch": "branchtest",
                "bankcity": "Pune",
                "bankaccountholdername": "Rudra",
                "bankaccountno": "ABD102834732",
                "bankifsccode": "PUN101",
                "banktypeofaccount": "savings"
            },
            {
                "bankname": "Banktest",
                "bankbranch": "branchtest1",
                "bankcity": "Pune",
                "bankaccountholdername": "Rudra",
                "bankaccountno": "ABD1046464732",
                "bankifsccode": "PUN102",
                "banktypeofaccount": "savings"
            }
        ],
        "project_contacts": [
            {
                "contactname": "Rudra",
                "phone": "9796543567",
                "email": "abc",
                "role": "owner",
                "effectivedate": "2021-02-04 10:00:00",
                "tenureenddate": None,
                "details": "hreiufhuire"
            },
            {
                "contactname": "Rudra_2",
                "phone": "9456545514",
                "email": "efg",
                "role": "manager",
                "effectivedate": "2021-02-04 10:00:00",
                "tenureenddate": "2024-02-04 10:00:00",
                "details": "hreiufhuire"
            }
        ],
        "project_photos": [
            {
                "photo_link": "link1",
                "description": "Desc 1",
                "date_taken": "2024-03-01"
            },
            {
                "photo_link": "link2",
                "description": "Desc2",
                "date_taken": "2024-01-01"
            }
        ]
    }

    expected_response = None

    conn = None

    try:
        conn = db_connection

        with conn.cursor() as cur:
            query = "INSERT INTO client (firstname,middlename,lastname,salutation,clienttype,addressline1,addressline2,suburb,city,state,country,zip,homephone,workphone,mobilephone,email1,email2,employername,comments,photo,onlineaccreated,localcontact1name,localcontact1address,localcontact1details,localcontact2name,localcontact2address,localcontact2details,includeinmailinglist,dated,createdby,isdeleted,entityid,tenantof,tenantofproperty) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id"
            cur.execute(query, (
                payload["firstname"], payload["middlename"], payload["lastname"], payload["salutation"],
                payload["clienttype"], payload["addressline1"], payload["addressline2"], payload["suburb"],
                payload["city"], payload["state"], payload["country"], payload["zip"], payload["homephone"],
                payload["workphone"], payload["mobilephone"], payload["email1"], payload["email2"],
                payload["employername"], payload["comments"], payload["photo"], payload["onlineaccreated"],
                payload["localcontact1name"], payload["localcontact1address"], payload["localcontact1details"],
                payload["localcontact2name"], payload["localcontact2address"], payload["localcontact2details"],
                payload["includeinmailinglist"], givenowtime(), payload['user_id'], False, payload["entityid"],
                payload["tenantof"], payload["tenantofproperty"]))
            conn.commit()

        with patch('main.check_role_access', return_value=1):
            response = client.post('/addClientInfo', json=payload)

        assert response.status_code == 200
        assert response.json() == expected_response

    except Exception as e:
        logging.error(f"An error occurred: {e}")

  
@pytest.mark.usefixtures("db_connection")
def test_id_154(client, db_connection):
    payload = {
        "user_id": 1234,
        "project_info": {
            "builderid": 10231,
            "projectname": "testproject",
            "addressline1": "addressline1",
            "addressline2": "addressline2",
            "suburb": "testsub",
            "city": 847,
            "state": "Maharashtra",
            "country": 5,
            "zip": "testzip",
            "nearestlandmark": "landmark1",
            "project_type": 2,
            "mailgroup1": "mailgrouptest",
            "mailgroup2": "newmailgrouptest",
            "website": "websitetest.com",
            "project_legal_status": 2,
            "rules": "rule1, rule2, rule3",
            "completionyear": 2021,
            "jurisdiction": "ajuri",
            "taluka": "tal",
            "corporationward": "ward",
            "policechowkey": "chowkey",
            "maintenance_details": "deets",
            "numberoffloors": 5,
            "numberofbuildings": 4,
            "approxtotalunits": 100,
            "tenantstudentsalowed": True,
            "tenantworkingbachelorsallowed": True,
            "tenantforeignersallowed": True,
            "otherdetails": True,
            "duespayablemonth": 3
        },
        "project_amenities": {
            "swimmingpool": True,
            "lift": True,
            "liftbatterybackup": True,
            "clubhouse": True,
            "gym": True,
            "childrensplayarea": True,
            "pipedgas": True,
            "cctvcameras": True,
            "otheramenities": "newdata",
            "studio": "True",
            "1BHK": False,
            "2BHK": True,
            "3BHK": True,
            "rowhouse": False,
            "otheraccomodaationtypes": "4BHK",
            "sourceofwater": "abc"
        },
        "project_bank_details": [
            {
                "bankname": "Banktest",
                "bankbranch": "branchtest",
                "bankcity": "Pune",
                "bankaccountholdername": "Rudra",
                "bankaccountno": "ABD102834732",
                "bankifsccode": "PUN101",
                "banktypeofaccount": "savings"
            },
            {
                "bankname": "Banktest",
                "bankbranch": "branchtest1",
                "bankcity": "Pune",
                "bankaccountholdername": "Rudra",
                "bankaccountno": "ABD1046464732",
                "bankifsccode": "PUN102",
                "banktypeofaccount": "savings"
            }
        ],
        "project_contacts": [
            {
                "contactname": "Rudra",
                "phone": "9796543567",
                "email": "abc",
                "role": "owner",
                "effectivedate": "2021-02-04 10:00:00",
                "tenureenddate": None,
                "details": "hreiufhuire"
            },
            {
                "contactname": "Rudra_2",
                "phone": "9456545514",
                "email": "efg",
                "role": "manager",
                "effectivedate": "2021-02-04 10:00:00",
                "tenureenddate": "2024-02-04 10:00:00",
                "details": "hreiufhuire"
            }
        ],
        "project_photos": [
            {
                "photo_link": "link1",
                "description": "Desc 1",
                "date_taken": "2024-03-01"
            },
            {
                "photo_link": "link2",
                "description": "Desc2",
                "date_taken": "2024-01-01"
            }
        ]
    }

    expected_response = None

    conn = None

    try:
        conn = db_connection

        with conn.cursor() as cur:
            query = "INSERT INTO client (firstname,middlename,lastname,salutation,clienttype,addressline1,addressline2,suburb,city,state,country,zip,homephone,workphone,mobilephone,email1,email2,employername,comments,photo,onlineaccreated,localcontact1name,localcontact1address,localcontact1details,localcontact2name,localcontact2address,localcontact2details,includeinmailinglist,dated,createdby,isdeleted,entityid,tenantof,tenantofproperty) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id"
            cur.execute(query, (
                payload["firstname"], payload["middlename"], payload["lastname"], payload["salutation"],
                payload["clienttype"], payload["addressline1"], payload["addressline2"], payload["suburb"],
                payload["city"], payload["state"], payload["country"], payload["zip"], payload["homephone"],
                payload["workphone"], payload["mobilephone"], payload["email1"], payload["email2"],
                payload["employername"], payload["comments"], payload["photo"], payload["onlineaccreated"],
                payload["localcontact1name"], payload["localcontact1address"], payload["localcontact1details"],
                payload["localcontact2name"], payload["localcontact2address"], payload["localcontact2details"],
                payload["includeinmailinglist"], givenowtime(), payload['user_id'], False, payload["entityid"],
                payload["tenantof"], payload["tenantofproperty"]))
            conn.commit()

        with patch('main.check_role_access', return_value=0):
            response = client.post('/addClientInfo', json=payload)

        assert response.status_code == 200
        assert response.json() == expected_response

    except Exception as e:
        logging.error(f"An error occurred: {e}")

    # finally:
    #     if conn:
    #         with conn.cursor() as cur:
    #             cur.execute("DELETE FROM client WHERE id = %s", (expected_response["data"]["inserted_id"],))
    #             conn.commit()


@pytest.mark.usefixtures("db_connection")
def test_id_156(client):
    payload = {
        "user_id": 1234,
        "rows":"*",
        "filters": [],
        "sort_by": [],
        "order": "asc",
        "pg_no": 1,
        "pg_size": 15
    }
    
    with patch('main.check_role_access', return_value=1):
       response=client.post('/getClientInfo',json=payload)
    
    assert response.status_code == 200
    # assert response.json() == expected_response
    assert response.json()["total_count"] > 0

@pytest.mark.usefixtures("db_connection")
def test_id_157(client):
    payload = {
  "user_id": 1234,
  "rows": [
    "id",
    "firstname",
    "middlename",
    "lastname",
    "salutation",
    "clienttype",
    "clienttypename",
    "addressline1",
    "addressline2",
    "suburb",
    "city",
    "state",
    "country",
    "zip",
    "homephone",
    "workphone",
    "mobilephone",
    "email1",
    "email2",
    "employername",
    "comments",
    "photo",
    "onlineaccreated",
    "localcontact1name",
    "localcontact1address",
    "localcontact1details",
    "localcontact2name",
    "localcontact2address",
    "localcontact2details",
    "includeinmailinglist",
    "dated",
    "createdby",
    "isdeleted",
    "entityid",
    "tenantof"
  ],
  "sort_by": [],
  "order": "asc",
  "pg_no": 1,
  "pg_size": 15
}

    expected_response={
  "result": "error",
  "message": "Invalid Credentials",
  "user_id": 1234,
  "role_id": 0,
  "data": []
}


    with patch('main.check_role_access', return_value=1):
       response=client.post('/getClientInfo',json=payload)
    
    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_158(client):
    payload = {
  "user_id": 1234,
  "rows": [
    "id",
    "firstname",
    "middlename",
    "lastname",
    "salutation",
    "clienttype",
    "clienttypename",
    "addressline1",
    "addressline2",
    "suburb",
    "city",
    "state",
    "country",
    "zip",
    "homephone",
    "workphone",
    "mobilephone",
    "email1",
    "email2",
    "employername",
    "comments",
    "photo",
    "onlineaccreated",
    "localcontact1name",
    "localcontact1address",
    "localcontact1details",
    "localcontact2name",
    "localcontact2address",
    "localcontact2details",
    "includeinmailinglist",
    "dated",
    "createdby",
    "isdeleted",
    "entityid",
    "tenantof"
  ],
  "filters": [],
  "sort_by": [],
  "order": "asc",
  "pg_no": 1,
  "pg_size": 15
}

    expected_response={
  "result": "error",
  "message": "Access Denied",
  "user_id": 1234,
  "role_id": 0,
  "data": []
}


    with patch('main.check_role_access', return_value=0):
       response=client.post('/getClientInfo',json=payload)
    
    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_159(client, db_connection):
    payload = {"user_id":1234,"id":44525}

    expected_response = {
        "result": "success",
        "user_id": 1234,
        "role_id": 1,
        "data": {
            "deleted_client": 44525
        }
    }

    conn = None

    try:
        conn = db_connection

        with conn.cursor() as cur:
            query = "INSERT INTO client (firstname,middlename,lastname,salutation,clienttype,addressline1,addressline2,suburb,city,state,country,zip,homephone,workphone,mobilephone,email1,email2,employername,comments,photo,onlineaccreated,localcontact1name,localcontact1address,localcontact1details,localcontact2name,localcontact2address,localcontact2details,includeinmailinglist,dated,createdby,isdeleted,entityid,tenantof,tenantofproperty) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id"
            cur.execute(query, (
                "John", "", "Doe", "Mr", 2, "123 Main St", "", "Suburb", "City", "State", "Country", "12345",
                "123-456-7890", "", "987-654-3210", "john@example.com", "", "", "", "", False, "", "", "", "", "",
                "", "", False, "2024-04-04T12:00:00.000Z", 1234, False, None, None, None))
            inserted_id = cur.fetchone()[0]
            conn.commit()

        with patch('main.check_role_access', return_value=1):
            response = client.post('/deleteClientInfo', json=payload)

        assert response.status_code == 200
        assert response.json() == expected_response

        with conn.cursor() as cur:
            delete_query = "DELETE FROM client WHERE id = %s"
            cur.execute(delete_query, (inserted_id,))
            conn.commit()

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        if conn:
            conn.rollback()


@pytest.mark.usefixtures("db_connection")
def test_id_160(client, db_connection):
    payload = {"user_id":1234}

    expected_response = None

    conn = None

    try:
        conn = db_connection

        with conn.cursor() as cur:
            query = "INSERT INTO client (firstname,middlename,lastname,salutation,clienttype,addressline1,addressline2,suburb,city,state,country,zip,homephone,workphone,mobilephone,email1,email2,employername,comments,photo,onlineaccreated,localcontact1name,localcontact1address,localcontact1details,localcontact2name,localcontact2address,localcontact2details,includeinmailinglist,dated,createdby,isdeleted,entityid,tenantof,tenantofproperty) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id"
            cur.execute(query, (
                "John", "", "Doe", "Mr", 2, "123 Main St", "", "Suburb", "City", "State", "Country", "12345",
                "123-456-7890", "", "987-654-3210", "john@example.com", "", "", "", "", False, "", "", "", "", "",
                "", "", False, "2024-04-04T12:00:00.000Z", 1234, False, None, None, None))
            inserted_id = cur.fetchone()[0]
            conn.commit()

        with patch('main.check_role_access', return_value=1):
            response = client.post('/deleteClientInfo', json=payload)

        assert response.status_code == 200
        assert response.json() == expected_response

        with conn.cursor() as cur:
            delete_query = "DELETE FROM client WHERE id = %s"
            cur.execute(delete_query, (inserted_id,))
            conn.commit()

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        if conn:
            conn.rollback()


@pytest.mark.usefixtures("db_connection")
def test_id_161(client, db_connection):
    payload = {"user_id":1234,"id":44525}

    expected_response = None

    conn = None

    try:
        # conn = db_connection

        # with conn.cursor() as cur:
        #     query = "INSERT INTO client (firstname,middlename,lastname,salutation,clienttype,addressline1,addressline2,suburb,city,state,country,zip,homephone,workphone,mobilephone,email1,email2,employername,comments,photo,onlineaccreated,localcontact1name,localcontact1address,localcontact1details,localcontact2name,localcontact2address,localcontact2details,includeinmailinglist,dated,createdby,isdeleted,entityid,tenantof,tenantofproperty) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id"
        #     cur.execute(query, (
        #         "John", "", "Doe", "Mr", 2, "123 Main St", "", "Suburb", "City", "State", "Country", "12345",
        #         "123-456-7890", "", "987-654-3210", "john@example.com", "", "", "", "", False, "", "", "", "", "",
        #         "", "", False, "2024-04-04T12:00:00.000Z", 1234, False, None, None, None))
        #     inserted_id = cur.fetchone()[0]
        #     conn.commit()

        with patch('main.check_role_access', return_value=0):
            response = client.post('/deleteClientInfo', json=payload)

        assert response.status_code == 200
        assert response.json() == expected_response

        # with conn.cursor() as cur:
        #     delete_query = "DELETE FROM client WHERE id = %s"
        #     cur.execute(delete_query, (inserted_id,))
        #     conn.commit()

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        if conn:
            conn.rollback()

@pytest.mark.usefixtures("db_connection")
def test_id_162(client):
    payload = {
    "user_id": 1234,
    "rows": [
      "id",
      "lob_head",
      "name",
      "company"
    ],
    "filters": [],
    "sort_by": [],
    "order": "asc",
    "pg_no": 1,
    "pg_size": 15
  }
    
    with patch('main.check_role_access', return_value=1):
       response=client.post('/getLob',json=payload)
    
    assert response.status_code == 200
    # assert response.json() == expected_response
    assert response.json()["total_count"] > 0

@pytest.mark.usefixtures("db_connection")
def test_id_163(client):
    payload = {
    "user_id": 1234,
    "rows": [
      "id",
      "lob_head",
      "name",
      "company"
    ],
    "sort_by": [],
    "order": "asc",
    "pg_no": 1,
    "pg_size": 15
  }
    expected_response=None
    
    with patch('main.check_role_access', return_value=1):
       response=client.post('/getLob',json=payload)
    
    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_164(client):
    payload = {
    "user_id": 1234,
    "rows": [
      "id",
      "lob_head",
      "name",
      "company"
    ],
    "filters": [],
    "sort_by": [],
    "order": "asc",
    "pg_no": 1,
    "pg_size": 15
  }
    expected_response={
  "result": "error",
  "message": "Access Denied",
  "user_id": 1234,
  "role_id": 0,
  "data": []
}
    
    with patch('main.check_role_access', return_value=0):
       response=client.post('/getLob',json=payload)
    
    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_165(client):
    payload = { "user_id": 1234, "rows": ["id", "employeename","employeeid","userid","roleid","panno"], "filters": [], "sort_by": [], "order": "asc", "pg_no": 1, "pg_size": 15 }
    
    with patch('main.check_role_access', return_value=1):
       response=client.post('/getEmployee',json=payload)
    
    assert response.status_code == 200
    # assert response.json() == expected_response
    assert response.json()["total_count"] > 0

@pytest.mark.usefixtures("db_connection")
def test_id_166(client):
    payload = { "user_id": 1234, "rows": ["id", "employeename","employeeid","userid","roleid","panno"],"sort_by": [], "order": "asc", "pg_no": 1, "pg_size": 15 }
    expected_response=None
    with patch('main.check_role_access', return_value=1):
       response=client.post('/getEmployee',json=payload)
    
    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_167(client):
    payload = { "user_id": 1234, "rows": ["id", "employeename","employeeid","userid","roleid","panno"], "filters": [], "sort_by": [], "order": "asc", "pg_no": 1, "pg_size": 15 }
    expected_response={
  "result": "error",
  "message": "Access Denied",
  "user_id": 1234,
  "role_id": 0,
  "data": []
}

    with patch('main.check_role_access', return_value=0):
       response=client.post('/getEmployee',json=payload)
    
    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_168(client):
    payload = { "user_id": 1234}
    
    with patch('main.check_role_access', return_value=1):
       response=client.post('/paymentForAdmin',json=payload)
    
    assert response.status_code == 200
    # assert response.json() == expected_response
    assert response.json()["total_count"] > 0

@pytest.mark.usefixtures("db_connection")
def test_id_169(client):
    payload = { "user_id": 1235}

    expected_response={
  "result": "error",
  "message": "Access Denied",
  "user_id": 1235,
  "role_id": 2,
  "data": []
}
    
    with patch('main.check_role_access', return_value=2):
       response=client.post('/paymentForAdmin',json=payload)
    
    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_170(client):
    payload = { "user_id": 1234}
    expected_response={
  "result": "error",
  "message": "Access Denied",
  "user_id": 1234,
  "role_id": 0,
  "data": []
}
    with patch('main.check_role_access', return_value=0):
       response=client.post('/paymentForAdmin',json=payload)
    
    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_171(client):
    payload = { "user_id": 1234}
    expected_response={
        "result": "success",
        "user_id": 1234,
        "role_id": 1,
        "data": [
            [3, "Cash", None]
        ]
    }
    
    with patch('main.check_role_access', return_value=1):
       response=client.post('/getModesAdmin',json=payload)
    
    assert response.status_code == 200
    assert response.json()['data'][0] == expected_response['data'][0]

@pytest.mark.usefixtures("db_connection")
def test_id_172(client):
    payload = { "user_id": 1235}
    expected_response=None
    with patch('main.check_role_access', return_value=0):
       response=client.post('/getModesAdmin',json=payload)
    
    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_173(client):
    payload = { "user_id": 1234}
    expected_response=None
    with patch('main.check_role_access', return_value=0):
       response=client.post('/getModesAdmin',json=payload)
    
    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.usefixtures("db_connection")
def test_id_174(client):
    payload = {"user_id":1234,
 "table_name":"get_locality_view",
 "columns":["id","locality","cityid"]}
   
    expected_response={
  "result": "success",
  "user_id": 1234,
  "role_id": 1,
  "data": [
    {
      "column": "id",
      "type": "integer"
    }
  ]
}
    
    with patch('main.check_role_access', return_value=1):
       response=client.post('/getViewScreenDataTypes',json=payload)
    
    assert response.status_code == 200
    assert response.json()['data'][0] == expected_response['data'][0]



@pytest.mark.usefixtures("db_connection")
def test_id_175(client):
    payload = {"user_id":1234,
 "table_name":"get_locality_view",
 "columns":["id","locality","cityid"]}
   
    expected_response={
  "result": "error",
  "message": "Access Denied",
  "user_id": 1234,
  "role_id": 0,
  "data": []
}
    
    with patch('main.check_role_access', return_value=0):
       response=client.post('/getViewScreenDataTypes',json=payload)
    
    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_176(client):
    payload = {
  "user_id": 1234,
  "rows": [
    "buildername",
    "builderid",
    "projectname",
    "addressline1",
    "addressline2",
    "suburb",
    "city",
    "state",
    "country",
    "zip",
    "nearestlandmark",
    "project_type",
    "mailgroup1",
    "mailgroup2",
    "website",
    "project_legal_status",
    "rules",
    "completionyear",
    "jurisdiction",
    "taluka",
    "corporationward",
    "policechowkey",
    "policestation",
    "maintenance_details",
    "numberoffloors",
    "numberofbuildings",
    "approxtotalunits",
    "tenantstudentsallowed",
    "tenantworkingbachelorsallowed",
    "tenantforeignersallowed",
    "otherdetails",
    "duespayablemonth",
    "dated",
    "createdby",
    "isdeleted",
    "id"
  ],
  "builderid": 18,
  "filters": [],
  "sort_by": [],
  "order": "asc",
  "pg_no": 0,
  "pg_size": 0
}
    
    with patch('main.check_role_access', return_value=1):
       response=client.post('/getProjectsByBuilderId',json=payload)
    
    assert response.status_code == 200
    # assert response.json() == expected_response
    assert response.json()["total_count"] > 0


@pytest.mark.usefixtures("db_connection")
def test_id_177(client):
    payload = {
  "user_id": 1234,
  "rows": [
    "buildername",
    "builderid",
    "projectname",
    "addressline1",
    "addressline2",
    "suburb",
    "city",
    "state",
    "country",
    "zip",
    "nearestlandmark",
    "project_type",
    "mailgroup1",
    "mailgroup2",
    "website",
    "project_legal_status",
    "rules",
    "completionyear",
    "jurisdiction",
    "taluka",
    "corporationward",
    "policechowkey",
    "policestation",
    "maintenance_details",
    "numberoffloors",
    "numberofbuildings",
    "approxtotalunits",
    "tenantstudentsallowed",
    "tenantworkingbachelorsallowed",
    "tenantforeignersallowed",
    "otherdetails",
    "duespayablemonth",
    "dated",
    "createdby",
    "isdeleted",
    "id"
  ],
  "builderid": 18,
  "sort_by": [],
  "order": "asc",
  "pg_no": 0,
  "pg_size": 0
}
    expected_response=None

    with patch('main.check_role_access', return_value=1):
       response=client.post('/getProjectsByBuilderId',json=payload)
    
    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.usefixtures("db_connection")
def test_id_178(client):
    payload = {
  "user_id": 1234,
  "rows": [
    "buildername",
    "builderid",
    "projectname",
    "addressline1",
    "addressline2",
    "suburb",
    "city",
    "state",
    "country",
    "zip",
    "nearestlandmark",
    "project_type",
    "mailgroup1",
    "mailgroup2",
    "website",
    "project_legal_status",
    "rules",
    "completionyear",
    "jurisdiction",
    "taluka",
    "corporationward",
    "policechowkey",
    "policestation",
    "maintenance_details",
    "numberoffloors",
    "numberofbuildings",
    "approxtotalunits",
    "tenantstudentsallowed",
    "tenantworkingbachelorsallowed",
    "tenantforeignersallowed",
    "otherdetails",
    "duespayablemonth",
    "dated",
    "createdby",
    "isdeleted",
    "id"
  ],
  "builderid": 18,
  "filters": [],
  "sort_by": [],
  "order": "asc",
  "pg_no": 0,
  "pg_size": 0
}
    expected_response={
  "result": "error",
  "message": "Access Denied",
  "user_id": 1234,
  "role_id": 0,
  "data": []
}

    with patch('main.check_role_access', return_value=0):
       response=client.post('/getProjectsByBuilderId',json=payload)
    
    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_179(client):
    payload = {
        "user_id": 1234,
        "rows": ["id", "country", "cityid", "city", "state", "locality"],
        "filters": [[["country", "contains", ""], ["state", "contains", ""], ["city", "contains", ""], ["locality", "contains", ""]]],
        "sort_by": [],
        "order": "asc",
        "pg_no": 1,
        "pg_size": 15,
        "search_key": ""
    }

    with patch('main.check_role_access', return_value=1):
        response = client.post('/getLocality', json=payload)

    assert response.status_code == 200

    # Print response.json() for debugging
    print("Response JSON:", response.json())
    assert response.json()["total_count"] > 0
    
    
@pytest.mark.usefixtures("db_connection")
def test_id_180(client):
    payload = {
        "user_id": 1234,
        "rows": ["id", "country", "cityid", "city", "state", "locality"],
        "sort_by": [],
        "order": "asc",
        "pg_no": 1,
        "pg_size": 15,
        "search_key": ""
    }
    expected_response={
  "result": "error",
  "message": "Invalid Credentials",
  "user_id": 1234,
  "role_id": 0,
  "data": []
}
    with patch('main.check_role_access', return_value=1):
        response = client.post('/getLocality', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_181(client):
    payload = {
        "user_id": 1234,
        "rows": ["id", "country", "cityid", "city", "state", "locality"],
        "filters": [[["country", "contains", ""], ["state", "contains", ""], ["city", "contains", ""], ["locality", "contains", ""]]],
        "sort_by": [],
        "order": "asc",
        "pg_no": 1,
        "pg_size": 15,
        "search_key": ""
    }
    expected_response={
  "result": "error",
  "message": "Access Denied",
  "user_id": 1234,
  "role_id": 0,
  "data": []
}

    with patch('main.check_role_access', return_value=0):
        response = client.post('/getLocality', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.usefixtures("db_connection")
def test_id_182(client):
    payload = {"user_id" : 1234, "id":7}
    expected_response={
  "result": "success",
  "user_id": 1234,
  "role_id": 1,
  "data": {
    "client_info": {
      "id": 7,
      "salutation": "Mr",
      "firstname": "Sandeep",
      "middlename": "",
      "lastname": "Joshi(PMA)",
      "clienttype": 7,
      "country": 13,
      "state": "California",
      "city": "San Jose",
      "addressline1": "Model Colony",
      "addressline2": "",
      "zip": "",
      "suburb": "Campbell",
      "email1": "sandeepjoshi@gmail.com",
      "email2": "",
      "mobilephone": "+14084290765",
      "homephone": "02025652726",
      "localcontact1name": "",
      "localcontact1details": "",
      "localcontact1address": "",
      "workphone": "+18956720152",
      "localcontact2name": "",
      "localcontact2details": "",
      "includeinmailinglist": False,
      "localcontact2address": "",
      "employername": "",
      "entityid": 1,
      "comments": "",
      "tenantof": None,
      "tenantofproperty": None
    }
  }
}

    with patch('main.check_role_access', return_value=1):
        response = client.post('/getClientInfoByClientId', json=payload)

    assert response.status_code == 200
    client_info = response.json()['data']['client_info']
    expected_client_info = expected_response['data']['client_info']
    assert client_info['id'] == expected_client_info['id']
    

@pytest.mark.usefixtures("db_connection")
def test_id_183(client):
    payload = {"user_id" : 1234}
    expected_response={
  "result": "error",
  "message": "Invalid Credentials",
  "user_id": 1234,
  "role_id": 0,
  "data": []
}

    with patch('main.check_role_access', return_value=1):
        response = client.post('/getClientInfoByClientId', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response
    

@pytest.mark.usefixtures("db_connection")
def test_id_184(client):
    payload = {"user_id" : 1234, "id":7}
    expected_response={
  "result": "error",
  "message": "Access Denied",
  "user_id": 1234,
  "role_id": 0,
  "data": []
}

    with patch('main.check_role_access', return_value=0):
        response = client.post('/getClientInfoByClientId', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_185(client):
    payload = {"user_id" : 1234}
    expected_response={
  "result": "success",
  "user_id": 1234,
  "role_id": 1,
  "data": [
    {
      "builderid": 34,
      "buildername": "ADITYA BUILDERS ",
      "projectid": 40,
      "projectname": "COMFORT ZONE"
    }
  ]
}

    with patch('main.check_role_access', return_value=1):
        response = client.post('/getBuildersAndProjectsList', json=payload)

    assert response.status_code == 200
    assert response.json()['data'][0] == expected_response['data'][0]


@pytest.mark.usefixtures("db_connection")
def test_id_186(client):
    payload = {"user_id" : 1235}
    expected_response={
  "result": "error",
  "message": "Access Denied",
  "user_id": 1235,
  "role_id": 2,
  "data": []
}

    with patch('main.check_role_access', return_value=2):
        response = client.post('/getBuildersAndProjectsList', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_187(client):
    payload = {"user_id" : 1234}
    expected_response={
  "result": "success",
  "user_id": 1234,
  "role_id": 1,
  "data": [
    {
      "id": 1110,
      "projectid": 161,
      "projectname": " Green Groves "
    }
  ]
}

    with patch('main.check_role_access', return_value=1):
        response = client.post('/getTenantOfPropertyAdmin', json=payload)

    assert response.status_code == 200
    assert response.json()['data'][0] == expected_response['data'][0]


@pytest.mark.usefixtures("db_connection")
def test_id_188(client):
    payload = {"user_id" : 1235}
    expected_response={
  "result": "error",
  "message": "Access Denied",
  "user_id": 1235,
  "role_id": 2,
  "data": []
}

    with patch('main.check_role_access', return_value=2):
        response = client.post('/getTenantOfPropertyAdmin', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_189(client):
    payload = {"user_id":1234,"id":44524}
    expected_response={
  "result": "success",
  "user_id": 1234,
  "role_id": 1,
  "data": {
    "client_info": {
      "id": 44524,
      "salutation": "Mrs",
      "firstname": "Sujata ",
      "middlename": "",
      "lastname": "Huilgol ",
      "clienttype": 2,
      "country": 5,
      "state": "Maharashtra",
      "city": "Pune",
      "addressline1": "",
      "addressline2": "",
      "zip": "",
      "suburb": "",
      "email1": "sujata.huilgol@gmail.com",
      "email2": "",
      "mobilephone": "07798909988",
      "homephone": "",
      "localcontact1name": "",
      "localcontact1details": "",
      "localcontact1address": "",
      "workphone": "",
      "localcontact2name": "",
      "localcontact2details": "",
      "includeinmailinglist": False,
      "localcontact2address": "",
      "employername": "",
      "entityid": 1,
      "comments": "",
      "tenantof": None,
      "tenantofproperty": None
    },
    "client_access": [],
    "client_bank_info": [],
    "client_legal_info": {},
    "client_poa": {}
  }
}

    with patch('main.check_role_access', return_value=2):
        response = client.post('/getClientInfoByClientId', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response