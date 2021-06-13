from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import selenium.webdriver.support.ui as ui
import json
import os
from datetime import datetime


class Browser:
	def __init__(self):
		self.browser = webdriver.Firefox(executable_path='./geckodriver')
		self.wait = ui.WebDriverWait(self.browser,120)

	def run_all(self, data):
		now = datetime.now()
		for day in data['courses']:
			if now.isoweekday() == int(day):
				for hour in data['courses'][day]:
					if now.hour == int(hour):
						self.register(data['courses'][day][hour], data)

	def register(self, url, data):
		self.browser.get(url)
		self.browser.find_element_by_xpath('//td[@class="bs_sbuch"]').click()

		#Switch tab
		handles = self.browser.window_handles
		current = self.browser.current_window_handle
		value = [x for x in handles if x!=current]
		self.browser.switch_to.window(value[0])
		self.wait.until(lambda _: self.browser.find_element_by_xpath('//input[@class="inlbutton buchen"]'))

		self.browser.find_element_by_xpath('//input[@class="inlbutton buchen"]').click()

		self.browser.find_element_by_xpath('//input[@name="sex"][@value="X"]').click()
		for attr in ['vorname', 'name', 'strasse', 'ort']:
			self.browser.find_element_by_xpath('//input[@name="%s"]'%attr).send_keys(data[attr])

		Select(self.browser.find_element_by_xpath('//select[@name="statusorig"]')).select_by_value('S-TUD')
		
		for attr in ['matnr', 'email', 'telefon']:
			self.browser.find_element_by_xpath('//input[@name="%s"]'%attr).send_keys(data[attr])

		self.browser.find_element_by_xpath('//input[@name="tnbed"]').click()
		self.browser.find_element_by_xpath('//div[@id="bs_foot"]//input[@class="sub"][@type="submit"]').click()
		#Hier fehlt noch der letzte click! Max Mustermann kann aber leider keine Sportkarte

browser = Browser()
for file in os.listdir('entries'):
	with open(os.path.join('entries', file), "rb") as read_file:
		data = json.load(read_file)
		browser.run_all(data)
browser.browser.quit()
