from fastapi.testclient import TestClient
from ..lecture33 import app

client = TestClient(app)

def test_read_item():
    response = client.get("/items/foo", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 200
    assert response.json() == {
        "id": "foo",
        "title": "Foo",
        "description": "There goes my hero"
    }

"""
"assert" keyword validates code conditions and assumptions.
It checks program execution circumstances. 
The "assert" statement accepts boolean expressions that evaluate to True or False. 
If the expression is True, the program runs uninterrupted.
"""

# pip install mock before running pytest
# run the following command on terminal:
# pytest test_main.py
# we can run simply 'pytest' as well, but it will test all the files and folders present in the current directory

def test_read_item_bad_token():
    response = client.get("/items/foo", headers={"X-Token": "wrong"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}

def test_read_inexistent_item():
    response = client.get("/items/baz", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}

def test_create_item():
    response = client.post(
        "/items/",
        json={"id": "foobar","title": "Foo Bar", "description": "The Foo Bartender"},
        headers={"X-Token": "coneofsilence"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": "foobar",
        "title": "Foo Bar",
        "description": "The Foo Bartender"
    }

def test_create_item_bad_token():
    response = client.post(
        "/items/",
        headers={"X-Token": "badheader"},
        json={"id": "bazz","title": "Bazz", "description": "Drop the bazz"}
    )   
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}
 
def test_create_existing_item():
    response = client.post(
        "/items/",
        headers={"X-Token": "coneofsilence"},
        json={"id": "foo","title": "Bazz", "description": "Drop the bazz"}
    )   
    assert response.status_code == 400
    assert response.json() == {"detail": "Item already exists"}
     
# now run 'pytest test_main.py'
# we will see that all of our tests passed

# if we purposely rewrite one of the tests like this:
def test_create_existing_item():
    response = client.post(
        "/items/",
        headers={"X-Token": "coneofsilence"},
        json={"id": "foo","title": "Bazz", "description": "Drop the bazz"}
    )   
    assert response.status_code == 401   # it should be 400 and not 401
    assert response.json() == {"detail": "Item already exists"}

# now if we run 'pytest test_main.py', we will get one test failed along with other information.
# ......F (6 tests passed and final(1) test failed)

# go back to lecture33.py