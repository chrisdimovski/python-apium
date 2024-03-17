import time
from time import sleep
from appium.webdriver.common.mobileby import MobileBy

from lib import kpi_names
from hs_logger import logger

from pages.base_page import BasePage
from pages.boost_page import BoostPage
from pages.profile_page import ProfilePage
from pages.payment_page import PaymentPage

###############################################################################################################
################################################### Android ###################################################
###############################################################################################################

class HomePage(BasePage):

	def __init__(self, driver, session_data):
		super().__init__(driver, session_data)

		self.walletbox=(MobileBy.ID,'com.virginmobile.uae:id/label_balance_integer_digits') #wallet balance box displayed 
		self.unit=(MobileBy.ID,'com.virginmobile.uae:id/label_currency_uae') #unit for aed +00.+00
		self.real=(MobileBy.ID,'com.virginmobile.uae:id/label_balance_integer_digits')#non point
		self.decimal=(MobileBy.ID,'com.virginmobile.uae:id/label_balance_fraction_digits')#after point
		self.recharge=(MobileBy.ACCESSIBILITY_ID,'Wallet Recharge')#wallet recharge button
		self.this_month=(MobileBy.XPATH,'//android.widget.TextView[@text="This month"]')
		self.remainingdata=(MobileBy.XPATH,'(//android.widget.TextView[@resource-id="com.virginmobile.uae:id/label_pack_total_value"])[2]')
		self.boostdata=(MobileBy.ACCESSIBILITY_ID,'Boost data')
		self.verify_pop=(MobileBy.XPATH,'//android.widget.TextView[contains(@text,"recommend us")]')
		self.popup=(MobileBy.XPATH,'(//android.widget.Button)[1]')
		self.back=(MobileBy.XPATH,'//android.widget.ImageButton[@content-desc="Back"]')
		self.continuebutton=(MobileBy.ID,'com.virginmobile.uae:id/ub_page_button_proceed')
		self.close=(MobileBy.XPATH,'//android.widget.Button[@resource-id="com.virginmobile.uae:id/vPositiveButton"]')
		self.setting = (MobileBy.ACCESSIBILITY_ID,'Open navigation drawer')
		self.profile_name = (MobileBy.ID,'com.virginmobile.uae:id/titleLabel')
		self.payment_icon=(MobileBy.XPATH,'//android.widget.TextView[@text="Payments"]')
		

# Login Page Confirmation
	def confirm_home_page(self):
		self.session_data.status = "Fail_to_confirm_home_page"
		self.wait_for(self.walletbox)
		sleep(1)
		self.session_data.kpi_labels[kpi_names.HOME_PAGE_LOAD_TIME]['end'] = int(round(time.time() * 1000))
		self.session_data.kpi_labels[kpi_names.HOME_PAGE_LOAD_TIME]['end_sensitivity'] = self.assign(kpi_names.HOME_PAGE_LOAD_TIME,'end_sensitivity')
		self.session_data.kpi_labels[kpi_names.HOME_PAGE_LOAD_TIME]['start_sensitivity'] = self.assign(kpi_names.HOME_PAGE_LOAD_TIME,'start_sensitivity')
		logger.info("Home Page Confirmed")
		self.session_data.pass_count += 1

# Direct to Boost page
	def go_to_boost_page(self):
		self.session_data.status="Fail_to_navigate_to_boost_page"
		sleep(3)
		self.screen_size_swipe()
		logger.info(f'Remaining data : {self.get_text_data(self.remainingdata)}')
		
		self.session_data.kpi_labels[kpi_names.BOOST_PAGE_LOAD_TIME]['start'] = int(round(time.time() * 1000))
		self.click_element(self.boostdata)
		BoostPageObject = BoostPage.instance(self.driver, self.session_data)
		return BoostPageObject
	
# Direct to Profile page 
	def go_to_profile_page(self):
		self.session_data.status = "Failed_go_to_profile_page"
		self.click_element(self.setting)
		self.click_element(self.profile_name)
		profile = ProfilePage.instance(self.driver, self.session_data)
		self.session_data.pass_count += 1
		return profile
	
# Direct to Payment page
	def go_to_payment_page(self):
		self.session_data.status = "Failed_go_to_payment_page"
		self.click_element(self.payment_icon)
		payment = PaymentPage.instance(self.driver, self.session_data)
		self.session_data.pass_count += 1
		return payment


###############################################################################################################
##################################################### iOS #####################################################
###############################################################################################################

class HomePageIOS(BasePage):
	def __init__(self, driver, session_data):
		super().__init__(driver, session_data)