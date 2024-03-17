from __future__ import absolute_import
from __future__ import print_function
import time
from device_info import DeviceInfo
from hs_logger import logger

# Fetch data from the terminal
def addoption(parser):
	parser.addoption('--udid', '--udid', dest='udid',
						type=str, nargs='?',
						default=None,
						required=True,
						help="udid")
	parser.addoption('--appium_input', '--appium_input', dest='appium_input',
						type=str, nargs='?',
						default=None,
						required=True,
						help="appium_input")
	parser.addoption('--os', '--os', dest='os',
						type=str, nargs='?',
						default=None,
						required=True,
						help="os")
	parser.addoption('--network_type', '--network_type', dest='network_type',
						type=str, nargs='?',
						default="MOBILE",
						required=True,
						help="network_type")
	parser.addoption('--no_reset', '--no_reset', dest='no_reset',
						type=str, nargs='?',
						default="False",
						required=False,
						help="no_reset")
	parser.addoption('--auto_launch', '--auto_launch', dest='auto_launch',
						type=str, nargs='?',
						default="False",
						required=False,
						help="auto_launch")
	parser.addoption('--use_capture', '--use_capture', dest='use_capture',
						type=str, nargs='?',
						default="True",
						required=False,
						help="use_capture")
	parser.addoption('--video_only', '--video_only', dest='video_only',
						type=str, nargs='?',
						default="True",
						required=False,
						help="video_only")


# Read parser 
def init_args(request, session_data):

	# Set package and activity
	#Android
	session_data.package = "com.virginmobile.uae"
	session_data.activity = "com.virginmobile.uae.activity.IntroActivity"
 
	# iOS
	session_data.bundle_id = "com.virginmobile.uae"
	session_data.udid = request.config.getoption("udid")
	session_data.appium_input = request.config.getoption("appium_input")
	session_data.os = request.config.getoption("os")
 
	# Basic config
	session_data.network_type = request.config.getoption("network_type")
	session_data.no_reset = False if request.config.getoption("no_reset").lower() == "false" else True
	session_data.auto_launch = True if request.config.getoption("auto_launch").lower() == "true" else False
	session_data.use_capture = True if request.config.getoption("use_capture").lower() == "true" else False
	session_data.video_only = True if request.config.getoption("video_only").lower() == "true" else False
	session_data.url = session_data.appium_input
	session_data.access_token = session_data.url.split('/')[-3]
 
	if 'localhost' in session_data.url or '0.0.0.0' in session_data.url :
		session_data.running_on_pbox = True
	init_caps(session_data)
	return session_data  

# Set desired_caps accordingly
def init_caps(session_data):
	# desired caps for the app
	session_data.desired_caps = {}
	session_data.desired_caps['platformName'] = session_data.os
	session_data.desired_caps['newCommandTimeout'] = 320
	session_data.desired_caps["pageLoadStrategy"]= "none"
	session_data.desired_caps['udid'] = session_data.udid
	session_data.desired_caps['deviceName'] = session_data.udid
	
	# Android specific caps
	if session_data.os.lower() == "android":
		session_data.desired_caps['appPackage'] = session_data.package
		session_data.desired_caps['appActivity'] = session_data.activity
		session_data.desired_caps['automationName'] = "UiAutomator2"
		session_data.desired_caps['autoGrantPermissions'] = True
		
	# iOS specific caps
	elif session_data.os.lower() == "ios":
		session_data.desired_caps['automationName'] = "XCUITest"
		session_data.desired_caps['bundleId'] = session_data.bundle_id
		session_data.desired_caps['autoAcceptAlerts'] = False

	
	if not session_data.auto_launch:
		session_data.desired_caps['autoLaunch'] = False
	
	if session_data.no_reset:
		session_data.desired_caps['noReset'] = session_data.no_reset
	else:
		session_data.desired_caps['noReset'] = False

	# Headspin caps
	if session_data.use_capture:
		# starts capture at driver creation
		session_data.desired_caps['headspin:capture.autoStart'] = True
		if session_data.video_only:
			session_data.desired_caps['headspin:capture.video'] = True
			session_data.desired_caps['headspin:capture.network'] = False
		else:
			session_data.desired_caps['headspin:capture.video'] = True
			session_data.desired_caps['headspin:capture.network'] = True
	return session_data

# Get and Set device status of headspin device
def device_state_var(session_data):

	session_data.device_info = DeviceInfo(session_data.udid, session_data.access_token)
	session_data.connection_status = session_data.device_info.get_connection_type()
		
	# for android devices. using --network_type command line argument we can switch to mobile data or wifi
	if session_data.os.lower() == "android":
		if session_data.network_type not in session_data.connection_status:
			if 'WIFI' in session_data.network_type:
				session_data.hs_api_call.run_adb_command("svc wifi enable")
				logger.info("changing to WIFI")
				session_data.connection_status = "WIFI"

			else:
				session_data.hs_api_call.run_adb_command("svc wifi disable")
				logger.info("changing to MOBILE")
				session_data.connection_status = "MOBILE"

			time.sleep(3)

	# get app version
	try:
		session_data.apk_version = session_data.device_info.get_app_version(session_data.package)
		logger.info(f'App Version: {session_data.apk_version}')
	except Exception as error:
		logger.info(error)
		session_data.apk_version = None
		logger.info('Get apk_version Failed')