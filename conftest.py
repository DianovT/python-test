from fixture.application import Application
from fixture.db import DbFixture
from fixture.orm import ORMfixture
import pytest
import json
import os.path
import importlib
import jsonpickle


fixture = None
target = None

def load_config(file):
    global target
    if target is None:
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(config_file) as f:
            target = json.load(f)
    return target

@pytest.fixture
def app(request):
    global fixture
    global target
    browser = request.config.getoption("--browser")
    web_config = load_config(request.config.getoption("--target"))['web']
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, base_url=web_config['baseUrl'])
    fixture.session.insure_login(username=web_config['username'], password=web_config['password'])
    return fixture

@pytest.fixture(scope="session")
def db(request):
    db_config = load_config(request.config.getoption("--target")) ['db']
    dbfixture = DbFixture(host=db_config['host'], name=db_config['name'], user=db_config['user'],password=db_config['password'])
    def fin():
        dbfixture.destroy()
    request.addfinalizer(fin)
    return dbfixture


@pytest.fixture(scope="session")
def orm(request):
    db_config = load_config(request.config.getoption("--target"))["db"]
    db_orm_fixture = ORMfixture(host=db_config["host"], name=db_config["name"], user=db_config["user"], password=db_config["password"])
    return db_orm_fixture


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="firefox")
    parser.addoption("--target", action="store", default="target.json")
    parser.addoption("--check_ui", action="store_true")


def pytest_generate_tests(metafunc):
    for fixture in metafunc.fixturenames:
        if fixture.startswith("data_"):
            testdate = load_from_module(fixture[5:])
            metafunc.parametrize(fixture, testdate, ids=[str(x) for x in testdate])
        elif fixture.startswith("json_"):
            testdate = load_from_json(fixture[5:])
            metafunc.parametrize(fixture, testdate, ids=[str(x) for x in testdate])


def load_from_module(module):
    return importlib.import_module("data.%s" % module).testdate

def load_from_json(file):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/%s.json" % file)) as file_json:
        return jsonpickle.decode(file_json.read())


@pytest.fixture(scope="session", autouse=True)
def stop(request):
    def fin():
        fixture.session.insure_logout()
        fixture.destroy()
    request.addfinalizer(fin)
    return fixture

@pytest.fixture
def check_ui(request):
    return request.config.getoption("--check_ui")





