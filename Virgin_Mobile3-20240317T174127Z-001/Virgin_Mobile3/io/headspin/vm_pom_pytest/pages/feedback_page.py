import time
from appium.webdriver.common.mobileby import MobileBy

from lib import kpi_names
from hs_logger import logger

from pages.base_page import BasePage

###############################################################################################################
################################################### Android ###################################################
###############################################################################################################

class FeedbackPage(BasePage):

    def __init__(self, driver, session_data):
        super().__init__(driver, session_data)
        self.feedbacktextbox=(MobileBy.XPATH,'//android.widget.EditText[@text="Tell us what you think!"]')
        self.i_like__itemoji=(MobileBy.ACCESSIBILITY_ID,'I like it!')
        self.submit=(MobileBy.ID,'com.virginmobile.uae:id/ub_page_button_proceed')
        self.thankyou=(MobileBy.XPATH,'//android.widget.TextView[@text="Thanks!"]')
    

    def app_feedback(self):
        self.session_data.status = "Fail_feedback"
        self.wait_for(self.i_like__itemoji)
        self.session_data.kpi_labels[kpi_names.FEEDBACK_PAGE_LOAD_TIME]['end'] = int(round(time.time() * 1000)) 
        logger.info("Feedback")
        self.session_data.pass_count += 1
        self.click_element(self.i_like__itemoji)
        
        self.session_data.status = "Fail_feedback_submit"
        self.send_keys(self.feedbacktextbox,"Test Feedback")
        self.wait_for(self.submit)
        self.session_data.kpi_labels[kpi_names.FEEDBACK_SUBMISSION_TIME]['start'] = int(round(time.time() * 1000)) 
        self.click_element(self.submit)
        self.wait_for(self.thankyou)
        self.session_data.kpi_labels[kpi_names.FEEDBACK_SUBMISSION_TIME]['end'] = int(round(time.time() * 1000)) 
        logger.info("Feedback done")
        self.session_data.pass_count += 1


###############################################################################################################
##################################################### iOS #####################################################
###############################################################################################################

class FeedbackPageIOS(BasePage):

    def __init__(self, driver, session_data):
        super().__init__(driver, session_data)