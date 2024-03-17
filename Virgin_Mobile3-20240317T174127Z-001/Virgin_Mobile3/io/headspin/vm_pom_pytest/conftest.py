import pytest
import sys
import time
import logging
import json
import os
import requests
import sys
from appium import webdriver
import warnings

@pytest.fixture(autouse=True)
def suppress_deprecation_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)

root_dir = os.path.dirname(__file__)
lib_dir = os.path.join(root_dir, 'lib')
pages_dir = os.path.join(root_dir, 'pages')
sys.path.append(lib_dir)
sys.path.append(pages_dir)

from hs_api import hsApi
from args_lib import addoption, init_args, device_state_var
import vm_lib
from hs_logger import logger, setup_logger
import session_visual_lib

from pages.launch_page import LaunchPage

setup_logger(logger, logging.DEBUG)
session_data = None
driver = None

# Command line args 
def pytest_addoption(parser):
    addoption(parser)
  
# Read data from sensitivity.json
def read_sensitivity(session_data):
    cur = os.getcwd()
    actualdir = os.path.join(cur,'sensitivity.json')
    if not os.path.exists(actualdir):
        logger.info("Doesn't contain sensitivity file...")
        exit()
    else:
        with open(actualdir,'r') as file:
            data_load = json.load(file)
            my_dict = dict(data_load)
            session_data.data = my_dict.get(session_data.test_name).get(session_data.udid,my_dict.get(session_data.test_name).get("default"))

# Preporcessing method with headspin api     
def init_vars(driver, session_data): 
    session_data.session_id = driver.session_id
    r = driver.session
    session_data.udid = r['udid']
    session_data.status = "Fail_creating_hs_api_object"
    
    session_data.hs_api_call = hsApi(session_data.udid, session_data.access_token)
    if driver.capabilities['platformName'].lower() =="android":
        device_model = r['deviceModel']
    else:
        device_model = r['device']
    logger.info(f'Running test on {device_model} : {session_data.udid}') 


    session_data.status = "Fail_fetch_app_version"
    device_state_var(session_data)

#Driver creation & initial setup         
@pytest.fixture
def driver(request):
    global session_data, driver
    session_data = request.cls()
    request.cls.session_data = session_data

    session_data = init_args(request, session_data)
    vm_lib.init_timing(session_data)

# Log Desired Capability for debugging
    debug_caps = session_data.desired_caps
    logger.info('debug_caps:\n'+json.dumps(debug_caps))
    session_data.status = "Fail_creating_driver"
    driver = webdriver.Remote(
                command_executor=session_data.url,
                desired_capabilities=session_data.desired_caps
                ,strict_ssl=False
            )
    logger.info("Driver created")

    session_data.session_id = driver.session_id
    logger.info("Session Id : "+str(session_data.session_id))
    read_sensitivity(session_data)
    yield driver
    tearDown(session_data,driver)

# Convert the long url into short readable url
def shorten_url(url_long):
    URL = "http://tinyurl.com/api-create.php"
    try:
        url = URL + "?" \
            + urllib.parse.urlencode({"url": url_long})
        res = requests.get(url)
        return res.text
    except Exception as e:
        raise

# Postprocessing method (Integrated with headspin api)
def tearDown(self, driver):
    print("")
    non_time_kpis = {}

    if self.session_data.pass_count==self.KPI_COUNT:
        self.status="Pass"
    self.fail_count = self.KPI_COUNT - self.pass_count
    logger.info(self.status)
    logger.info(f"Pass count : {self.pass_count}")
    logger.info(f"Fail count : {self.fail_count}")

#Capture failed screenshot
    if self.status!="Pass":
        
        try:
            self.screenshotBase64 = driver.get_screenshot_as_base64()
            if(driver.capabilities['platformName'].lower() =="android"):
                screenshot_url = self.hs_api_call.get_screenshot_url()
                screenshot_url_short = shorten_url(screenshot_url)
                logger.info(f'URL Screenshot link: {screenshot_url_short}')
                non_time_kpis['screenshot_url_short'] = screenshot_url_short
            else:
                screenshot_url = self.hs_api_call.get_screenshot_url_ios()
                screenshot_url_short = shorten_url(screenshot_url)
                logger.info(f'URL Screenshot link: {screenshot_url_short}')
                non_time_kpis['screenshot_url_short'] = screenshot_url_short
        except:
            self.screenshotBase64 = None
        logger.error("Got exception in main handler")
        print("")


    try:
        driver.quit()
    except: 
        pass
    time.sleep(3)
    
# Post processing start
    if self.use_capture:
        try:
            session_visual_lib.run_record_session_info(self,non_time_kpis,kpi_tags=True)
        except Exception as e:
            logger.info(e)
            logger.exception("Got exception in post processing")


#App launching 
@pytest.fixture
def launch(driver): 
    global session_data
    init_vars(driver, session_data) 
    LaunchPageObject = LaunchPage.instance(driver, session_data)
    logger.info("Starting test")
    LaunchPageObject.app_launch()
    return LaunchPageObject