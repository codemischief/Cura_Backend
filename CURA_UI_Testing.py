
import os
import time
import ui_config
from ui_config import drivers_config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
import random
import string
import pytest

def filter_Common(driver, filter_xpath, text_css_selector, button_css_selector, starts_with_letter):
    wait=WebDriverWait(driver,10)
    driver.find_element(By.CSS_SELECTOR, text_css_selector).clear()
    driver.find_element(By.CSS_SELECTOR, text_css_selector).send_keys(starts_with_letter)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,button_css_selector))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH,filter_xpath))).click()
    time.sleep(1)
   
def filter_pagination_Common(driver, select_xpath, items_per_page):
    wait = WebDriverWait(driver, 10)
    select_element = driver.find_element(By.XPATH, select_xpath)
    dropdown = Select(select_element)
    dropdown.select_by_visible_text(items_per_page)
    time.sleep(2) 

def is_sorted_ascending_common(string_list):
        for i in range(len(string_list) - 1):
                if string_list[i] > string_list[i + 1]:
                   return False
        
        return True


def is_sorted_descending_common(string_list):
        for i in range(len(string_list) - 1):
                if string_list[i] < string_list[i + 1]:
                   return False
        
        return True

def login_and_navigate(username, password, comkey):
    driver = webdriver.Chrome()
    driver.get(drivers_config["login_url"])
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.NAME, "comkey").send_keys(comkey)
    login_button = driver.find_element(By.CSS_SELECTOR, "button[class='bg-[#004DD7] w-[200px] h-[35px] text-white text-[18px] rounded-lg cursor-pointer']")
    assert not login_button.get_attribute("disabled"), "Login button should be enabled"
    login_button.click()
    return driver

def test_login_success():
    driver = webdriver.Chrome()
    driver.get(drivers_config["login_url"])

    driver.find_element(By.NAME, "username").send_keys("ruderaw")
    driver.find_element(By.NAME, "password").send_keys("abcdefg")
    driver.find_element(By.NAME, "comkey").send_keys("9632")

    login_button = driver.find_element(By.CSS_SELECTOR, "button[class='bg-[#004DD7] w-[200px] h-[35px] text-white text-[18px] rounded-lg cursor-pointer']")
    assert not login_button.get_attribute("disabled"), "Login button should be enabled"
    login_button.click()
    
    time.sleep(2)
    try:
        dashboard_header = driver.find_element(By.CSS_SELECTOR, ".text-3xl.font-sans")
        assert dashboard_header.text == "Dashboard"
    except Exception as e: 
        print(f"Error finding Dashboard header: {e}")

    driver.close()

test_login_success()

def test_login_failure_username():
    
    driver = webdriver.Chrome()
    driver.get(drivers_config["login_url"])

    driver.find_element(By.NAME, "username").send_keys("aryan")
    driver.find_element(By.NAME, "password").send_keys("abcdefg")
    driver.find_element(By.NAME, "comkey").send_keys("9632")

    login_button = driver.find_element(By.CSS_SELECTOR, "button[class='bg-[#004DD7] w-[200px] h-[35px] text-white text-[18px] rounded-lg cursor-pointer']")
    assert not login_button.get_attribute("disabled"), "Login button should be enabled"
    login_button.click()
    
    time.sleep(2)
    try:
        success_element = driver.find_element(By.CSS_SELECTOR, "#inputError")
        assert success_element.text == "User does not exist"
    except Exception as e: 
        print(f"Error finding success element: {e}")

    driver.close()

test_login_failure_username() 


def test_login_failure_password():

    driver = webdriver.Chrome()
    driver.get(drivers_config["login_url"])

    driver.find_element(By.NAME, "username").send_keys("ruderaw")
    driver.find_element(By.NAME, "password").send_keys("hijklmn")
    driver.find_element(By.NAME, "comkey").send_keys("9632")

    login_button = driver.find_element(By.CSS_SELECTOR, "button[class='bg-[#004DD7] w-[200px] h-[35px] text-white text-[18px] rounded-lg cursor-pointer']")
    assert not login_button.get_attribute("disabled"), "Login button should be enabled"
    login_button.click()
    
    time.sleep(2)
    try:
        error_element = driver.find_element(By.CSS_SELECTOR, "#inputError")  
        assert error_element.text == "Invalid Credentials"
    except Exception as e: 
        print(f"Error finding error element: {e}")

    driver.close()

test_login_failure_password() 


def test_login_failure_companyskey():

    driver = webdriver.Chrome()
    driver.get(drivers_config["login_url"])

    driver.find_element(By.NAME, "username").send_keys("ruderaw")
    driver.find_element(By.NAME, "password").send_keys("abcdefg")
    driver.find_element(By.NAME, "comkey").send_keys("0000")

    login_button = driver.find_element(By.CSS_SELECTOR, "button[class='bg-[#004DD7] w-[200px] h-[35px] text-white text-[18px] rounded-lg cursor-pointer']")
    assert not login_button.get_attribute("disabled"), "Login button should be enabled"
    login_button.click()
    
    time.sleep(2)
    try:
        success_element = driver.find_element(By.CSS_SELECTOR, "#inputError")
        assert success_element.text == "Invalid Credentials"
    except Exception as e: 
        print(f"Error finding success element: {e}")

    driver.close()

test_login_failure_companyskey() 

def test_login_failure_all():
    driver = webdriver.Chrome()
    driver.get(drivers_config["login_url"])

    driver.find_element(By.NAME, "username").send_keys("aryan")
    driver.find_element(By.NAME, "password").send_keys("hijklmn")
    driver.find_element(By.NAME, "comkey").send_keys("0000")

    login_button = driver.find_element(By.CSS_SELECTOR, "button[class='bg-[#004DD7] w-[200px] h-[35px] text-white text-[18px] rounded-lg cursor-pointer']")
    assert not login_button.get_attribute("disabled"), "Login button should be enabled"
    login_button.click()
    
    time.sleep(2)
    try:
        success_element = driver.find_element(By.CSS_SELECTOR, "#inputError")
        assert success_element.text == "User does not exist"
    except Exception as e: 
        print(f"Error finding success element: {e}")

    driver.close()
    
test_login_failure_all()


def test_Dashboard_Admin(driver):
        admin_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div:nth-child(2) div:nth-child(1) button:nth-child(1) p:nth-child(1)"))
        )
        assert not admin_button.get_attribute("disabled"), "Admin button should be enabled"
        admin_button.click()

        admin_header = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div:nth-child(1) > div:nth-child(1) > h1:nth-child(1)"))
        )
        assert admin_header.text == "Personnel", "Admin header text is incorrect"
        time.sleep(2)

def test_Dashboard_Manager(driver):
        Manager_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div:nth-child(2) > div:nth-child(2)"))
        )
        assert not Manager_button.get_attribute("disabled"), "Manager button should be enabled"
        Manager_button.click()

        manager_header = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div:nth-child(1) > div:nth-child(1) > h1:nth-child(1)"))
        )
        assert manager_header.text == "Builder", "Manager header text is incorrect"
        time.sleep(2)

def test_Dashboard_Report(driver):
        Report_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div:nth-child(2) > div:nth-child(3)"))
        )
        assert not Report_button.get_attribute("disabled"), "Report button should be enabled"
        Report_button.click()

        report_header = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div:nth-child(5) > div:nth-child(1) > h1:nth-child(1)"))
        )
        assert report_header.text == "Contact", "Report header text is incorrect"
        time.sleep(2)


def test_Dashboard_Research(driver):
        driver.find_element(By.XPATH,"//p[normalize-space()='Research']").click()
        time.sleep(2)

def test_Dashboard_Logout(driver):
        Logout_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/']"))
        )
        assert not Logout_button.get_attribute("disabled"), "Logout button should be enabled"
        Logout_button.click()

        Logout_header = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='text-center text-[21px] mb-[35px]']"))
        )
        assert Logout_header.text == "Login Panel", "Logout header text is incorrect"
        
def Dashboard_Webpage():
    try:
        driver=login_and_navigate("ruderaw", "abcdefg", "9632")
        test_Dashboard_Admin(driver)
        test_Dashboard_Manager(driver)
        test_Dashboard_Report(driver)
        test_Dashboard_Research(driver)
        test_Dashboard_Logout(driver)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
Dashboard_Webpage()


def login_and_navigate_employee(username, password, comkey):
    driver = webdriver.Chrome()
    driver.get(drivers_config["login_url"])
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.NAME, "comkey").send_keys(comkey)
    login_button = driver.find_element(By.CSS_SELECTOR, "button[class='bg-[#004DD7] w-[200px] h-[35px] text-white text-[18px] rounded-lg cursor-pointer']")
    assert not login_button.get_attribute("disabled"), "Login button should be enabled"
    login_button.click()
    admin_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div:nth-child(2) div:nth-child(1) button:nth-child(1) p:nth-child(1)"))
        )
    assert not admin_button.get_attribute("disabled"), "Admin button should be enabled"
    admin_button.click()
    driver.find_element(By.XPATH,"//a[normalize-space()='Employees']").click()
    time.sleep(2)
    return driver

def add_new_employee(driver,employee_name, pan_no, username, doj, designation, email, dob, last_dow, role, ph_no, country, state, city, suburb, entity):
    wait=WebDriverWait(driver,10)
    driver.find_element(By.CSS_SELECTOR, ".flex.items-center.justify-center.gap-4").click()
    wait.until(EC.element_to_be_clickable((By.XPATH,"//input[@name='employeeName']"))).send_keys(employee_name)
    driver.find_element(By.XPATH,"//input[@name='panNo']").send_keys(pan_no)
    element=driver.find_element(By.XPATH,"//select[@name='userName']")
    drp=Select(element)
    drp.select_by_visible_text(username)
    driver.find_element(By.XPATH,"//input[@name='doj']").send_keys(doj)
    driver.find_element(By.XPATH,"//input[@name='designation']").send_keys(designation)
    driver.find_element(By.XPATH,"//input[@name='email']").send_keys(email)
    employee_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    driver.find_element(By.XPATH,"//input[@name='employeeId']").send_keys(employee_id)
    element1=driver.find_element(By.XPATH,"//select[@name='lob']")
    drp1=Select(element1)
    drp1.select_by_visible_text('Reimbursements')
    driver.find_element(By.XPATH,"//input[@name='dob']").send_keys(dob)
    driver.find_element(By.XPATH,"//input[@name='lastDOW']").send_keys(last_dow)
    element2=driver.find_element(By.XPATH,"//select[@name='role']")
    drp2=Select(element2)
    drp2.select_by_visible_text(role)
    driver.find_element(By.XPATH,"//input[@name='phNo']").send_keys(ph_no)
    element3=wait.until(EC.element_to_be_clickable((By.XPATH,"//select[@name='country']")))
    drp3=Select(element3)
    drp3.select_by_visible_text(country)
    time.sleep(2)
    element4=wait.until(EC.element_to_be_clickable((By.XPATH,"//select[@name='state']")))
    drp4=Select(element4)
    drp4.select_by_visible_text(state)
    time.sleep(2)
    element5=wait.until(EC.element_to_be_clickable((By.XPATH,"//select[@name='city']")))
    drp5=Select(element5)
    drp5.select_by_visible_text(city)
    wait.until(EC.element_to_be_clickable((By.XPATH,"//input[@name='suburb']"))).send_keys(suburb)
    element6=wait.until(EC.element_to_be_clickable((By.XPATH,"//select[@name='entity']")))
    drp6=Select(element6)
    drp6.select_by_visible_text(entity)
    driver.find_element(By.XPATH, "//button[normalize-space()='Add']").click()
    wait.until(EC.element_to_be_clickable((By.XPATH,"//button[normalize-space()='Save']"))).click()
    time.sleep(4)
    driver.find_element(By.XPATH,"//body/div[@id='root']/div/div/div/div/div/div/input[1]").send_keys("aryan ashish")
    wait.until(EC.element_to_be_clickable((By.XPATH,"//img[@alt='search-icon']"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH,"//img[@alt='trash']"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH,"//body/div[@role='presentation']/div/div/div/button[1]"))).click()
    time.sleep(2)
    
   


# add_new_employee(driver, "aryan ashish", "ijklmn", "Admin User", "06-05-2024", "intern", "ashish.com", "06-05-2003", "31-05-2024", "Admin", "11100000", "UAE", "UAE", "Dubai", "q", "Z-CASH")

def test_Edit_Employee_Success(driver):
        wait=WebDriverWait(driver,10)
        addEmployee_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > button:nth-child(1)"))
        )
        assert not addEmployee_button.get_attribute("disabled"), "Logout button should be enabled"
        addEmployee_button.click()

        addEmployee_header = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".text-base"))
        )
        assert addEmployee_header.text == "Add New Employee", "Add New Employee header text is incorrect"
        time.sleep(2)
        driver.find_element(By.XPATH,"//input[@name='employeeName']").send_keys("aryan ashish")
        driver.find_element(By.XPATH,"//input[@name='panNo']").send_keys("ijklmn")
        element=driver.find_element(By.XPATH,"//select[@name='userName']")
        drp=Select(element)
        drp.select_by_visible_text('Admin User')
        driver.find_element(By.XPATH,"//input[@name='doj']").send_keys("06-05-2024")
        driver.find_element(By.XPATH,"//input[@name='designation']").send_keys("intern")
        driver.find_element(By.XPATH,"//input[@name='email']").send_keys("ashish.com")
        employee_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        driver.find_element(By.XPATH,"//input[@name='employeeId']").send_keys(employee_id)
        element1=driver.find_element(By.XPATH,"//select[@name='lob']")
        drp1=Select(element1)
        drp1.select_by_visible_text('Reimbursements')
        driver.find_element(By.XPATH,"//input[@name='dob']").send_keys("06-05-2003")
        driver.find_element(By.XPATH,"//input[@name='lastDOW']").send_keys("31-05-2024")
        element2=driver.find_element(By.XPATH,"//select[@name='role']")
        drp2=Select(element2)
        drp2.select_by_visible_text('Admin')
        driver.find_element(By.XPATH,"//input[@name='phNo']").send_keys("11100000")
        element3=wait.until(EC.element_to_be_clickable((By.XPATH,"//select[@name='country']")))
        drp3=Select(element3)
        drp3.select_by_visible_text('UAE')
        time.sleep(2)
        element4=wait.until(EC.element_to_be_clickable((By.XPATH,"//select[@name='state']")))
        drp4=Select(element4)
        drp4.select_by_visible_text('UAE')
        time.sleep(2)
        element5=wait.until(EC.element_to_be_clickable((By.XPATH,"//select[@name='city']")))
        drp5=Select(element5)
        drp5.select_by_visible_text('Dubai')
        wait.until(EC.element_to_be_clickable((By.XPATH,"//input[@name='suburb']"))).send_keys('q')
        element6=wait.until(EC.element_to_be_clickable((By.XPATH,"//select[@name='entity']")))
        drp6=Select(element6)
        drp6.select_by_visible_text('Z-CASH')
        driver.find_element(By.XPATH, "//button[normalize-space()='Add']").click()
        wait.until(EC.element_to_be_clickable((By.XPATH,"//button[normalize-space()='Save']"))).click()
        time.sleep(4)
        # driver.find_element(By.XPATH,"//body/div[@id='root']/div/div/div/div/div/div/input[1]").send_keys("aryan ashish")
        # time.sleep(2)
        driver.find_element(By.XPATH,"//img[@alt='search-icon']").click()
        time.sleep(2)
        driver.find_element(By.XPATH,"//img[@alt='edit']").click()
        time.sleep(2)
        driver.find_element(By.XPATH,"//input[@name='employeename']").clear()
        time.sleep(2)
        driver.find_element(By.XPATH,"//input[@name='employeename']").send_keys("ashish aryan")
        time.sleep(2)
        driver.find_element(By.XPATH,"//button[normalize-space()='Save']").click()
        time.sleep(4)
        driver.find_element(By.XPATH,"//body/div[@id='root']/div/div/div/div/div/div/input[1]").clear()
        time.sleep(4)
        driver.find_element(By.XPATH,"//body/div[@id='root']/div/div/div/div/div/div/input[1]").send_keys("ashish aryan")
        time.sleep(2)
        driver.find_element(By.XPATH,"//img[@alt='search-icon']").click()
        wait.until(EC.element_to_be_clickable((By.XPATH,"//div//div//div//div[1]//div[2]//div[2]//button[2]//img[1]"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH,"//button[normalize-space()='Delete']"))).click()
        time.sleep(2)
        
def filter_Common(driver, filter_xpath, text_css_selector, button_css_selector, starts_with_letter):
    wait=WebDriverWait(driver,10)
    driver.find_element(By.CSS_SELECTOR, text_css_selector).clear()
    driver.find_element(By.CSS_SELECTOR, text_css_selector).send_keys(starts_with_letter)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,button_css_selector))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH,filter_xpath))).click()
    time.sleep(1)
   
def filter_pagination_Common(driver, select_xpath, items_per_page):
    wait = WebDriverWait(driver, 10)
    select_element = driver.find_element(By.XPATH, select_xpath)
    dropdown = Select(select_element)
    dropdown.select_by_visible_text(items_per_page)
    time.sleep(2) 


def test_Filter_Employee_Name_StartsWith_Success(driver):
    filter_Common(
        driver,
        "//h1[normalize-space()='StartsWith']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "a"
    )


def test_Filter_Employee_Name_Contains_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='Contains']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "a"
    )



def test_Filter_Employee_Name_DoesNotContains_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='DoesNotContain']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "a"
    )



def test_Filter_Employee_Name_EndsWith_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='EndsWith']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "a"
    )

def test_Filter_Employee_Name_EqualTo_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='EqualTo']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "a"
    )


def test_Filter_Employee_Name_isNotNull_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='isNotNull']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "a"
    )


def test_Filter_Employee_Name_isNull_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='isNull']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "a"
    )


def test_Filter_Employee_Name_NoFilter_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='No Filter']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "a"
    )


def test_Filter_Employee_ID_StartsWith_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='StartsWith']",
        "div:nth-child(3) div:nth-child(1) input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "a"
    )


def test_Filter_Employee_ID_Contains_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='Contains']",
        "div:nth-child(3) div:nth-child(1) input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "a"
    )

def test_Filter_Employee_ID_DoesNotContains_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='DoesNotContain']",
        "div:nth-child(3) div:nth-child(1) input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "a"
    )

def test_Filter_Employee_ID_EndsWith_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='EndsWith']",
        "div:nth-child(3) div:nth-child(1) input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "a"
    )

def test_Filter_Employee_ID_EqualsTo_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='EqualTo']",
        "div:nth-child(3) div:nth-child(1) input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "a"
    )


def test_Filter_Employee_ID_isNotNull_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='isNotNull']",
        "div:nth-child(3) div:nth-child(1) input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "a"
    )

def test_Filter_Employee_ID_isNull_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='isNull']",
        "div:nth-child(3) div:nth-child(1) input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "a"
    )

def test_Filter_Employee_ID_NoFilter_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='No Filter']",
        "div:nth-child(3) div:nth-child(1) input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "a"
    )


def test_Filter_Employee_PhoneID_Contains_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='Contains']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "9"
    )


def test_Filter_Employee_PhoneID_DoesNotContains_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='DoesNotContain']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "9"
    )


def test_Filter_Employee_PhoneID_StartsWith_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='StartsWith']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "9"
    )

def test_Filter_Employee_PhoneID_EndsWith_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='EndsWith']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "9"
    )

def test_Filter_Employee_PhoneID_EqualsTo_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='EqualTo']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "9"
    )

def test_Filter_Employee_PhoneID_isNull_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='isNull']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "9"
    )

def test_Filter_Employee_PhoneID_isNotNull_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='isNotNull']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "9"
    )

def test_Filter_Employee_PhoneID_NoFilter_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='No Filter']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "9"
    )

def test_Filter_Employee_Name_ascending_Success(driver):
        driver.find_element(By.XPATH,"//body[1]/div[1]/div[1]/div[1]/div[2]/div[3]/div[1]/div[1]/div[2]/div[1]/p[1]/button[1]/span[1]").click()
        time.sleep(2)


def test_Filter_Employee_Name_descending_Success(driver):
        driver.find_element(By.XPATH,"//body[1]/div[1]/div[1]/div[1]/div[2]/div[3]/div[1]/div[1]/div[2]/div[1]/p[1]/button[1]/span[1]").click()
        time.sleep(2)

def test_Filter_Employee_ID_descending_Success(driver):
        driver.find_element(By.XPATH,"//body//div[@id='root']//div//div//div//div//div[3]//div[1]//p[1]//button[1]//span[1]").click()
        time.sleep(2)


def test_Filter_Employee_ID_ascending_Success(driver):
        driver.find_element(By.XPATH,"//body//div[@id='root']//div//div//div//div//div[3]//div[1]//p[1]//button[1]//span[1]").click()
        time.sleep(2)


def test_Filter_Employee_EmailID_StartsWith_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='StartsWith']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(5) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(5) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "customer@gmail.com"
    )

def test_Filter_Employee_EmailID_DoesNotContains_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='DoesNotContain']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(5) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(5) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "customer@gmail.com"
    )

def test_Filter_Employee_EmailID_Contains_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='Contains']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(5) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(5) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "customer@gmail.com"
    )


def test_Filter_Employee_EmailID_EndsWith_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='EndsWith']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(5) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(5) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "customer@gmail.com"
    )

def test_Filter_Employee_EmailID_EqualsTo_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='EqualTo']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(5) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(5) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "customer@gmail.com"
    )


def test_Filter_Employee_EmailID_isNull_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='isNull']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(5) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(5) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "customer@gmail.com"
    )


def test_Filter_Employee_EmailID_isNotNull_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='isNotNull']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(5) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(5) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "customer@gmail.com"
    )

def test_Filter_Employee_EmailID_NoFilter_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='No Filter']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(5) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(5) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "customer@gmail.com"
    )

def test_Filter_Employee_Roles_StartsWith_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='StartsWith']",
        "div:nth-child(6) div:nth-child(1) input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(6) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "analyst"
    )


def test_Filter_Employee_Roles_EndsWith_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='EndsWith']",
        "div:nth-child(6) div:nth-child(1) input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(6) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "analyst"
    )


def test_Filter_Employee_Roles_EqualsTo_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='EqualTo']",
        "div:nth-child(6) div:nth-child(1) input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(6) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "analyst"
    )

def test_Filter_Employee_Roles_isNull_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='isNull']",
        "div:nth-child(6) div:nth-child(1) input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(6) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "analyst"
    )

def test_Filter_Employee_Roles_isNotNull_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='isNotNull']",
        "div:nth-child(6) div:nth-child(1) input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(6) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "analyst"
    )


def test_Filter_Employee_Roles_NoFilter_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='No Filter']",
        "div:nth-child(6) div:nth-child(1) input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(6) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "analyst"
    )


def test_Filter_Employee_Roles_Contains_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='Contains']",
        "div:nth-child(6) div:nth-child(1) input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(6) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "analyst"
    )


def test_Filter_Employee_Roles_DoesNotContains_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='DoesNotContain']",
        "div:nth-child(6) div:nth-child(1) input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(6) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "analyst"
    )


def test_Filter_Employee_Panno_StartsWith_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='StartsWith']",
        "div:nth-child(7) div:nth-child(1) input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(7) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "abcd"
    )


def test_Filter_Employee_Panno_EndsWith_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='EndsWith']",
        "div:nth-child(7) div:nth-child(1) input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(7) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "abcd"
    )

def test_Filter_Employee_Panno_EqualsTo_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='EqualTo']",
        "div:nth-child(7) div:nth-child(1) input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(7) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "abcd"
    )


def test_Filter_Employee_Panno_isNull_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='isNull']",
        "div:nth-child(7) div:nth-child(1) input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(7) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "abcd"
    )

def test_Filter_Employee_Panno_isNotNull_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='isNotNull']",
        "div:nth-child(7) div:nth-child(1) input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(7) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "abcd"
    )

def test_Filter_Employee_Panno_Contains_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='Contains']",
        "div:nth-child(7) div:nth-child(1) input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(7) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "abcd"
    )


def test_Filter_Employee_Panno_DoesNotContains_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='DoesNotContain']",
        "div:nth-child(7) div:nth-child(1) input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(7) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "abcd"
    )

def test_Filter_Employee_Panno_NoFilter_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='No Filter']",
        "div:nth-child(7) div:nth-child(1) input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(7) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "abcd"
    )

def filter_employee_doj_starts_with(driver, starts_with_letter):
        wait=WebDriverWait(driver,10)
        wait.until(EC.visibility_of_element_located((By.XPATH,"//input[@value='false']"))).send_keys(starts_with_letter)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(8) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)"))).click()
        time.sleep(2)


def test_Filter_Employee_doj_EqualsTo_Success(driver):
        filter_employee_doj_starts_with(driver, "13-01-2024")
        driver.find_element(By.XPATH,"//h1[normalize-space()='EqualTo']").click()
        time.sleep(2)
        
def test_Filter_Employee_doj_NotEqualTo_Success(driver):
        wait=WebDriverWait(driver,10)
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(8) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        wait.until(EC.element_to_be_clickable((By.XPATH,"//h1[normalize-space()='NotEqualTo']"))).click()
        time.sleep(2)


def test_Filter_Employee_doj_GreaterThan_Success(driver):
        wait=WebDriverWait(driver,10)
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(8) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        wait.until(EC.element_to_be_clickable((By.XPATH,"//h1[normalize-space()='GreaterThan']"))).click()
        time.sleep(2)


def test_Filter_Employee_doj_LessThan_Success(driver):
        wait=WebDriverWait(driver,10)
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(8) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        wait.until(EC.element_to_be_clickable((By.XPATH,"//h1[normalize-space()='LessThan']"))).click()
        time.sleep(2)


def test_Filter_Employee_doj_GreaterThanOrEqualTo_Success(driver):
        wait=WebDriverWait(driver,10)
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(8) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        wait.until(EC.element_to_be_clickable((By.XPATH,"//h1[normalize-space()='GreaterThanOrEqualTo']"))).click()
        time.sleep(2)


def test_Filter_Employee_doj_LessThanOrEqualTo_Success(driver):
        wait=WebDriverWait(driver,10)
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(8) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        wait.until(EC.element_to_be_clickable((By.XPATH,"//h1[normalize-space()='LessThanOrEqualTo']"))).click()
        time.sleep(2)

def test_Filter_Employee_doj_isNull_Success(driver):
        wait=WebDriverWait(driver,10)
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(8) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        wait.until(EC.element_to_be_clickable((By.XPATH,"//h1[normalize-space()='isNull']"))).click()
        time.sleep(2)

def test_Filter_Employee_doj_isNotNull_Success(driver):
        wait=WebDriverWait(driver,10)
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(8) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        wait.until(EC.element_to_be_clickable((By.XPATH,"//h1[normalize-space()='isNotNull']"))).click()
        time.sleep(2)

def test_Filter_Employee_doj_NoFilter_Success(driver):
        wait=WebDriverWait(driver,10)
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(8) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        wait.until(EC.element_to_be_clickable((By.XPATH,"//h1[normalize-space()='No Filter']"))).click()
        time.sleep(2)

def filter_employee_low_starts_with(driver, starts_with_letter):
        wait=WebDriverWait(driver,10)
        driver.find_element(By.CSS_SELECTOR,"div:nth-child(9) div:nth-child(1) input:nth-child(1)").send_keys(starts_with_letter)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(9) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)"))).click()
        time.sleep(2)


def test_Filter_Employee_low_EqualsTo_Success(driver):
        wait=WebDriverWait(driver,10)
        filter_employee_low_starts_with(driver, "20-02-2020")
        wait.until(EC.element_to_be_clickable((By.XPATH, "//h1[normalize-space()='EqualTo']"))).click()
        time.sleep(2)

def test_Filter_Employee_low_NotEqualTo_Success(driver):
        wait=WebDriverWait(driver,10)
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(9) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        wait.until(EC.element_to_be_clickable((By.XPATH,"//h1[normalize-space()='NotEqualTo']"))).click()
        time.sleep(2)

def test_Filter_Employee_low_GreaterThan_Success(driver):
        wait=WebDriverWait(driver,10)
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(9) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        wait.until(EC.element_to_be_clickable((By.XPATH,"//h1[normalize-space()='GreaterThan']"))).click()
        time.sleep(2)

def test_Filter_Employee_low_LessThan_Success(driver):
        wait=WebDriverWait(driver,10)
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(9) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        wait.until(EC.element_to_be_clickable((By.XPATH,"//h1[normalize-space()='LessThan']"))).click()
        time.sleep(2)

def test_Filter_Employee_low_GreaterThanOrEqualTo_Success(driver):
        wait=WebDriverWait(driver,10)
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(9) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        wait.until(EC.element_to_be_clickable((By.XPATH,"//h1[normalize-space()='GreaterThanOrEqualTo']"))).click()
        time.sleep(2)

def test_Filter_Employee_low_LessThanOrEqualTo_Success(driver):
        wait=WebDriverWait(driver,10)
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(9) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        wait.until(EC.element_to_be_clickable((By.XPATH,"//h1[normalize-space()='LessThanOrEqualTo']"))).click()
        time.sleep(2)

def test_Filter_Employee_low_isNull_Success(driver):
        wait=WebDriverWait(driver,10)
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(9) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        wait.until(EC.element_to_be_clickable((By.XPATH,"//h1[normalize-space()='isNull']"))).click()
        time.sleep(2)

def test_Filter_Employee_low_isNotNull_Success(driver):
        wait=WebDriverWait(driver,10)
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(9) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        wait.until(EC.element_to_be_clickable((By.XPATH,"//h1[normalize-space()='isNotNull']"))).click()
        time.sleep(2)

def test_Filter_Employee_low_NoFilter_Success(driver):
        wait=WebDriverWait(driver,10)
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(9) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        wait.until(EC.element_to_be_clickable((By.XPATH,"//h1[normalize-space()='No Filter']"))).click()
        time.sleep(2)

def test_Filter_Employee_status_EqualsTo_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='EqualTo']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(10) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(10) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "active"
    )

def test_Filter_Employee_status_NotEqualsTo_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='NotEqualTo']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(10) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(10) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "active"
    )

def test_Filter_Employee_status_GreaterThan_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='GreaterThan']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(10) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(10) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "active"
    )

def test_Filter_Employee_status_LessThan_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='LessThan']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(10) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(10) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "active"
    )

def test_Filter_Employee_status_GreaterThanOrEqualTo_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='GreaterThanOrEqualTo']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(10) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(10) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "active"
    )

def test_Filter_Employee_status_LessThanOrEqualTo_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='LessThanOrEqualTo']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(10) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(10) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "active"
    )

def test_Filter_Employee_status_isNull_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='isNull']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(10) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(10) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "active"
    )

def test_Filter_Employee_status_isNotNull_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='isNotNull']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(10) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(10) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "active"
    )
        

def test_Filter_Employee_status_NoFilter_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='No Filter']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(10) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(10) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "active"
    )

def test_Filter_Employee_employee_id_EqualsTo_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='EqualTo']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "43"
    )


def test_Filter_Employee_employee_id_NotEqualsTo_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='NotEqualTo']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "43"
    )

def test_Filter_Employee_employee_id_LessThan_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='LessThan']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "43"
    )

def test_Filter_Employee_employee_id_GreaterThan_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='GreaterThan']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "43"
    )

def test_Filter_Employee_employee_id_GreaterThanOrEqualTo_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='GreaterThanOrEqualTo']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "43"
    )

def test_Filter_Employee_employee_id_LessThanOrEqualTo_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='LessThanOrEqualTo']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "43"
    )


def test_Filter_Employee_employee_id_isNull_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='isNull']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "43"
    )


def test_Filter_Employee_employee_id_isNotNull_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='isNotNull']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "43"
    )
        

def test_Filter_Employee_employee_id_NoFilter_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='No Filter']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "43"
    )
def test_Filter_Employee_Pagination15_NoFilter_Success(driver):
    select_xpath = "//div[@id='root']//div//div//div//div//div//select"
    next_page="//button[@aria-label='Go to page 2']"
    filter_pagination_Common(driver, select_xpath, '15', next_page)

# %%
def test_Filter_Employee_Pagination25_NoFilter_Success(driver):
    select_xpath = "//div[@id='root']//div//div//div//div//div//select"
    next_page="//button[@aria-label='Go to page 2']"
    filter_pagination_Common(driver, select_xpath, '25' ,next_page)

# %%
def test_Filter_Employee_Pagination50_NoFilter_Success(driver):
    select_xpath = "//div[@id='root']//div//div//div//div//div//select"
    next_page="//button[@aria-label='Go to page 2']"
    filter_pagination_Common(driver, select_xpath, '50', next_page)

# %%
def test_Filter_Employee_phone_ascending_Success(driver):
        driver.find_element(By.XPATH,"//body[1]/div[1]/div[1]/div[1]/div[2]/div[3]/div[1]/div[1]/div[4]/div[1]/p[1]/button[1]/span[1]").click()
        time.sleep(2)


# %%
def test_Filter_Employee_phone_descending_Success(driver):
        driver.find_element(By.XPATH,"//body[1]/div[1]/div[1]/div[1]/div[2]/div[3]/div[1]/div[1]/div[4]/div[1]/p[1]/button[1]/span[1]").click()
        time.sleep(2)


# %%
def test_Filter_Employee_email_descending_Success(driver):
        driver.find_element(By.XPATH,"//body[1]/div[1]/div[1]/div[1]/div[2]/div[3]/div[1]/div[1]/div[5]/div[1]/p[1]/button[1]/span[1]").click()
        time.sleep(2)


# %%
def test_Filter_Employee_email_ascending_Success(driver):
        driver.find_element(By.XPATH,"//body[1]/div[1]/div[1]/div[1]/div[2]/div[3]/div[1]/div[1]/div[5]/div[1]/p[1]/button[1]/span[1]").click()
        time.sleep(2)


# %%
def test_Filter_Employee_role_ascending_Success(driver):
        driver.find_element(By.XPATH,"//body[1]/div[1]/div[1]/div[1]/div[2]/div[3]/div[1]/div[1]/div[6]/div[1]/p[1]/button[1]/span[1]").click()
        time.sleep(2)


# %%
def test_Filter_Employee_role_descending_Success(driver):
        driver.find_element(By.XPATH,"//body[1]/div[1]/div[1]/div[1]/div[2]/div[3]/div[1]/div[1]/div[6]/div[1]/p[1]/button[1]/span[1]").click()
        time.sleep(2)


# %%
def test_Filter_Employee_panno_descending_Success(driver):
        driver.find_element(By.XPATH,"//body[1]/div[1]/div[1]/div[1]/div[2]/div[3]/div[1]/div[1]/div[7]/div[1]/p[1]/button[1]/span[1]").click()
        time.sleep(2)


# %%
def test_Filter_Employee_panno_ascending_Success(driver):
        driver.find_element(By.XPATH,"//body[1]/div[1]/div[1]/div[1]/div[2]/div[3]/div[1]/div[1]/div[7]/div[1]/p[1]/button[1]/span[1]").click()
        time.sleep(2)


# %%
def test_Filter_Employee_doj_ascending_Success(driver):
        driver.find_element(By.XPATH,"//body[1]/div[1]/div[1]/div[1]/div[2]/div[3]/div[1]/div[1]/div[8]/div[1]/p[1]/button[1]/span[1]").click()
        time.sleep(2)


# %%
def test_Filter_Employee_doj_descending_Success(driver):
        driver.find_element(By.XPATH,"//body[1]/div[1]/div[1]/div[1]/div[2]/div[3]/div[1]/div[1]/div[8]/div[1]/p[1]/button[1]/span[1]").click()
        time.sleep(2)


# %%
def test_Filter_Employee_low_descending_Success(driver):
        driver.find_element(By.XPATH,"//body[1]/div[1]/div[1]/div[1]/div[2]/div[3]/div[1]/div[1]/div[9]/div[1]/p[1]/button[1]/span[1]").click()
        time.sleep(2)


# %%
def test_Filter_Employee_low_ascending_Success(driver):
        driver.find_element(By.XPATH,"//body[1]/div[1]/div[1]/div[1]/div[2]/div[3]/div[1]/div[1]/div[9]/div[1]/p[1]/button[1]/span[1]").click()
        time.sleep(2)

# %%
def test_Filter_Employee_status_ascending_Success(driver):
        driver.find_element(By.XPATH,"//body[1]/div[1]/div[1]/div[1]/div[2]/div[3]/div[1]/div[1]/div[10]/div[1]/p[1]/button[1]/span[1]").click()
        time.sleep(2)


# %%
def test_Filter_Employee_status_descending_Success(driver):
        driver.find_element(By.XPATH,"//body[1]/div[1]/div[1]/div[1]/div[2]/div[3]/div[1]/div[1]/div[10]/div[1]/p[1]/button[1]/span[1]").click()
        time.sleep(2)

# %%
def test_Filter_Employee_employeeid_descending_Success(driver):
        driver.find_element(By.XPATH,"//body[1]/div[1]/div[1]/div[1]/div[2]/div[3]/div[1]/div[2]/div[1]/div[1]/p[1]/button[1]/span[1]").click()
        time.sleep(2)


# %%
def test_Filter_Employee_employeeid_ascending_Success(driver):
        driver.find_element(By.XPATH,"//body[1]/div[1]/div[1]/div[1]/div[2]/div[3]/div[1]/div[2]/div[1]/div[1]/p[1]/button[1]/span[1]").click()
        time.sleep(2)


# %%
def test_Filter_Employee_Refresh_Success(driver):
        driver.find_element(By.XPATH,"//p[normalize-space()='Refresh']").click()
        time.sleep(2)


# %%
def test_employee_return_arrow(driver):
        return_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//img[@src='/src/assets/back.png']"))
        )
        assert not return_button.get_attribute("disabled"), "Return button should be enabled"
        return_button.click()

        dashboard_header = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h1[normalize-space()='Dashboard']"))
        )
        assert dashboard_header.text == "Dashboard", "Dashboard header text is incorrect"


# %%
def Employee_Webpage():
        driver = login_and_navigate_employee("ruderaw", "abcdefg", "9632")
        test_functions = [
        test_Filter_Employee_Name_ascending_Success(driver),
        test_Filter_Employee_Name_descending_Success(driver),
        test_Filter_Employee_ID_ascending_Success(driver),
        test_Filter_Employee_ID_descending_Success(driver),
        test_Filter_Employee_phone_ascending_Success(driver),
        test_Filter_Employee_phone_descending_Success(driver),
        test_Filter_Employee_email_ascending_Success(driver),
        test_Filter_Employee_email_descending_Success(driver),
        test_Filter_Employee_role_ascending_Success(driver),
        test_Filter_Employee_role_descending_Success(driver),
        test_Filter_Employee_panno_ascending_Success(driver),
        test_Filter_Employee_panno_descending_Success(driver),
        test_Filter_Employee_low_ascending_Success(driver),
        test_Filter_Employee_low_descending_Success(driver),
        test_Filter_Employee_employeeid_ascending_Success(driver),
        test_Filter_Employee_employeeid_descending_Success(driver),
        test_Filter_Employee_Name_StartsWith_Success(driver),
        test_Filter_Employee_Name_EndsWith_Success(driver),
        test_Filter_Employee_Name_EqualTo_Success(driver),
        test_Filter_Employee_Name_isNull_Success(driver),
        test_Filter_Employee_Name_isNotNull_Success(driver),
        test_Filter_Employee_Name_Contains_Success(driver),
        test_Filter_Employee_Name_DoesNotContains_Success(driver),
        test_Filter_Employee_Name_NoFilter_Success(driver),
        test_Filter_Employee_ID_StartsWith_Success(driver),
        test_Filter_Employee_ID_EndsWith_Success(driver),
        test_Filter_Employee_ID_EqualsTo_Success(driver),
        test_Filter_Employee_ID_isNull_Success(driver),
        test_Filter_Employee_ID_isNotNull_Success(driver),
        test_Filter_Employee_ID_Contains_Success(driver),
        test_Filter_Employee_ID_DoesNotContains_Success(driver),
        test_Filter_Employee_ID_NoFilter_Success(driver),
        test_Filter_Employee_PhoneID_Contains_Success(driver),
        test_Filter_Employee_PhoneID_DoesNotContains_Success(driver),
        test_Filter_Employee_PhoneID_StartsWith_Success(driver),
        test_Filter_Employee_PhoneID_EndsWith_Success(driver),
        test_Filter_Employee_PhoneID_EqualsTo_Success(driver),
        test_Filter_Employee_PhoneID_isNull_Success(driver),
        test_Filter_Employee_PhoneID_isNotNull_Success(driver),
        test_Filter_Employee_PhoneID_NoFilter_Success(driver),
        test_Filter_Employee_EmailID_StartsWith_Success(driver),
        test_Filter_Employee_EmailID_EndsWith_Success(driver),
        test_Filter_Employee_EmailID_EqualsTo_Success(driver),
        test_Filter_Employee_EmailID_isNull_Success(driver),
        test_Filter_Employee_EmailID_isNotNull_Success(driver),
        test_Filter_Employee_EmailID_Contains_Success(driver),
        test_Filter_Employee_EmailID_DoesNotContains_Success(driver),
        test_Filter_Employee_EmailID_NoFilter_Success(driver),
        test_Filter_Employee_Roles_StartsWith_Success(driver),
        test_Filter_Employee_Roles_EndsWith_Success(driver),
        test_Filter_Employee_Roles_EqualsTo_Success(driver),
        test_Filter_Employee_Roles_isNull_Success(driver),
        test_Filter_Employee_Roles_isNotNull_Success(driver),
        test_Filter_Employee_Roles_Contains_Success(driver),
        test_Filter_Employee_Roles_DoesNotContains_Success(driver),
        test_Filter_Employee_Roles_NoFilter_Success(driver),
        test_Filter_Employee_Panno_StartsWith_Success(driver),
        test_Filter_Employee_Panno_EndsWith_Success(driver),
        test_Filter_Employee_Panno_EqualsTo_Success(driver),
        test_Filter_Employee_Panno_isNull_Success(driver),
        test_Filter_Employee_Panno_isNotNull_Success(driver),
        test_Filter_Employee_Panno_Contains_Success(driver),
        test_Filter_Employee_Panno_DoesNotContains_Success(driver),
        test_Filter_Employee_Panno_NoFilter_Success(driver),
        test_Filter_Employee_doj_EqualsTo_Success(driver),
        test_Filter_Employee_doj_NotEqualTo_Success(driver),
        test_Filter_Employee_doj_GreaterThan_Success(driver),
        test_Filter_Employee_doj_LessThan_Success(driver),
        test_Filter_Employee_doj_GreaterThanOrEqualTo_Success(driver),
        test_Filter_Employee_doj_LessThanOrEqualTo_Success(driver),
        test_Filter_Employee_doj_isNotNull_Success(driver),
        test_Filter_Employee_doj_isNull_Success(driver),
        test_Filter_Employee_doj_NoFilter_Success(driver),
        test_Filter_Employee_low_EqualsTo_Success(driver),
        test_Filter_Employee_low_NotEqualTo_Success(driver),
        test_Filter_Employee_low_GreaterThan_Success(driver),
        test_Filter_Employee_low_LessThan_Success(driver),
        test_Filter_Employee_low_GreaterThanOrEqualTo_Success(driver),
        test_Filter_Employee_low_LessThanOrEqualTo_Success(driver),
        test_Filter_Employee_low_isNotNull_Success(driver),
        test_Filter_Employee_low_NoFilter_Success(driver),
        test_Filter_Employee_low_isNull_Success(driver),
        test_Filter_Employee_status_EqualsTo_Success(driver),
        test_Filter_Employee_status_NotEqualsTo_Success(driver),
        test_Filter_Employee_status_GreaterThan_Success(driver),
        test_Filter_Employee_status_LessThan_Success(driver),
        test_Filter_Employee_status_GreaterThanOrEqualTo_Success(driver),
        test_Filter_Employee_status_LessThanOrEqualTo_Success(driver),
        test_Filter_Employee_status_isNotNull_Success(driver),
        test_Filter_Employee_status_isNull_Success(driver),
        test_Filter_Employee_status_NoFilter_Success(driver),
        test_Filter_Employee_employee_id_EqualsTo_Success(driver),
        test_Filter_Employee_employee_id_NotEqualsTo_Success(driver),
        test_Filter_Employee_employee_id_GreaterThan_Success(driver),
        test_Filter_Employee_employee_id_LessThan_Success(driver),
        test_Filter_Employee_employee_id_GreaterThanOrEqualTo_Success(driver),
        test_Filter_Employee_employee_id_LessThanOrEqualTo_Success(driver),
        test_Filter_Employee_employee_id_isNotNull_Success(driver),
        test_Filter_Employee_employee_id_isNull_Success(driver),
        test_Filter_Employee_employee_id_NoFilter_Success(driver),
        test_Filter_Employee_Pagination15_NoFilter_Success(driver),
        test_Filter_Employee_Pagination25_NoFilter_Success(driver),
        test_Filter_Employee_Pagination50_NoFilter_Success(driver),
        test_Filter_Employee_Refresh_Success(driver),
        add_new_employee(driver, "aryan ashish", "ijklmn", "Admin User", "06-05-2024", "intern", "ashish.com", "06-05-2003", "31-05-2024", "Admin", "11100000", "UAE", "UAE", "Dubai", "q", "Z-CASH"),
        test_Edit_Employee_Success(driver)
    ]
    
        for func_test in test_functions:
          func_test
        
Employee_Webpage()

def login_and_navigate_city(username, password, comkey):
    driver = webdriver.Chrome()
    driver.get(drivers_config["login_url"])
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.NAME, "comkey").send_keys(comkey)
    login_button = driver.find_element(By.CSS_SELECTOR, "button[class='bg-[#004DD7] w-[200px] h-[35px] text-white text-[18px] rounded-lg cursor-pointer']")
    assert not login_button.get_attribute("disabled"), "Login button should be enabled"
    login_button.click()
    admin_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div:nth-child(2) div:nth-child(1) button:nth-child(1) p:nth-child(1)"))
        )
    assert not admin_button.get_attribute("disabled"), "Admin button should be enabled"
    admin_button.click()
    driver.find_element(By.XPATH,"//a[normalize-space()='City']").click()
    time.sleep(2)
    return driver

def filter_city_country_Contains_Success(driver):
    filter_Common(
        driver,
        "//h1[normalize-space()='Contains']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "i"
    )
    filtered_elements = driver.find_elements(By.XPATH,"//div[@class='w-[20%]  p-4'][position()=1]")
    element_found = True 
    for item in filtered_elements[2:]:
        if "i" not in item.text:
            element_found = False
            break

    if element_found:
        print("Contains filter in City with Country Name is working fine.")
    else:
        print("Error.")

    
def filter_city_country_DoesNotContains_Success(driver):
    filter_Common(
        driver,
        "//h1[normalize-space()='DoesNotContain']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "India"
    )
    filtered_elements = driver.find_elements(By.XPATH,"//div[@class='w-[20%]  p-4'][position()=1]")
    element_found = False
    for item in filtered_elements[2:]:
        if item.text == "India":
            element_found = True
            break

    if not element_found:
        print("DoesNotContains Filter in City with Country Name is Working fine.")
    else:
        print("Error.")

    


def filter_city_country_StartsWith_Success(driver):
    filter_Common(
        driver,
        "//h1[normalize-space()='StartsWith']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "i"
    )
    filtered_elements = driver.find_elements(By.XPATH,"//div[@class='w-[20%]  p-4'][position()=1]")
    element_found = True
    for item in filtered_elements[2:]:
        if not item.text.lower().startswith("i"):
            element_found = False
            break

    if element_found:
        print("StartsWith filter in City with Country Name is working fine.")
    else:
        print("Error.")

    

def filter_city_country_EndsWith_Success(driver):
    filter_Common(
        driver,
        "//h1[normalize-space()='EndsWith']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "a"
    )
    filtered_elements = driver.find_elements(By.XPATH,"//div[@class='w-[20%]  p-4'][position()=1]")
    element_found = True
    for item in filtered_elements[2:]:
        if not item.text.endswith("a"):
            element_found = False
            break

    if element_found:
        print("EndsWith filter in City with Country Name is working fine.")
    else:
        print("Error.")


    
def filter_city_country_EqualTo_Success(driver):
    filter_Common(
        driver,
        "//h1[normalize-space()='EndsWith']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "India"
    )
    filtered_elements = driver.find_elements(By.XPATH,"//div[@class='w-[20%]  p-4'][position()=1]")
    element_found = True
    for item in filtered_elements[2:]:
        if item.text != "India":
            element_found = False
            break

    if element_found:
        print("EqualsTo filter in City with Country Name is working fine.")
    else:
        print("Error")

    

def filter_city_country_isNull_Success(driver):
    filter_Common(
        driver,
        "//h1[normalize-space()='isNull']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "India"
    )
    a=driver.find_element(By.XPATH,"//p[normalize-space()='0 Items in 0 Pages']").text
    words = a[:2]
    filtered_element = driver.find_element(By.XPATH,"//p[normalize-space()='0 Items in 0 Pages']")
    if(filtered_element.text.startswith(words)):
            print("isNull filter in City With Country Name is working fine")

    

def filter_city_country_isNotNull_Success(driver):
    filter_Common(
        driver,
        "//h1[normalize-space()='isNotNull']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "India"
    )
    a=driver.find_element(By.XPATH,"//p[normalize-space()='196 Items in 14 Pages']").text
    words = a[:2]
    filtered_element = driver.find_element(By.XPATH,"//p[normalize-space()='196 Items in 14 Pages']")
    if(filtered_element.text.startswith(words)):
            print("isNotNull filter in City With Country Name is working fine")

    
def filter_city_country_NoFilter_Success(driver):
    filter_Common(
        driver,
        "//h1[normalize-space()='No Filter']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "India"
    )
    a=driver.find_element(By.XPATH,"//p[normalize-space()='196 Items in 14 Pages']").text
    words = a[:2]
    filtered_element = driver.find_element(By.XPATH,"//p[normalize-space()='196 Items in 14 Pages']")
    if(filtered_element.text.startswith(words)):
            print("NOfilter in City With Country Name is working fine")
    

def filter_city_state_Contains_Success(driver):
    filter_Common(
        driver,
        "//h1[normalize-space()='Contains']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "u"
    )
    filtered_elements = driver.find_elements(By.XPATH,"//div[@class='w-[20%]  p-4'][position()=2]")
    element_found = True 
    for item in filtered_elements[2:]:
        if "u" not in item.text.lower():
            element_found = False
            break

    if element_found:
        print("Contains filter in City with State Name is working fine.")
    else:
        print("Error.")

    
def filter_city_state_DoesNotContains_Success(driver):
    filter_Common(
        driver,
        "//h1[normalize-space()='DoesNotContain']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "Oman"
    )
    filtered_elements = driver.find_elements(By.XPATH,"//div[@class='w-[20%]  p-4'][position()=2]")
    element_found = False
    for item in filtered_elements[2:]:
        if item.text == "Oman":
            element_found = True
            break

    if not element_found:
        print("DoesNotContains Filter in City with State Name is Working fine.")
    else:
        print("Error.")

    

def filter_city_state_StartsWith_Success(driver):
    filter_Common(
        driver,
        "//h1[normalize-space()='StartsWith']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "m"
    )
    filtered_elements = driver.find_elements(By.XPATH,"//div[@class='w-[20%]  p-4'][position()=2]")
    element_found = True
    for item in filtered_elements[2:]:
        if not item.text.lower().startswith("m"):
            element_found = False
            break

    if element_found:
        print("StartsWith filter in City with State Name is working fine.")
    else:
        print("Error.")

    
def filter_city_state_EndsWith_Success(driver):
    filter_Common(
        driver,
        "//h1[normalize-space()='EndsWith']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "m"
    )
    filtered_elements = driver.find_elements(By.XPATH,"//div[@class='w-[20%]  p-4'][position()=2]")
    element_found = True
    for item in filtered_elements[2:]:
        if not item.text.endswith("m"):
            element_found = False
            break

    if element_found:
        print("EndsWith filter in City with State Name is working fine.")
    else:
        print("Error.")

    
def filter_city_state_EqualsTo_Success(driver):
    filter_Common(
        driver,
        "//h1[normalize-space()='EqualTo']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "Oman"
    )
    filtered_elements = driver.find_elements(By.XPATH,"//div[@class='w-[20%]  p-4'][position()=2]")
    element_found = True
    for item in filtered_elements[2:]:
        if item.text != "Oman":
            element_found = False
            break

    if element_found:
        print("EqualsTo filter in City with State Name is working fine.")
    else:
        print("Error")

    
def filter_city_state_isNull_Success(driver):
    filter_Common(
        driver,
        "//h1[normalize-space()='isNull']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "Oman"
    )
    a=driver.find_element(By.XPATH,"//p[normalize-space()='0 Items in 0 Pages']").text
    words = a[:2]
    filtered_element = driver.find_element(By.XPATH,"//p[normalize-space()='0 Items in 0 Pages']")
    if(filtered_element.text.startswith(words)):
            print("isNull filter in City With State Name is working fine")

    
def filter_city_state_isNotNull_Success(driver):
    filter_Common(
        driver,
        "//h1[normalize-space()='isNotNull']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "Oman"
    )
    a=driver.find_element(By.XPATH,"//p[normalize-space()='196 Items in 14 Pages']").text
    words = a[:2]
    filtered_element = driver.find_element(By.XPATH,"//p[normalize-space()='196 Items in 14 Pages']")
    if(filtered_element.text.startswith(words)):
            print("isNotNull filter in City With State Name is working fine")

    
def filter_city_state_NoFilter_Success(driver):
    filter_Common(
        driver,
        "//h1[normalize-space()='No Filter']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "Oman"
    )
    a=driver.find_element(By.XPATH,"//p[normalize-space()='196 Items in 14 Pages']").text
    words = a[:2]
    filtered_element = driver.find_element(By.XPATH,"//p[normalize-space()='196 Items in 14 Pages']")
    if(filtered_element.text.startswith(words)):
            print("No filter in City With State Name is working fine")

    
def filter_city_City_Contains_Success(driver):
    filter_Common(
        driver,
        "//h1[normalize-space()='Contains']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "o"
    )
    filtered_elements = driver.find_elements(By.XPATH,"//div[@class='w-[25%]  p-4']")
    element_found = True 
    for item in filtered_elements[2:]:
        if "o" not in item.text.lower():
            element_found = False
            break

    if element_found:
        print("Contains filter in City with City Name is working fine.")
    else:
        print("Error.")

    
def filter_city_City_DoesNotContains_Success(driver):
    filter_Common(
        driver,
        "//h1[normalize-space()='DoesNotContain']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "o"
    )
    filtered_elements = driver.find_elements(By.XPATH,"//div[@class='w-[25%]  p-4']")
    element_found = False
    for item in filtered_elements[2:]:
        if item.text == "o":
            element_found = True
            break

    if not element_found:
        print("DoesNotContains Filter in City with City Name is Working fine.")
    else:
        print("Error.")

    
def filter_city_City_StartsWith_Success(driver):
    filter_Common(
        driver,
        "//h1[normalize-space()='StartsWith']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "m"
    )
    filtered_elements = driver.find_elements(By.XPATH,"//div[@class='w-[25%]  p-4']")
    element_found = True
    for item in filtered_elements[2:]:
        if not item.text.lower().startswith("m"):
            element_found = False
            break

    if element_found:
        print("StartsWith filter in City with City Name is working fine.")
    else:
        print("Error.")

    
def filter_city_City_EndssWith_Success(driver):
    filter_Common(
        driver,
        "//h1[normalize-space()='EndsWith']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "m"
    )
    filtered_elements = driver.find_elements(By.XPATH,"//div[@class='w-[25%]  p-4']")
    element_found = True
    for item in filtered_elements[2:]:
        if not item.text.endswith("m"):
            element_found = False
            break

    if element_found:
        print("EndsWith filter in City with City Name is working fine.")
    else:
        print("Error.")

    

def filter_city_City_EqualsTo_Success(driver):
    filter_Common(
        driver,
        "//h1[normalize-space()='EqualTo']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "Pune"
    )
    filtered_elements = driver.find_elements(By.XPATH,"//div[@class='w-[25%]  p-4']")
    element_found = True
    for item in filtered_elements[2:]:
        if item.text != "Pune":
            element_found = False
            break

    if element_found:
        print("EqualsTo filter in City with City Name is working fine.")
    else:
        print("Error")

    
def filter_city_City_isNull_Success(driver):
    filter_Common(
        driver,
        "//h1[normalize-space()='isNull']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "Pune"
    )
    a=driver.find_element(By.XPATH,"//p[normalize-space()='0 Items in 0 Pages']").text
    words = a[:2]
    filtered_element = driver.find_element(By.XPATH,"//p[normalize-space()='0 Items in 0 Pages']")
    if(filtered_element.text.startswith(words)):
            print("isNull filter in City With State Name is working fine")

    

def filter_city_City_isNotNull_Success(driver):
    filter_Common(
        driver,
        "//h1[normalize-space()='isNotNull']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "Pune"
    )
    a=driver.find_element(By.XPATH,"//p[normalize-space()='196 Items in 14 Pages']").text
    words = a[:2]
    filtered_element = driver.find_element(By.XPATH,"//p[normalize-space()='196 Items in 14 Pages']")
    if(filtered_element.text.startswith(words)):
            print("isNotNull filter in City With City Name is working fine")


    
def filter_city_City_NoFilter_Success(driver):
    filter_Common(
        driver,
        "//h1[normalize-space()='No Filter']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "Pune"
    )
    a=driver.find_element(By.XPATH,"//p[normalize-space()='196 Items in 14 Pages']").text
    words = a[:2]
    filtered_element = driver.find_element(By.XPATH,"//p[normalize-space()='196 Items in 14 Pages']")
    if(filtered_element.text.startswith(words)):
            print("No filter in City With City Name is working fine")



def filter_city_ID_EqualsTo_Success(driver):
    filter_Common(
        driver,
        "//h1[normalize-space()='EqualTo']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "1808"
    )
    filtered_elements = driver.find_elements(By.XPATH,"//div[@class='w-1/2  p-4']")
    element_found = True
    for item in filtered_elements[2:]:
        if item.text != "1808":
            element_found = False
            break

    if element_found:
        print("EqualTo filter in City with ID is working fine")
    else:
        print("Error")
    

def filter_city_ID_NotEqualsTo_Success(driver):
    filter_Common(
        driver,
        "//h1[normalize-space()='NotEqualTo']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "1808"
    )
    filtered_elements = driver.find_elements(By.XPATH,"//div[@class='w-1/2  p-4']")
    element_found = True
    for item in filtered_elements[2:]:
        if item.text == "1808":
            element_found = False
            break

    if element_found:
        print("NotEqualTo Filter in City with ID is working fine.")
    else:
        print("Error.")

    
def filter_city_ID_GreaterThan_Success(driver):
    filter_Common(
        driver,
        "//h1[normalize-space()='GreaterThan']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "1808"
    )
    filtered_elements = driver.find_elements(By.XPATH,"//div[@class='w-1/2  p-4']")
    element_found = True
    for item in filtered_elements[2:]:
        if item.text <= '1808':
            element_found = False
            break

    if element_found:
        print("Greater Than Filter in City with ID is working fine.")
    else:
        print("Error.")

    
def filter_city_ID_LessThan_Success(driver):
    filter_Common(
        driver,
        "//h1[normalize-space()='LessThan']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "1808"
    )
    filtered_elements = driver.find_elements(By.XPATH,"//div[@class='w-1/2  p-4']")
    element_found = True
    for item in filtered_elements[2:]:
        if item.text >= "1808":
            element_found = False
            break

    if element_found:
        print("LessThan Filter in City with ID is working fine.")
    else:
        print("Error")

    
def filter_city_ID_GreaterThanOrEqual_Success(driver):
    filter_Common(
        driver,
        "//h1[normalize-space()='GreaterThanOrEqualTo']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "1808"
    )
    filtered_elements = driver.find_elements(By.XPATH,"//div[@class='w-1/2  p-4']")
    element_found = True
    for item in filtered_elements[2:]:
        if item.text < "1808":
            element_found = False
            break

    if element_found:
        print("GreaterThanOrEqualTo Filter in City with ID is working fine")
    else:
        print("Error")

    

def filter_city_ID_LessThanOrEqual_Success(driver):
    filter_Common(
        driver,
        "//h1[normalize-space()='LessThanOrEqualTo']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "1808"
    )
    filtered_elements = driver.find_elements(By.XPATH,"//div[@class='w-1/2  p-4']")
    element_found = True
    for item in filtered_elements[2:]:
        if item.text > "1808":
            element_found = False
            break

    if element_found:
        print("LessThanOrEqualTo Filter in City with ID is working fine")
    else:
        print("Error")
    


def filter_city_ID_isNull_Success(driver):
    filter_Common(
        driver,
        "//h1[normalize-space()='isNull']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "1808"
    )
    a=driver.find_element(By.XPATH,"//p[@class='mr-11 text-gray-700']").text
    words = a[:2]
    filtered_element = driver.find_element(By.XPATH,"//p[@class='mr-11 text-gray-700']")
    element_found = False
    if filtered_element.text.startswith(words):
        element_found = True

    if element_found:
        print("isNull Filter in ID is working fine")
    else:
        print("Error")

    

def filter_city_ID_isNotNull_Success(driver):
    filter_Common(
        driver,
        "//h1[normalize-space()='isNotNull']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "1808"
    )
    a=driver.find_element(By.XPATH,"//p[@class='mr-11 text-gray-700']").text
    words = a[:2]
    filtered_element = driver.find_element(By.XPATH,"//p[@class='mr-11 text-gray-700']")
    element_found = False
    if filtered_element.text.startswith(words):
        element_found = True

    if element_found:
        print("isNotNull Filter in ID is working fine")
    else:
        print("Error")

    

def filter_city_ID_NoFilter_Success(driver):
    filter_Common(
        driver,
        "//h1[normalize-space()='No Filter']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "1808"
    )
    a=driver.find_element(By.XPATH,"//p[@class='mr-11 text-gray-700']").text
    words = a[:2]
    filtered_element = driver.find_element(By.XPATH,"//p[@class='mr-11 text-gray-700']")
    element_found = False
    if filtered_element.text.startswith(words):
        element_found = True

    if element_found:
        print("No Filter in ID is working fine")
    else:
        print("Error")

    
def test_Filter_City_Pagination15_Success(driver):
    select_xpath = "//select[@name='currentPages']"
    filter_pagination_Common(driver, select_xpath, '15')
    Number_of_pages = driver.find_elements(By.XPATH, "//div[contains(@class,'w-[10%] p-4')]")
    count = 0
    for pages in Number_of_pages[2:]:
        count += 1

    if count <= 15:  
        print("Pagination for 15 Pages in City is Working fine")


def test_Filter_City_Pagination25_Success(driver):
    select_xpath = "//select[@name='currentPages']"
    filter_pagination_Common(driver, select_xpath, '25')
    Number_of_pages = driver.find_elements(By.XPATH, "//div[contains(@class,'w-[10%] p-4')]")
    count = 0
    for pages in Number_of_pages[2:]:
        count += 1

    if count <= 25:  
        print("Pagination for 25 Pages in City is Working fine")

def test_Filter_City_Pagination50_Success(driver):
    select_xpath = "//select[@name='currentPages']"
    filter_pagination_Common(driver, select_xpath, '50')
    Number_of_pages = driver.find_elements(By.XPATH, "//div[contains(@class,'w-[10%] p-4')]")
    count = 0
    for pages in Number_of_pages[2:]:
        count += 1

    if count <= 50:  
        print("Pagination for 50 Pages in City is Working fine")

def add_City(driver):
    wait=WebDriverWait(driver,10)
    wait.until(EC.element_to_be_clickable((By.XPATH,"//body//div//div//div//div//div//div//div//button//div"))).click()
    time.sleep(2)
    a=driver.find_element(By.XPATH,"//select[@name='country']")
    drp1=Select(a)
    drp1.select_by_visible_text('India')
    driver.find_element(By.XPATH,"//input[@name='state']").send_keys("State01")
    driver.find_element(By.XPATH,"//input[@name='cityName']").send_keys("City01")
    wait.until(EC.element_to_be_clickable((By.XPATH,"//body/div[contains(@role,'presentation')]/div/div/div/button[1]"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH,"//body/div[contains(@role,'presentation')]/div/div/button[1]"))).click()
    time.sleep(4)
    driver.find_element(By.XPATH,"//input[@type='text']").send_keys("India")
    driver.find_element(By.XPATH,"//img[@alt='search-icon']").click()
    wait.until(EC.element_to_be_clickable((By.XPATH,"//div//div//div//div[1]//div[2]//div[2]//button[2]//img[1]"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH,"//button[normalize-space()='Delete']"))).click()
    time.sleep(2)

def edit_City(driver):
    wait=WebDriverWait(driver,10)
    driver.find_element(By.XPATH,"//body//div//div//div//div//div//div//div//button//div").click()
    time.sleep(2)
    a=driver.find_element(By.XPATH,"//select[@name='country']")
    drp1=Select(a)
    drp1.select_by_visible_text('India')
    driver.find_element(By.XPATH,"//input[@name='state']").send_keys("State01")
    driver.find_element(By.XPATH,"//input[@name='cityName']").send_keys("City01")
    wait.until(EC.element_to_be_clickable((By.XPATH,"//body/div[contains(@role,'presentation')]/div/div/div/button[1]"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH,"//body/div[contains(@role,'presentation')]/div/div/button[1]"))).click()
    time.sleep(4)
    driver.find_element(By.XPATH,"//input[@type='text']").clear()
    driver.find_element(By.XPATH,"//input[@type='text']").send_keys("India")
    driver.find_element(By.XPATH,"//img[@alt='search-icon']").click()
    wait.until(EC.element_to_be_clickable((By.XPATH,"//img[@alt='edit']"))).click()
    time.sleep(2)
    driver.find_element(By.XPATH,"//input[@name='cityName']").clear()
    time.sleep(2)
    driver.find_element(By.XPATH,"//input[@name='cityName']").send_keys("City100")
    driver.find_element(By.XPATH,"//button[@type='submit']").click()
    time.sleep(4)
    driver.find_element(By.XPATH,"//input[@type='text']").clear()
    driver.find_element(By.XPATH,"//input[@type='text']").send_keys("City100")
    driver.find_element(By.XPATH,"//img[@alt='search-icon']").click()
    wait.until(EC.element_to_be_clickable((By.XPATH,"//div//div//div//div[1]//div[2]//div[2]//button[2]//img[1]"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH,"//button[normalize-space()='Delete']"))).click()
    time.sleep(2)

def City_Refresh(driver):
    wait=WebDriverWait(driver,10)
    wait.until(EC.element_to_be_clickable((By.XPATH,"//p[normalize-space()='Refresh']"))).click()
    time.sleep(2)


def City_DownloadasExcel(driver):
    wait=WebDriverWait(driver,10)
    wait.until(EC.element_to_be_clickable((By.XPATH,"//p[normalize-space()='Download']"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH,"//p[normalize-space()='Download as Excel']"))).click()
    time.sleep(2)


def City_Country_ascending(driver):
    driver.find_element(By.XPATH,"//body/div/div/div/div/div/div/div/div[2]/p[1]/button[1]/span[1]").click()
    Country_list = driver.find_elements(By.XPATH, "//div[contains(@class,'w-[20%]  p-4')][position()=1]")
    country_names = [country.text for country in Country_list[2:]]

    if is_sorted_ascending_common(country_names):
            print("The country list is sorted in ascending order.")
    else:
            print("The country list is not sorted in ascending order.")
    time.sleep(2)


def City_Country_descending(driver):
    driver.find_element(By.XPATH,"//body/div/div/div/div/div/div/div/div[2]/p[1]/button[1]/span[1]").click()
    Country_list = driver.find_elements(By.XPATH, "//div[contains(@class,'w-[20%]  p-4')][position()=1]")
    country_names = [country.text for country in Country_list[2:]]

    if is_sorted_descending_common(country_names):
            print("The country list is sorted in descending order.")
    else:
            print("The country list is not sorted in descending order.")

    time.sleep(2)


def City_State_descending(driver):
    driver.find_element(By.XPATH,"//div//div//div//div//div//div[3]//p[1]//button[1]//span[1]").click()
    State_list = driver.find_elements(By.XPATH, "//div[contains(@class,'w-[20%]  p-4')][position()=2]")
    State_names = [country.text for country in State_list[2:]]

    if is_sorted_descending_common(State_names):
            print("The state list is sorted in descending order.")
    else:
            print("The state list is not sorted in descending order.")

    time.sleep(2)


def City_State_ascending(driver):
    driver.find_element(By.XPATH,"//div//div//div//div//div//div[3]//p[1]//button[1]//span[1]").click()
    State_list = driver.find_elements(By.XPATH, "//div[contains(@class,'w-[20%]  p-4')][position()=2]")
    State_names = [country.text for country in State_list[2:]]

    if is_sorted_ascending_common(State_names):
            print("The state list is sorted in ascending order.")
    else:
            print("The state list is not sorted in ascending order.")

    time.sleep(2)

def City_Cityname_ascending(driver):
    driver.find_element(By.XPATH,"//div[4]//p[1]//button[1]//span[1]").click()
    City_list = driver.find_elements(By.XPATH, "//div[contains(@class,'w-[25%]  p-4')]")
    city_names = [country.text for country in City_list[2:]]

    if is_sorted_ascending_common(city_names):
            print("The city list is sorted in ascending order.")
    else:
            print("The city list is not sorted in ascending order.")

    time.sleep(2)

def City_Cityname_descending(driver):
    driver.find_element(By.XPATH,"//div[4]//p[1]//button[1]//span[1]").click()
    City_list = driver.find_elements(By.XPATH, "//div[contains(@class,'w-[25%]  p-4')]")
    city_names = [country.text for country in City_list[2:]]

    if is_sorted_descending_common(city_names):
            print("The city list is sorted in descending order.")
    else:
            print("The city list is not sorted in descending order.")

    time.sleep(2)


def City_ID_descending(driver):
    driver.find_element(By.XPATH,"//body/div/div/div/div/div/div/div/div[1]/p[1]/button[1]/span[1]").click()
    ID_list = driver.find_elements(By.XPATH, "//div[contains(@class,'w-1/2  p-4')]")
    ID_names = [country.text for country in ID_list[2:]]

    if is_sorted_descending_common(ID_names):
            print("The city ID is sorted in descending order.")
    else:
            print("The city ID is not sorted in descending order.")

    time.sleep(2)


def City_ID_ascending(driver):
    driver.find_element(By.XPATH,"//body/div/div/div/div/div/div/div/div[1]/p[1]/button[1]/span[1]").click()
    ID_list = driver.find_elements(By.XPATH, "//div[contains(@class,'w-1/2  p-4')]")
    ID_names = [country.text for country in ID_list[2:]]

    if is_sorted_descending_common(ID_names):
            print("The city ID is sorted in ascending order.")
    else:
            print("The city ID is not sorted in ascending order.")

    time.sleep(2)

def City_webpage():
       driver=login_and_navigate_city("ruderaw", "abcdefg", "9632")
      
       test_functions=[
            City_Country_ascending,
            City_Country_descending,
            City_State_ascending,
            City_State_descending,
            City_Cityname_ascending,
            City_Cityname_descending,
            City_ID_ascending,
            City_ID_descending,
            filter_city_country_Contains_Success,
            filter_city_country_DoesNotContains_Success,
            filter_city_country_StartsWith_Success,
            filter_city_country_EndsWith_Success,
            filter_city_country_EqualTo_Success,
            filter_city_country_isNull_Success,
            filter_city_country_isNotNull_Success,
            filter_city_country_NoFilter_Success,
            filter_city_state_Contains_Success,
            filter_city_state_DoesNotContains_Success,
            filter_city_state_StartsWith_Success,
            filter_city_state_EndsWith_Success,
            filter_city_state_EqualsTo_Success,
            filter_city_state_isNull_Success,
            filter_city_state_isNotNull_Success,
            filter_city_state_NoFilter_Success,
            filter_city_City_Contains_Success,
            filter_city_City_DoesNotContains_Success,
            filter_city_City_StartsWith_Success,
            filter_city_City_EndssWith_Success,
            filter_city_City_EqualsTo_Success,
            filter_city_City_isNull_Success,
            filter_city_City_isNotNull_Success,
            filter_city_City_NoFilter_Success,
            filter_city_ID_EqualsTo_Success,
            filter_city_ID_NotEqualsTo_Success,
            filter_city_ID_GreaterThan_Success,
            filter_city_ID_LessThan_Success,
            filter_city_ID_GreaterThanOrEqual_Success,
            filter_city_ID_LessThanOrEqual_Success,
            filter_city_ID_isNull_Success,
            filter_city_ID_isNotNull_Success,
            filter_city_ID_NoFilter_Success,
            test_Filter_City_Pagination15_Success,
            test_Filter_City_Pagination25_Success,
            test_Filter_City_Pagination50_Success,
            add_City,
            edit_City,
            City_Refresh,
            City_DownloadasExcel
            
       ]
       for test in test_functions:
            test(driver)

       time.sleep(2)



City_webpage()

    
def login_and_navigate_LOB(username, password, comkey):
    driver = webdriver.Chrome()
    driver.get(drivers_config["login_url"])
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.NAME, "comkey").send_keys(comkey)
    login_button = driver.find_element(By.CSS_SELECTOR, "button[class='bg-[#004DD7] w-[200px] h-[35px] text-white text-[18px] rounded-lg cursor-pointer']")
    assert not login_button.get_attribute("disabled"), "Login button should be enabled"
    login_button.click()
    admin_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div:nth-child(2) div:nth-child(1) button:nth-child(1) p:nth-child(1)"))
        )
    assert not admin_button.get_attribute("disabled"), "Admin button should be enabled"
    admin_button.click()
    driver.find_element(By.XPATH,"//a[normalize-space()='LOB (Line of business)']").click()
    time.sleep(2)
    return driver

def test_Add_New_LOB_Success(driver):
        wait=WebDriverWait(driver,10)
        addLOB_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".flex.items-center.justify-center.gap-4"))
        )
        assert not addLOB_button.get_attribute("disabled"), "Lob button should be enabled"
        addLOB_button.click()

        addLOB_header = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div:nth-child(3) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)"))
        )
        assert addLOB_header.text == "New LOB", "Add New LOB header text is incorrect"
        driver.find_element(By.XPATH,"//input[@name='empName']").send_keys("aa")
        driver.find_element(By.XPATH,"//button[normalize-space()='Add']").click()
        wait.until(EC.element_to_be_clickable((By.XPATH,"//button[normalize-space()='Add']"))).click()
        time.sleep(2)
        driver.find_element(By.XPATH,"//input[@type='text']").clear()
        time.sleep(2)
        driver.find_element(By.XPATH,"//input[@type='text']").send_keys("aa")
        driver.find_element(By.XPATH,"//img[@alt='search-icon']").click()
        wait.until(EC.element_to_be_clickable((By.XPATH,"//img[@alt='trash']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH,"//button[normalize-space()='Delete']"))).click()
        time.sleep(2)


def test_Edit_LOB_Success(driver):
        wait=WebDriverWait(driver,10)
        driver.find_element(By.XPATH,"//input[@type='text']").clear()
        time.sleep(2)
        addLOB_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".flex.items-center.justify-center.gap-4"))
        )
        assert not addLOB_button.get_attribute("disabled"), "Lob button should be enabled"
        addLOB_button.click()

        addLOB_header = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div:nth-child(3) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)"))
        )
        assert addLOB_header.text == "New LOB", "Add New LOB header text is incorrect"
        time.sleep(2)
        driver.find_element(By.XPATH,"//input[@name='empName']").send_keys("aa")
        wait.until(EC.element_to_be_clickable((By.XPATH,"//button[normalize-space()='Add']"))).click()
        addLOB_header = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='mt-4 w-full text-center'] p[class='text-[14px]']"))
        )
        wait.until(EC.element_to_be_clickable((By.XPATH,"//button[normalize-space()='Add']"))).click()
        # wait.until(EC.element_to_be_clickable((By.XPATH,"//img[@alt='search-icon']"))).click()
        time.sleep(2)
        wait.until(EC.element_to_be_clickable((By.XPATH,"//img[@alt='edit']"))).click()
        driver.find_element(By.XPATH,"//input[@name='empName']").clear()
        driver.find_element(By.XPATH,"//input[@name='empName']").send_keys("ashish")
        driver.find_element(By.XPATH,"//button[normalize-space()='Save']").click()
        time.sleep(4)
        driver.find_element(By.XPATH,"//input[@type='text']").clear()
        time.sleep(2)
        driver.find_element(By.XPATH,"//input[@type='text']").send_keys("ashish")
        wait.until(EC.element_to_be_clickable((By.XPATH,"//img[@alt='search-icon']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH,"//img[@alt='trash']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH,"//button[normalize-space()='Delete']"))).click()
        time.sleep(2)

def test_Filter_LOB_StartsWith_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='StartsWith']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2)",
        "a"
    )
        filtered_elements = driver.find_elements(By.XPATH,"//div[contains(@class,'w-[20%]  p-3 ml-[3px]')]")
        element_found = True
        for item in filtered_elements:
            if not item.text.lower().startswith("a"):
                element_found = False
                break

        if element_found:
            print("StartsWith filter in LOB with LOB Name is working fine.")
        else:
            print("Error.")
        driver.find_element(By.XPATH,"//h1[normalize-space()='LOB']").click()
        time.sleep(2)
        

def test_Filter_LOB_Contains_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='Contains']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2)",
        "a"
    )
        filtered_elements = driver.find_elements(By.XPATH,"//div[contains(@class,'w-[20%]  p-3 ml-[3px]')]")
        element_found = True 
        for item in filtered_elements:
            if "a" not in item.text.lower():
                element_found = False
                break

        if element_found:
            print("Contains filter in LOB with LOB Name is working fine.")
        else:
            print("Error.")
        driver.find_element(By.XPATH,"//h1[normalize-space()='LOB']").click()
        time.sleep(2)
        

def test_Filter_LOB_DoesNotContain_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='DoesNotContain']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2)",
        "a"
    )
        filtered_elements = driver.find_elements(By.XPATH,"//div[contains(@class,'w-[20%]  p-3 ml-[3px]')]")
        element_found = False
        for item in filtered_elements:
            if item.text == "a":
                element_found = True
                break

        if not element_found:
            print("DoesNotContains Filter in LOB with LOB Name is Working fine.")
        else:
            print("Error.")
        driver.find_element(By.XPATH,"//div[contains(@class,'flex text-sm')]").click()
        time.sleep(2)


def test_Filter_LOB_EndsWith_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='EndsWith']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2)",
        "a"
    )
        filtered_elements = driver.find_elements(By.XPATH,"//div[contains(@class,'w-[20%]  p-3 ml-[3px]')]")
        element_found = True
        for item in filtered_elements:
            if not item.text.endswith("a"):
                element_found = False
                break

        if element_found:
            print("EndsWith filter in LOB with LOB Name is working fine.")
        else:
            print("Error.")
        driver.find_element(By.XPATH,"//div[contains(@class,'flex text-sm')]").click()
        time.sleep(2)


def test_Filter_LOB_EqualTo_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='EqualTo']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2)",
        "Builder Sale"
    )
        filtered_elements = driver.find_elements(By.XPATH,"//div[contains(@class,'w-[20%]  p-3 ml-[3px]')]")
        element_found = True
        for item in filtered_elements:
            if item.text != "Builder Sale":
                element_found = False
                break

        if element_found:
            print("EqualsTo filter in City with Country Name is working fine.")
        else:
            print("Error")
        driver.find_element(By.XPATH,"//div[@class='flex text-sm']").click()
        time.sleep(2)
        

def test_Filter_LOB_isNull_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='isNull']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2)",
        "a"
    )
        a=driver.find_element(By.XPATH,"//p[@class='mr-11 text-gray-700']").text
        words = a[:2]
        filtered_element = driver.find_element(By.XPATH,"//p[@class='mr-11 text-gray-700']")
        if(filtered_element.text.startswith(words)):
                print("isNull filter in LOB With LOB Name is working fine")
        driver.find_element(By.XPATH,"//h1[normalize-space()='LOB']").click()
        time.sleep(2)

def test_Filter_LOB_isNotNull_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='isNotNull']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2)",
        "a"
    )
        a=driver.find_element(By.XPATH,"//p[@class='mr-11 text-gray-700']").text
        words = a[:2]
        filtered_element = driver.find_element(By.XPATH,"//p[@class='mr-11 text-gray-700']")
        if(filtered_element.text.startswith(words)):
                print("isNotNull filter in LOB With LOB Name is working fine")
        driver.find_element(By.XPATH,"//h1[normalize-space()='LOB']").click()
        time.sleep(2)


def test_Filter_LOB_Nofilter_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='No Filter']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2)",
        "a"
    )
        a=driver.find_element(By.XPATH,"//p[@class='mr-11 text-gray-700']").text
        words = a[:2]
        filtered_element = driver.find_element(By.XPATH,"//p[@class='mr-11 text-gray-700']")
        if(filtered_element.text.startswith(words)):
                print("No filter in LOB With LOB Name is working fine")
        driver.find_element(By.XPATH,"//h1[normalize-space()='LOB']").click()
        time.sleep(2)


def test_Filter_ID_LOB_Equalto_Success(driver):        
        filter_Common(
        driver,
        "//h1[normalize-space()='EqualTo']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2)",
        "12"
    )
        filtered_elements = driver.find_elements(By.XPATH,"//div[@class='w-1/2 p-3 flex ml-[9px]']")
        element_found = True
        for item in filtered_elements:
            if item.text != "12":
                element_found = False
                break

        if element_found:
            print("EqualTo filter in LOB with ID is working fine")
        else:
            print("Error")
        driver.find_element(By.XPATH,"//h1[normalize-space()='LOB']").click()
        time.sleep(2)
    

def test_Filter_ID_LOB_NotEqualTo_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='NotEqualTo']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2)",
        "12"
    )
        filtered_elements = driver.find_elements(By.XPATH,"//div[@class='w-1/2 p-3 flex ml-[9px]']")
        element_found = True
        for item in filtered_elements:
            if item.text == "12":
                element_found = False
                break

        if element_found:
            print("NotEqualTo Filter in LOB with ID is working fine.")
        else:
            print("Error.")
        driver.find_element(By.XPATH,"//h1[normalize-space()='LOB']").click()
        time.sleep(2)
    

def test_Filter_ID_LOB_GreaterThan_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='GreaterThan']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2)",
        "12"
    )
        filtered_elements = driver.find_elements(By.XPATH,"//div[@class='w-1/2 p-3 flex ml-[9px]']")
        element_found = True
        for item in filtered_elements:
            if item.text <= '12':
                element_found = False
                break

        if element_found:
            print("Greater Than Filter in LOB with ID is working fine.")
        else:
            print("Error.")
        driver.find_element(By.XPATH,"//h1[normalize-space()='LOB']").click()
        time.sleep(2)
    

def test_Filter_ID_LOB_GreaterThanOrEqualTo_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='GreaterThanOrEqualTo']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2)",
        "12"
    )
        filtered_elements = driver.find_elements(By.XPATH,"//div[@class='w-1/2 p-3 flex ml-[9px]']")
        element_found = True
        for item in filtered_elements:
            if item.text < "12":
                element_found = False
                break

        if element_found:
            print("GreaterThanOrEqualTo Filter in LOB with ID is working fine")
        else:
            print("Error")
        driver.find_element(By.XPATH,"//h1[normalize-space()='LOB']").click()
        time.sleep(2)


def test_Filter_ID_LOB_LessThan_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='LessThan']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2)",
        "12"
    )
        filtered_elements = driver.find_elements(By.XPATH,"//div[@class='w-1/2 p-3 flex ml-[9px]']")
        element_found = True
        for item in filtered_elements:
            if int(item.text) >= 12:
                element_found = False
                break

        if element_found:
            print("LessThan Filter in LOB with ID is working fine.")
        else:
            print("Error")
        driver.find_element(By.XPATH,"//h1[normalize-space()='LOB']").click()
        time.sleep(2)


def test_Filter_ID_LOB_LessThanOrEqualTo_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='LessThanOrEqualTo']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2)",
        "12"
    )
        filtered_elements = driver.find_elements(By.XPATH,"//div[@class='w-1/2 p-3 flex ml-[9px]']")
        element_found = True
        for item in filtered_elements:
            if int(item.text) > 12:
                element_found = False
                break

        if element_found:
            print("LessThanOrEqualTo Filter in LOB with ID is working fine")
        else:
            print("Error")
        driver.find_element(By.XPATH,"//h1[normalize-space()='LOB']").click()
        time.sleep(2)


def test_Filter_ID_LOB_isNull_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='isNull']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2)",
        "12"
    )
        a=driver.find_element(By.XPATH,"//p[@class='mr-11 text-gray-700']").text
        words = a[:2]
        filtered_element = driver.find_element(By.XPATH,"//p[@class='mr-11 text-gray-700']")
        if(filtered_element.text.startswith(words)):
                print("isNull filter in LOB With ID is working fine")
        driver.find_element(By.XPATH,"//h1[normalize-space()='LOB']").click()
        time.sleep(2)
       


def test_Filter_ID_LOB_isNotNull_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='isNotNull']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2)",
        "12"
    )
        a=driver.find_element(By.XPATH,"//p[@class='mr-11 text-gray-700']").text
        words = a[:2]
        filtered_element = driver.find_element(By.XPATH,"//p[@class='mr-11 text-gray-700']")
        if(filtered_element.text.startswith(words)):
                print("isNotNull filter in LOB With ID is working fine")
        driver.find_element(By.XPATH,"//h1[normalize-space()='LOB']").click()
        time.sleep(2)
    


def test_Filter_ID_LOB_NoFilter_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='No Filter']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2)",
        "12"
    )
        a=driver.find_element(By.XPATH,"//p[@class='mr-11 text-gray-700']").text
        words = a[:2]
        filtered_element = driver.find_element(By.XPATH,"//p[@class='mr-11 text-gray-700']")
        if(filtered_element.text.startswith(words)):
                print("NO filter in LOB With ID is working fine")
        driver.find_element(By.XPATH,"//h1[normalize-space()='LOB']").click()
        time.sleep(2)

def test_Filter_LOB_Pagination_15_Success(driver):
        select_xpath = "//select[@name='currentPages']"
        filter_pagination_Common(driver, select_xpath, '15')
        Number_of_pages = driver.find_elements(By.XPATH, "//div[@class='w-[10%] p-3 ml-[3px]']")
        count = 0
        for pages in Number_of_pages:
            count += 1

        if count <= 15:  
            print("Pagination for 15 Pages in LOB is Working fine")

def test_Filter_LOB_Pagination_25_Success(driver):
        select_xpath = "//select[@name='currentPages']"
        filter_pagination_Common(driver, select_xpath, '25')
        Number_of_pages = driver.find_elements(By.XPATH, "//div[@class='w-[10%] p-3 ml-[3px]']")
        count = 0
        for pages in Number_of_pages:
            count += 1

        if count <= 25:  
            print("Pagination for 25 Pages in LOB is Working fine")


def test_Filter_LOB_Pagination_50_Success(driver):
        select_xpath = "//select[@name='currentPages']"
        filter_pagination_Common(driver, select_xpath, '50')
        Number_of_pages = driver.find_elements(By.XPATH, "//div[@class='w-[10%] p-3 ml-[3px]']")
        count = 0
        for pages in Number_of_pages:
            count += 1

        if count <= 50:  
            print("Pagination for 50 Pages in LOB is Working fine")


def test_Filter_LOB_Refresh_Success(driver):
        a=driver.find_element(By.XPATH,"//h1[normalize-space()='LOB']").text
        driver.find_element(By.XPATH,"//p[normalize-space()='Refresh']").click()
        a=driver.find_element(By.XPATH,"//h1[normalize-space()='LOB']").text
        if(a==a):
             print("Refresh Button in LOB is Working fine")
        time.sleep(2)
        

def test_LOB_Download_Success(driver):
        wait=WebDriverWait(driver,10)
        wait.until(EC.element_to_be_clickable((By.XPATH,"//p[normalize-space()='Download']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH,"//p[normalize-space()='Download as Excel']"))).click()
        time.sleep(2)


def test_LOB_return_Success(driver):
        wait=WebDriverWait(driver,10)
        wait.until(EC.element_to_be_clickable((By.XPATH,"//img[@src='/src/assets/back.png']"))).click()
        time.sleep(2)
        
def LOB_ascending(driver):
    driver.find_element(By.XPATH,"//body[1]/div[1]/div[1]/div[1]/div[2]/div[3]/div[1]/div[1]/div[2]/p[1]/button[1]/span[1]").click()
    LOB_list = driver.find_elements(By.XPATH, "//div[@class='w-[20%]  p-3 ml-[3px]']")
    LOB_names = [country.text for country in LOB_list]

    if is_sorted_ascending_common(LOB_names):
            print("The LOB list is sorted in ascending order.")
    else:
            print("The LOB list is not sorted in ascending order.")
    time.sleep(2)

def LOB_descending(driver):
    driver.find_element(By.XPATH,"//body[1]/div[1]/div[1]/div[1]/div[2]/div[3]/div[1]/div[1]/div[2]/p[1]/button[1]/span[1]").click()
    LOB_list = driver.find_elements(By.XPATH, "//div[@class='w-[20%]  p-3 ml-[3px]']")
    LOB_names = [country.text for country in LOB_list]

    if is_sorted_descending_common(LOB_names):
            print("The LOB list is sorted in descending order.")
    else:
            print("The LOB list is not sorted in descending order.")
    time.sleep(2)

def LOB_ID_descending(driver):
    driver.find_element(By.XPATH,"//body/div[@id='root']/div/div/div/div/div/div/div[1]/p[1]/button[1]/span[1]").click()
    LOB_ID = driver.find_elements(By.XPATH, "//div[@class='w-1/2 p-3 flex ml-[9px]']")
    LOB_names = [country.text for country in LOB_ID]

    if is_sorted_descending_common(LOB_names):
            print("The LOB ID is sorted in descending order.")
    else:
            print("The LOB ID is not sorted in descending order.")
    time.sleep(2)

def LOB_ID_ascending(driver):
    driver.find_element(By.XPATH,"//body/div[@id='root']/div/div/div/div/div/div/div[1]/p[1]/button[1]/span[1]").click()
    LOB_ID = driver.find_elements(By.XPATH, "//div[@class='w-1/2 p-3 flex ml-[9px]']")
    LOB_names = [country.text for country in LOB_ID]

    if is_sorted_ascending_common(LOB_names):
            print("The LOB ID is sorted in ascending order.")
    else:
            print("The LOB ID is not sorted in ascending order.")
    time.sleep(2)

def LOB_Webpage():
        driver=login_and_navigate_LOB("ruderaw", "abcdefg", "9632")
        test_functions=[
            LOB_ascending,
            LOB_descending,
            LOB_ID_descending,
            LOB_ID_ascending,
            test_Filter_LOB_StartsWith_Success,
            test_Filter_LOB_Contains_Success,
            test_Filter_LOB_DoesNotContain_Success,
            test_Filter_LOB_EndsWith_Success,
            test_Filter_LOB_EqualTo_Success,
            test_Filter_LOB_isNull_Success,
            test_Filter_LOB_isNotNull_Success,
            test_Filter_LOB_Nofilter_Success,
            test_Filter_ID_LOB_Equalto_Success,
            test_Filter_ID_LOB_NotEqualTo_Success,
            test_Filter_ID_LOB_GreaterThan_Success,
            test_Filter_ID_LOB_GreaterThanOrEqualTo_Success,
            test_Filter_ID_LOB_LessThan_Success,
            test_Filter_ID_LOB_LessThanOrEqualTo_Success,
            test_Filter_ID_LOB_isNull_Success,
            test_Filter_ID_LOB_isNotNull_Success,
            test_Filter_ID_LOB_NoFilter_Success,
            test_Filter_LOB_Pagination_15_Success,
            test_Filter_LOB_Pagination_25_Success,
            test_Filter_LOB_Pagination_50_Success,
            test_Add_New_LOB_Success,
            test_Edit_LOB_Success,
            test_Filter_LOB_Refresh_Success,
            test_LOB_Download_Success,
            test_LOB_return_Success
        ]
        for test_func in test_functions:
             test_func(driver)


LOB_Webpage()

def login_and_navigate_Country(username, password, comkey):
    driver = webdriver.Chrome()
    driver.get(drivers_config["login_url"])
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.NAME, "comkey").send_keys(comkey)
    login_button = driver.find_element(By.CSS_SELECTOR, "button[class='bg-[#004DD7] w-[200px] h-[35px] text-white text-[18px] rounded-lg cursor-pointer']")
    assert not login_button.get_attribute("disabled"), "Login button should be enabled"
    login_button.click()
    admin_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div:nth-child(2) div:nth-child(1) button:nth-child(1) p:nth-child(1)"))
        )
    assert not admin_button.get_attribute("disabled"), "Admin button should be enabled"
    admin_button.click()
    driver.find_element(By.XPATH,"//a[normalize-space()='Country']").click()
    time.sleep(2)
    return driver

def test_Add_New_Country_Success(driver):
        wait=WebDriverWait(driver,10)
        addCountry_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".flex.items-center.justify-center.gap-4"))
        )
        assert not addCountry_button.get_attribute("disabled"), "Lob button should be enabled"
        addCountry_button.click()

        addCountry_header = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h1[normalize-space()='Country']"))
        )
        assert addCountry_header.text == "Country", "Add New Country header text is incorrect"
        a=driver.find_element(By.XPATH,"//p[@class='mr-11 text-gray-700']").text
        driver.find_element(By.XPATH,"//input[@name='countryName']").send_keys("aryan")
        wait.until(EC.element_to_be_clickable((By.XPATH,"//button[normalize-space()='Add']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH,"//button[normalize-space()='Save']"))).click()
        time.sleep(2)
        driver.find_element(By.XPATH,"//input[@type='text']").clear()
        time.sleep(2)
        driver.find_element(By.XPATH,"//input[@type='text']").send_keys("aryan")
        wait.until(EC.element_to_be_clickable((By.XPATH,"//img[@alt='search-icon']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH,"//img[@alt='trash']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH,"//button[normalize-space()='Delete']"))).click()
        assert a==a,"Country is not added successfully"
        print("Add Country is working Fine")
        time.sleep(2)


def test_Edit_Country_Success(driver):
        wait=WebDriverWait(driver,10)
        addCountry_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".flex.items-center.justify-center.gap-4"))
        )
        assert not addCountry_button.get_attribute("disabled"), "Lob button should be enabled"
        addCountry_button.click()

        addCountry_header = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h1[normalize-space()='Country']"))
        )
        assert addCountry_header.text == "Country", "Add New Country header text is incorrect"
        driver.find_element(By.XPATH,"//input[@name='countryName']").send_keys("aryan")
        wait.until(EC.element_to_be_clickable((By.XPATH,"//button[normalize-space()='Add']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH,"//button[normalize-space()='Save']"))).click()
        time.sleep(2)
        driver.find_element(By.XPATH,"//input[@type='text']").clear()
        wait.until(EC.element_to_be_clickable((By.XPATH,"//img[@alt='search-icon']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH,"//img[@alt='edit']"))).click()
        driver.find_element(By.XPATH,"//input[@name='countryName']").clear()
        driver.find_element(By.XPATH,"//input[@name='countryName']").send_keys("ashish")
        driver.find_element(By.XPATH,"//button[normalize-space()='Save']").click()
        time.sleep(4)
        driver.find_element(By.XPATH,"//input[@type='text']").clear()
        time.sleep(2)
        driver.find_element(By.XPATH,"//input[@type='text']").send_keys("ashish")
        wait.until(EC.element_to_be_clickable((By.XPATH,"//img[@alt='search-icon']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH,"//img[@alt='trash']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH,"//button[normalize-space()='Delete']"))).click()
        print("Edit Country is Working Fine")
        time.sleep(2)


def test_Filter_Country_StartsWith_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='StartsWith']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "a"
    )
        filtered_elements = driver.find_elements(By.XPATH,"//div[contains(@class,'w-[95%]  px-3 py-2')]")
        element_found = False
        for item in filtered_elements:
            if not item.text.lower().startswith("a"):
                element_found = False
                break
        else:
            element_found = True

        if element_found:
            print("StartsWith filter in Country Name is working fine.")
        else:
            print("Error.")

   
        
def test_Filter_Country_Contains_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='Contains']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "India"
    )
        filtered_elements = driver.find_elements(By.XPATH,"//div[contains(@class,'w-[95%]  px-3 py-2')]")
        element_found = True 
        for item in filtered_elements:
            if "India" not in item.text:
                element_found = False
                break

        if element_found:
            print("Contains filter in the Country Name is working fine.")
        else:
            print("Error.")


def test_Filter_Country_DoesNotContains_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='DoesNotContain']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "India"
    )
        filtered_elements = driver.find_elements(By.XPATH,"//div[contains(@class,'w-[95%]  px-3 py-2')]")
        element_found = False
        for item in filtered_elements:
            if item.text == "India":
                element_found = True
                break

        if not element_found:
            print("DoesNotContains Filter in Country Name is Working fine.")
        else:
            print("Error.")

def test_Filter_Country_EndsWith_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='EndsWith']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "a"
    )
        filtered_elements = driver.find_elements(By.XPATH,"//div[contains(@class,'w-[95%]  px-3 py-2')]")
        element_found = True
        for item in filtered_elements:
            if not item.text.endswith("a"):
                element_found = False
                break

        if element_found:
            print("EndsWith filter in Country Name is working fine.")
        else:
            print("Error.")


def test_Filter_Country_EqualsTo_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='EqualTo']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "India"
    )
        filtered_elements = driver.find_elements(By.XPATH,"//div[contains(@class,'w-[95%]  px-3 py-2')]")
        element_found = True
        for item in filtered_elements:
            if item.text != "India":
                element_found = False
                break

        if element_found:
            print("EqualsTo filter in the Country Name is working fine.")
        else:
            print("Error")


def test_Filter_Country_isNotNull_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='isNotNull']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "India"
    )
        a=driver.find_element(By.XPATH,"//p[@class='mr-11 text-gray-700']").text
        words = a[:2]
        filtered_element = driver.find_element(By.XPATH,"//p[.='0 Items in 0 Pages']")
        if(filtered_element.text.startswith(words)):
             print("isNotNull filter in Country Name is working fine")


def test_Filter_Country_isNull_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='isNull']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "India"
    )
        a=driver.find_element(By.XPATH,"//p[@class='mr-11 text-gray-700']").text
        words = a[:2]
        filtered_element = driver.find_element(By.XPATH,"//p[.='0 Items in 0 Pages']")
        if(filtered_element.text.startswith(words)):
             print("isNull filter in Country Name is working fine")
        

def test_Filter_Country_Nofilter_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='No Filter']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "India"
    )
        a=driver.find_element(By.XPATH,"//p[@class='mr-11 text-gray-700']").text
        words = a[:2]
        filtered_element = driver.find_element(By.XPATH, "//p[@class='mr-11 text-gray-700']")
        if filtered_element.text.startswith(words):
            print("Nofilter in Country Name is working fine")
        else:
            print("Error")


def test_Filter_ID_Country_Equalto_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='EqualTo']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "12"
    )
        filtered_elements = driver.find_elements(By.XPATH,"//div[@class='w-1/2  px-3 py-2 ml-1']")
        element_found = True
        for item in filtered_elements:
            if item.text != "12":
                element_found = False
                break

        if element_found:
            print("EqualTo filter in ID is working fine")
        else:
            print("Error")


def test_Filter_ID_Country_NotEqualto_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='NotEqualTo']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "12"
    )
        filtered_elements = driver.find_elements(By.XPATH,"//div[@class='w-1/2  px-3 py-2 ml-1']")
        element_found = True
        for item in filtered_elements:
            if item.text == "12":
                element_found = False
                break

        if element_found:
            print("NotEqualTo Filter in ID is working fine.")
        else:
            print("Error.")



def test_Filter_ID_Country_GreaterThan_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='GreaterThan']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "12"
    )
        filtered_elements = driver.find_elements(By.XPATH,"//div[@class='w-1/2  px-3 py-2 ml-1']")
        element_found = True
        for item in filtered_elements:
            if item.text <= 12:
                element_found = False
                break

        if element_found:
            print("Greater Than Filter in ID is working fine.")
        else:
            print("Error.")




def test_Filter_ID_Country_LessThan_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='LessThan']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "12"
    )
        filtered_elements = driver.find_elements(By.XPATH,"//div[@class='w-1/2  px-3 py-2 ml-1']")
        element_found = True
        for item in filtered_elements:
            if item.text >= "12":
                element_found = False
                break

        if element_found:
            print("LessThan Filter in ID is working fine.")
        else:
            print("Error")



def test_Filter_ID_Country_LessThanOrEqualTo_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='LessThanOrEqualTo']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "12"
    )
        filtered_elements = driver.find_elements(By.XPATH,"//div[@class='w-1/2  px-3 py-2 ml-1']")
        element_found = True
        for item in filtered_elements:
            if item.text > "12":
                element_found = False
                break

        if element_found:
            print("LessThanOrEqualTo Filter in ID is working fine")
        else:
            print("Error")



def test_Filter_ID_Country_isNull_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='isNull']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "12"
    )
        a=driver.find_element(By.XPATH,"//p[@class='mr-11 text-gray-700']").text
        words = a[:2]
        filtered_element = driver.find_element(By.XPATH,"//p[@class='mr-11 text-gray-700']")
        element_found = False
        if filtered_element.text.startswith(words):
            element_found = True

        if element_found:
            print("isNull Filter in ID is working fine")
        else:
            print("Error")



def test_Filter_ID_Country_isNotNull_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='isNotNull']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "12"
    )
        a=driver.find_element(By.XPATH,"//p[@class='mr-11 text-gray-700']").text
        words = a[:2]
        filtered_element = driver.find_element(By.XPATH,"//p[@class='mr-11 text-gray-700']")
        element_found = False
        if filtered_element.text.startswith(words):
            element_found = True

        if element_found:
            print("isNotNull Filter in ID is working fine")
        else:
            print("Error")
    


def test_Filter_ID_Country_NoFilter_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='No Filter']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "12"
    )
        a=driver.find_element(By.XPATH,"//p[@class='mr-11 text-gray-700']").text
        words = a[:2]
        filtered_element = driver.find_element(By.XPATH,"//p[@class='mr-11 text-gray-700']")
        element_found = False
        if filtered_element.text.startswith(words):
            element_found = True

        if element_found:
            print("NoFilter in ID is working fine")
        else:
            print("Error")

def test_Filter_ID_Country_GreaterThanOrEqualTo_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='LessThanOrEqualTo']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "12"
    )
        filtered_elements = driver.find_elements(By.XPATH,"//div[@class='w-1/2  px-3 py-2 ml-1']")
        element_found = True
        for item in filtered_elements:
            if item.text < "12":
                element_found = False
                break

        if element_found:
            print("GreaterThanOrEqualTo Filter in ID is working fine")
        else:
            print("Error")


def test_Filter_Country_Pagination_15_Success(driver):
    select_xpath = "//select[@name='currentPages']"
    filter_pagination_Common(driver, select_xpath, '15')
    Number_of_pages = driver.find_elements(By.XPATH, "//div[contains(@class,'w-[5%] px-3 py-2')]")
    count = 0
    for pages in Number_of_pages:
        count += 1

    if count <= 15:  
        print("Pagination for 15 Pages is Working fine")

def test_Filter_Country_Pagination_25_Success(driver):
        select_xpath = "//select[@name='currentPages']"
        filter_pagination_Common(driver, select_xpath, '25')
        Number_of_pages = driver.find_elements(By.XPATH, "//div[contains(@class,'w-[5%] px-3 py-2')]")
        count = 0
        for pages in Number_of_pages:
                count += 1

        if count <= 25:  
                print("Pagination for 25 Pages is Working fine")



def test_Filter_Country_Pagination_50_Success(driver):
        select_xpath = "//select[@name='currentPages']"
        filter_pagination_Common(driver, select_xpath, '50')
        Number_of_pages = driver.find_elements(By.XPATH, "//div[contains(@class,'w-[5%] px-3 py-2')]")
        count = 0
        for pages in Number_of_pages:
                count += 1

        if count <= 50:  
                print("Pagination for 50 Pages is Working fine")


def test_Country_Refresh_Success(driver):
        a=driver.find_element(By.XPATH,"//h1[normalize-space()='Country']")
        driver.find_element(By.XPATH,"//p[normalize-space()='Refresh']").click()
        a=driver.find_element(By.XPATH,"//h1[normalize-space()='Country']")
        if a.text=='Country':
              print("Refresh Button is working fine")
        time.sleep(2)


def test_Country_Download_Success(driver):
        wait=WebDriverWait(driver,10)
        wait.until(EC.element_to_be_clickable((By.XPATH,"//p[normalize-space()='Download']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH,"//p[normalize-space()='Download as Excel']"))).click()
        time.sleep(2)



def test_Country_return_Success(driver):
        wait=WebDriverWait(driver,10)
        wait.until(EC.element_to_be_clickable((By.XPATH,"//img[@src='/src/assets/back.png']"))).click()
        a=driver.find_element(By.XPATH,"//h1[normalize-space()='Dashboard']").text
        if a=='Dashboard':
              print("Return Button is Working Fine")

        time.sleep(2)


def is_sorted_ascending_common(string_list):
        for i in range(len(string_list) - 1):
                if string_list[i] > string_list[i + 1]:
                   return False
        
        return True


def is_sorted_descending_common(string_list):
        for i in range(len(string_list) - 1):
                if string_list[i] < string_list[i + 1]:
                   return False
        
        return True

def test_Country_Countryname_ascending(driver):
        driver.find_element(By.XPATH,"//body/div/div/div/div/div/div/div/div[2]/p[1]/button[1]/span[1]").click()
        Country_list = driver.find_elements(By.XPATH, "//div[@class='w-[95%]  px-3 py-2']")
        country_names = [country.text for country in Country_list]

        if is_sorted_ascending_common(country_names):
                print("The country list is sorted in ascending order.")
        else:
                print("The country list is not sorted in ascending order.")

        time.sleep(2)


def test_Country_Countryname_descending(driver):
        driver.find_element(By.XPATH,"//body/div/div/div/div/div/div/div/div[2]/p[1]/button[1]/span[1]").click()
        Country_list = driver.find_elements(By.XPATH, "//div[@class='w-[95%]  px-3 py-2']")
        country_names = [country.text for country in Country_list]

        if is_sorted_descending_common(country_names):
                print("The country list is sorted in descending order.")
        else:
                print("The country list is not sorted in descending order.")

        time.sleep(2)



def test_Country_ID_descending(driver):
        driver.find_element(By.XPATH,"//body/div/div/div/div/div/div/div/div[1]/p[1]/button[1]/span[1]").click()
        ID_list = driver.find_elements(By.XPATH, "//div[@class='w-1/2  px-3 py-2 ml-1']")
        ID_No = [country.text for country in ID_list]

        if is_sorted_descending_common(ID_No):
                print("The ID list is sorted in descending order.")
        else:
                print("The ID list is not sorted in descending order.")
        time.sleep(2)


def test_Country_ID_ascending(driver):
        driver.find_element(By.XPATH,"//body/div/div/div/div/div/div/div/div[1]/p[1]/button[1]/span[1]").click()
        ID_list = driver.find_elements(By.XPATH, "//div[@class='w-1/2  px-3 py-2 ml-1']")
        ID_No = [country.text for country in ID_list]

        if is_sorted_descending_common(ID_No):
                print("The ID list is sorted in ascending order.")
        else:
                print("The ID list is not sorted in ascending order.")
        time.sleep(2)


def Country_Webpage():
        driver = login_and_navigate_Country("ruderaw", "abcdefg", "9632")
        test_functions=[
            test_Country_Countryname_ascending,
            test_Country_Countryname_descending,
            test_Country_ID_ascending,
            test_Country_ID_descending,
            test_Filter_Country_StartsWith_Success,
            test_Filter_Country_Contains_Success,
            test_Filter_Country_DoesNotContains_Success,
            test_Filter_Country_EndsWith_Success,
            test_Filter_Country_EqualsTo_Success,
            test_Filter_Country_isNotNull_Success,
            test_Filter_Country_isNull_Success,
            test_Filter_Country_Nofilter_Success,
            test_Filter_ID_Country_Equalto_Success,
            test_Filter_ID_Country_NotEqualto_Success,
            test_Filter_ID_Country_GreaterThan_Success,
            test_Filter_ID_Country_LessThan_Success,
            test_Filter_ID_Country_LessThanOrEqualTo_Success,
            test_Filter_ID_Country_isNull_Success,
            test_Filter_ID_Country_isNotNull_Success,
            test_Filter_ID_Country_GreaterThanOrEqualTo_Success,
            test_Filter_ID_Country_NoFilter_Success,
            test_Filter_Country_Pagination_15_Success,
            test_Filter_Country_Pagination_25_Success,
            test_Filter_Country_Pagination_50_Success,
            test_Add_New_Country_Success,
            test_Edit_Country_Success,
            test_Country_Refresh_Success,
            test_Country_Download_Success,
            test_Country_return_Success
        ]
        for test in test_functions:
              test(driver)

Country_Webpage()


# %%

def login_and_navigate_Locality(username, password, comkey):
    driver = webdriver.Chrome()
    driver.get(drivers_config["login_url"])
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.NAME, "comkey").send_keys(comkey)
    login_button = driver.find_element(By.CSS_SELECTOR, "button[class='bg-[#004DD7] w-[200px] h-[35px] text-white text-[18px] rounded-lg cursor-pointer']")
    assert not login_button.get_attribute("disabled"), "Login button should be enabled"
    login_button.click()
    admin_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div:nth-child(2) div:nth-child(1) button:nth-child(1) p:nth-child(1)"))
        )
    assert not admin_button.get_attribute("disabled"), "Admin button should be enabled"
    admin_button.click()
    driver.find_element(By.XPATH,"//a[normalize-space()='Locality']").click()
    time.sleep(2)
    return driver

def test_Add_New_Locality_Success(driver):
        wait=WebDriverWait(driver,10)
        addLocality_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".flex.items-center.justify-center.gap-4"))
        )
        assert not addLocality_button.get_attribute("disabled"), "Lob button should be enabled"
        addLocality_button.click()
        time.sleep(2)
        x=driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(3) > div:nth-child(3) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > select:nth-child(2)")
        d=Select(x)
        d.select_by_visible_text('India')
        time.sleep(2)
        x1=driver.find_element(By.XPATH,"//select[@name='state']")
        d1=Select(x1)
        d1.select_by_visible_text('Maharashtra')
        time.sleep(2)
        x2=driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(3) > div:nth-child(3) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > select:nth-child(2)")
        d2=Select(x2)
        d2.select_by_visible_text('Pune')
        time.sleep(2)
        driver.find_element(By.XPATH,"//input[@name='empName']").send_keys("a")
        wait.until(EC.element_to_be_clickable((By.XPATH,"//button[normalize-space()='Add']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH,"//button[normalize-space()='Add']"))).click()
        time.sleep(2)
        driver.find_element(By.XPATH,"//input[@type='text']").clear()
        time.sleep(2)
        driver.find_element(By.XPATH,"//input[@type='text']").send_keys("India")
        wait.until(EC.element_to_be_clickable((By.XPATH,"//img[@alt='search-icon']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH,"//body[1]/div[1]/div[1]/div[1]/div[2]/div[3]/div[2]/div[1]/div[2]/div[2]/button[2]/img[1]"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH,"//button[normalize-space()='Delete']"))).click()
        time.sleep(2)


def test_Edit_Locality_Success(driver):
        wait=WebDriverWait(driver,10)
        addLocality_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".flex.items-center.justify-center.gap-4"))
        )
        assert not addLocality_button.get_attribute("disabled"), "Lob button should be enabled"
        addLocality_button.click()
        time.sleep(2)
        x=driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(3) > div:nth-child(3) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > select:nth-child(2)")
        d=Select(x)
        d.select_by_visible_text('India')
        time.sleep(2)
        x1=driver.find_element(By.XPATH,"//select[@name='state']")
        d1=Select(x1)
        d1.select_by_visible_text('Maharashtra')
        time.sleep(2)
        x2=driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(3) > div:nth-child(3) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > select:nth-child(2)")
        d2=Select(x2)
        d2.select_by_visible_text('Pune')
        time.sleep(2)
        driver.find_element(By.XPATH,"//input[@name='empName']").send_keys("a")
        wait.until(EC.element_to_be_clickable((By.XPATH,"//button[normalize-space()='Add']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH,"//button[normalize-space()='Add']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH,"//img[@alt='search-icon']"))).click()
        time.sleep(2)
        wait.until(EC.element_to_be_clickable((By.XPATH,"//div//div//div//div//div//div[1]//div[2]//div[2]//button[1]//img[1]"))).click()
        driver.find_element(By.XPATH,"//input[@name='empName']").clear()
        driver.find_element(By.XPATH,"//input[@name='empName']").send_keys("ashish")
        driver.find_element(By.XPATH,"//button[normalize-space()='Save']").click()
        time.sleep(4)
        driver.find_element(By.XPATH,"//input[@type='text']").clear()
        time.sleep(2)
        driver.find_element(By.XPATH,"//input[@type='text']").send_keys("ashish")
        wait.until(EC.element_to_be_clickable((By.XPATH,"//img[@alt='search-icon']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH,"//img[@alt='trash']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH,"//button[normalize-space()='Delete']"))).click()
        time.sleep(2)


def test_Filter_Locality_Country_name_StartsWith_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='StartsWith']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "i"
    )
        filtered_elements = driver.find_elements(By.XPATH,"//div[@class='w-[15%]  p-4']")
        element_found = True
        for item in filtered_elements[1:]:
            if not item.text.lower().startswith("i"):
                element_found = False
                break

        if element_found:
            print("StartsWith filter in Locality with Country Name is working fine.")
        else:
            print("Error.")
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)
        

def test_Filter_Locality_Country_name_Contains_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='Contains']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "i"
    )
        filtered_elements = driver.find_elements(By.XPATH,"//div[@class='w-[15%]  p-4']")
        element_found = True 
        for item in filtered_elements[1:]:
            if "i" not in item.text.lower():
                element_found = False
                break

        if element_found:
            print("Contains filter in Locality with Country Name is working fine.")
        else:
            print("Error.")
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)
        

def test_Filter_Locality_Country_name_DoesNotContains_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='DoesNotContain']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "India"
    )
        filtered_elements = driver.find_elements(By.XPATH,"//div[@class='w-[15%]  p-4']")
        element_found = False
        for item in filtered_elements[1:]:
            if item.text == "India":
                element_found = True
                break

        if not element_found:
            print("DoesNotContains Filter in Locality with Country Name is Working fine.")
        else:
            print("Error.")
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)
        


def test_Filter_Locality_Country_name_EndsWith_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='EndsWith']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "i"
    )
        filtered_elements = driver.find_elements(By.XPATH,"//div[@class='w-[15%]  p-4']")
        element_found = True
        for item in filtered_elements[1:]:
            if not item.text.endswith("i"):
                element_found = False
                break

        if element_found:
            print("EndsWith filter in Locality with Country Name is working fine.")
        else:
            print("Error.")
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)
         
        
def test_Filter_Locality_Country_name_EqualsTo_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='EqualTo']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "UK"
    )
        filtered_elements = driver.find_elements(By.XPATH,"//div[@class='w-[15%]  p-4']")
        element_found = True
        for item in filtered_elements[1:]:
            if item.text != "UK":
                element_found = False
                break

        if element_found:
            print("EqualsTo filter in Locality with Country Name is working fine.")
        else:
            print("Error")
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)
    

def test_Filter_Locality_Country_name_isNotNull_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='isNotNull']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "UK"
    )
        a=driver.find_element(By.XPATH,"//p[normalize-space()='47 Items in 4 Pages']").text
        words = a[:2]
        filtered_element = driver.find_element(By.XPATH,"//p[normalize-space()='47 Items in 4 Pages']")
        if(filtered_element.text.startswith(words)):
                print("isNotNull filter in Locality With Country Name is working fine")
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)

def test_Filter_Locality_Country_name_isNull_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='isNull']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "UK"
    )
        a=driver.find_element(By.XPATH,"//p[normalize-space()='0 Items in 0 Pages']").text
        words = a[:2]
        filtered_element = driver.find_element(By.XPATH,"//p[normalize-space()='0 Items in 0 Pages']")
        if(filtered_element.text.startswith(words)):
                print("isNull filter in Locality With Country Name is working fine")
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)


def test_Filter_Locality_Country_name_NoFilter_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='No Filter']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "UK"
    )
        a=driver.find_element(By.XPATH,"//p[normalize-space()='47 Items in 4 Pages']").text
        words = a[:2]
        filtered_element = driver.find_element(By.XPATH,"//p[normalize-space()='47 Items in 4 Pages']")
        if(filtered_element.text.startswith(words)):
                print("NO filter in Locality With Country Name is working fine")
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)

        
def test_Filter_Locality_State_name_StartsWith_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='StartsWith']",
        "div:nth-child(3) div:nth-child(1) input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "m"
    )
        filtered_elements = driver.find_elements(By.XPATH,"//div[@class='w-[20%]  p-4'][position()=1]")
        element_found = True
        for item in filtered_elements[1:]:
            if not item.text.lower().startswith("m"):
                element_found = False
                break

        if element_found:
            print("StartsWith filter in Locality with State Name is working fine.")
        else:
            print("Error.")
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)


def test_Filter_Locality_State_name_Contains_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='Contains']",
        "div:nth-child(3) div:nth-child(1) input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "m"
    )
        filtered_elements = driver.find_elements(By.XPATH,"//div[@class='w-[20%]  p-4'][position()=1]")
        element_found = True 
        for item in filtered_elements[1:]:
            if "m" not in item.text.lower():
                element_found = False
                break

        if element_found:
            print("Contains filter in Locality with State Name is working fine.")
        else:
            print("Error.")
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)
    

def test_Filter_Locality_State_name_DoesNotContains_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='DoesNotContain']",
        "div:nth-child(3) div:nth-child(1) input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "UAE"
    )
        filtered_elements = driver.find_elements(By.XPATH,"//div[@class='w-[20%]  p-4'][position()=1]")
        element_found = False
        for item in filtered_elements[1:]:
            if item.text == "UAE":
                element_found = True
                break

        if not element_found:
            print("DoesNotContains Filter in Locality with State Name is Working fine.")
        else:
            print("Error.")
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)
    

def test_Filter_Locality_State_name_EndsWith_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='EndsWith']",
        "div:nth-child(3) div:nth-child(1) input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "a"
    )
        filtered_elements = driver.find_elements(By.XPATH,"//div[@class='w-[20%]  p-4'][position()=1]")
        element_found = True
        for item in filtered_elements[1:]:
            if not item.text.endswith("a"):
                element_found = False
                break

        if element_found:
            print("EndsWith filter in Locality with State Name is working fine.")
        else:
            print("Error.")
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)


def test_Filter_Locality_State_name_EqualsTo_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='EqualTo']",
        "div:nth-child(3) div:nth-child(1) input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "Colombo"
    )
        filtered_elements = driver.find_elements(By.XPATH,"//div[@class='w-[20%]  p-4'][position()=1]")
        element_found = True
        for item in filtered_elements[2:]:
            if item.text != "Colombo":
                element_found = False
                break

        if element_found:
            print("EqualsTo filter in Locality with State Name is working fine.")
        else:
            print("Error")
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)
    


def test_Filter_Locality_State_name_isNotNull_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='isNotNull']",
        "div:nth-child(3) div:nth-child(1) input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "Colombo"
    )
        a=driver.find_element(By.XPATH,"//p[normalize-space()='47 Items in 4 Pages']").text
        words = a[:2]
        filtered_element = driver.find_element(By.XPATH,"//p[normalize-space()='47 Items in 4 Pages']")
        if(filtered_element.text.startswith(words)):
                print("isNotNull filter in Locality With State Name is working fine")
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)
        

def test_Filter_Locality_State_name_isNull_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='isNull']",
        "div:nth-child(3) div:nth-child(1) input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "Colombo"
    )
        a=driver.find_element(By.XPATH,"//p[normalize-space()='0 Items in 0 Pages']").text
        words = a[:2]
        filtered_element = driver.find_element(By.XPATH,"//p[normalize-space()='0 Items in 0 Pages']")
        if(filtered_element.text.startswith(words)):
                print("isNull filter in Locality With State Name is working fine")
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)
    

def test_Filter_Locality_State_name_NoFilter_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='No Filter']",
        "div:nth-child(3) div:nth-child(1) input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "Colombo"
    )
        a=driver.find_element(By.XPATH,"//p[normalize-space()='47 Items in 4 Pages']").text
        words = a[:2]
        filtered_element = driver.find_element(By.XPATH,"//p[normalize-space()='47 Items in 4 Pages']")
        if(filtered_element.text.startswith(words)):
                print("No filter in Locality With State Name is working fine")
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)


def test_Filter_Locality_City_name_StartsWith_Success(driver):      
        filter_Common(
        driver,
        "//h1[normalize-space()='StartsWith']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "m"
    )
        filtered_elements = driver.find_elements(By.XPATH,"//div[@class='w-[20%]  p-4'][position()=2]")
        element_found = True
        for item in filtered_elements[1:]:
            if not item.text.lower().startswith("m"):
                element_found = False
                break

        if element_found:
            print("StartsWith filter in Locality with City Name is working fine.")
        else:
            print("Error.")
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)
        


def test_Filter_Locality_City_name_Contains_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='Contains']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "m"
    )
        filtered_elements = driver.find_elements(By.XPATH,"//div[@class='w-[20%]  p-4'][position()=2]")
        element_found = True 
        for item in filtered_elements[1:]:
            if "m" not in item.text.lower():
                element_found = False
                break

        if element_found:
            print("Contains filter in Locality with city Name is working fine.")
        else:
            print("Error.")
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)

def test_Filter_Locality_City_name_DoesNotContains_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='DoesNotContain']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "Pune"
    )
        filtered_elements = driver.find_elements(By.XPATH,"//div[@class='w-[20%]  p-4'][position()=2]")
        element_found = False
        for item in filtered_elements[1:]:
            if item.text == "Pune":
                element_found = True
                break

        if not element_found:
            print("DoesNotContains Filter in Locality with City Name is Working fine.")
        else:
            print("Error.")
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)
        

def test_Filter_Locality_City_name_EndsWith_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='EndsWith']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "m"
    )
        filtered_elements = driver.find_elements(By.XPATH,"//div[@class='w-[20%]  p-4'][position()=2]")
        element_found = True
        for item in filtered_elements[1:]:
            if not item.text.endswith("m"):
                element_found = False
                break

        if element_found:
            print("EndsWith filter in City with State Name is working fine.")
        else:
            print("Error.")
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)


def test_Filter_Locality_City_name_EqualsTo_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='EqualTo']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "Pune"
    )
        filtered_elements = driver.find_elements(By.XPATH,"//div[@class='w-[20%]  p-4'][position()=2]")
        element_found = True
        for item in filtered_elements[2:]:
            if item.text != "Pune":
                element_found = False
                break

        if element_found:
            print("EqualsTo filter in Locality with City Name is working fine.")
        else:
            print("Error")
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)
    

def test_Filter_Locality_City_name_isNotNull_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='isNotNull']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "Pune"
    )
        a=driver.find_element(By.XPATH,"//p[normalize-space()='47 Items in 4 Pages']").text
        words = a[:2]
        filtered_element = driver.find_element(By.XPATH,"//p[normalize-space()='47 Items in 4 Pages']")
        if(filtered_element.text.startswith(words)):
                print("isNotNull filter in Locality With City Name is working fine")
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)
    


def test_Filter_Locality_City_name_isNull_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='isNull']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "Pune"
    )
        a=driver.find_element(By.XPATH,"//p[normalize-space()='0 Items in 0 Pages']").text
        words = a[:2]
        filtered_element = driver.find_element(By.XPATH,"//p[normalize-space()='0 Items in 0 Pages']")
        if(filtered_element.text.startswith(words)):
                print("isNull filter in Locality With City Name is working fine")
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)
        
def test_Filter_Locality_City_name_NoFilter_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='No Filter']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "Pune"
    )
        a=driver.find_element(By.XPATH,"//p[normalize-space()='47 Items in 4 Pages']").text
        words = a[:2]
        filtered_element = driver.find_element(By.XPATH,"//p[normalize-space()='47 Items in 4 Pages']")
        if(filtered_element.text.startswith(words)):
                print("No filter in Locality With City Name is working fine")
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)
    

def test_filter_Locality_LocalityName_StartsWith(driver,send_letter):

        filter_Common(
        driver,
        "//h1[normalize-space()='No Filter']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(5) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(5) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "Pune"
    )

def test_Filter_Locality_name_StartsWith_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='StartsWith']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(5) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(5) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "p"
    )
        filtered_elements = driver.find_elements(By.XPATH,"//div[@class='w-[25%]  p-4 ml-1']")
        element_found = True
        for item in filtered_elements:
            if not item.text.lower().startswith("p"):
                element_found = False
                break

        if element_found:
            print("StartsWith filter in Locality with Locality Name is working fine.")
        else:
            print("Error.")
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)
        

def test_Filter_Locality_name_Contains_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='Contains']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(5) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(5) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "p"
    )
        filtered_elements = driver.find_elements(By.XPATH,"//div[@class='w-[25%]  p-4 ml-1']")
        element_found = True 
        for item in filtered_elements:
            if "p" not in item.text.lower():
                element_found = False
                break

        if element_found:
            print("Contains filter in Locality with Locality Name is working fine.")
        else:
            print("Error.")
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)
    

def test_Filter_Locality_name_DoesNotContains_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='DoesNotContain']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(5) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(5) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "a"
    )
        filtered_elements = driver.find_elements(By.XPATH,"//div[@class='w-[25%]  p-4 ml-1']")
        element_found = False
        for item in filtered_elements:
            if item.text == "a":
                element_found = True
                break

        if not element_found:
            print("DoesNotContains Filter in Locality with Locality Name is Working fine.")
        else:
            print("Error.")
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)
    

def test_Filter_Locality_name_EndsWith_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='EndsWith']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(5) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(5) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "a"
    )
        filtered_elements = driver.find_elements(By.XPATH,"//div[@class='w-[25%]  p-4 ml-1']")
        element_found = True
        for item in filtered_elements:
            if not item.text.endswith("a"):
                element_found = False
                break

        if element_found:
            print("EndsWith filter in Locality with Locality Name is working fine.")
        else:
            print("Error.")
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)
    

def test_Filter_Locality_name_EqualsTo_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='EqualTo']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(5) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(5) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "Lavasa"
    )
        filtered_elements = driver.find_elements(By.XPATH,"//div[@class='w-[25%]  p-4 ml-1']")
        element_found = True
        for item in filtered_elements:
            if item.text != "Lavasa":
                element_found = False
                break

        if element_found:
            print("EqualsTo filter in Locality with Locality Name is working fine.")
        else:
            print("Error")
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)


def test_Filter_Locality_name_isNotNull_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='isNotNull']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(5) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(5) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "Lavasa"
    )
        a=driver.find_element(By.XPATH,"//p[normalize-space()='47 Items in 4 Pages']").text
        words = a[:2]
        filtered_element = driver.find_element(By.XPATH,"//p[normalize-space()='47 Items in 4 Pages']")
        if(filtered_element.text.startswith(words)):
                print("isNotNull filter in Locality With City Name is working fine")
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)


def test_Filter_Locality_name_isNull_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='isNull']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(5) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(5) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "Lavasa"
    )
        a=driver.find_element(By.XPATH,"//p[normalize-space()='0 Items in 0 Pages']").text
        words = a[:2]
        filtered_element = driver.find_element(By.XPATH,"//p[normalize-space()='0 Items in 0 Pages']")
        if(filtered_element.text.startswith(words)):
                print("isNotNull filter in Locality With City Name is working fine")
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)
    

def test_Filter_Locality_name_NoFilter_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='No Filter']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(5) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(5) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "Lavasa"
    )
        a=driver.find_element(By.XPATH,"//p[normalize-space()='47 Items in 4 Pages']").text
        words = a[:2]
        filtered_element = driver.find_element(By.XPATH,"//p[normalize-space()='47 Items in 4 Pages']")
        if(filtered_element.text.startswith(words)):
                print("Nofilter in Locality With City Name is working fine")
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)


def test_Filter_Locality_ID_EqualsTo_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='EqualTo']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "16"
    )
        filtered_elements = driver.find_elements(By.XPATH,"//div[contains(@class,'w-1/2  p-4 ml-1')]")
        element_found = True
        for item in filtered_elements:
            if item.text != "16":
                element_found = False
                break

        if element_found:
            print("EqualsTo filter in Locality with ID is working fine.")
        else:
            print("Error")
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)


def test_Filter_Locality_ID_NotEqualTo_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='NotEqualTo']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "16"
    )
        filtered_elements = driver.find_elements(By.XPATH,"//div[contains(@class,'w-1/2  p-4 ml-1')]")
        element_found = True
        for item in filtered_elements:
            if item.text == "16":
                element_found = False
                break

        if element_found:
            print("NotEqualTo Filter in Locality with ID is working fine.")
        else:
            print("Error.")
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)
    
def test_Filter_Locality_ID_GreaterThan_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='GreaterThan']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "16"
    )
        filtered_elements = driver.find_elements(By.XPATH,"//div[contains(@class,'w-1/2  p-4 ml-1')]")
        element_found = True
        for item in filtered_elements:
            if item.text <= '16':
                element_found = False
                break

        if element_found:
            print("Greater Than Filter in Locality with ID is working fine.")
        else:
            print("Error.")
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)


def test_Filter_Locality_ID_LessThan_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='LessThan']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "16"
    )
        filtered_elements = driver.find_elements(By.XPATH,"//div[contains(@class,'w-1/2  p-4 ml-1')]")
        element_found = True
        for item in filtered_elements:
            if item.text >= "16":
                element_found = False
                break

        if element_found:
            print("LessThan Filter in Locality with ID is working fine.")
        else:
            print("Error")
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)
    

def test_Filter_Locality_ID_GreaterThanOrEqualTo_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='GreaterThanOrEqualTo']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "16"
    )
        filtered_elements = driver.find_elements(By.XPATH,"//div[contains(@class,'w-1/2  p-4 ml-1')]")
        element_found = True
        for item in filtered_elements:
            if item.text < "16":
                element_found = False
                break

        if element_found:
            print("GreaterThanOrEqualTo Filter in Locality with ID is working fine")
        else:
            print("Error")
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)


def test_Filter_Locality_ID_LessThanOrEqualTo_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='LessThanOrEqualTo']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "16"
    )
        filtered_elements = driver.find_elements(By.XPATH,"//div[contains(@class,'w-1/2  p-4 ml-1')]")
        element_found = True
        for item in filtered_elements:
            if item.text > "16":
                element_found = False
                break

        if element_found:
            print("LessThanOrEqualTo Filter in Locality with ID is working fine")
        else:
            print("Error")
        


def test_Filter_Locality_ID_isNull_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='isNull']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "16"
    )
        a=driver.find_element(By.XPATH,"//p[@class='mr-11 text-gray-700']").text
        words = a[:2]
        filtered_element = driver.find_element(By.XPATH,"//p[@class='mr-11 text-gray-700']")
        element_found = False
        if filtered_element.text.startswith(words):
            element_found = True

        if element_found:
            print("isNull Filter in Locality is working fine")
        else:
            print("Error")
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)
        

def test_Filter_Locality_ID_isNotNull_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='isNotNull']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "16"
    )
        a=driver.find_element(By.XPATH,"//p[@class='mr-11 text-gray-700']").text
        words = a[:2]
        filtered_element = driver.find_element(By.XPATH,"//p[@class='mr-11 text-gray-700']")
        element_found = False
        if filtered_element.text.startswith(words):
            element_found = True

        if element_found:
            print("isNotNull Filter in Locality is working fine")
        else:
            print("Error")
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)
    

def test_Filter_Locality_ID_NoFilter_Success(driver):
        filter_Common(
        driver,
        "//h1[normalize-space()='No Filter']",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)",
        "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)",
        "16"
    )
        a=driver.find_element(By.XPATH,"//p[@class='mr-11 text-gray-700']").text
        words = a[:2]
        filtered_element = driver.find_element(By.XPATH,"//p[@class='mr-11 text-gray-700']")
        element_found = False
        if filtered_element.text.startswith(words):
            element_found = True

        if element_found:
            print("NoFilter in Locality is working fine")
        else:
            print("Error")
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)
        

def test_Filter_Locality_Pagination_15_Success(driver):
        select_xpath = "//select[@name='currentPages']"
        filter_pagination_Common(driver, select_xpath, '15')
        Number_of_pages = driver.find_elements(By.XPATH, "//div[contains(@class,'w-[5%] p-4')]")
        count = 0
        for pages in Number_of_pages[2:]:
            count += 1

        if count <= 15:  
            print("Pagination for 15 Pages in Locality is Working fine")


def test_Filter_Locality_Pagination_25_Success(driver):
        select_xpath = "//select[@name='currentPages']"
        filter_pagination_Common(driver, select_xpath, '25')
        Number_of_pages = driver.find_elements(By.XPATH, "//div[contains(@class,'w-[5%] p-4')]")
        count = 0
        for pages in Number_of_pages[2:]:
            count += 1

        if count <= 25:  
            print("Pagination for 25 Pages in Locality is Working fine")


def test_Filter_Locality_Pagination_50_Success(driver):
        select_xpath = "//select[@name='currentPages']"
        filter_pagination_Common(driver, select_xpath, '50')
        Number_of_pages = driver.find_elements(By.XPATH, "//div[contains(@class,'w-[5%] p-4')]")
        count = 0
        for pages in Number_of_pages[2:]:
            count += 1

        if count <= 50:  
            print("Pagination for 50 Pages in Locality is Working fine")


def test_Filter_Locality_Refresh_Success(driver):
        a=driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").text
        driver.find_element(By.XPATH,"//p[normalize-space()='Refresh']").click()
        a=driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").text
        if(a==a):
             print("Refresh Button is Working Fine")
        time.sleep(2)


def test_Locality_Download_Success(driver):
        wait=WebDriverWait(driver,10)
        driver.find_element(By.XPATH,"//p[normalize-space()='Download']").click()
        wait.until(EC.element_to_be_clickable((By.XPATH,"//p[normalize-space()='Download as Excel']"))).click()
        time.sleep(2)


def test_Locality_Return_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > a:nth-child(1) > img:nth-child(1)").click()
        time.sleep(2)
        


def test_Locality_Country_ascending(driver):
    driver.find_element(By.XPATH,"//body/div/div/div/div/div/div/div/div[2]/p[1]/button[1]/span[1]").click()
    Country_list = driver.find_elements(By.XPATH, "//div[contains(@class,'w-[15%]  p-4')]")
    country_names = [country.text for country in Country_list[1:]]

    if is_sorted_ascending_common(country_names):
            print("The country list is sorted in ascending order.")
    else:
            print("The country list is not sorted in ascending order.")
    time.sleep(2)

def test_Locality_Country_descending(driver):
    driver.find_element(By.XPATH,"//body/div/div/div/div/div/div/div/div[2]/p[1]/button[1]/span[1]").click()
    Country_list = driver.find_elements(By.XPATH, "//div[contains(@class,'w-[15%]  p-4')]")
    country_names = [country.text for country in Country_list[1:]]

    if is_sorted_descending_common(country_names):
            print("The country list is sorted in descending order.")
    else:
            print("The country list is not sorted in descending order.")

    time.sleep(2)
    

def test_Locality_State_descending(driver):
    driver.find_element(By.XPATH,"//div//div//div//div//div//div[3]//p[1]//button[1]//span[1]").click()
    State_list = driver.find_elements(By.XPATH, "//div[contains(@class,'w-[20%]  p-4')][position()=1]")
    country_names = [country.text for country in State_list[1:]]

    if is_sorted_descending_common(country_names):
            print("The state list is sorted in descending order.")
    else:
            print("The state list is not sorted in descending order.")

    time.sleep(2)
    

def test_Locality_State_ascending(driver):
    driver.find_element(By.XPATH,"//div//div//div//div//div//div[3]//p[1]//button[1]//span[1]").click()
    state_list = driver.find_elements(By.XPATH, "//div[contains(@class,'w-[20%]  p-4')][position()=1]")
    state_names = [country.text for country in state_list[1:]]

    if is_sorted_ascending_common(state_names):
            print("The state list is sorted in ascending order.")
    else:
            print("The state list is not sorted in ascending order.")
    time.sleep(2)
    

def test_Locality_City_ascending(driver):
    driver.find_element(By.XPATH,"//div[4]//p[1]//button[1]//span[1]").click()
    city_list = driver.find_elements(By.XPATH, "//div[contains(@class,'w-[20%]  p-4')][position()=2]")
    city_names = [country.text for country in city_list[1:]]

    if is_sorted_ascending_common(city_names):
            print("The city list is sorted in ascending order.")
    else:
            print("The city list is not sorted in ascending order.")
    time.sleep(2)
    

def test_Locality_City_descending(driver):
    driver.find_element(By.XPATH,"//div[4]//p[1]//button[1]//span[1]").click()
    city_list = driver.find_elements(By.XPATH, "//div[contains(@class,'w-[20%]  p-4')][position()=2]")
    city_names = [country.text for country in city_list[1:]]

    if is_sorted_descending_common(city_names):
            print("The city list is sorted in descending order.")
    else:
            print("The city list is not sorted in descending order.")
    time.sleep(2)
    

def test_Locality_Localityname_descending(driver):
    driver.find_element(By.XPATH,"//div[5]//p[1]//button[1]//span[1]").click()
    locality_list = driver.find_elements(By.XPATH, "//div[contains(@class,'w-[25%]  p-4 ml-1')]")
    locality_names = [country.text for country in locality_list]

    if is_sorted_descending_common(locality_names):
            print("The Locality list is sorted in descending order.")
    else:
            print("The Locality list is not sorted in descending order.")
    time.sleep(2)
    

def test_Locality_Localityname_ascending(driver):
    driver.find_element(By.XPATH,"//div[5]//p[1]//button[1]//span[1]").click()
    locality_list = driver.find_elements(By.XPATH, "//div[contains(@class,'w-[25%]  p-4 ml-1')]")
    locality_names = [country.text for country in locality_list]

    if is_sorted_ascending_common(locality_names):
            print("The Locality list is sorted in ascending order.")
    else:
            print("The Locality list is not sorted in ascending order.")
    time.sleep(2)
    

def test_Locality_ID_ascending(driver):
    driver.find_element(By.XPATH,"//body/div/div/div/div/div/div/div/div[1]/p[1]/button[1]/span[1]").click()
    locality_list = driver.find_elements(By.XPATH, "//div[contains(@class,'w-1/2  p-4 ml-1')]")
    locality_names = [country.text for country in locality_list]

    if is_sorted_ascending_common(locality_names):
            print("The Locality ID is sorted in ascending order.")
    else:
            print("The Locality ID is not sorted in ascending order.")
    time.sleep(2)
    

def test_Locality_ID_descending(driver):
    driver.find_element(By.XPATH,"//body/div/div/div/div/div/div/div/div[1]/p[1]/button[1]/span[1]").click()
    locality_list = driver.find_elements(By.XPATH, "//div[contains(@class,'w-1/2  p-4 ml-1')]")
    locality_names = [country.text for country in locality_list]

    if is_sorted_descending_common(locality_names):
            print("The Locality ID is sorted in descending order.")
    else:
            print("The Locality ID is not sorted in descending order.")
    time.sleep(2)
    

def Locality_Webpage():
        driver=login_and_navigate_Locality("ruderaw", "abcdefg", "9632")
        test_functions=[
            test_Locality_Country_ascending,
            test_Locality_Country_descending,
            test_Locality_State_ascending,
            test_Locality_State_descending,
            test_Locality_City_ascending,
            test_Locality_City_descending,
            test_Locality_Localityname_ascending,
            test_Locality_Localityname_descending,
            test_Locality_ID_ascending,
            test_Locality_ID_descending,
            test_Filter_Locality_Country_name_StartsWith_Success,
            test_Filter_Locality_Country_name_Contains_Success,
            test_Filter_Locality_Country_name_DoesNotContains_Success,
            test_Filter_Locality_Country_name_EndsWith_Success,
            test_Filter_Locality_Country_name_EqualsTo_Success,
            test_Filter_Locality_Country_name_isNotNull_Success,
            test_Filter_Locality_Country_name_isNull_Success,
            test_Filter_Locality_Country_name_NoFilter_Success,
            test_Filter_Locality_State_name_StartsWith_Success,
            test_Filter_Locality_State_name_Contains_Success,
            test_Filter_Locality_State_name_DoesNotContains_Success,
            test_Filter_Locality_State_name_EndsWith_Success,
            test_Filter_Locality_State_name_EqualsTo_Success,
            test_Filter_Locality_State_name_isNotNull_Success,
            test_Filter_Locality_State_name_isNull_Success,
            test_Filter_Locality_State_name_NoFilter_Success,
            test_Filter_Locality_City_name_StartsWith_Success,
            test_Filter_Locality_City_name_Contains_Success,
            test_Filter_Locality_City_name_DoesNotContains_Success,
            test_Filter_Locality_City_name_EndsWith_Success,
            test_Filter_Locality_City_name_EqualsTo_Success,
            test_Filter_Locality_City_name_isNotNull_Success,
            test_Filter_Locality_City_name_isNull_Success,
            test_Filter_Locality_City_name_NoFilter_Success,
            test_Filter_Locality_name_StartsWith_Success,
            test_Filter_Locality_name_Contains_Success,
            test_Filter_Locality_name_DoesNotContains_Success,
            test_Filter_Locality_name_EndsWith_Success,
            test_Filter_Locality_name_EqualsTo_Success,
            test_Filter_Locality_name_isNotNull_Success,
            test_Filter_Locality_name_isNull_Success,
            test_Filter_Locality_name_NoFilter_Success,
            test_Filter_Locality_ID_EqualsTo_Success,
            test_Filter_Locality_ID_NotEqualTo_Success,
            test_Filter_Locality_ID_GreaterThan_Success,
            test_Filter_Locality_ID_LessThan_Success,
            test_Filter_Locality_ID_GreaterThanOrEqualTo_Success,
            test_Filter_Locality_ID_LessThanOrEqualTo_Success,
            test_Filter_Locality_ID_isNull_Success,
            test_Filter_Locality_ID_isNotNull_Success,
            test_Filter_Locality_ID_NoFilter_Success,
            test_Filter_Locality_Pagination_15_Success,
            test_Filter_Locality_Pagination_25_Success,
            test_Filter_Locality_Pagination_50_Success,
            test_Add_New_Locality_Success,
            test_Edit_Locality_Success,
            test_Filter_Locality_Refresh_Success,
            test_Locality_Download_Success,
            test_Locality_Return_Success       
        ]
        for test_func in test_functions:
              test_func(driver)

Locality_Webpage()


# %%
def login_and_navigate_Managebuilder(username, password, comkey):
    driver = webdriver.Chrome()
    driver.get(drivers_config["login_url"])
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.NAME, "comkey").send_keys(comkey)
    login_button = driver.find_element(By.CSS_SELECTOR, "button[class='bg-[#004DD7] w-[200px] h-[35px] text-white text-[18px] rounded-lg cursor-pointer']")
    assert not login_button.get_attribute("disabled"), "Login button should be enabled"
    login_button.click()
    manage_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "body div div div div div div:nth-child(2) button:nth-child(1) p:nth-child(1)"))
        )
    assert not manage_button.get_attribute("disabled"), "Admin button should be enabled"
    manage_button.click()
    driver.find_element(By.XPATH,"//a[normalize-space()='Manage Builder']").click()
    time.sleep(2)
    return driver

# %%
def addBuilder(driver):
    driver.find_element(By.XPATH,"//body//div//div//div//div//div//div//div//button//div").click()
    driver.find_element(By.XPATH,"//body//div[@role='presentation']//div//div//div//div//div//div[1]//input[1]").send_keys("test_builder")
    driver.find_element(By.XPATH,"//body//div[@role='presentation']//div//div//div//div//div//div[2]//input[1]").send_keys("123456789")
    driver.find_element(By.XPATH,"//body//div[@role='presentation']//div//div//div//div//div[1]//div[6]//input[1]").send_keys("test_Pune")
    time.sleep(2)
    a=driver.find_element(By.XPATH,"//select[@name='country']")
    drp=Select(a)
    drp.select_by_visible_text('India')
    time.sleep(2)
    b=driver.find_element(By.XPATH,"//select[@name='state']")
    drp1=Select(b)
    drp1.select_by_visible_text('Maharashtra')
    time.sleep(2)
    c=driver.find_element(By.XPATH,"//body[1]/div[2]/div[3]/div[1]/form[1]/div[1]/div[1]/div[2]/div[3]/select[1]")
    drp2=Select(c)
    drp2.select_by_visible_text("Pune")
    driver.find_element(By.XPATH,"//input[@name='suburb']").send_keys("a")
    driver.find_element(By.XPATH,"//button[@type='submit']").click()
    time.sleep(2)
    driver.find_element(By.XPATH,"//body/div[contains(@role,'presentation')]/div/div/button[1]").click()
    time.sleep(3)
    driver.find_element(By.XPATH,"//input[@type='text']").send_keys("test_builder")
    time.sleep(2)
    driver.find_element(By.XPATH,"//img[@alt='search-icon']").click()
    time.sleep(2)
    driver.find_element(By.XPATH,"//img[@alt='trash']").click()
    time.sleep(2)
    driver.find_element(By.XPATH,"//div[contains(@role,'presentation')]//button[1]").click()
    time.sleep(2)



# %%
def editBuilder(driver):
    driver.find_element(By.XPATH,"//body//div//div//div//div//div//div//div//button//div").click()
    driver.find_element(By.XPATH,"//body//div[@role='presentation']//div//div//div//div//div//div[1]//input[1]").send_keys("test_builder")
    driver.find_element(By.XPATH,"//body//div[@role='presentation']//div//div//div//div//div//div[2]//input[1]").send_keys("123456789")
    driver.find_element(By.XPATH,"//body//div[@role='presentation']//div//div//div//div//div[1]//div[6]//input[1]").send_keys("test_Pune")
    time.sleep(2)
    a=driver.find_element(By.XPATH,"//select[@name='country']")
    drp=Select(a)
    drp.select_by_visible_text('India')
    time.sleep(2)
    b=driver.find_element(By.XPATH,"//select[@name='state']")
    drp1=Select(b)
    drp1.select_by_visible_text('Maharashtra')
    time.sleep(2)
    c=driver.find_element(By.XPATH,"//body[1]/div[2]/div[3]/div[1]/form[1]/div[1]/div[1]/div[2]/div[3]/select[1]")
    drp2=Select(c)
    drp2.select_by_visible_text("Pune")
    driver.find_element(By.XPATH,"//input[@name='suburb']").send_keys("a")
    driver.find_element(By.XPATH,"//button[@type='submit']").click()
    time.sleep(2)
    driver.find_element(By.XPATH,"//body/div[contains(@role,'presentation')]/div/div/button[1]").click()
    time.sleep(3)
    # driver.find_element(By.XPATH,"//input[@type='text']").send_keys("test_builder")
    # time.sleep(2)
    driver.find_element(By.XPATH,"//img[@alt='search-icon']").click()
    time.sleep(2)
    driver.find_element(By.XPATH,"//img[@alt='edit']").click()
    driver.find_element(By.XPATH,"//body//div[@role='presentation']//div//div//div//div//div//div[1]//input[1]").clear()
    driver.find_element(By.XPATH,"//body//div[@role='presentation']//div//div//div//div//div//div[1]//input[1]").send_keys("ashish")
    driver.find_element(By.XPATH,"//button[@type='submit']").click()
    time.sleep(4)
    driver.find_element(By.XPATH,"//input[@type='text']").clear()
    driver.find_element(By.XPATH,"//input[@type='text']").send_keys("ashish")
    time.sleep(2)
    driver.find_element(By.XPATH,"//img[@alt='search-icon']").click()
    time.sleep(2)
    driver.find_element(By.XPATH,"//img[@alt='trash']").click()
    time.sleep(2)
    driver.find_element(By.XPATH,"//div[contains(@role,'presentation')]//button[1]").click()
    time.sleep(2)



# %%
def test_filter_Builder_Name_StartsWith(driver,send_letter):
        driver.find_element(By.CSS_SELECTOR,"body div div div div div div div:nth-child(2) div:nth-child(1) input:nth-child(1)").send_keys(send_letter)
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        time.sleep(2)

# %%
def test_Filter_Builder_name_Contains_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body div div div div div div div:nth-child(2) div:nth-child(1) input:nth-child(1)").clear()
        test_filter_Builder_Name_StartsWith(driver,"a")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='Contains']").click()
        driver.find_element(By.XPATH,"//div[@id='root']//div//div//div//div//div//div//h1").click()
        time.sleep(2)
        


# %%
def test_Filter_Builder_name_DoesNotContains_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body div div div div div div div:nth-child(2) div:nth-child(1) input:nth-child(1)").clear()
        test_filter_Builder_Name_StartsWith(driver,"a")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='DoesNotContain']").click()
        driver.find_element(By.XPATH,"//div[@id='root']//div//div//div//div//div//div//h1").click()
        time.sleep(2)
        


# %%
def test_Filter_Builder_name_StartsWith_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body div div div div div div div:nth-child(2) div:nth-child(1) input:nth-child(1)").clear()
        test_filter_Builder_Name_StartsWith(driver,"a")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='StartsWith']").click()
        driver.find_element(By.XPATH,"//div[@id='root']//div//div//div//div//div//div//h1").click()
        time.sleep(2)
        


# %%
def test_Filter_Builder_name_EndsWith_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body div div div div div div div:nth-child(2) div:nth-child(1) input:nth-child(1)").clear()
        test_filter_Builder_Name_StartsWith(driver,"a")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='EndsWith']").click()
        driver.find_element(By.XPATH,"//div[@id='root']//div//div//div//div//div//div//h1").click()
        time.sleep(2)
        


# %%
def test_Filter_Builder_name_EqualsTo_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body div div div div div div div:nth-child(2) div:nth-child(1) input:nth-child(1)").clear()
        test_filter_Builder_Name_StartsWith(driver,"a")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='EqualTo']").click()
        driver.find_element(By.XPATH,"//div[@id='root']//div//div//div//div//div//div//h1").click()
        time.sleep(2)
        


# %%
def test_Filter_Builder_name_isNull_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body div div div div div div div:nth-child(2) div:nth-child(1) input:nth-child(1)").clear()
        test_filter_Builder_Name_StartsWith(driver,"a")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='isNull']").click()
        driver.find_element(By.XPATH,"//div[@id='root']//div//div//div//div//div//div//h1").click()
        time.sleep(2)
        


# %%
def test_Filter_Builder_name_isNotNull_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body div div div div div div div:nth-child(2) div:nth-child(1) input:nth-child(1)").clear()
        test_filter_Builder_Name_StartsWith(driver,"a")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='isNotNull']").click()
        driver.find_element(By.XPATH,"//div[@id='root']//div//div//div//div//div//div//h1").click()
        time.sleep(2)
        


# %%
def test_Filter_Builder_name_NoFilter_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body div div div div div div div:nth-child(2) div:nth-child(1) input:nth-child(1)").clear()
        test_filter_Builder_Name_StartsWith(driver,"a")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='No Filter']").click()
        driver.find_element(By.XPATH,"//div[@id='root']//div//div//div//div//div//div//h1").click()
        time.sleep(2)
        


# %%
def test_filter_Builder_Country_StartsWith(driver,send_letter):
        driver.find_element(By.CSS_SELECTOR,"div:nth-child(3) div:nth-child(1) input:nth-child(1)").send_keys(send_letter)
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        time.sleep(2)

# %%
def test_Filter_Builder_Country_Contains_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"div:nth-child(3) div:nth-child(1) input:nth-child(1)").clear()
        test_filter_Builder_Country_StartsWith(driver,"Sri Lanka")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='Contains']").click()
        driver.find_element(By.XPATH,"//div[@id='root']//div//div//div//div//div//div//h1").click()
        time.sleep(2)
        


# %%
def test_Filter_Builder_Country_DoesNotContains_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"div:nth-child(3) div:nth-child(1) input:nth-child(1)").clear()
        test_filter_Builder_Country_StartsWith(driver,"Sri Lanka")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='DoesNotContain']").click()
        driver.find_element(By.XPATH,"//div[@id='root']//div//div//div//div//div//div//h1").click()
        time.sleep(2)
        


# %%
def test_Filter_Builder_Country_StartsWith_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"div:nth-child(3) div:nth-child(1) input:nth-child(1)").clear()
        test_filter_Builder_Country_StartsWith(driver,"Sri Lanka")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='StartsWith']").click()
        driver.find_element(By.XPATH,"//div[@id='root']//div//div//div//div//div//div//h1").click()
        time.sleep(2)
        


# %%
def test_Filter_Builder_Country_EndsWith_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"div:nth-child(3) div:nth-child(1) input:nth-child(1)").clear()
        test_filter_Builder_Country_StartsWith(driver,"Sri Lanka")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='EndsWith']").click()
        driver.find_element(By.XPATH,"//div[@id='root']//div//div//div//div//div//div//h1").click()
        time.sleep(2)
        


# %%
def test_Filter_Builder_Country_EqualsTo_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"div:nth-child(3) div:nth-child(1) input:nth-child(1)").clear()
        test_filter_Builder_Country_StartsWith(driver,"Sri Lanka")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='EqualTo']").click()
        driver.find_element(By.XPATH,"//div[@id='root']//div//div//div//div//div//div//h1").click()
        time.sleep(2)
        


# %%
def test_Filter_Builder_Country_isNull_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"div:nth-child(3) div:nth-child(1) input:nth-child(1)").clear()
        test_filter_Builder_Country_StartsWith(driver,"Sri Lanka")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='isNull']").click()
        driver.find_element(By.XPATH,"//div[@id='root']//div//div//div//div//div//div//h1").click()
        time.sleep(2)
        


# %%
def test_Filter_Builder_Country_isNotNull_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"div:nth-child(3) div:nth-child(1) input:nth-child(1)").clear()
        test_filter_Builder_Country_StartsWith(driver,"Sri Lanka")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='isNotNull']").click()
        driver.find_element(By.XPATH,"//div[@id='root']//div//div//div//div//div//div//h1").click()
        time.sleep(2)
        


# %%
def test_Filter_Builder_Country_NoFilter_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"div:nth-child(3) div:nth-child(1) input:nth-child(1)").clear()
        test_filter_Builder_Country_StartsWith(driver,"Sri Lanka")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='No Filter']").click()
        driver.find_element(By.XPATH,"//div[@id='root']//div//div//div//div//div//div//h1").click()
        time.sleep(2)
        


# %%
def test_filter_Builder_City_StartsWith(driver,send_letter):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)").send_keys(send_letter)
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        time.sleep(2)

# %%
def test_Filter_Builder_City_Contains_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_Builder_City_StartsWith(driver,"Pune")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='Contains']").click()
        driver.find_element(By.XPATH,"//div[@id='root']//div//div//div//div//div//div//h1").click()
        time.sleep(2)
        


# %%
def test_Filter_Builder_City_DoesNotContains_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_Builder_City_StartsWith(driver,"Pune")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='DoesNotContain']").click()
        driver.find_element(By.XPATH,"//div[@id='root']//div//div//div//div//div//div//h1").click()
        time.sleep(2)
        


# %%
def test_Filter_Builder_City_StartsWith_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_Builder_City_StartsWith(driver,"Pune")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='StartsWith']").click()
        driver.find_element(By.XPATH,"//div[@id='root']//div//div//div//div//div//div//h1").click()
        time.sleep(2)
        


# %%
def test_Filter_Builder_City_EndsWith_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_Builder_City_StartsWith(driver,"Pune")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='EndsWith']").click()
        driver.find_element(By.XPATH,"//div[@id='root']//div//div//div//div//div//div//h1").click()
        time.sleep(2)
        


# %%
def test_Filter_Builder_City_EqualTo_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_Builder_City_StartsWith(driver,"Pune")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='EqualTo']").click()
        driver.find_element(By.XPATH,"//div[@id='root']//div//div//div//div//div//div//h1").click()
        time.sleep(2)
        


# %%
def test_Filter_Builder_City_isNull_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_Builder_City_StartsWith(driver,"Pune")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='isNull']").click()
        driver.find_element(By.XPATH,"//div[@id='root']//div//div//div//div//div//div//h1").click()
        time.sleep(2)
        


# %%
def test_Filter_Builder_City_isNotNull_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_Builder_City_StartsWith(driver,"Pune")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='isNotNull']").click()
        driver.find_element(By.XPATH,"//div[@id='root']//div//div//div//div//div//div//h1").click()
        time.sleep(2)
        


# %%
def test_Filter_Builder_City_NoFilter_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_Builder_City_StartsWith(driver,"Pune")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='No Filter']").click()
        driver.find_element(By.XPATH,"//div[@id='root']//div//div//div//div//div//div//h1").click()
        time.sleep(2)
        


# %%
def test_filter_Builder_Suburb_StartsWith(driver,send_letter):
        driver.find_element(By.CSS_SELECTOR,"div:nth-child(5) div:nth-child(1) input:nth-child(1)").send_keys(send_letter)
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(5) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        time.sleep(2)

# %%
def test_Filter_Builder_Suburb_Contains_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"div:nth-child(5) div:nth-child(1) input:nth-child(1)").clear()
        test_filter_Builder_Suburb_StartsWith(driver,"ijkl")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='Contains']").click()
        driver.find_element(By.XPATH,"//div[@id='root']//div//div//div//div//div//div//h1").click()
        time.sleep(2)
        


# %%
def test_Filter_Builder_Suburb_DoesNotContains_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"div:nth-child(5) div:nth-child(1) input:nth-child(1)").clear()
        test_filter_Builder_Suburb_StartsWith(driver,"ijkl")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='DoesNotContain']").click()
        driver.find_element(By.XPATH,"//div[@id='root']//div//div//div//div//div//div//h1").click()
        time.sleep(2)
        


# %%
def test_Filter_Builder_Suburb_StartsWith_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"div:nth-child(5) div:nth-child(1) input:nth-child(1)").clear()
        test_filter_Builder_Suburb_StartsWith(driver,"ijkl")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='StartsWith']").click()
        driver.find_element(By.XPATH,"//div[@id='root']//div//div//div//div//div//div//h1").click()
        time.sleep(2)
        


# %%
def test_Filter_Builder_Suburb_EndsWith_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"div:nth-child(5) div:nth-child(1) input:nth-child(1)").clear()
        test_filter_Builder_Suburb_StartsWith(driver,"ijkl")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='EndsWith']").click()
        driver.find_element(By.XPATH,"//div[@id='root']//div//div//div//div//div//div//h1").click()
        time.sleep(2)
        


# %%
def test_Filter_Builder_Suburb_EqualsTo_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"div:nth-child(5) div:nth-child(1) input:nth-child(1)").clear()
        test_filter_Builder_Suburb_StartsWith(driver,"ijkl")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='EqualTo']").click()
        driver.find_element(By.XPATH,"//div[@id='root']//div//div//div//div//div//div//h1").click()
        time.sleep(2)
        


# %%
def test_Filter_Builder_Suburb_isNull_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"div:nth-child(5) div:nth-child(1) input:nth-child(1)").clear()
        test_filter_Builder_Suburb_StartsWith(driver,"ijkl")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='isNull']").click()
        driver.find_element(By.XPATH,"//div[@id='root']//div//div//div//div//div//div//h1").click()
        time.sleep(2)
        


# %%
def test_Filter_Builder_Suburb_isNotNull_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"div:nth-child(5) div:nth-child(1) input:nth-child(1)").clear()
        test_filter_Builder_Suburb_StartsWith(driver,"ijkl")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='isNotNull']").click()
        driver.find_element(By.XPATH,"//div[@id='root']//div//div//div//div//div//div//h1").click()
        time.sleep(2)
        


# %%
def test_Filter_Builder_Suburb_NoFilter_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"div:nth-child(5) div:nth-child(1) input:nth-child(1)").clear()
        test_filter_Builder_Suburb_StartsWith(driver,"ijkl")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='No Filter']").click()
        driver.find_element(By.XPATH,"//div[@id='root']//div//div//div//div//div//div//h1").click()
        time.sleep(2)
        


# %%
def test_filter_Builder_ID_StartsWith(driver,send_letter):
        driver.find_element(By.CSS_SELECTOR,"body div[id='root'] div div div div div div:nth-child(1) div:nth-child(1) input:nth-child(1)").send_keys(send_letter)
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        time.sleep(2)

# %%
def test_Filter_Builder_ID_EqualTo_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body div[id='root'] div div div div div div:nth-child(1) div:nth-child(1) input:nth-child(1)").clear()
        test_filter_Builder_ID_StartsWith(driver,"11")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='EqualTo']").click()
        driver.find_element(By.XPATH,"//div[@id='root']//div//div//div//div//div//div//h1").click()
        time.sleep(2)
        


# %%
def test_Filter_Builder_ID_NotEqualTo_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body div[id='root'] div div div div div div:nth-child(1) div:nth-child(1) input:nth-child(1)").clear()
        test_filter_Builder_ID_StartsWith(driver,"11")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='NotEqualTo']").click()
        driver.find_element(By.XPATH,"//div[@id='root']//div//div//div//div//div//div//h1").click()
        time.sleep(2)
        


# %%
def test_Filter_Builder_ID_GreaterThan_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body div[id='root'] div div div div div div:nth-child(1) div:nth-child(1) input:nth-child(1)").clear()
        test_filter_Builder_ID_StartsWith(driver,"11")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='GreaterThan']").click()
        driver.find_element(By.XPATH,"//div[@id='root']//div//div//div//div//div//div//h1").click()
        time.sleep(2)
        


# %%
def test_Filter_Builder_ID_LessThan_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body div[id='root'] div div div div div div:nth-child(1) div:nth-child(1) input:nth-child(1)").clear()
        test_filter_Builder_ID_StartsWith(driver,"11")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='LessThan']").click()
        driver.find_element(By.XPATH,"//div[@id='root']//div//div//div//div//div//div//h1").click()
        time.sleep(2)
        


# %%
def test_Filter_Builder_ID_GreaterThanOrEqualTo_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body div[id='root'] div div div div div div:nth-child(1) div:nth-child(1) input:nth-child(1)").clear()
        test_filter_Builder_ID_StartsWith(driver,"11")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='GreaterThanOrEqualTo']").click()
        driver.find_element(By.XPATH,"//div[@id='root']//div//div//div//div//div//div//h1").click()
        time.sleep(2)
        


# %%
def test_Filter_Builder_ID_LessThanOrEqualTo_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body div[id='root'] div div div div div div:nth-child(1) div:nth-child(1) input:nth-child(1)").clear()
        test_filter_Builder_ID_StartsWith(driver,"11")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='LessThanOrEqualTo']").click()
        driver.find_element(By.XPATH,"//div[@id='root']//div//div//div//div//div//div//h1").click()
        time.sleep(2)
        


# %%
def test_Filter_Builder_ID_isNull_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body div[id='root'] div div div div div div:nth-child(1) div:nth-child(1) input:nth-child(1)").clear()
        test_filter_Builder_ID_StartsWith(driver,"11")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='isNull']").click()
        driver.find_element(By.XPATH,"//div[@id='root']//div//div//div//div//div//div//h1").click()
        time.sleep(2)
        


# %%
def test_Filter_Builder_ID_isNotNull_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body div[id='root'] div div div div div div:nth-child(1) div:nth-child(1) input:nth-child(1)").clear()
        test_filter_Builder_ID_StartsWith(driver,"11")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='isNotNull']").click()
        driver.find_element(By.XPATH,"//div[@id='root']//div//div//div//div//div//div//h1").click()
        time.sleep(2)
        


# %%
def test_Filter_Builder_ID_NoFilter_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body div[id='root'] div div div div div div:nth-child(1) div:nth-child(1) input:nth-child(1)").clear()
        test_filter_Builder_ID_StartsWith(driver,"11")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='No Filter']").click()
        driver.find_element(By.XPATH,"//div[@id='root']//div//div//div//div//div//div//h1").click()
        time.sleep(2)
        


# %%
def Builder_Name_ascending(driver):
    driver.find_element(By.XPATH,"//body/div[@id='root']/div/div/div/div/div/div/div[2]/p[1]/button[1]/span[1]").click()
    time.sleep(2)

# %%
def Builder_Name_descending(driver):
    driver.find_element(By.XPATH,"//body/div[@id='root']/div/div/div/div/div/div/div[2]/p[1]/button[1]/span[1]").click()
    time.sleep(2)

# %%
def Builder_Country_descending(driver):
    driver.find_element(By.XPATH,"//body//div[@id='root']//div//div//div//div//div[3]//p[1]//button[1]//span[1]").click()
    time.sleep(2)

# %%
def Builder_Country_ascending(driver):
    driver.find_element(By.XPATH,"//body//div[@id='root']//div//div//div//div//div[3]//p[1]//button[1]//span[1]").click()
    time.sleep(2)

# %%
def Builder_City_ascending(driver):
    driver.find_element(By.XPATH,"//div[4]//p[1]//button[1]//span[1]").click()
    time.sleep(2)

# %%
def Builder_City_descending(driver):
    driver.find_element(By.XPATH,"//div[4]//p[1]//button[1]//span[1]").click()
    time.sleep(2)

# %%
def Builder_Suburb_descending(driver):
    driver.find_element(By.XPATH,"//div[5]//p[1]//button[1]//span[1]").click()
    time.sleep(2)

# %%
def Builder_Suburb_ascending(driver):
    driver.find_element(By.XPATH,"//div[5]//p[1]//button[1]//span[1]").click()
    time.sleep(2)

# %%
def Builder_ID_ascending(driver):
    driver.find_element(By.XPATH,"//body/div[@id='root']/div/div/div/div/div/div/div[1]/p[1]/button[1]/span[1]").click()
    time.sleep(2)

# %%
def Builder_ID_descending(driver):
    driver.find_element(By.XPATH,"//body/div[@id='root']/div/div/div/div/div/div/div[1]/p[1]/button[1]/span[1]").click()
    time.sleep(2)

# %%
def Builder_Pagination15_Success(driver):
    a=driver.find_element(By.XPATH,"//div[@id='root']//div//div//div//div//div//select")
    drop=Select(a)
    drop.select_by_visible_text("15")
    time.sleep(2)
    driver.find_element(By.XPATH,"//button[@aria-label='Go to page 2']").click()
    time.sleep(2)

# %%
def Builder_Pagination25_Success(driver):
    a=driver.find_element(By.XPATH,"//div[@id='root']//div//div//div//div//div//select")
    drop=Select(a)
    drop.select_by_visible_text("25")
    time.sleep(2)
    driver.find_element(By.XPATH,"//button[@aria-label='Go to page 2']").click()
    time.sleep(2)

# %%
def Builder_Pagination50_Success(driver):
    a=driver.find_element(By.XPATH,"//div[@id='root']//div//div//div//div//div//select")
    drop=Select(a)
    drop.select_by_visible_text("50")
    time.sleep(2)
    driver.find_element(By.XPATH,"//button[@aria-label='Go to page 2']").click()
    time.sleep(2)

# %%
def Builder_Refresh(driver):
    driver.find_element(By.XPATH,"//p[normalize-space()='Refresh']").click()
    time.sleep(2)

# %%
def Builder_Download(driver):
    driver.find_element(By.XPATH,"//p[normalize-space()='Download']").click()
    time.sleep(2)

# %%
def Builder_webpage():
    try:
        driver=login_and_navigate_Managebuilder("ruderaw", "abcdefg", "9632")
        Builder_Name_ascending(driver)
        Builder_Name_descending(driver)
        Builder_Country_ascending(driver)
        Builder_Country_descending(driver)
        Builder_City_ascending(driver)
        Builder_City_descending(driver)
        Builder_Suburb_ascending(driver)
        Builder_Suburb_descending(driver)
        Builder_ID_ascending(driver)
        Builder_ID_ascending(driver)
        Builder_Pagination15_Success(driver)
        Builder_Pagination25_Success(driver)
        Builder_Pagination50_Success(driver)
        test_Filter_Builder_name_Contains_Success(driver)
        test_Filter_Builder_name_DoesNotContains_Success(driver)
        test_Filter_Builder_name_StartsWith_Success(driver)
        test_Filter_Builder_name_EndsWith_Success(driver)
        test_Filter_Builder_name_EqualsTo_Success(driver)
        test_Filter_Builder_name_isNull_Success(driver)
        test_Filter_Builder_name_isNotNull_Success(driver)
        test_Filter_Builder_name_NoFilter_Success(driver)
        test_Filter_Builder_Country_Contains_Success(driver)
        test_Filter_Builder_Country_DoesNotContains_Success(driver)
        test_Filter_Builder_Country_StartsWith_Success(driver)
        test_Filter_Builder_Country_EndsWith_Success(driver)
        test_Filter_Builder_Country_EqualsTo_Success(driver)
        test_Filter_Builder_Country_isNull_Success(driver)
        test_Filter_Builder_Country_isNotNull_Success(driver)
        test_Filter_Builder_Country_NoFilter_Success(driver)
        test_Filter_Builder_City_Contains_Success(driver)
        test_Filter_Builder_City_DoesNotContains_Success(driver)
        test_Filter_Builder_City_StartsWith_Success(driver)
        test_Filter_Builder_City_EndsWith_Success(driver)
        test_Filter_Builder_City_EqualTo_Success(driver)
        test_Filter_Builder_City_isNull_Success(driver)
        test_Filter_Builder_City_isNotNull_Success(driver)
        test_Filter_Builder_City_NoFilter_Success(driver)
        test_Filter_Builder_Suburb_Contains_Success(driver)
        test_Filter_Builder_Suburb_DoesNotContains_Success(driver)
        test_Filter_Builder_Suburb_StartsWith_Success(driver)
        test_Filter_Builder_Suburb_EndsWith_Success(driver)
        test_Filter_Builder_Suburb_EqualsTo_Success(driver)
        test_Filter_Builder_Suburb_isNull_Success(driver)
        test_Filter_Builder_Suburb_isNotNull_Success(driver)
        test_Filter_Builder_Suburb_NoFilter_Success(driver)
        test_Filter_Builder_ID_EqualTo_Success(driver)
        test_Filter_Builder_ID_NotEqualTo_Success(driver)
        test_Filter_Builder_ID_GreaterThan_Success(driver)
        test_Filter_Builder_ID_GreaterThanOrEqualTo_Success(driver)
        test_Filter_Builder_ID_LessThan_Success(driver)
        test_Filter_Builder_ID_LessThanOrEqualTo_Success(driver)
        test_Filter_Builder_ID_isNull_Success(driver)
        test_Filter_Builder_ID_isNotNull_Success(driver)
        test_Filter_Builder_ID_NoFilter_Success(driver)
        addBuilder(driver)
        editBuilder(driver)
        Builder_Refresh(driver)
        Builder_Download(driver)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
    
Builder_webpage()


