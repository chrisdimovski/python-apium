from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.interaction import POINTER_TOUCH
from selenium.webdriver.common.actions.mouse_button import MouseButton


from lib.hs_logger import logger
import importlib


def class_for_name(module_name, class_name):
	""" This is a helper method to get a class reference dynamically """
	dir_name = importlib.import_module(module_name)
	return getattr(dir_name, class_name)


class BasePage(object):
    
	def __init__(self , driver, session_data):
		self.driver = driver
		self.session_data = session_data
  
# Read data from sensitivity.json file 	
	def assign(self,kpi_name,type):
		return self.session_data.data.get(kpi_name).get(type)

# Click the element
	def click_element(self, locator):
		self.driver.implicitly_wait(30)
		element = self.find(locator)
		return element.click()

# Find_element
	def find(self, locator):
		return self.driver.find_element(*locator)

# Implicitly_wait for element
	def wait_for(self, locator, wait_period=30):
		self.driver.implicitly_wait(wait_period)
		return self.find(locator)
   
# Send_keys  
	def send_keys(self, locator, text):
		element = self.find(locator)
		return element.send_keys(text)
	
#Clear_field
	def clear_field(self, locator):
		element = self.find(locator)
		return element.clear()
	
     
# Get attribute
	def getattribute(self,element,value):
		a=element.get_attribute(value)
		return a    

	def get_text_data(self, locator):
		self.driver.implicitly_wait(30)
		element = self.find(locator)
		return element.text
	

#Wait_for_visibility
	def wait_for_visibility(self, locator, wait_period=30):
		self.driver.implicitly_wait(wait_period)
		try:
			self.find(locator).is_displayed()
			return True
		except:
			return False
	
# Hard tap on an element
	def hard_tap(self, element=None, x_ratio=0.5, y_ratio=0.5):
		if not element:
			screen_size = self.driver.get_window_size()
			logger.info(screen_size)
			width = screen_size['width']	
			height = screen_size['height']	
			x = width * x_ratio
			y = height * y_ratio
			logger.info(f'{x},{y}')
		else:
			location = element.location
			size = element.size
			x = location['x'] + (size['width'] * x_ratio)
			y = location['y'] + (size['height'] * y_ratio)
			logger.info(f'{x},{y}')
		self.driver.tap([(x, y)])
		logger.info(f'Tapped {element}')

# Swipe the screen 
	def screen_size_swipe(
			self, start_x_ratio=0.5, start_y_ratio=0.8,
			end_x_ratio=0.5, end_y_ratio=0.2, swipe_delay=300
		):
		screen_size = self.driver.get_window_size()
		width = screen_size['width']
		height = screen_size['height']
		self.start_x = width * start_x_ratio
		self.start_y = height * start_y_ratio
		self.end_x = width * end_x_ratio
		self.end_y = height * end_y_ratio
		self.driver.swipe(self.start_x, self.start_y, self.end_x, self.end_y, swipe_delay)

# Scroll
	def scroll(self,x1,y1,x2,y2):
		self.status = "Fail_to_scroll"
		self.actions = ActionBuilder(self.driver)
		finger = self.actions.add_pointer_input(POINTER_TOUCH, "finger")
		finger.create_pointer_move(duration=0, x=x1, y=y1)
		finger.create_pointer_down(button=MouseButton.LEFT)
		finger.create_pointer_move(duration=600, x=x2, y=y2)
		finger.create_pointer_up(button=MouseButton.LEFT)
		self.actions.perform()

# Restart application 
	def restart_app(self):
		
		self.session_data.status = "Fail_restart_app"
		self.driver.terminate_app(self.session_data.package)
		self.driver.launch_app()
		logger.info("App relaunching")

# Kill the app or terminal the application 
	def kill_app(self):

		self.session_data.status = "Fail_kill_app"
		self.driver.terminate_app(self.session_data.package)
		logger.info("App killed")
		print("")

# Start the application
	def start_app(self):
		self.session_data.status = "Fail_app_launch"
		self.driver.launch_app()    
  
	# OS switching		
	@classmethod
	def instance(cls, driver, session_data):
		plat = session_data.os.lower()
		klass = cls.__name__
		if plat == 'ios':
			klass = f'{klass}IOS'
		page_object = class_for_name('pages', klass)(driver, session_data)
		return page_object