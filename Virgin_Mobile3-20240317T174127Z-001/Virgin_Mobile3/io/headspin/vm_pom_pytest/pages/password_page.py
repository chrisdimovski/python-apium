from appium.webdriver.common.mobileby import MobileBy

from hs_logger import logger
from pages.base_page import BasePage

###############################################################################################################
################################################### Android ###################################################
###############################################################################################################

class PasswordPage(BasePage):
    def __init__(self, driver, session_data):
        super().__init__(driver, session_data)
        
        self.password_entrybox = (MobileBy.XPATH,'//android.widget.EditText[@resource-id="com.virginmobile.uae:id/edit"]')
        self.CONFIRM = (MobileBy.XPATH,'//android.widget.Button[contains(@text,"CONFIRM")]')
        self.set_password = (MobileBy.XPATH,'//android.widget.EditText[contains(@text,"new")]')
        self.try_again = (MobileBy.XPATH,'//android.widget.Button[@text="TRY AGAIN"]')
        self.sign_out = (MobileBy.XPATH,"//android.widget.Button[contains(@text,'Sign out')]")
        self.sign_out1 = (MobileBy.XPATH,"//android.widget.Button[contains(@text,'SIGN OUT')]")
        
# Reset the password
    def reset_password(self):
        self.session_data.status = "Fail_reset_password"
        _,current_password,old_password = self.session_data.hs_api_call.read_csv()
        try:
            self.send_keys(self.password_entrybox,current_password)
            self.click_element(self.CONFIRM)
            self.send_keys(self.set_password,old_password)
            self.click_element(self.CONFIRM)
            self.session_data.hs_api_call.update_password()
        except:
            self.click_element(self.try_again)
            self.clear_field(self.password_entrybox)
            self.send_keys(self.password_entrybox,old_password)
            self.click_element(self.CONFIRM)
            self.send_keys(self.set_password,current_password)
            self.click_element(self.CONFIRM)
            self.session_data.hs_api_call.update_password()
        logger.info("Password changed")
        self.session_data.pass_count += 1
    
# Logout
    def logout(self):
        self.session_data.status = "Fail_logout"
        self.click_element(self.sign_out)
        self.click_element(self.sign_out1)
        logger.info("Logout")
        self.session_data.pass_count += 1
        

###############################################################################################################
##################################################### iOS #####################################################
###############################################################################################################

class PasswordIOS(BasePage):

    def __init__(self, driver, session_data):
        super().__init__(driver, session_data)