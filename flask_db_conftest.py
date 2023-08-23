import sys
import os
import pytest
import json


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.sqlite_rx_connector import database_query  # noqa: E402
from config import load_config_webserver  # noqa: E402


KONFUZIO_ID = os.environ.get('PROJECT_ID')
USER1 = "oleksandra@domen.com"
USER2 = "second_user@post.de"
REVIEWER1_TIME = "2023-09-01 14:30:00"
REVIEWER2_TIME = "2023-09-02 17:00:00"

INSERT_QUERY = (
            "INSERT INTO table ("
            "id, reviewer1, reviewer1_time, reviewer2, reviewer2_time, to_update"
            ") VALUES ("
            ":id, :reviewer1, :reviewer1_time, :reviewer2, :reviewer2_time, :to_update);"
        )

DELETE_QUERY = (
            "DELETE FROM table WHERE id = :id;"
        )


@pytest.fixture(scope="session")
def test_app():
    """
    Fixture that provides the Flask application object for testing.

    This fixture imports the webserver module, loads the configuration file,
    and sets the web server configuration in the application object. It then
    returns the application object for testing.

    Returns:
        app (Flask): The Flask application object for testing.
    """
    from webserver import app

    path_to_ini_file = os.path.join(
        os.path.dirname(__file__), "..", "webserver_unittest.ini"
    )
    path_to_ini_file = os.path.normpath(path_to_ini_file)
    webserver_config = load_config_webserver(path_to_ini_file)
    app.config["WEB_SERVER_CONFIG"] = webserver_config
    # print(f"Path to ini file: {path_to_ini_file}")
    print(f"app: {app}")
    return app


@pytest.fixture
def client(test_app):
    """
    Fixture that provides a test client for making requests to the Flask application.

    This fixture depends on the 'test_app' fixture to get the Flask application object.
    It returns a test client that can be used to make requests to the application during testing.

    The test client makes requests to the application without running a live server.
    The client has methods that match the common HTTP request methods,
    such as client.get() and client.post().

    Args:
        test_app (Flask): The Flask application object for testing.

    Returns:
        client (FlaskClient): A test client for making requests to the Flask application.
    """
    return test_app.test_client()


@pytest.fixture(scope="session")
def db_url(test_app):
    """
    Fixture that provides the database URL for testing.

    This fixture depends on the 'test_app' fixture to get the Flask application object.
    It retrieves the database URL from the application configuration and returns it for testing.

    Args:
        test_app (Flask): The Flask application object for testing.

    Returns:
        db_url (str): The URL of the database for testing.
    """
    db_url = test_app.config["WEB_SERVER_CONFIG"].database_service.base_url
    print(f"Working with TEST DB: {db_url}")
    return db_url


@pytest.fixture
def mock_data_no_reviewers(request, test_app, db_url):
    """
    Fixture to add mock data from multiple JSON files to the test database
    and delete them after tests finish.

    The process of creating and deleting known records will be repeated
    for every test function that requires fixture.
    This ensures that each test function starts with a clean and consistent state,
    preventing any interference or dependencies between tests.
    """
    # List of JSON files
    json_files = ["NOREW0000001.json",
                  "NOREW0000002.json",
                  "NOREW0000003.json"]
    added_records = []

    for json_file in json_files:
        json_path = os.path.join(os.path.dirname(__file__), "mocks", json_file)

        with open(json_path, "r") as json_file:
            data = json.load(json_file)

            params = {
                "id": data["id"],
                "reviewer1": None,
                "reviewer1_time": None,
                "reviewer2": None,
                "reviewer2_time": None,
                "to_update": None
            }

            # Add data to the database
            database_query(db_url, INSERT_QUERY, params)
            # Store the identifier for deletion later
            added_records.append(data['id'])

    def finalize():
        # Delete the added records from the database when tests finish
        for idin added_records:
            params = {
                "id": id}
            database_query(db_url, DELETE_QUERY, params)

    request.addfinalizer(finalize)
    return added_records


@pytest.fixture
def mock_data_one_reviewer(request, test_app, db_url):
    """
    Fixture to add mock data from multiple JSON files to the test database
    and delete them after tests finish.
    """
    # List of JSON files
    json_files = ["ONEREW000001.json",
                  "ONEREW000002.json",
                  "ONEREW000003.json"]
    added_records = []

    for json_file in json_files:
        json_path = os.path.join(os.path.dirname(__file__), "mocks", json_file)

        with open(json_path, "r") as json_file:
            data = json.load(json_file)

            params = {
                "id": data["id"],
                "reviewer1": USER1,
                "reviewer1_time": REVIEWER1_TIME,
                "reviewer2": None,
                "reviewer2_time": None,
                "to_update": None
            }

            # Add data to the database
            database_query(db_url, INSERT_QUERY, params)
            # Store the identifier for deletion later
            added_records.append(data['id'])

    def finalize():
        # Delete the added records from the database when tests finish
        for id in added_records:
            params = {
                "id": id}
            database_query(db_url, DELETE_QUERY, params)

    request.addfinalizer(finalize)
    return added_records


@pytest.fixture
def mock_data_both_reviewers(request, test_app, db_url):
    """
    Fixture to add mock data from multiple JSON files to the test database
    and delete them after tests finish.

    The process of creating and deleting known records will be repeated
    for every test function that requures fixture.
    This ensures that each test function starts with a clean and consistent state,
    preventing any interference or dependencies between tests.
    """

    # List of JSON files
    json_files = ["BOTHREW00001.json",
                  "BOTHREW00002.json",
                  "BOTHREW00003.json"]
    added_records = []

    for json_file in json_files:
        json_path = os.path.join(os.path.dirname(__file__), "mocks", json_file)

        with open(json_path, "r") as json_file:
            data = json.load(json_file)

            params = {
                "id": data["id"],
                "reviewer1": USER1,
                "reviewer1_time": REVIEWER1_TIME,
                "reviewer2": USER2,
                "reviewer2_time": REVIEWER2_TIME,
                "to_update": None
            }

            # Add data to the database
            database_query(db_url, INSERT_QUERY, params)
            # Store the identifier for deletion later
            added_records.append(data['id'])

    def finalize():
        # Delete the added records from the database when tests finish
        for id in added_records:
            params = {
                "id": id}
            database_query(db_url, DELETE_QUERY, params)

    request.addfinalizer(finalize)
    return added_records


@pytest.fixture
def user1():
    return USER1


@pytest.fixture
def user2():
    return USER2


@pytest.fixture
def reviewer1_data():
    return USER1, REVIEWER1_TIME


@pytest.fixture
def reviewer2_data():
    return USER2, REVIEWER2_TIME
