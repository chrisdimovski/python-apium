import time
from time import sleep
from appium.webdriver.common.mobileby import MobileBy

from lib import kpi_names
from hs_logger import logger

from base_page import BasePage
from pages.feedback_page import FeedbackPage

###############################################################################################################
################################################### Android ###################################################
###############################################################################################################

class RoamingPage(BasePage):

    def __init__(self, driver, session_data):
        super().__init__(driver, session_data)

        
        self.startdate=(MobileBy.ID,'com.virginmobile.uae:id/label_expiry_date')
        self.editstartdate=(MobileBy.ID,'com.virginmobile.uae:id/btn_edit_start_date')
        self.checkeddate=(MobileBy.XPATH,'//android.view.View[@checked="true"]')
        self.selectdate=(MobileBy.ID,'com.virginmobile.uae:id/selectDate')
        self.nextmonth=(MobileBy.ACCESSIBILITY_ID,'Next month')
        self.nextmonthfirstday=(MobileBy.XPATH,"//android.view.View[contains(@content-desc,'01 ')]")
        self.need_more_data=(MobileBy.XPATH,'//android.widget.TextView[@resource-id="com.virginmobile.uae:id/titleLabel" and contains(@text,"Need more data")]')
        self.get_data=(MobileBy.ID,'com.virginmobile.uae:id/getDataButton')
        self.search_country=(MobileBy.ID,'com.virginmobile.uae:id/edit_search_country')
        self.Qatar=(MobileBy.XPATH,'//android.widget.TextView[@resource-id="com.virginmobile.uae:id/row_title" and contains(@text,"Qatar")]')
        self.gotitpopup=(MobileBy.XPATH,'//android.widget.Button[@resource-id="com.virginmobile.uae:id/gotItButton"]')
        self.countryname=(MobileBy.ID,'com.virginmobile.uae:id/countryName')
        self.openroaming=(MobileBy.ID,'com.virginmobile.uae:id/openRoaming')
        self.selected_roamplan_price=(MobileBy.ID,'com.virginmobile.uae:id/label_selected_plan_price')
        self.PayButton=(MobileBy.ID,'com.virginmobile.uae:id/btn_pay')
        self.Cancel=(MobileBy.ID,'com.virginmobile.uae:id/label_left')
        self.appfeedback=(MobileBy.XPATH,'//android.widget.TextView[@resource-id="com.virginmobile.uae:id/label_navigation" and @text="App feedback"]')
        self.back=(MobileBy.ACCESSIBILITY_ID,'Back')
        self.BACK=(MobileBy.XPATH,'//android.widget.ImageButton')
        self.setting = (MobileBy.XPATH,'//android.widget.ImageButton[@content-desc="Back"]')
        


# Roam plan page
    def Roam_plan(self):

        self.session_data.status = "Fail_to_find_current_date"
        sleep(1)
        self.wait_for(self.startdate)
        self.session_data.kpi_labels[kpi_names.ROAMING_PAGE_LOAD_TIME]['end'] = int(round(time.time() * 1000)) 
        logger.info("Current date visible")
        self.session_data.pass_count += 1

    
        self.session_data.status = "Fail_to_edit_date"
        self.wait_for(self.editstartdate)
        self.click_element(self.editstartdate)
       
        logger.info(f'Currentdate is,{self.getattribute(self.checkeddate,"content-desc")}')
        setdate=int(self.get_text_data(self.checkeddate))
        setdate=setdate+2
        uncheckeddates=(MobileBy.XPATH,'//android.view.View[@checked="false" and contains(@text,"{}")]'.format(setdate))


        try:
            self.wait_for(uncheckeddates)
            self.click_element(uncheckeddates)
            logger.info("Selected 2 days after current day")
        except:
            logger.info("Selecting first of next month as selecting 2 days after current day failed")
            self.wait_for(self.nextmonth)
            self.click_element(self.nextmonth)
            self.wait_for(self.nextmonthfirstday)
            self.click_element(self.nextmonthfirstday)
            setdate=1
        sleep(1)


        logger.info("Clicked date {}".format(setdate))
        self.wait_for(self.selectdate)
        self.click_element(self.selectdate)
        self.session_data.kpi_labels[kpi_names.ROAMING_DATE_SET_TIME]['start'] = int(round(time.time() * 1000)) 
        logger.info("Selected the date")
        verifydate=str(setdate)+'.'
        assert verifydate in self.get_text_data(self.startdate)
        self.session_data.kpi_labels[kpi_names.ROAMING_DATE_SET_TIME]['end'] = int(round(time.time() * 1000)) 
        logger.info("Date set to {}".format(self.get_text_data(self.startdate)))
        self.session_data.pass_count += 1


    # Add roaming pass
    def adding_roaming_pass(self):

        self.session_data.status = "Fail_to_get_data"
        self.wait_for(self.get_data)
        self.session_data.kpi_labels[kpi_names.ROAMING_PAGE_LOAD_TIME]['end'] = int(round(time.time() * 1000)) 
        self.session_data.pass_count += 1


        self.click_element(self.get_data)
        logger.info('Clicked get data')


        self.session_data.status = "Fail_select_country"
        self.wait_for(self.search_country)
        logger.info("Country selection")
        self.click_element(self.search_country)
        sleep(1)

        self.send_keys(self.search_country,'Qatar')
        self.wait_for(self.Qatar)
        self.click_element(self.Qatar)
        logger.info("Qatar")


        try:
            self.wait_for(self.gotitpopup)
            logger.info("Roaming passed")
            self.click_element(self.gotitpopup)
        except:
            pass

        self.wait_for(self.countryname)
        assert self.get_text_data(self.countryname)=='Qatar'
       

        self.click_element(self.openroaming)
        selectedprice=self.get_text_data(self.selected_roamplan_price)
        self.wait_for(self.PayButton)


        self.session_data.status = "Fail_payment"
        assert selectedprice in self.get_text_data(self.PayButton)
        logger.info(f'Pay option found and confirms the price selected {selectedprice}')
        self.click_element(self.PayButton)
        self.click_element(self.Cancel)
        self.wait_for(self.PayButton)
        logger.info("Payment done")


        for _ in range(3):
            self.wait_for(self.BACK)
            self.click_element(self.BACK)
        sleep(1)
        

        self.click_element(self.setting)
        try:
            self.click_element(self.appfeedback)
        except:
            self.click_element(self.BACK)
            self.click_element(self.appfeedback)


        self.session_data.kpi_labels[kpi_names.FEEDBACK_PAGE_LOAD_TIME]['start'] = int(round(time.time() * 1000)) 

        FeedbackPageObject = FeedbackPage.instance(self.driver, self.session_data)
        return FeedbackPageObject
    

###############################################################################################################
##################################################### iOS #####################################################
###############################################################################################################

class RoamingPageIOS(BasePage):

    def __init__(self, driver, session_data):
        super().__init__(driver, session_data)