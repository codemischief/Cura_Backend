import pytest
import psycopg2
from fastapi import HTTPException
import logging
import bcrypt
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
    # ... (Add more assertions on data if needed)

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
    assert response.status_code == 200  # Or a different code for auth errors
    assert response.json() == {
        "result": "Error",
        "message": "Wrong input",
        "data": {}
    }

@pytest.mark.usefixtures("db_connection")
def test_id_15(client):
    payload={"user_id":1234,"country_name":"country"}

    expected_response={
         "result": "success",
        "user_id": 1234,
        "role_id": 1,
        "data": {
          "added": "country"
        }
    }
    with patch('main.check_role_access', return_value=1):
       response=client.post('/addCountry',json=payload)
    
    assert response.status_code == 200
    assert response.json() == expected_response

# @pytest.mark.usefixtures("db_connection")
# def test_add_country_failure_existing_country(client):
#     payload = {
#         'country_id': 104,  
#         'country_name': 'Pakistan', 
#         'user_id': 1234  
#     }

#     response = client.post('/addCountry', json=payload)

#     assert response.status_code == 200  
#     data = response.json()
#     assert data['result'] == 'error'
#     assert data['message'] == 'Country already exists'

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
def test_id_19(client):
    payload = {"user_id":1234,"old_country_name":"country", "new_country_name" : "edited_country"}

    expected_response={
  "result": "success",
  "user_id": 1234,
  "role_id": 1,
  "data": {
    "original": "country",
    "new country": "edited_country"
  }
}

    with patch('main.check_role_access', return_value=1):
       response=client.post('/editCountry',json=payload)
    
    assert response.status_code == 200
    assert response.json() == expected_response


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

# @pytest.mark.usefixtures("db_connection")
# def test_id_21(client, db_connection, monkeypatch):
#     # Pre-populate with a country and a user with an invalid role
#     with db_connection.cursor() as cursor:
#         cursor.execute("INSERT INTO country (id, name) VALUES (%s, %s)", (300, 'India')) 
#         cursor.execute("INSERT INTO usertable (id, roleid) VALUES (%s, %s)", (1234, 0))
#         db_connection.commit()

#     with patch('main.check_role_access', return_value=1):
#        response = client.put('/editCountry', json={
#         'old_country_name': 'India', 
#         'new_country_name': 'Bharat',
#         'user_id': 1234
#     })

#     assert response.status_code == 200 
#     data = response.json()
#     assert data['result'] == 'error'
#     assert data['message'] == 'Access Denied'

@pytest.mark.usefixtures("db_connection")
def test_id_22(client):
    payload = {"user_id":1234,"old_country_name":"country"}

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
def test_id_48(client):
    payload = {"user_id":1234,"country_name":"country"}

    expected_response={
  "result": "success",
  "user_id": 1234,
  "role_id": 1,
  "data": {
    "deleted": "country"
  }
}


    with patch('main.check_role_access', return_value=1):
       response=client.post('/deleteCountry',json=payload)
    
    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_49(client):
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
def test_id_52(client):
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

    expected_response = {
        "result": "success",
        "user_id": 1234,
        "role_id": 1,
        "data": {
            "Inserted Employee": "changed emp"
        }
    }

    with patch('main.check_role_access', return_value=1):  
        response = client.post('/addEmployee', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

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
def test_id_55(client):
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
        "result": "success",
        "user_id": 1234,
        "role_id": 1,
        "data": {
            "Updated Employee": "changed emp"
        }
    }

    with patch('main.check_role_access', return_value=1):
        response = client.post('/editEmployee', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

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
def test_id_58(client):
    payload = {"user_id":1234,"id": 129 }

    expected_response = {
  "result": "success",
  "user_id": 1234,
  "role_id": 1,
  "data": {
    "deleted_user": 129
  }
}

    with patch('main.check_role_access', return_value=1):
        response = client.post('/deleteEmployee', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

@pytest.mark.usefixtures("db_connection")
def test_id_59(client):
    payload = {"user_id":1234,"id": 100}

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


@pytest.mark.usefixtures("db_connection")
def test_id_59(client):
    payload = {"user_id":1234,"id": 129}

    expected_response = {
  "result": "error",
  "message": "No record exists",
  "user_id": 1234,
  "role_id":1,
  "data": []
}

    with patch('main.check_role_access', return_value=1):
        response = client.post('/deleteEmployee', json=payload)

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
def test_id_61(client):
    payload = {
        "user_id": 1234,
        "locality": "Test Locality",
        "cityid": 8111 
    }

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
def test_id_65(client):
    payload = {
        "user_id": 1234,
        "id": 45,
        "locality": "Locality132",
        "cityid": 8111
    }

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

# Test case for access denied scenario
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
        "message": "Access Denied",
        "user_id": 1235,
        "role_id": 2,
        "data":[]
    }

    response = client.post('/editLocality', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

# Test case for successful locality deletion
@pytest.mark.usefixtures("db_connection")
def test_id_68(client):
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

    with patch('main.check_role_access', return_value=1):
        response = client.post('/deleteLocality', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

# Test case for access denied scenario
@pytest.mark.usefixtures("db_connection")
def test_id_69(client):
    payload = {
        "user_id": 1235,
        "id": 45  
    }

    expected_response = {
        "result": "error",
        "message": "Access Denied",
        "user_id": 1235,
        "role_id": 0,
        "data": []
    }

    with patch('main.check_role_access', return_value=0):
        response = client.post('/deleteLocality', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response

# Test case for invalid credentials scenario
@pytest.mark.usefixtures("db_connection")
def test_id_70(client):
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
    with patch('main.check_role_access', return_value=2):
       response = client.post('/deleteLocality', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.usefixtures("db_connection")
def test_id_71(client):
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
    with patch('main.check_role_access', return_value=1):
       response=client.post('/addLob',json=payload)
    
    assert response.status_code == 200
    assert response.json() == expected_response

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
def test_id_74(client):
    payload={
    "user_id":1234,
    "old_name" : "lobname",
    "new_name" : "new_lobname"
}

    expected_response={
  "result": "success",
  "user_id": 1234,
  "role_id": 1,
  "data": {
    "edited_lob": "lobname"
  }
}

    

    with patch('main.check_role_access', return_value=1):
       response=client.post('/editLob',json=payload)
    
    assert response.status_code == 200
    assert response.json() == expected_response


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
def test_id_37(client):
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
def test_id_38(client):
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
def test_id_39(client):
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
def test_id_40(client):
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
  "result": "success",
  "user_id": 1234,
  "role_id": 1,
  "data": {
    "entered": "Rudra"
  },
  "total_count": {
    "entered": "Rudra"
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
