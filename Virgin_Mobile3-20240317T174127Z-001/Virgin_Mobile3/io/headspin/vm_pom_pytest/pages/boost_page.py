import time
from time import sleep
from appium.webdriver.common.mobileby import MobileBy

from lib import kpi_names
from hs_logger import logger

from pages.base_page import BasePage
from pages.roaming_page import RoamingPage

###############################################################################################################
################################################### Android ###################################################
###############################################################################################################

class BoostPage(BasePage):

    def __init__(self, driver, session_data):
        super().__init__(driver, session_data)
        
        self.boostprice=(MobileBy.ID,'com.virginmobile.uae:id/label_booster_price')
        self.pay=(MobileBy.ID,'com.virginmobile.uae:id/btn_pay')
        self.cancel=(MobileBy.ID,'com.virginmobile.uae:id/btn_left')
        self.back=(MobileBy.ACCESSIBILITY_ID,'Back')
        self.roaming_option=(MobileBy.XPATH,'//android.widget.FrameLayout[@content-desc="Roaming"]')
        
# Boost current plan
    def boost_plan(self):
        self.session_data.status = "Fail_to_get_current_plan"
        self.wait_for(self.boostprice)
        self.session_data.kpi_labels[kpi_names.BOOST_PAGE_LOAD_TIME]['end'] = int(round(time.time() * 1000))
        logger.info("Boost page")
        self.session_data.pass_count += 1
        
        currentprice=self.get_text_data(self.boostprice)
        self.scroll(x1=550,y1=779,x2=550,y2=609)
        nextprice= self.get_text_data(self.boostprice)
        final=""

        if(currentprice<nextprice):
            self.scroll(x1=550,y1=609,x2=550,y2=779)
            logger.info("Reverse scrolled to go back")
            final=final+currentprice
        else:
            final=final+nextprice
        logger.info(f'Selected plan with price : {final}')
        sleep(1)

        self.session_data.status = "Fail_to_boost_current_plan"
        logger.info (f'{final} <-F P-> {self.get_text_data(self.pay)}')
        assert final in self.get_text_data(self.pay)
        logger.info("Plan selected")
        self.click_element(self.pay)
        self.wait_for(self.cancel)
        self.click_element(self.cancel)
        sleep(1)
        self.click_element(self.back)
        sleep(1)

        self.session_data.status = "Fail_to_find_roaming"
        self.wait_for(self.roaming_option)
        self.session_data.kpi_labels[kpi_names.ROAMING_PAGE_LOAD_TIME]['start'] = int(round(time.time() * 1000)) 
        self.click_element(self.roaming_option)
        logger.info("Roaming selected")

        RoamingPageObject = RoamingPage.instance(self.driver, self.session_data)
        return RoamingPageObject


###############################################################################################################
##################################################### iOS #####################################################
###############################################################################################################

class BoostPageIOS(BasePage):
    def __init__(self, driver, session_data):
        super().__init__(driver, session_data)