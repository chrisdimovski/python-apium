from appium.webdriver.common.mobileby import MobileBy

from hs_logger import logger
from pages.base_page import BasePage

###############################################################################################################
################################################### Android ###################################################
###############################################################################################################

class PaymentPage(BasePage):
    def __init__(self, driver, session_data):
        super().__init__(driver, session_data)
        # Locators of the PaymentPage element 
        self.change_payment_mode=(MobileBy.XPATH,'//android.widget.TextView[@text="CHANGE"]')
        self.verfiy_Payment_Method=(MobileBy.XPATH,'//android.widget.TextView[@text="Payment Method"]')
        self.select_card=(MobileBy.XPATH,'//android.widget.TextView[contains(@text,"debit card")]')
        self.enter_card_num=(MobileBy.XPATH,'//android.widget.EditText[@text="Card Number"]')
        self.enter_card_expire=(MobileBy.XPATH,'//android.widget.EditText[contains(@text,"Expires")]')
        self.enter_cvv=(MobileBy.XPATH,'//android.widget.EditText[@text="CVV"]')
        self.enter_cardholder=(MobileBy.XPATH,'//android.widget.EditText[@text="Card holder"]')
        self.add_card=(MobileBy.XPATH,'//android.widget.Button[@text="ADD"]')
        self.cancel=(MobileBy.XPATH,'//android.widget.Button[@text="CANCEL"]')
        self.back=(MobileBy.XPATH,'//android.widget.ImageButton[@content-desc="Back"]')
        self.click_home=(MobileBy.XPATH,'//android.widget.TextView[@text="Home"]')
      
# Add payment details of the card
    def add_payment_card(self):
        self.session_data.status = "Failed_change_payment_mode"
        self.click_element(self.change_payment_mode)
        logger.info("Payment mode")

        self.wait_for(self.verfiy_Payment_Method)
        self.click_element(self.select_card)
        self.click_element(self.cancel)
        logger.info("Payment Over")
        self.session_data.pass_count += 1
       

###############################################################################################################
##################################################### iOS #####################################################
###############################################################################################################

class PaymentPageIOS(BasePage):

    def __init__(self, driver, session_data):
        super().__init__(driver, session_data)