from selenium import webdriver
import selenium.webdriver.common.action_chains as actionchains
firefox_profile = webdriver.FirefoxProfile()
firefox_profile.set_preference("browser.privatebrowsing.autostart", True)

driver = webdriver.Firefox(firefox_profile=firefox_profile)
actions = actionchains(driver)
driver.get('https://www.google.com/search?q=linkedin+amazon')
elements = driver.find_elements_by_id("rso")
for i in elements:
    actionchains.move_to_element(i.find_element_by_xpath('(//h3)[1]/../../a')).click()