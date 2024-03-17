import time
from time import sleep
from appium.webdriver.common.mobileby import MobileBy

from lib import kpi_names
from lib.hs_logger import logger

from base_page import BasePage
from pages.login_page import LoginPage

###############################################################################################################
################################################### Android ###################################################
###############################################################################################################

class LaunchPage(BasePage):

	def __init__(self, driver, session_data):
		super().__init__(driver, session_data)
		self.login_button = (MobileBy.XPATH, '//android.widget.Button[@text="LOGIN"]')
		self.email_box = (MobileBy.XPATH,'//android.widget.EditText[@resource-id="com.virginmobile.uae:id/edit_email"]')
		self.back = (MobileBy.ACCESSIBILITY_ID,"Back")
		self.kill_app()
  
# Launch the app 
	def app_launch(self):
		self.session_data.status = "Fail_app_launch"
		self.session_data.kpi_labels[kpi_names.LAUNCH_TIME]['start'] = int(round(time.time() * 1000))
		self.start_app()
		self.confirm_app_launch()
		self.session_data.pass_count += 1
  
# Launch verification
	def confirm_app_launch(self):
		self.session_data.status="Fail_to_confirm_app_launch"
		self.wait_for(self.login_button)
		self.session_data.kpi_labels[kpi_names.LAUNCH_TIME]['end'] = int(round(time.time() * 1000))
		logger.info("App launched")
		try:
			self.wait_for(self.email_box,10)
			self.click_element(self.back)
		except:
			pass
		
# Navigate to Login page 
	def go_to_login_page(self):
		self.session_data.status="Fail_to_navigate_to_login_page"
		LoginPageObject = LoginPage.instance(self.driver, self.session_data)
		sleep(2)
		self.session_data.kpi_labels[kpi_names.LOGIN_PAGE_LOAD_TIME]['start'] = int(round(time.time() * 1000))
		self.click_element(self.login_button)
		LoginPageObject.confirm_login_page()
		return LoginPageObject


###############################################################################################################
##################################################### iOS #####################################################
###############################################################################################################

class LaunchPageIOS(BasePage):
	def __init__(self, driver, session_data):
		super().__init__(driver, session_data)