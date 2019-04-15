# -*- coding: utf-8 -*-

import pytest
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Used to suppress InsecureRequestWarning: Unverified HTTPS request is being made.
# Adding certificate verification is strongly advised.
# See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
import urllib3
urllib3.disable_warnings()

# list of known application acronym
KNOWN_APP_ACRONYMS = [
    "app1",  # example app 1
    "app2"   # example app 2
]

# list of known hosts to run tests against
KNOWN_HOSTS = ["local", "remote"]

# Add some runtime parsers to consume command line arguments
def pytest_addoption(parser):
    parser.addoption("--aut", action="store",
                     help="the app under test acronym used to help establish app specific environment variables")
    parser.addoption("--base_url", action="store",
                     help="the baseurl that is used for all apps - should be something like: 'http://my_app_example.com'")
    parser.addoption("--host", action="store", default="local", help="where to run your tests: local or remote")
    parser.addoption("--platform", action="store", default="WIN10",
                     help="the operating system to run your tests against specifically used in host=remote mode")
    parser.addoption("--machine_name", action="store", default="",
                     help="the specific machine name you want to execute tests against when in host=remote mode")

def is_value_empty_or_noneness(value_to_validate):
    if value_to_validate is None or value_to_validate == '' or str(value_to_validate).lower() == 'none':
        return True
    else:
	    return False

# parse and validate the command line options
@pytest.fixture
def cfg(request):
    # get and process the command line options
    aut = str(request.config.getoption("--aut")).lower()
    base_url = str(request.config.getoption("--base_url")).lower()
    host = str(request.config.getoption("--host")).lower()
    platform = str(request.config.getoption("--platform"))  # not lower() due to specific platform value set on the remote grid node machines being uppercase
    machine_name = str(request.config.getoption("--machine_name")).lower()
	
    # validate aut against KNOWN_APP_ACRONYMS
    if aut not in KNOWN_APP_ACRONYMS:
        raise AttributeError("unknown aut: '{0}', known --aut values: '{1}'".format(aut, KNOWN_APP_ACRONYMS))

    # validate host value is known
    if host not in KNOWN_HOSTS:
        raise AttributeError("unknown host: '{0}', known --host values: '{1}'".format(host, KNOWN_HOSTS))
		
    # validate base_url is not empty or none
    if is_value_empty_or_noneness(base_url):
        raise AttributeError("--base_url is required to not be empty or none")

    # get currently running test name
    test_name = request.node.name
	
    # set the se_hub url used for host=remote node
    se_hub = "http://localhost:4444/wd/hub"

    # set the admin_user, admin_pswd, exp_title value based on aut
    if aut == "app1": # example app1
        admin_user = "some_user"
        admin_pswd = "SuperSecret"
        exp_title = "Example App1"
    
    elif aut == "app2": # example app2
        admin_user = "another_user"
        admin_pswd = "AnotherSuperSecret"
        exp_title = "Example App2"

    else:  # unknown aut catch
        raise AttributeError("unknown aut: '{0}', known --aut values: '{1}'".format(aut, KNOWN_APP_ACRONYMS))

    # create opts dictionary
    opts = {
        "aut": aut,
        "base_url": base_url,
        "host": host,
        "platform": platform,
        "machine_name": machine_name,
        "admin_user": admin_user,
        "admin_pswd": admin_pswd,
        "exp_title": exp_title,
        "test_name": test_name,
		"se_hub": se_hub
    }

    return opts

@pytest.fixture
def driver(request, cfg):
    driver_ = None
    # create webdriver object based on host
    host = cfg['host']
    if host == "remote":
        
		# set capabilities so selenium grid knows about where to run test
        _desired_caps = {
            "browserName": "chrome",
            "platform": cfg['platform']
        }

        # set the desired capability to allow for specific remote node execution
        machine_name = cfg['machine_name']
        if machine_name != "":
            _desired_caps.update({"applicationName": machine_name})

        # driver object
        driver_ = webdriver.Remote(cfg['se_hub'], _desired_caps)

    elif host == "local":

        # driver object
        driver_ = webdriver.Chrome()

    else:  # unknown host catch
        raise ("unknown host: '{0}', known --host values: '{1}'".format(host, KNOWN_HOSTS))

    # needed to close out browser after test completes
    # pytest magic - addfinalizer
    def quit():
        driver_.quit()

    request.addfinalizer(quit)

    # this sets the window that was first established for better handles when switching windows or tabs, etc...
    cfg['orig_window_handle'] = driver_.current_window_handle

    # sets the session ID because driver object is not available everywhere
    cfg['se_session_id'] = driver_.session_id
 
    return driver_
