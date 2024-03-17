from appium.webdriver.common.mobileby import MobileBy

from hs_logger import logger

from pages.base_page import BasePage
from pages.password_page import PasswordPage

###############################################################################################################
################################################### Android ###################################################
###############################################################################################################

class ProfilePage(BasePage):
    def __init__(self, driver, session_data):

        super().__init__(driver, session_data)
        
        self.password1 = (MobileBy.XPATH,'//android.widget.TextView[contains(@text,"password")]')
        self.password2 = (MobileBy.XPATH,'//android.widget.TextView[contains(@text,"Password")]')
          
# Direct to password page      
    def direct_to_password_page(self):

        self.session_data.status = "Fail_load_password_page"
        self.wait_for(self.password1)
        self.click_element(self.password1)
        self.wait_for(self.password2)
        self.click_element(self.password2)

        passwd = PasswordPage.instance(self.driver, self.session_data)
        self.session_data.pass_count += 1
        logger.info("Password")
        return passwd


###############################################################################################################
##################################################### iOS #####################################################
###############################################################################################################

class ProfilePageIOS(BasePage):

    def __init__(self, driver, session_data):
        super().__init__(driver, session_data)