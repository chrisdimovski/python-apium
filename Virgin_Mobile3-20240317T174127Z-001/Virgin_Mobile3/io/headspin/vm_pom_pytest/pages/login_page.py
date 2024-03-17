import time
from time import sleep
from appium.webdriver.common.mobileby import MobileBy

from lib import kpi_names
from lib.hs_logger import logger

from pages.base_page import BasePage
from pages.home_page import HomePage

###############################################################################################################
################################################### Android ###################################################
###############################################################################################################

class LoginPage(BasePage):

	def __init__(self, driver, session_data):
		super().__init__(driver, session_data)

		self.email_box = (MobileBy.XPATH,'//android.widget.EditText[@resource-id="com.virginmobile.uae:id/edit_email"]')
		self.login_btn = (MobileBy.ID,'com.virginmobile.uae:id/btn_next')
		self.welcome_back = (MobileBy.XPATH,'//android.widget.TextView[@text="Welcome back!"]') #Welcome back
		self.weltext = (MobileBy.ID,'com.virginmobile.uae:id/label_email') #read text to see email 
		self.password = (MobileBy.XPATH,'//android.widget.EditText[@resource-id="com.virginmobile.uae:id/edit"]') # passwordbox Abcabc123
		self.signin = (MobileBy.ID,'com.virginmobile.uae:id/btn_sign_in') #continue.Sign in
		self.setting = (MobileBy.ACCESSIBILITY_ID,'Open navigation drawer')
		self.try_again = (MobileBy.XPATH,'//*[@text="TRY AGAIN"]')


# Login Page Confirmation
	def confirm_login_page(self):
		self.session_data.status="Fail_to_confirm_login_page"
		self.wait_for(self.email_box)
		sleep(1)
		self.session_data.kpi_labels[kpi_names.LOGIN_PAGE_LOAD_TIME]['end'] = int(round(time.time() * 1000))
		logger.info("Login Page Confirmed")
		self.session_data.pass_count += 1

# Login to Home page
	def login_to_home_page(self): 
		self.session_data.status = "Fail_to_login"
		self.testmail,self.testpassword1,self.testpassword2=self.session_data.hs_api_call.read_csv()
		self.send_keys(self.email_box,self.testmail)
		logger.info(f'Entered email : {self.testmail}')
		self.click_element(self.login_btn)
		self.wait_for(self.welcome_back)
		user=self.wait_for(self.weltext)
		assert user.text==self.testmail

		self.send_keys(self.password,self.testpassword1)
		logger.info(f'Entered Password : {self.testpassword1}')
		sleep(1)

		HomePageObject = HomePage.instance(self.driver, self.session_data)
		self.session_data.kpi_labels[kpi_names.HOME_PAGE_LOAD_TIME]['start'] = int(round(time.time() * 1000))
		self.click_element(self.signin)

		if self.wait_for_visibility(self.try_again,5):
			self.click_element(self.try_again)
			self.wait_for(self.password)
			self.clear_field(self.password)
			self.send_keys(self.password,self.testpassword2)
			self.click_element(self.signin) 
			self.session_data.hs_api_call.update_password()    
		
		HomePageObject.confirm_home_page()
		logger.info('Login successfully')
		return HomePageObject


###############################################################################################################
##################################################### iOS #####################################################
###############################################################################################################

class LoginPageIOS(BasePage):

	def __init__(self, driver, session_data):
		super().__init__(driver, session_data)