

# %%
import os
import time
import ui_config
import ipytest
ipytest.autoconfig()
ipytest.config.rewrite_asserts = True
from ui_config import drivers_config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import random
import string


# %%
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

# %%
def test_login_success(driver):
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

# %%

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


# %%

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


# %%

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


# %%
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


# %%
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



# %%
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


# %%
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


# %%
def test_Dashboard_Research(driver):
        driver.find_element(By.XPATH,"//p[normalize-space()='Research']").click()
        time.sleep(2)


# %%
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
        


# %%
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

# %%
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

# %%
def add_new_employee(driver,employee_name, pan_no, username, doj, designation, email, dob, last_dow, role, ph_no, country, state, city, suburb, entity):
    driver.find_element(By.CSS_SELECTOR, ".flex.items-center.justify-center.gap-4").click()
    time.sleep(2)
    driver.find_element(By.XPATH,"//input[@name='employeeName']").send_keys(employee_name)
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
    time.sleep(2)
    element3=driver.find_element(By.XPATH,"//select[@name='country']")
    drp3=Select(element3)
    drp3.select_by_visible_text(country)
    time.sleep(2)
    element4=driver.find_element(By.XPATH,"//select[contains(@name,'state')]")
    drp4=Select(element4)
    drp4.select_by_visible_text(state)
    time.sleep(2)
    element5=driver.find_element(By.XPATH,"//select[@name='city']")
    drp5=Select(element5)
    drp5.select_by_visible_text(city)
    time.sleep(2)
    driver.find_element(By.XPATH,"//input[@name='suburb']").send_keys(suburb)
    time.sleep(2)
    element6=driver.find_element(By.XPATH,"//select[@name='entity']")
    drp6=Select(element6)
    drp6.select_by_visible_text(entity)
    driver.find_element(By.XPATH, "//button[normalize-space()='Add']").click()
    time.sleep(2)
    driver.find_element(By.XPATH,"//button[normalize-space()='Save']").click()
    time.sleep(4)
    driver.find_element(By.XPATH,"//body/div[@id='root']/div/div/div/div/div/div/input[1]").send_keys("aryan ashish")
    time.sleep(2)
    driver.find_element(By.XPATH,"//img[@alt='search-icon']").click()
    time.sleep(2)
    driver.find_element(By.XPATH,"//img[@alt='trash']").click()
    time.sleep(2)
    driver.find_element(By.XPATH,"//body/div[@role='presentation']/div/div/div/button[1]").click()
    time.sleep(2)
    
   


# add_new_employee(driver, "aryan ashish", "ijklmn", "Admin User", "06-05-2024", "intern", "ashish.com", "06-05-2003", "31-05-2024", "Admin", "11100000", "UAE", "UAE", "Dubai", "q", "Z-CASH")


# %%
def test_Add_New_Employee_button(driver):
        driver.find_element(By.CSS_SELECTOR, ".flex.items-center.justify-center.gap-4").click()
        time.sleep(2)

# %%
def test_Edit_Employee_Success(driver):
    try:
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
        time.sleep(2)
        element3=driver.find_element(By.XPATH,"//select[@name='country']")
        drp3=Select(element3)
        drp3.select_by_visible_text('UAE')
        time.sleep(2)
        element4=driver.find_element(By.XPATH,"//select[contains(@name,'state')]")
        drp4=Select(element4)
        drp4.select_by_visible_text('UAE')
        time.sleep(2)
        element5=driver.find_element(By.XPATH,"//select[@name='city']")
        drp5=Select(element5)
        drp5.select_by_visible_text('Dubai')
        time.sleep(2)
        driver.find_element(By.XPATH,"//input[@name='suburb']").send_keys("q")
        time.sleep(2)
        element6=driver.find_element(By.XPATH,"//select[@name='entity']")
        drp6=Select(element6)
        drp6.select_by_visible_text('Z-CASH')
        driver.find_element(By.XPATH, "//button[normalize-space()='Add']").click()
        time.sleep(2)
        driver.find_element(By.XPATH,"//button[normalize-space()='Save']").click()
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
        time.sleep(2)
        driver.find_element(By.XPATH,"//div//div//div//div[1]//div[2]//div[2]//button[2]//img[1]").click()
        time.sleep(2)
        driver.find_element(By.XPATH,"//button[normalize-space()='Delete']").click()
        time.sleep(2)
        driver.find_element(By.XPATH,"//body/div/div/div/div/div/div/div/input[1]").clear()
        driver.find_element(By.XPATH,"//img[@alt='search-icon']").click()
        time.sleep(2)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
        


# %%
def filter_employee_name_starts_with(driver, starts_with_letter):
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").send_keys(starts_with_letter)
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        time.sleep(2)



# %%
def test_Filter_Employee_Name_StartsWith_Success(driver):
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        filter_employee_name_starts_with(driver, "a")
        driver.find_element(By.XPATH,"//h1[normalize-space()='StartsWith']").click()   
        time.sleep(2)
        



# %%
def test_Filter_Employee_Name_Contains_Success(driver):
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        filter_employee_name_starts_with(driver, "a")
        driver.find_element(By.XPATH,"//h1[normalize-space()='Contains']").click()
        time.sleep(2)



# %%
def test_Filter_Employee_Name_DoesNotContains_Success(driver):
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        filter_employee_name_starts_with(driver, "a")
        driver.find_element(By.XPATH,"//h1[normalize-space()='DoesNotContain']").click()
        time.sleep(2)



# %%
def test_Filter_Employee_Name_EndsWith_Success(driver):
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        filter_employee_name_starts_with(driver, "a")
        driver.find_element(By.XPATH,"//h1[normalize-space()='EndsWith']").click()
        time.sleep(2)



# %%
def test_Filter_Employee_Name_EqualTo_Success(driver):
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        filter_employee_name_starts_with(driver, "a")
        driver.find_element(By.XPATH,"//h1[normalize-space()='EqualTo']").click()
        time.sleep(2)


# %%
def test_Filter_Employee_Name_isNotNull_Success(driver):
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        filter_employee_name_starts_with(driver, "a")
        driver.find_element(By.XPATH,"//h1[normalize-space()='isNotNull']").click()
        time.sleep(2)


# %%
def test_Filter_Employee_Name_isNull_Success(driver):
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        filter_employee_name_starts_with(driver, "a")
        driver.find_element(By.XPATH,"//h1[normalize-space()='isNull']").click()
        time.sleep(2)


# %%
def test_Filter_Employee_Name_NoFilter_Success(driver):
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        filter_employee_name_starts_with(driver, "a")
        driver.find_element(By.XPATH,"//h1[normalize-space()='No Filter']").click()
        driver.find_element(By.XPATH,"//body/div/div/div/div/div/div/div/div[2]/div[1]/input[1]").clear()
        time.sleep(2)


# %%
def filter_employee_ID_starts_with(driver, starts_with_letter):
        driver.find_element(By.CSS_SELECTOR, "div:nth-child(3) div:nth-child(1) input:nth-child(1)").send_keys(starts_with_letter)
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        time.sleep(2)


# %%
def test_Filter_Employee_ID_StartsWith_Success(driver):
        driver.find_element(By.CSS_SELECTOR, "div:nth-child(3) div:nth-child(1) input:nth-child(1)").clear()
        filter_employee_ID_starts_with(driver,"a")
        driver.find_element(By.XPATH,"//h1[normalize-space()='StartsWith']").click()
        time.sleep(2)



# %%
def test_Filter_Employee_ID_Contains_Success(driver):
        driver.find_element(By.CSS_SELECTOR, "div:nth-child(3) div:nth-child(1) input:nth-child(1)").clear()
        filter_employee_ID_starts_with(driver,"a")
        driver.find_element(By.XPATH,"//h1[normalize-space()='Contains']").click()
        time.sleep(2)


# %%
def test_Filter_Employee_ID_DoesNotContains_Success(driver):
        driver.find_element(By.CSS_SELECTOR, "div:nth-child(3) div:nth-child(1) input:nth-child(1)").clear()
        filter_employee_ID_starts_with(driver,"a")
        driver.find_element(By.XPATH,"//h1[normalize-space()='DoesNotContain']").click()
        time.sleep(2)



# %%
def test_Filter_Employee_ID_EndsWith_Success(driver):
        driver.find_element(By.CSS_SELECTOR, "div:nth-child(3) div:nth-child(1) input:nth-child(1)").clear()
        filter_employee_ID_starts_with(driver,"a")
        driver.find_element(By.XPATH,"//h1[normalize-space()='EndsWith']").click()
        time.sleep(2)


# %%
def test_Filter_Employee_ID_EqualsTo_Success(driver):
        driver.find_element(By.CSS_SELECTOR, "div:nth-child(3) div:nth-child(1) input:nth-child(1)").clear()
        filter_employee_ID_starts_with(driver,"a")
        driver.find_element(By.XPATH,"//h1[normalize-space()='EqualTo']").click()
        time.sleep(2)


# %%
def test_Filter_Employee_ID_isNotNull_Success(driver):
        driver.find_element(By.CSS_SELECTOR, "div:nth-child(3) div:nth-child(1) input:nth-child(1)").clear()
        filter_employee_ID_starts_with(driver,"a")
        driver.find_element(By.XPATH,"//h1[normalize-space()='isNotNull']").click()
        time.sleep(2)


# %%
def test_Filter_Employee_ID_isNull_Success(driver):
        driver.find_element(By.CSS_SELECTOR, "div:nth-child(3) div:nth-child(1) input:nth-child(1)").clear()
        filter_employee_ID_starts_with(driver,"a")
        driver.find_element(By.XPATH,"//h1[normalize-space()='isNull']").click()
        time.sleep(2)


# %%
def test_Filter_Employee_ID_NoFilter_Success(driver):
        driver.find_element(By.CSS_SELECTOR, "div:nth-child(3) div:nth-child(1) input:nth-child(1)").clear()
        filter_employee_ID_starts_with(driver,"a")
        driver.find_element(By.XPATH,"//h1[normalize-space()='No Filter']").click()
        time.sleep(2)


# %%
def filter_employee_PhoneID_starts_with(driver, starts_with_letter):
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)").send_keys(starts_with_letter)
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        time.sleep(2)


# %%
def test_Filter_Employee_PhoneID_Contains_Success(driver):
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)").clear()
        filter_employee_PhoneID_starts_with(driver,"9")
        driver.find_element(By.XPATH,"//h1[normalize-space()='Contains']").click()
        time.sleep(2)


# %%
def test_Filter_Employee_PhoneID_DoesNotContains_Success(driver):
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)").clear()
        filter_employee_PhoneID_starts_with(driver,"9")
        driver.find_element(By.XPATH,"//h1[normalize-space()='DoesNotContain']").click()
        time.sleep(2)



# %%
def test_Filter_Employee_PhoneID_StartsWith_Success(driver):
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)").clear()
        filter_employee_PhoneID_starts_with(driver,"9")
        driver.find_element(By.XPATH,"//h1[normalize-space()='StartsWith']").click()
        time.sleep(2)


# %%
def test_Filter_Employee_PhoneID_EndsWith_Success(driver):
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)").clear()
        filter_employee_PhoneID_starts_with(driver,"9")
        driver.find_element(By.XPATH,"//h1[normalize-space()='EndsWith']").click()
        time.sleep(2)


# %%
def test_Filter_Employee_PhoneID_EqualsTo_Success(driver):
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)").clear()
        filter_employee_PhoneID_starts_with(driver,"9")
        driver.find_element(By.XPATH,"//h1[normalize-space()='EqualTo']").click()
        time.sleep(2)


# %%
def test_Filter_Employee_PhoneID_isNull_Success(driver):
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)").clear()
        filter_employee_PhoneID_starts_with(driver,"9")
        driver.find_element(By.XPATH,"//h1[normalize-space()='isNull']").click()
        time.sleep(2)

# %%
def test_Filter_Employee_PhoneID_isNotNull_Success(driver):
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)").clear()
        filter_employee_PhoneID_starts_with(driver,"9")
        driver.find_element(By.XPATH,"//h1[normalize-space()='isNotNull']").click()
        time.sleep(2)


# %%
def test_Filter_Employee_PhoneID_NoFilter_Success(driver):
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)").clear()
        filter_employee_PhoneID_starts_with(driver,"9")
        driver.find_element(By.XPATH,"//h1[normalize-space()='No Filter']").click()
        time.sleep(2)


# %%
def test_Filter_Employee_Name_ascending_Success(driver):
        driver.find_element(By.XPATH,"//body[1]/div[1]/div[1]/div[1]/div[2]/div[3]/div[1]/div[1]/div[2]/div[1]/p[1]/button[1]/span[1]").click()
        time.sleep(2)



# %%
def test_Filter_Employee_Name_descending_Success(driver):
        driver.find_element(By.XPATH,"//body[1]/div[1]/div[1]/div[1]/div[2]/div[3]/div[1]/div[1]/div[2]/div[1]/p[1]/button[1]/span[1]").click()
        time.sleep(2)


# %%
def test_Filter_Employee_ID_descending_Success(driver):
        driver.find_element(By.XPATH,"//body//div[@id='root']//div//div//div//div//div[3]//div[1]//p[1]//button[1]//span[1]").click()
        time.sleep(2)


# %%
def test_Filter_Employee_ID_ascending_Success(driver):
        driver.find_element(By.XPATH,"//body//div[@id='root']//div//div//div//div//div[3]//div[1]//p[1]//button[1]//span[1]").click()
        time.sleep(2)



# %%
def filter_employee_emailID_starts_with(driver, starts_with_letter):
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(5) > div:nth-child(1) > input:nth-child(1)").send_keys(starts_with_letter)
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(5) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        time.sleep(2)


# %%
def test_Filter_Employee_EmailID_StartsWith_Success(driver):
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(5) > div:nth-child(1) > input:nth-child(1)").clear()
        filter_employee_emailID_starts_with(driver, "customer@gmail.com")
        driver.find_element(By.XPATH,"//h1[normalize-space()='StartsWith']").click()
        time.sleep(2)



# %%
def test_Filter_Employee_EmailID_DoesNotContains_Success(driver):
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(5) > div:nth-child(1) > input:nth-child(1)").clear()
        filter_employee_emailID_starts_with(driver, "customer@gmail.com")
        driver.find_element(By.XPATH,"//h1[normalize-space()='DoesNotContain']").click()
        time.sleep(2)



# %%
def test_Filter_Employee_EmailID_Contains_Success(driver):
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(5) > div:nth-child(1) > input:nth-child(1)").clear()
        filter_employee_emailID_starts_with(driver, "customer@gmail.com")
        driver.find_element(By.XPATH,"//h1[normalize-space()='Contains']").click()
        time.sleep(2)


# %%
def test_Filter_Employee_EmailID_EndsWith_Success(driver):
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(5) > div:nth-child(1) > input:nth-child(1)").clear()
        filter_employee_emailID_starts_with(driver, "customer@gmail.com")
        driver.find_element(By.XPATH,"//h1[normalize-space()='EndsWith']").click()
        time.sleep(2)


# %%
def test_Filter_Employee_EmailID_EqualsTo_Success(driver):
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(5) > div:nth-child(1) > input:nth-child(1)").clear()
        filter_employee_emailID_starts_with(driver, "customer@gmail.com")
        driver.find_element(By.XPATH,"//h1[normalize-space()='EqualTo']").click()
        time.sleep(2)


# %%
def test_Filter_Employee_EmailID_isNull_Success(driver):
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(5) > div:nth-child(1) > input:nth-child(1)").clear()
        filter_employee_emailID_starts_with(driver, "customer@gmail.com")
        driver.find_element(By.XPATH,"//h1[normalize-space()='isNull']").click()
        time.sleep(2)


# %%
def test_Filter_Employee_EmailID_isNotNull_Success(driver):
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(5) > div:nth-child(1) > input:nth-child(1)").clear()
        filter_employee_emailID_starts_with(driver, "customer@gmail.com")
        driver.find_element(By.XPATH,"//h1[normalize-space()='isNotNull']").click()
        time.sleep(2)



# %%
def test_Filter_Employee_EmailID_NoFilter_Success(driver):
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(5) > div:nth-child(1) > input:nth-child(1)").clear()
        filter_employee_emailID_starts_with(driver, "customer@gmail.com")
        driver.find_element(By.XPATH,"//h1[normalize-space()='No Filter']").click()
        time.sleep(2)


# %%
def filter_employee_Roles_starts_with(driver, starts_with_letter):
        driver.find_element(By.CSS_SELECTOR, "div:nth-child(6) div:nth-child(1) input:nth-child(1)").send_keys(starts_with_letter)
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(6) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        time.sleep(2)


# %%
def test_Filter_Employee_Roles_StartsWith_Success(driver):
        filter_employee_Roles_starts_with(driver, "analyst")
        driver.find_element(By.XPATH,"//h1[normalize-space()='StartsWith']").click()
        time.sleep(2)


# %%
def test_Filter_Employee_Roles_EndsWith_Success(driver):
        filter_employee_Roles_starts_with(driver, "analyst")
        driver.find_element(By.XPATH,"//h1[normalize-space()='EndsWith']").click()
        time.sleep(2)


# %%
def test_Filter_Employee_Roles_EqualsTo_Success(driver):
        filter_employee_Roles_starts_with(driver, "analyst")
        driver.find_element(By.XPATH,"//h1[normalize-space()='EqualTo']").click()
        time.sleep(2)


# %%
def test_Filter_Employee_Roles_isNull_Success(driver):
        filter_employee_Roles_starts_with(driver, "analyst")
        driver.find_element(By.XPATH,"//h1[normalize-space()='isNull']").click()
        time.sleep(2)


# %%
def test_Filter_Employee_Roles_isNotNull_Success(driver):
        filter_employee_Roles_starts_with(driver, "analyst")
        driver.find_element(By.XPATH,"//h1[normalize-space()='isNotNull']").click()
        time.sleep(2)



# %%
def test_Filter_Employee_Roles_NoFilter_Success(driver):
        filter_employee_Roles_starts_with(driver, "analyst")
        driver.find_element(By.XPATH,"//h1[normalize-space()='No Filter']").click()
        time.sleep(2)


# %%
def test_Filter_Employee_Roles_Contains_Success(driver):
        filter_employee_Roles_starts_with(driver, "analyst")
        driver.find_element(By.XPATH,"//h1[normalize-space()='Contains']").click()
        time.sleep(2)


# %%
def test_Filter_Employee_Roles_DoesNotContains_Success(driver):
        filter_employee_Roles_starts_with(driver, "analyst")
        driver.find_element(By.XPATH,"//h1[normalize-space()='DoesNotContain']").click()
        time.sleep(2)



# %%
def filter_employee_Panno_starts_with(driver, starts_with_letter):
        driver.find_element(By.CSS_SELECTOR,"div:nth-child(7) div:nth-child(1) input:nth-child(1)").send_keys(starts_with_letter)
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(7) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        time.sleep(2)


# %%
def test_Filter_Employee_Panno_StartsWith_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"div:nth-child(7) div:nth-child(1) input:nth-child(1)").clear()
        filter_employee_Panno_starts_with(driver, "abcd")
        driver.find_element(By.XPATH,"//h1[normalize-space()='StartsWith']").click()
        time.sleep(2)


# %%
def test_Filter_Employee_Panno_EndsWith_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(7) > div:nth-child(1) > input:nth-child(1)").clear()
        filter_employee_Panno_starts_with(driver, "abcd")
        driver.find_element(By.XPATH,"//h1[normalize-space()='EndsWith']").click()
        time.sleep(2)


# %%
def test_Filter_Employee_Panno_EqualsTo_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(7) > div:nth-child(1) > input:nth-child(1)").clear()
        filter_employee_Panno_starts_with(driver, "abcd")
        driver.find_element(By.XPATH,"//h1[normalize-space()='EqualTo']").click()
        time.sleep(2)


# %%
def test_Filter_Employee_Panno_isNull_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(7) > div:nth-child(1) > input:nth-child(1)").clear()
        filter_employee_Panno_starts_with(driver, "abcd")
        driver.find_element(By.XPATH,"//h1[normalize-space()='isNull']").click()
        time.sleep(2)


# %%
def test_Filter_Employee_Panno_isNotNull_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(7) > div:nth-child(1) > input:nth-child(1)").clear()
        filter_employee_Panno_starts_with(driver, "abcd")
        driver.find_element(By.XPATH,"//h1[normalize-space()='isNotNull']").click()
        time.sleep(2)


# %%
def test_Filter_Employee_Panno_Contains_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(7) > div:nth-child(1) > input:nth-child(1)").clear()
        filter_employee_Panno_starts_with(driver, "abcd")
        driver.find_element(By.XPATH,"//h1[normalize-space()='Contains']").click()
        time.sleep(2)


# %%
def test_Filter_Employee_Panno_DoesNotContains_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(7) > div:nth-child(1) > input:nth-child(1)").clear()
        filter_employee_Panno_starts_with(driver, "abcd")
        driver.find_element(By.XPATH,"//h1[normalize-space()='DoesNotContain']").click()
        time.sleep(2)


# %%
def test_Filter_Employee_Panno_NoFilter_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(7) > div:nth-child(1) > input:nth-child(1)").clear()
        filter_employee_Panno_starts_with(driver, "abcd")
        driver.find_element(By.XPATH,"//h1[normalize-space()='No Filter']").click()
        time.sleep(2)

# %%
def filter_employee_doj_starts_with(driver, starts_with_letter):
        driver.find_element(By.CSS_SELECTOR,"input[value='false']").send_keys(starts_with_letter)
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(8) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        time.sleep(2)


# %%
def test_Filter_Employee_doj_EqualsTo_Success(driver):
        filter_employee_doj_starts_with(driver, "13-01-2024")
        driver.find_element(By.XPATH,"//h1[normalize-space()='EqualTo']").click()
        time.sleep(2)

# %%
def test_Filter_Employee_doj_NotEqualTo_Success(driver):
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(8) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='NotEqualTo']").click()
        time.sleep(2)

# %%
def test_Filter_Employee_doj_GreaterThan_Success(driver):
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(8) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='GreaterThan']").click()
        time.sleep(2)

# %%
def test_Filter_Employee_doj_LessThan_Success(driver):
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(8) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='LessThan']").click()
        time.sleep(2)

# %%
def test_Filter_Employee_doj_GreaterThanOrEqualTo_Success(driver):
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(8) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='GreaterThanOrEqualTo']").click()
        time.sleep(2)

# %%
def test_Filter_Employee_doj_LessThanOrEqualTo_Success(driver):
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(8) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='LessThanOrEqualTo']").click()
        time.sleep(2)

# %%
def test_Filter_Employee_doj_isNull_Success(driver):
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(8) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='isNull']").click()
        time.sleep(2)

# %%
def test_Filter_Employee_doj_isNotNull_Success(driver):
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(8) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='isNotNull']").click()
        time.sleep(2)

# %%
def test_Filter_Employee_doj_NoFilter_Success(driver):
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(8) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='No Filter']").click()
        time.sleep(2)

# %%
def filter_employee_low_starts_with(driver, starts_with_letter):
        driver.find_element(By.CSS_SELECTOR,"div:nth-child(9) div:nth-child(1) input:nth-child(1)").send_keys(starts_with_letter)
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(9) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        time.sleep(2)


# %%
def test_Filter_Employee_low_EqualsTo_Success(driver):
        filter_employee_low_starts_with(driver, "20-02-2020")
        driver.find_element(By.XPATH,"//h1[normalize-space()='EqualTo']").click()
        time.sleep(2)

# %%
def test_Filter_Employee_low_NotEqualTo_Success(driver):
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(9) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='NotEqualTo']").click()
        time.sleep(2)

# %%
def test_Filter_Employee_low_GreaterThan_Success(driver):
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(9) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='GreaterThan']").click()
        time.sleep(2)

# %%
def test_Filter_Employee_low_LessThan_Success(driver):
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(9) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='LessThan']").click()
        time.sleep(2)

# %%
def test_Filter_Employee_low_GreaterThanOrEqualTo_Success(driver):
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(9) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='GreaterThanOrEqualTo']").click()
        time.sleep(2)

# %%
def test_Filter_Employee_low_LessThanOrEqualTo_Success(driver):
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(9) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='LessThanOrEqualTo']").click()
        time.sleep(2)

# %%
def test_Filter_Employee_low_isNull_Success(driver):
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(9) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='isNull']").click()
        time.sleep(2)

# %%
def test_Filter_Employee_low_isNotNull_Success(driver):
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(9) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='isNotNull']").click()
        time.sleep(2)

# %%
def test_Filter_Employee_low_NoFilter_Success(driver):
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(9) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='No Filter']").click()
        time.sleep(2)

# %%
def filter_employee_status_starts_with(driver, starts_with_letter):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(10) > div:nth-child(1) > input:nth-child(1)").send_keys(starts_with_letter)
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(10) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        time.sleep(2)


# %%
def test_Filter_Employee_status_EqualsTo_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(10) > div:nth-child(1) > input:nth-child(1)").clear()
        filter_employee_status_starts_with(driver, "active")
        driver.find_element(By.XPATH,"//h1[normalize-space()='EqualTo']").click()
        time.sleep(2)

# %%
def test_Filter_Employee_status_NotEqualsTo_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(10) > div:nth-child(1) > input:nth-child(1)").clear()
        filter_employee_status_starts_with(driver, "active")
        driver.find_element(By.XPATH,"//h1[normalize-space()='NotEqualTo']").click()
        time.sleep(2)

# %%
def test_Filter_Employee_status_GreaterThan_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(10) > div:nth-child(1) > input:nth-child(1)").clear()
        filter_employee_status_starts_with(driver, "active")
        driver.find_element(By.XPATH,"//h1[normalize-space()='GreaterThan']").click()
        time.sleep(2)

# %%
def test_Filter_Employee_status_LessThan_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(10) > div:nth-child(1) > input:nth-child(1)").clear()
        filter_employee_status_starts_with(driver, "active")
        driver.find_element(By.XPATH,"//h1[normalize-space()='LessThan']").click()
        time.sleep(2)

# %%
def test_Filter_Employee_status_GreaterThanOrEqualTo_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(10) > div:nth-child(1) > input:nth-child(1)").clear()
        filter_employee_status_starts_with(driver, "active")
        driver.find_element(By.XPATH,"//h1[normalize-space()='GreaterThanOrEqualTo']").click()
        time.sleep(2)

# %%
def test_Filter_Employee_status_LessThanOrEqualTo_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(10) > div:nth-child(1) > input:nth-child(1)").clear()
        filter_employee_status_starts_with(driver, "active")
        driver.find_element(By.XPATH,"//h1[normalize-space()='LessThanOrEqualTo']").click()
        time.sleep(2)

# %%
def test_Filter_Employee_status_isNull_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(10) > div:nth-child(1) > input:nth-child(1)").clear()
        filter_employee_status_starts_with(driver, "active")
        driver.find_element(By.XPATH,"//h1[normalize-space()='isNull']").click()
        time.sleep(2)

# %%
def test_Filter_Employee_status_isNotNull_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(10) > div:nth-child(1) > input:nth-child(1)").clear()
        filter_employee_status_starts_with(driver, "active")
        driver.find_element(By.XPATH,"//h1[normalize-space()='isNotNull']").click()
        time.sleep(2)

# %%
def test_Filter_Employee_status_NoFilter_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(10) > div:nth-child(1) > input:nth-child(1)").clear()
        filter_employee_status_starts_with(driver, "active")
        driver.find_element(By.XPATH,"//h1[normalize-space()='No Filter']").click()
        time.sleep(2)

# %%
def filter_employee_employee_id_starts_with(driver, starts_with_letter):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)").send_keys(starts_with_letter)
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        time.sleep(2)


# %%
def test_Filter_Employee_employee_id_EqualsTo_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)").clear()
        filter_employee_employee_id_starts_with(driver, "43")
        driver.find_element(By.XPATH,"//h1[normalize-space()='EqualTo']").click()
        time.sleep(2)

# %%
def test_Filter_Employee_employee_id_NotEqualsTo_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)").clear()
        filter_employee_employee_id_starts_with(driver, "43")
        driver.find_element(By.XPATH,"//h1[normalize-space()='NotEqualTo']").click()
        time.sleep(2)

# %%
def test_Filter_Employee_employee_id_LessThan_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)").clear()
        filter_employee_employee_id_starts_with(driver, "43")
        driver.find_element(By.XPATH,"//h1[normalize-space()='LessThan']").click()
        time.sleep(2)

# %%
def test_Filter_Employee_employee_id_GreaterThan_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)").clear()
        filter_employee_employee_id_starts_with(driver, "43")
        driver.find_element(By.XPATH,"//h1[normalize-space()='GreaterThan']").click()
        time.sleep(2)

# %%
def test_Filter_Employee_employee_id_GreaterThanOrEqualTo_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)").clear()
        filter_employee_employee_id_starts_with(driver, "43")
        driver.find_element(By.XPATH,"//h1[normalize-space()='GreaterThanOrEqualTo']").click()
        time.sleep(2)

# %%
def test_Filter_Employee_employee_id_LessThanOrEqualTo_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)").clear()
        filter_employee_employee_id_starts_with(driver, "43")
        driver.find_element(By.XPATH,"//h1[normalize-space()='LessThanOrEqualTo']").click()
        time.sleep(2)

# %%
def test_Filter_Employee_employee_id_isNull_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)").clear()
        filter_employee_employee_id_starts_with(driver, "43")
        driver.find_element(By.XPATH,"//h1[normalize-space()='isNull']").click()
        time.sleep(2)

# %%
def test_Filter_Employee_employee_id_isNotNull_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)").clear()
        filter_employee_employee_id_starts_with(driver, "43")
        driver.find_element(By.XPATH,"//h1[normalize-space()='isNotNull']").click()
        time.sleep(2)

# %%
def test_Filter_Employee_employee_id_NoFilter_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)").clear()
        filter_employee_employee_id_starts_with(driver, "43")
        driver.find_element(By.XPATH,"//h1[normalize-space()='No Filter']").click()
        time.sleep(2)

# %%
def test_Filter_Employee_Pagination15_NoFilter_Success(driver):
    a=driver.find_element(By.XPATH,"//div[@id='root']//div//div//div//div//div//select")
    drp1=Select(a)
    drp1.select_by_visible_text('15')
    driver.find_element(By.XPATH,"//button[@aria-label='Go to page 2']").click()
    time.sleep(2)

# %%
def test_Filter_Employee_Pagination25_NoFilter_Success(driver):
    a=driver.find_element(By.XPATH,"//div[@id='root']//div//div//div//div//div//select")
    drp1=Select(a)
    drp1.select_by_visible_text('25')
    driver.find_element(By.XPATH,"//button[@aria-label='Go to page 2']").click()
    time.sleep(2)

# %%
def test_Filter_Employee_Pagination50_NoFilter_Success(driver):
    a=driver.find_element(By.XPATH,"//div[@id='root']//div//div//div//div//div//select")
    drp1=Select(a)
    drp1.select_by_visible_text('50')
    driver.find_element(By.XPATH,"//button[@aria-label='Go to page 2']").click()
    time.sleep(2)

# %%
def test_Filter_Employee_phone_ascending_Success(driver):
        driver.find_element(By.XPATH,"//body[1]/div[1]/div[1]/div[1]/div[2]/div[3]/div[1]/div[1]/div[4]/div[1]/p[1]/button[1]/span[1]").click()
        time.sleep(2)


# %%
def test_Filter_Employee_phone_descending_Success(driver):
        driver.find_element(By.XPATH,"//body[1]/div[1]/div[1]/div[1]/div[2]/div[3]/div[1]/div[1]/div[4]/div[1]/p[1]/button[1]/span[1]").click()
        driver.find_element(By.XPATH,"//body[1]/div[1]/div[1]/div[1]/div[2]/div[3]/div[1]/div[1]/div[4]/div[1]/p[1]/button[1]/span[1]").click()
        time.sleep(4)


# %%
def test_Filter_Employee_email_ascending_Success(driver):
        driver.find_element(By.XPATH,"//body[1]/div[1]/div[1]/div[1]/div[2]/div[3]/div[1]/div[1]/div[5]/div[1]/p[1]/button[1]/span[1]").click()
        time.sleep(2)


# %%
def test_Filter_Employee_email_descending_Success(driver):
        driver.find_element(By.XPATH,"//body[1]/div[1]/div[1]/div[1]/div[2]/div[3]/div[1]/div[1]/div[5]/div[1]/p[1]/button[1]/span[1]").click()
        driver.find_element(By.XPATH,"//body[1]/div[1]/div[1]/div[1]/div[2]/div[3]/div[1]/div[1]/div[5]/div[1]/p[1]/button[1]/span[1]").click()
        time.sleep(2)


# %%
def test_Filter_Employee_role_ascending_Success(driver):
        driver.find_element(By.XPATH,"//body[1]/div[1]/div[1]/div[1]/div[2]/div[3]/div[1]/div[1]/div[6]/div[1]/p[1]/button[1]/span[1]").click()
        time.sleep(2)


# %%
def test_Filter_Employee_role_descending_Success(driver):
        driver.find_element(By.XPATH,"//body[1]/div[1]/div[1]/div[1]/div[2]/div[3]/div[1]/div[1]/div[6]/div[1]/p[1]/button[1]/span[1]").click()
        driver.find_element(By.XPATH,"//body[1]/div[1]/div[1]/div[1]/div[2]/div[3]/div[1]/div[1]/div[6]/div[1]/p[1]/button[1]/span[1]").click()
        time.sleep(4)


# %%
def test_Filter_Employee_panno_ascending_Success(driver):
        driver.find_element(By.XPATH,"//body[1]/div[1]/div[1]/div[1]/div[2]/div[3]/div[1]/div[1]/div[7]/div[1]/p[1]/button[1]/span[1]").click()
        time.sleep(2)


# %%
def test_Filter_Employee_panno_descending_Success(driver):
        driver.find_element(By.XPATH,"//body[1]/div[1]/div[1]/div[1]/div[2]/div[3]/div[1]/div[1]/div[7]/div[1]/p[1]/button[1]/span[1]").click()
        driver.find_element(By.XPATH,"//body[1]/div[1]/div[1]/div[1]/div[2]/div[3]/div[1]/div[1]/div[7]/div[1]/p[1]/button[1]/span[1]").click()
        time.sleep(2)


# %%
def test_Filter_Employee_doj_ascending_Success(driver):
        driver.find_element(By.XPATH,"//body[1]/div[1]/div[1]/div[1]/div[2]/div[3]/div[1]/div[1]/div[8]/div[1]/p[1]/button[1]/span[1]").click()
        time.sleep(2)


# %%
def test_Filter_Employee_doj_descending_Success(driver):
        driver.find_element(By.XPATH,"//body[1]/div[1]/div[1]/div[1]/div[2]/div[3]/div[1]/div[1]/div[8]/div[1]/p[1]/button[1]/span[1]").click()
        driver.find_element(By.XPATH,"//body[1]/div[1]/div[1]/div[1]/div[2]/div[3]/div[1]/div[1]/div[8]/div[1]/p[1]/button[1]/span[1]").click()
        time.sleep(2)


# %%
def test_Filter_Employee_low_ascending_Success(driver):
        driver.find_element(By.XPATH,"//body[1]/div[1]/div[1]/div[1]/div[2]/div[3]/div[1]/div[1]/div[9]/div[1]/p[1]/button[1]/span[1]").click()
        time.sleep(2)


# %%
def test_Filter_Employee_low_descending_Success(driver):
        driver.find_element(By.XPATH,"//body[1]/div[1]/div[1]/div[1]/div[2]/div[3]/div[1]/div[1]/div[9]/div[1]/p[1]/button[1]/span[1]").click()
        driver.find_element(By.XPATH,"//body[1]/div[1]/div[1]/div[1]/div[2]/div[3]/div[1]/div[1]/div[9]/div[1]/p[1]/button[1]/span[1]").click()
        time.sleep(2)

# %%
def test_Filter_Employee_status_ascending_Success(driver):
        driver.find_element(By.XPATH,"//body[1]/div[1]/div[1]/div[1]/div[2]/div[3]/div[1]/div[1]/div[10]/div[1]/p[1]/button[1]/span[1]").click()
        time.sleep(2)


# %%
def test_Filter_Employee_status_descending_Success(driver):
        driver.find_element(By.XPATH,"//body[1]/div[1]/div[1]/div[1]/div[2]/div[3]/div[1]/div[1]/div[10]/div[1]/p[1]/button[1]/span[1]").click()
        driver.find_element(By.XPATH,"//body[1]/div[1]/div[1]/div[1]/div[2]/div[3]/div[1]/div[1]/div[10]/div[1]/p[1]/button[1]/span[1]").click()
        time.sleep(2)

# %%
def test_Filter_Employee_employeeid_ascending_Success(driver):
        driver.find_element(By.XPATH,"//body[1]/div[1]/div[1]/div[1]/div[2]/div[3]/div[1]/div[2]/div[1]/div[1]/p[1]/button[1]/span[1]").click()
        time.sleep(2)


# %%
def test_Filter_Employee_employeeid_descending_Success(driver):
        driver.find_element(By.XPATH,"//body[1]/div[1]/div[1]/div[1]/div[2]/div[3]/div[1]/div[2]/div[1]/div[1]/p[1]/button[1]/span[1]").click()
        driver.find_element(By.XPATH,"//body[1]/div[1]/div[1]/div[1]/div[2]/div[3]/div[1]/div[2]/div[1]/div[1]/p[1]/button[1]/span[1]").click()
        time.sleep(2)


# %%
def test_Filter_Employee_Refresh_Success(driver):
        driver.find_element(By.XPATH,"//p[normalize-space()='Refresh']").click()
        time.sleep(2)


# %%
def test_employee_return_arrow(driver):
        return_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//img[contains(@src,'/src/assets/back.png')]"))
        )
        assert not return_button.get_attribute("disabled"), "Return button should be enabled"
        return_button.click()

        dashboard_header = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h1[normalize-space()='Dashboard']"))
        )
        assert dashboard_header.text == "Dashboard", "Dashboard header text is incorrect"


# %%
def Employee_Webpage():
    try:
        driver = login_and_navigate_employee("ruderaw", "abcdefg", "9632")
        test_Filter_Employee_Name_ascending_Success(driver)
        test_Filter_Employee_Name_descending_Success(driver)
        test_Filter_Employee_ID_ascending_Success(driver)
        test_Filter_Employee_ID_descending_Success(driver)
        test_Filter_Employee_phone_ascending_Success(driver)
        test_Filter_Employee_phone_descending_Success(driver)
        test_Filter_Employee_email_ascending_Success(driver)
        test_Filter_Employee_email_descending_Success(driver)
        test_Filter_Employee_role_ascending_Success(driver)
        test_Filter_Employee_role_descending_Success(driver)
        test_Filter_Employee_panno_ascending_Success(driver)
        test_Filter_Employee_panno_descending_Success(driver)
        test_Filter_Employee_low_ascending_Success(driver)
        test_Filter_Employee_low_descending_Success(driver)
        test_Filter_Employee_employeeid_ascending_Success(driver)
        test_Filter_Employee_employeeid_descending_Success(driver)
        test_Filter_Employee_Name_StartsWith_Success(driver)
        test_Filter_Employee_Name_EndsWith_Success(driver)
        test_Filter_Employee_Name_EqualTo_Success(driver)
        test_Filter_Employee_Name_isNull_Success(driver)
        test_Filter_Employee_Name_isNotNull_Success(driver)
        test_Filter_Employee_Name_Contains_Success(driver)
        test_Filter_Employee_Name_DoesNotContains_Success(driver)
        test_Filter_Employee_Name_NoFilter_Success(driver)
        test_Filter_Employee_ID_StartsWith_Success(driver)
        test_Filter_Employee_ID_EndsWith_Success(driver)
        test_Filter_Employee_ID_EqualsTo_Success(driver)
        test_Filter_Employee_ID_isNull_Success(driver)
        test_Filter_Employee_ID_isNotNull_Success(driver)
        test_Filter_Employee_ID_Contains_Success(driver)
        test_Filter_Employee_ID_DoesNotContains_Success(driver)
        test_Filter_Employee_ID_NoFilter_Success(driver)
        test_Filter_Employee_PhoneID_Contains_Success(driver)
        test_Filter_Employee_PhoneID_DoesNotContains_Success(driver)
        test_Filter_Employee_PhoneID_StartsWith_Success(driver)
        test_Filter_Employee_PhoneID_EndsWith_Success(driver)
        test_Filter_Employee_PhoneID_EqualsTo_Success(driver)
        test_Filter_Employee_PhoneID_isNull_Success(driver)
        test_Filter_Employee_PhoneID_isNotNull_Success(driver)
        test_Filter_Employee_PhoneID_NoFilter_Success(driver)
        test_Filter_Employee_EmailID_StartsWith_Success(driver)
        test_Filter_Employee_EmailID_EndsWith_Success(driver)
        test_Filter_Employee_EmailID_EqualsTo_Success(driver)
        test_Filter_Employee_EmailID_isNull_Success(driver)
        test_Filter_Employee_EmailID_isNotNull_Success(driver)
        test_Filter_Employee_EmailID_Contains_Success(driver)
        test_Filter_Employee_EmailID_DoesNotContains_Success(driver)
        test_Filter_Employee_EmailID_NoFilter_Success(driver)
        test_Filter_Employee_Roles_StartsWith_Success(driver)
        test_Filter_Employee_Roles_EndsWith_Success(driver)
        test_Filter_Employee_Roles_EqualsTo_Success(driver)
        test_Filter_Employee_Roles_isNull_Success(driver)
        test_Filter_Employee_Roles_isNotNull_Success(driver)
        test_Filter_Employee_Roles_Contains_Success(driver)
        test_Filter_Employee_Roles_DoesNotContains_Success(driver)
        test_Filter_Employee_Roles_NoFilter_Success(driver)
        test_Filter_Employee_Panno_StartsWith_Success(driver)
        test_Filter_Employee_Panno_EndsWith_Success(driver)
        test_Filter_Employee_Panno_EqualsTo_Success(driver)
        test_Filter_Employee_Panno_isNull_Success(driver)
        test_Filter_Employee_Panno_isNotNull_Success(driver)
        test_Filter_Employee_Panno_Contains_Success(driver)
        test_Filter_Employee_Panno_DoesNotContains_Success(driver)
        test_Filter_Employee_Panno_NoFilter_Success(driver)
        test_Filter_Employee_doj_EqualsTo_Success(driver)
        test_Filter_Employee_doj_NotEqualTo_Success(driver)
        test_Filter_Employee_doj_GreaterThan_Success(driver)
        test_Filter_Employee_doj_LessThan_Success(driver)
        test_Filter_Employee_doj_GreaterThanOrEqualTo_Success(driver)
        test_Filter_Employee_doj_LessThanOrEqualTo_Success(driver)
        test_Filter_Employee_doj_isNotNull_Success(driver)
        test_Filter_Employee_doj_isNull_Success(driver)
        test_Filter_Employee_doj_NoFilter_Success(driver)
        test_Filter_Employee_low_EqualsTo_Success(driver)
        test_Filter_Employee_low_NotEqualTo_Success(driver)
        test_Filter_Employee_low_GreaterThan_Success(driver)
        test_Filter_Employee_low_LessThan_Success(driver)
        test_Filter_Employee_low_GreaterThanOrEqualTo_Success(driver)
        test_Filter_Employee_low_LessThanOrEqualTo_Success(driver)
        test_Filter_Employee_low_isNotNull_Success(driver)
        test_Filter_Employee_low_isNull_Success(driver)
        test_Filter_Employee_low_NoFilter_Success(driver)
        test_Filter_Employee_status_EqualsTo_Success(driver)
        test_Filter_Employee_status_NotEqualsTo_Success(driver)
        test_Filter_Employee_status_GreaterThan_Success(driver)
        test_Filter_Employee_status_LessThan_Success(driver)
        test_Filter_Employee_status_GreaterThanOrEqualTo_Success(driver)
        test_Filter_Employee_status_LessThanOrEqualTo_Success(driver)
        test_Filter_Employee_status_isNotNull_Success(driver)
        test_Filter_Employee_status_isNull_Success(driver)
        test_Filter_Employee_status_NoFilter_Success(driver)
        test_Filter_Employee_employee_id_EqualsTo_Success(driver)
        test_Filter_Employee_employee_id_NotEqualsTo_Success(driver)
        test_Filter_Employee_employee_id_GreaterThan_Success(driver)
        test_Filter_Employee_employee_id_LessThan_Success(driver)
        test_Filter_Employee_employee_id_GreaterThanOrEqualTo_Success(driver)
        test_Filter_Employee_employee_id_LessThanOrEqualTo_Success(driver)
        test_Filter_Employee_employee_id_isNotNull_Success(driver)
        test_Filter_Employee_employee_id_isNull_Success(driver)
        test_Filter_Employee_employee_id_NoFilter_Success(driver)
        test_Filter_Employee_Pagination15_NoFilter_Success(driver)
        test_Filter_Employee_Pagination25_NoFilter_Success(driver)
        test_Filter_Employee_Pagination50_NoFilter_Success(driver)
        add_new_employee(driver, "aryan ashish", "ijklmn", "Admin User", "06-05-2024", "intern", "ashish.com", "06-05-2003", "31-05-2024", "Admin", "11100000", "UAE", "UAE", "Dubai", "q", "Z-CASH")
        test_Edit_Employee_Success(driver)
        test_Filter_Employee_Refresh_Success(driver)
        test_employee_return_arrow(driver)
        
        time.sleep(2)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

Employee_Webpage()


# %%
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

# %%
def filter_city_country_starts_with(driver, starts_with_letter):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").send_keys(starts_with_letter)
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        time.sleep(2)


# %%
def filter_city_country_Contains_Success(driver):
    driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
    filter_city_country_starts_with(driver, "india")
    driver.find_element(By.XPATH,"//button[2]//div[1]//h1[1]").click()
    time.sleep(2)

    

# %%
def filter_city_country_DoesNotContains_Success(driver):
    driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
    filter_city_country_starts_with(driver, "india")
    driver.find_element(By.XPATH,"//h1[normalize-space()='DoesNotContain']").click()
    time.sleep(2)

    

# %%
def filter_city_country_StartsWith_Success(driver):
    driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
    filter_city_country_starts_with(driver, "india")
    driver.find_element(By.XPATH,"//h1[normalize-space()='StartsWith']").click()
    time.sleep(2)

    

# %%
def filter_city_country_EndsWith_Success(driver):
    driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
    filter_city_country_starts_with(driver, "india")
    driver.find_element(By.XPATH,"//h1[normalize-space()='EndsWith']").click()
    time.sleep(2)

    

# %%
def filter_city_country_EqualTo_Success(driver):
    driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
    filter_city_country_starts_with(driver, "india")
    driver.find_element(By.XPATH,"//h1[normalize-space()='EqualTo']").click()
    time.sleep(2)

    

# %%
def filter_city_country_isNull_Success(driver):
    driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
    filter_city_country_starts_with(driver, "india")
    driver.find_element(By.XPATH,"//h1[normalize-space()='isNull']").click()
    time.sleep(2)

    

# %%
def filter_city_country_isNotNull_Success(driver):
    driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
    filter_city_country_starts_with(driver, "india")
    driver.find_element(By.XPATH,"//h1[normalize-space()='isNotNull']").click()
    time.sleep(2)

    

# %%
def filter_city_country_NoFilter_Success(driver):
    driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
    filter_city_country_starts_with(driver, "india")
    driver.find_element(By.XPATH,"//h1[normalize-space()='No Filter']").click()
    time.sleep(2)

    

# %%
def filter_city_state_starts_with(driver, starts_with_letter):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > input:nth-child(1)").send_keys(starts_with_letter)
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        time.sleep(2)


# %%
def filter_city_state_Contains_Success(driver):
    driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > input:nth-child(1)").clear()
    filter_city_state_starts_with(driver, "Uttar Pradesh")
    driver.find_element(By.XPATH,"//h1[normalize-space()='Contains']").click()
    time.sleep(2)

    

# %%
def filter_city_state_DoesNotContains_Success(driver):
    driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > input:nth-child(1)").clear()
    filter_city_state_starts_with(driver, "Uttar Pradesh")
    driver.find_element(By.XPATH,"//h1[normalize-space()='DoesNotContain']").click()
    time.sleep(2)

    

# %%
def filter_city_state_StartsWith_Success(driver):
    driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > input:nth-child(1)").clear()
    filter_city_state_starts_with(driver, "Uttar Pradesh")
    driver.find_element(By.XPATH,"//h1[normalize-space()='StartsWith']").click()
    time.sleep(2)

    

# %%
def filter_city_state_EndsWith_Success(driver):
    driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > input:nth-child(1)").clear()
    filter_city_state_starts_with(driver, "Uttar Pradesh")
    driver.find_element(By.XPATH,"//h1[normalize-space()='EndsWith']").click()
    time.sleep(2)

    

# %%
def filter_city_state_EqualsTo_Success(driver):
    driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > input:nth-child(1)").clear()
    filter_city_state_starts_with(driver, "Uttar Pradesh")
    driver.find_element(By.XPATH,"//h1[normalize-space()='EqualTo']").click()
    time.sleep(2)

    

# %%
def filter_city_state_isNull_Success(driver):
    driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > input:nth-child(1)").clear()
    filter_city_state_starts_with(driver, "Uttar Pradesh")
    driver.find_element(By.XPATH,"//h1[normalize-space()='isNull']").click()
    time.sleep(2)

    

# %%
def filter_city_state_isNotNull_Success(driver):
    driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > input:nth-child(1)").clear()
    filter_city_state_starts_with(driver, "Uttar Pradesh")
    driver.find_element(By.XPATH,"//h1[normalize-space()='isNotNull']").click()
    time.sleep(2)

    

# %%
def filter_city_state_NoFilter_Success(driver):
    driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > input:nth-child(1)").clear()
    filter_city_state_starts_with(driver, "Uttar Pradesh")
    driver.find_element(By.XPATH,"//h1[normalize-space()='No Filter']").click()
    time.sleep(2)

    

# %%
def filter_city_City_starts_with(driver, starts_with_letter):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)").send_keys(starts_with_letter)
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        time.sleep(2)


# %%
def filter_city_City_Contains_Success(driver):
    driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)").clear()
    filter_city_City_starts_with(driver, "Pune")
    driver.find_element(By.XPATH,"//h1[normalize-space()='Contains']").click()
    time.sleep(2)

    

# %%
def filter_city_City_DoesNotContains_Success(driver):
    driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)").clear()
    filter_city_City_starts_with(driver, "Pune")
    driver.find_element(By.XPATH,"//h1[normalize-space()='DoesNotContain']").click()
    time.sleep(2)

    

# %%
def filter_city_City_StartsWith_Success(driver):
    driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)").clear()
    filter_city_City_starts_with(driver, "Pune")
    driver.find_element(By.XPATH,"//h1[normalize-space()='StartsWith']").click()
    time.sleep(2)

    

# %%
def filter_city_City_EndssWith_Success(driver):
    driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)").clear()
    filter_city_City_starts_with(driver, "Pune")
    driver.find_element(By.XPATH,"//h1[normalize-space()='EndsWith']").click()
    time.sleep(2)

    

# %%
def filter_city_City_EqualsTo_Success(driver):
    driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)").clear()
    filter_city_City_starts_with(driver, "Pune")
    driver.find_element(By.XPATH,"//h1[normalize-space()='EqualTo']").click()
    time.sleep(2)

    

# %%
def filter_city_City_isNull_Success(driver):
    driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)").clear()
    filter_city_City_starts_with(driver, "Pune")
    driver.find_element(By.XPATH,"//h1[normalize-space()='isNull']").click()
    time.sleep(2)

    

# %%
def filter_city_City_isNotNull_Success(driver):
    driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)").clear()
    filter_city_City_starts_with(driver, "Pune")
    driver.find_element(By.XPATH,"//h1[normalize-space()='isNotNull']").click()
    time.sleep(2)

    

# %%
def filter_city_City_NoFilter_Success(driver):
    driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)").clear()
    filter_city_City_starts_with(driver, "Pune")
    driver.find_element(By.XPATH,"//h1[normalize-space()='No Filter']").click()
    time.sleep(2)

    

# %%
def filter_city_ID_starts_with(driver, starts_with_letter):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)").send_keys(starts_with_letter)
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        time.sleep(2)


# %%
def filter_city_ID_EqualsTo_Success(driver):
    driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)").clear()
    filter_city_ID_starts_with(driver, "1808")
    driver.find_element(By.XPATH,"//h1[normalize-space()='EqualTo']").click()
    time.sleep(2)

    

# %%
def filter_city_ID_NotEqualsTo_Success(driver):
    driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)").clear()
    filter_city_ID_starts_with(driver, "1808")
    driver.find_element(By.XPATH,"//h1[normalize-space()='NotEqualTo']").click()
    time.sleep(2)

    

# %%
def filter_city_ID_GreaterThan_Success(driver):
    driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)").clear()
    filter_city_ID_starts_with(driver, "1808")
    driver.find_element(By.XPATH,"//h1[normalize-space()='GreaterThan']").click()
    time.sleep(2)

    

# %%
def filter_city_ID_LessThan_Success(driver):
    driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)").clear()
    filter_city_ID_starts_with(driver, "1808")
    driver.find_element(By.XPATH,"//h1[normalize-space()='LessThan']").click()
    time.sleep(2)

    

# %%
def filter_city_ID_GreaterThanOrEqual_Success(driver):
    driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)").clear()
    filter_city_ID_starts_with(driver, "1808")
    driver.find_element(By.XPATH,"//h1[normalize-space()='GreaterThanOrEqualTo']").click()
    time.sleep(2)

    

# %%
def filter_city_ID_LessThanOrEqual_Success(driver):
    driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)").clear()
    filter_city_ID_starts_with(driver, "1808")
    driver.find_element(By.XPATH,"//h1[normalize-space()='LessThanOrEqualTo']").click()
    time.sleep(2)

    

# %%
def filter_city_ID_isNull_Success(driver):
    driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)").clear()
    filter_city_ID_starts_with(driver, "1808")
    driver.find_element(By.XPATH,"//h1[normalize-space()='isNull']").click()
    time.sleep(2)

    

# %%
def filter_city_ID_isNotNull_Success(driver):
    driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)").clear()
    filter_city_ID_starts_with(driver, "1808")
    driver.find_element(By.XPATH,"//h1[normalize-space()='isNotNull']").click()
    time.sleep(2)

    

# %%
def filter_city_ID_NoFilter_Success(driver):
    driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)").clear()
    filter_city_ID_starts_with(driver, "1808")
    driver.find_element(By.XPATH,"//h1[normalize-space()='No Filter']").click()
    time.sleep(2)

    

# %%
def test_Filter_City_Pagination15_Success(driver):
    a=driver.find_element(By.XPATH,"//select[contains(@name,'currentPages')]")
    drp1=Select(a)
    drp1.select_by_visible_text('15')
    time.sleep(2)
    driver.find_element(By.XPATH,"//button[@aria-label='Go to page 2']").click()
    time.sleep(2)

# %%
def test_Filter_City_Pagination25_Success(driver):
    a=driver.find_element(By.XPATH,"//select[contains(@name,'currentPages')]")
    drp1=Select(a)
    drp1.select_by_visible_text('25')
    time.sleep(2)
    driver.find_element(By.XPATH,"//button[@aria-label='Go to page 2']").click()
    time.sleep(2)

# %%
def test_Filter_City_Pagination50_Success(driver):
    a=driver.find_element(By.XPATH,"//select[contains(@name,'currentPages')]")
    drp1=Select(a)
    drp1.select_by_visible_text('50')
    time.sleep(2)
    driver.find_element(By.XPATH,"//button[@aria-label='Go to page 2']").click()
    time.sleep(2)

# %%
def add_City(driver):
    driver.find_element(By.XPATH,"//body//div//div//div//div//div//div//div//button//div").click()
    time.sleep(2)
    a=driver.find_element(By.XPATH,"//select[@name='country']")
    drp1=Select(a)
    drp1.select_by_visible_text('India')
    driver.find_element(By.XPATH,"//input[@name='state']").send_keys("State01")
    driver.find_element(By.XPATH,"//input[@name='cityName']").send_keys("City01")
    time.sleep(2)
    driver.find_element(By.XPATH,"//body/div[contains(@role,'presentation')]/div/div/div/button[1]").click()
    time.sleep(2)
    driver.find_element(By.XPATH,"//body/div[contains(@role,'presentation')]/div/div/button[1]").click()
    time.sleep(4)
    driver.find_element(By.XPATH,"//input[@type='text']").send_keys("India")
    driver.find_element(By.XPATH,"//img[@alt='search-icon']").click()
    time.sleep(2)
    driver.find_element(By.XPATH,"//div//div//div//div[1]//div[2]//div[2]//button[2]//img[1]").click()
    time.sleep(2)
    driver.find_element(By.XPATH,"//button[normalize-space()='Delete']").click()
    time.sleep(2)

# %%
def edit_City(driver):
    driver.find_element(By.XPATH,"//body//div//div//div//div//div//div//div//button//div").click()
    time.sleep(2)
    a=driver.find_element(By.XPATH,"//select[@name='country']")
    drp1=Select(a)
    drp1.select_by_visible_text('India')
    driver.find_element(By.XPATH,"//input[@name='state']").send_keys("State01")
    driver.find_element(By.XPATH,"//input[@name='cityName']").send_keys("City01")
    time.sleep(2)
    driver.find_element(By.XPATH,"//body/div[contains(@role,'presentation')]/div/div/div/button[1]").click()
    time.sleep(2)
    driver.find_element(By.XPATH,"//body/div[contains(@role,'presentation')]/div/div/button[1]").click()
    time.sleep(4)
    driver.find_element(By.XPATH,"//input[@type='text']").clear()
    driver.find_element(By.XPATH,"//input[@type='text']").send_keys("India")
    driver.find_element(By.XPATH,"//img[@alt='search-icon']").click()
    time.sleep(3)
    driver.find_element(By.XPATH,"//img[@alt='edit']").click()
    time.sleep(2)
    driver.find_element(By.XPATH,"//input[@name='cityName']").clear()
    time.sleep(2)
    driver.find_element(By.XPATH,"//input[@name='cityName']").send_keys("City100")
    driver.find_element(By.XPATH,"//button[@type='submit']").click()
    time.sleep(4)
    driver.find_element(By.XPATH,"//input[@type='text']").clear()
    driver.find_element(By.XPATH,"//input[@type='text']").send_keys("City100")
    driver.find_element(By.XPATH,"//img[@alt='search-icon']").click()
    time.sleep(2)
    driver.find_element(By.XPATH,"//div//div//div//div[1]//div[2]//div[2]//button[2]//img[1]").click()
    time.sleep(2)
    driver.find_element(By.XPATH,"//button[normalize-space()='Delete']").click()
    time.sleep(2)

# %%
def City_Refresh(driver):
    driver.find_element(By.XPATH,"//p[normalize-space()='Refresh']").click()
    time.sleep(2)

# %%
def City_DownloadasExcel(driver):
    driver.find_element(By.XPATH,"//p[normalize-space()='Download']").click()
    driver.find_element(By.XPATH,"//p[normalize-space()='Download as Excel']").click()
    time.sleep(2)

# %%
def City_Country_ascending(driver):
    driver.find_element(By.XPATH,"//body/div/div/div/div/div/div/div/div[2]/p[1]/button[1]/span[1]").click()
    time.sleep(2)

# %%
def City_Country_descending(driver):
    driver.find_element(By.XPATH,"//body/div/div/div/div/div/div/div/div[2]/p[1]/button[1]/span[1]").click()
    time.sleep(2)

# %%
def City_State_descending(driver):
    driver.find_element(By.XPATH,"//div//div//div//div//div//div[3]//p[1]//button[1]//span[1]").click()
    time.sleep(2)

# %%
def City_State_ascending(driver):
    driver.find_element(By.XPATH,"//div//div//div//div//div//div[3]//p[1]//button[1]//span[1]").click()
    time.sleep(2)

# %%
def City_Cityname_ascending(driver):
    driver.find_element(By.XPATH,"//div[4]//p[1]//button[1]//span[1]").click()
    time.sleep(2)

# %%
def City_Cityname_descending(driver):
    driver.find_element(By.XPATH,"//div[4]//p[1]//button[1]//span[1]").click()
    time.sleep(2)

# %%
def City_ID_descending(driver):
    driver.find_element(By.XPATH,"//body/div/div/div/div/div/div/div/div[1]/p[1]/button[1]/span[1]").click()
    time.sleep(2)

# %%
def City_ID_ascending(driver):
    driver.find_element(By.XPATH,"//body/div/div/div/div/div/div/div/div[1]/p[1]/button[1]/span[1]").click()
    time.sleep(2)

# %%
def City_webpage():
    try:
       driver=login_and_navigate_city("ruderaw", "abcdefg", "9632")
       City_Country_ascending(driver)
       City_Country_descending(driver)
       City_State_ascending(driver)
       City_State_descending(driver)
       City_Cityname_ascending(driver)
       City_Cityname_descending(driver)
       City_ID_ascending(driver)
       City_ID_descending(driver)
       filter_city_country_Contains_Success(driver)
       filter_city_country_DoesNotContains_Success(driver)
       filter_city_country_StartsWith_Success(driver)
       filter_city_country_EndsWith_Success(driver)
       filter_city_country_EqualTo_Success(driver)
       filter_city_country_isNull_Success(driver)
       filter_city_country_isNotNull_Success(driver)
       filter_city_country_NoFilter_Success(driver)
       filter_city_state_Contains_Success(driver)
       filter_city_state_DoesNotContains_Success(driver)
       filter_city_state_StartsWith_Success(driver)
       filter_city_state_EndsWith_Success(driver)
       filter_city_state_EqualsTo_Success(driver)
       filter_city_state_isNull_Success(driver)
       filter_city_state_isNotNull_Success(driver)
       filter_city_state_NoFilter_Success(driver)
       filter_city_City_Contains_Success(driver)
       filter_city_City_DoesNotContains_Success(driver)
       filter_city_City_StartsWith_Success(driver)
       filter_city_City_EndssWith_Success(driver)
       filter_city_City_EqualsTo_Success(driver)
       filter_city_City_isNull_Success(driver)
       filter_city_City_isNotNull_Success(driver)
       filter_city_City_NoFilter_Success(driver)
       filter_city_ID_EqualsTo_Success(driver)
       filter_city_ID_NotEqualsTo_Success(driver)
       filter_city_ID_GreaterThan_Success(driver)
       filter_city_ID_LessThan_Success(driver)
       filter_city_ID_GreaterThanOrEqual_Success(driver)
       filter_city_ID_LessThanOrEqual_Success(driver)
       filter_city_ID_isNull_Success(driver)
       filter_city_ID_isNotNull_Success(driver)
       filter_city_ID_NoFilter_Success(driver)
       test_Filter_City_Pagination15_Success(driver)
       test_Filter_City_Pagination25_Success(driver)
       test_Filter_City_Pagination50_Success(driver)
       add_City(driver)
       edit_City(driver)
       City_Refresh(driver)
       City_DownloadasExcel(driver)
       time.sleep(2)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()


City_webpage()

    

# %%
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

# %%
def test_Add_New_LOB_Success(driver):
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
        time.sleep(2)
        driver.find_element(By.XPATH,"//button[normalize-space()='Add']").click()
        time.sleep(2)
        driver.find_element(By.XPATH,"//input[@type='text']").clear()
        time.sleep(2)
        driver.find_element(By.XPATH,"//input[@type='text']").send_keys("aa")
        driver.find_element(By.XPATH,"//img[@alt='search-icon']").click()
        time.sleep(2)
        driver.find_element(By.XPATH,"//img[@alt='trash']").click()
        driver.find_element(By.XPATH,"//button[normalize-space()='Delete']").click()
        time.sleep(2)


# %%
def test_Edit_LOB_Success(driver):
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
        driver.find_element(By.XPATH,"//button[normalize-space()='Add']").click()
        addLOB_header = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='mt-4 w-full text-center'] p[class='text-[14px]']"))
        )
        driver.find_element(By.XPATH,"//button[normalize-space()='Add']").click()
        # driver.find_element(By.XPATH,"//input[@type='text']").send_keys("")
        time.sleep(4)
        driver.find_element(By.XPATH,"//img[@alt='search-icon']").click()
        # driver.find_element(By.XPATH,"//input[@placeholder='Search']").clear()
        time.sleep(2)
        driver.find_element(By.XPATH,"//img[@alt='edit']").click()
        driver.find_element(By.XPATH,"//input[@name='empName']").clear()
        driver.find_element(By.XPATH,"//input[@name='empName']").send_keys("ashish")
        driver.find_element(By.XPATH,"//button[normalize-space()='Save']").click()
        time.sleep(4)
        driver.find_element(By.XPATH,"//input[@type='text']").clear()
        time.sleep(2)
        driver.find_element(By.XPATH,"//input[@type='text']").send_keys("ashish")
        time.sleep(2)
        driver.find_element(By.XPATH,"//img[@alt='search-icon']").click()
        time.sleep(2)
        driver.find_element(By.XPATH,"//img[@alt='trash']").click()
        time.sleep(2)
        driver.find_element(By.XPATH,"//button[normalize-space()='Delete']").click()
        time.sleep(2)


# %%
def test_filter_LOB_StartsWith(driver,send_letter):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").send_keys(send_letter)
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2)").click()
        time.sleep(2)

# %%
def test_Filter_LOB_StartsWith_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_LOB_StartsWith(driver,"a")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='StartsWith']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='LOB']").click()
        time.sleep(2)
        


# %%
def test_Filter_LOB_Contains_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_LOB_StartsWith(driver,"a")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='Contains']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='LOB']").click()
        time.sleep(2)
        


# %%
def test_Filter_LOB_DoesNotContain_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_LOB_StartsWith(driver,"a")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='DoesNotContain']").click()
        driver.find_element(By.XPATH,"//div[contains(@class,'flex text-sm')]").click()
        time.sleep(2)



# %%
def test_Filter_LOB_EndsWith_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_LOB_StartsWith(driver,"a")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='EndsWith']").click()
        driver.find_element(By.XPATH,"//div[contains(@class,'flex text-sm')]").click()
        time.sleep(2)


# %%
def test_Filter_LOB_EqualTo_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_LOB_StartsWith(driver,"a")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='EqualTo']").click()
        driver.find_element(By.XPATH,"//div[@class='flex text-sm']").click()
        time.sleep(2)
        


# %%
def test_Filter_LOB_isNull_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_LOB_StartsWith(driver,"a")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='isNull']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='LOB']").click()
        time.sleep(2)

# %%
def test_Filter_LOB_isNotNull_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_LOB_StartsWith(driver,"a")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='isNotNull']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='LOB']").click()
        time.sleep(2)



# %%
def test_Filter_LOB_Nofilter_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_LOB_StartsWith(driver,"a")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='No Filter']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='LOB']").click()
        time.sleep(2)



# %%
def test_filter_ID_LOB_StartsWith(driver,send_letter):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").send_keys(send_letter)
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2)").click()
        time.sleep(2)

# %%
def test_Filter_ID_LOB_Equalto_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_ID_LOB_StartsWith(driver,"12")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='EqualTo']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='LOB']").click()
        time.sleep(2)
    


# %%
def test_Filter_ID_LOB_NotEqualTo_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_ID_LOB_StartsWith(driver,"12")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='NotEqualTo']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='LOB']").click()
        time.sleep(2)
    


# %%
def test_Filter_ID_LOB_GreaterThan_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_ID_LOB_StartsWith(driver,"12")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='GreaterThan']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='LOB']").click()
        time.sleep(2)
    


# %%
def test_Filter_ID_LOB_GreaterThanOrEqualTo_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_ID_LOB_StartsWith(driver,"12")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='GreaterThanOrEqualTo']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='LOB']").click()
        time.sleep(2)



# %%
def test_Filter_ID_LOB_LessThan_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_ID_LOB_StartsWith(driver,"12")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='LessThan']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='LOB']").click()
        time.sleep(2)


# %%
def test_Filter_ID_LOB_LessThanOrEqualTo_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_ID_LOB_StartsWith(driver,"12")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='LessThanOrEqualTo']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='LOB']").click()
        time.sleep(2)



# %%
def test_Filter_ID_LOB_Between_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_ID_LOB_StartsWith(driver,"12")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='Between']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='LOB']").click()
        time.sleep(1)
       

# %%
def test_Filter_ID_LOB_NotBetween_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_ID_LOB_StartsWith(driver,"12")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='NotBetween']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='LOB']").click()
        time.sleep(2)
       


# %%
def test_Filter_ID_LOB_isNull_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_ID_LOB_StartsWith(driver,"12")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='isNull']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='LOB']").click()
        time.sleep(2)
       



# %%
def test_Filter_ID_LOB_isNotNull_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_ID_LOB_StartsWith(driver,"12")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='isNotNull']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='LOB']").click()
        time.sleep(2)
    


# %%
def test_Filter_ID_LOB_NoFilter_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_ID_LOB_StartsWith(driver,"12")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='No Filter']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='LOB']").click()
        time.sleep(2)


# %%
def test_Filter_LOB_Pagination_15_Success(driver):
        ele=driver.find_element(By.XPATH,"//select[@name='currentPages']")
        d=Select(ele)
        d.select_by_visible_text('15')
        time.sleep(2)


# %%
def test_Filter_LOB_Pagination_25_Success(driver):
        ele=driver.find_element(By.XPATH,"//select[@name='currentPages']")
        d=Select(ele)
        d.select_by_visible_text('25')
        time.sleep(2)


# %%
def test_Filter_LOB_Pagination_50_Success(driver):
        ele=driver.find_element(By.XPATH,"//select[@name='currentPages']")
        d=Select(ele)
        d.select_by_visible_text('50')
        time.sleep(2)


# %%
def test_Filter_LOB_Refresh_Success(driver):
        driver.find_element(By.XPATH,"//p[normalize-space()='Refresh']").click()
        time.sleep(2)
        



# %%
def test_LOB_Download_Success(driver):
        driver.find_element(By.XPATH,"//p[normalize-space()='Download']").click()
        time.sleep(2)
        driver.find_element(By.XPATH,"//p[normalize-space()='Download as Excel']").click()
        time.sleep(2)


# %%
def test_LOB_return_Success(driver):
        driver.find_element(By.XPATH,"//img[contains(@class,'w-5 h-5')]").click()
        time.sleep(2)
        


# %%
def LOB_Webpage():
    try:
        driver=login_and_navigate_LOB("ruderaw", "abcdefg", "9632")
        test_Filter_LOB_StartsWith_Success(driver)
        test_Filter_LOB_Contains_Success(driver)
        test_Filter_LOB_DoesNotContain_Success(driver)
        test_Filter_LOB_EndsWith_Success(driver)
        test_Filter_LOB_EqualTo_Success(driver)
        test_Filter_LOB_isNull_Success(driver)
        test_Filter_LOB_isNotNull_Success(driver)
        test_Filter_LOB_Nofilter_Success(driver)
        test_Filter_ID_LOB_Equalto_Success(driver)
        test_Filter_ID_LOB_NotEqualTo_Success(driver)
        test_Filter_ID_LOB_GreaterThan_Success(driver)
        test_Filter_ID_LOB_GreaterThanOrEqualTo_Success(driver)
        test_Filter_ID_LOB_LessThan_Success(driver)
        test_Filter_ID_LOB_LessThanOrEqualTo_Success(driver)
        test_Filter_ID_LOB_isNull_Success(driver)
        test_Filter_ID_LOB_isNotNull_Success(driver)
        test_Filter_ID_LOB_NoFilter_Success(driver)
        test_Filter_LOB_Pagination_15_Success(driver)
        test_Filter_LOB_Pagination_25_Success(driver)
        test_Filter_LOB_Pagination_50_Success(driver)
        test_Add_New_LOB_Success(driver)
        test_Edit_LOB_Success(driver)
        test_Filter_LOB_Refresh_Success(driver)
        test_LOB_Download_Success(driver)
        test_LOB_return_Success(driver)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

LOB_Webpage()

# %%
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

# %%
def test_Add_New_Country_Success(driver):
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
        time.sleep(2)
        driver.find_element(By.XPATH,"//button[normalize-space()='Add']").click()
        time.sleep(2)
        driver.find_element(By.XPATH,"//button[normalize-space()='Save']").click()
        time.sleep(2)
        driver.find_element(By.XPATH,"//input[@type='text']").clear()
        time.sleep(2)
        driver.find_element(By.XPATH,"//input[@type='text']").send_keys("aryan")
        time.sleep(2)
        driver.find_element(By.XPATH,"//img[@alt='search-icon']").click()
        time.sleep(2)
        driver.find_element(By.XPATH,"//img[@alt='trash']").click()
        time.sleep(2)
        driver.find_element(By.XPATH,"//button[normalize-space()='Delete']").click()
        time.sleep(2)


# %%
def test_Edit_Country_Success(driver):
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
        time.sleep(2)
        driver.find_element(By.XPATH,"//button[normalize-space()='Add']").click()
        time.sleep(2)
        driver.find_element(By.XPATH,"//button[normalize-space()='Save']").click()
        time.sleep(2)
        driver.find_element(By.XPATH,"//input[@type='text']").clear()
        time.sleep(2)
        # driver.find_element(By.XPATH,"//input[@type='text']").send_keys("aryan")
        # time.sleep(2)
        driver.find_element(By.XPATH,"//img[@alt='search-icon']").click()
        time.sleep(2)
        driver.find_element(By.XPATH,"//img[@alt='edit']").click()
        driver.find_element(By.XPATH,"//input[@name='countryName']").clear()
        driver.find_element(By.XPATH,"//input[@name='countryName']").send_keys("ashish")
        driver.find_element(By.XPATH,"//button[normalize-space()='Save']").click()
        time.sleep(4)
        driver.find_element(By.XPATH,"//input[@type='text']").clear()
        time.sleep(2)
        driver.find_element(By.XPATH,"//input[@type='text']").send_keys("ashish")
        time.sleep(3)
        driver.find_element(By.XPATH,"//img[@alt='search-icon']").click()
        time.sleep(2)
        driver.find_element(By.XPATH,"//img[@alt='trash']").click()
        time.sleep(2)
        driver.find_element(By.XPATH,"//button[normalize-space()='Delete']").click()
        time.sleep(2)


# %%
def test_filter_LOB_Country_StartsWith(driver,send_letter):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").send_keys(send_letter)
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        time.sleep(2)

# %%
def test_Filter_Country_StartsWith_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_ID_LOB_StartsWith(driver,"a")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='StartsWith']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Country']").click()
        time.sleep(2)
        


# %%
def test_Filter_Country_Contains_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_ID_LOB_StartsWith(driver,"a")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='Contains']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Country']").click()
        time.sleep(2)


# %%
def test_Filter_Country_DoesNotContains_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_ID_LOB_StartsWith(driver,"a")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='DoesNotContain']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Country']").click()
        time.sleep(2)


# %%
def test_Filter_Country_EndsWith_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_ID_LOB_StartsWith(driver,"a")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='EndsWith']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Country']").click()
        time.sleep(2)


# %%
def test_Filter_Country_EqualsTo_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_ID_LOB_StartsWith(driver,"a")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='EqualTo']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Country']").click()
        time.sleep(2)


# %%
def test_Filter_Country_isNotNull_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_ID_LOB_StartsWith(driver,"a")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='isNotNull']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Country']").click()
        time.sleep(2)



# %%
def test_Filter_Country_isNull_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_ID_LOB_StartsWith(driver,"a")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='isNull']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Country']").click()
        time.sleep(2)

# %%
def test_Filter_Country_Nofilter_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_ID_LOB_StartsWith(driver,"a")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='No Filter']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Country']").click()
        time.sleep(2)

# %%
def test_filter_Country_ID_StartsWith(driver,send_letter):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").send_keys(send_letter)
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        time.sleep(2)

# %%
def test_Filter_ID_Country_Equalto_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_Country_ID_StartsWith(driver,"12")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='EqualTo']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Country']").click()
        time.sleep(2)


# %%
def test_Filter_ID_Country_NotEqualto_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_Country_ID_StartsWith(driver,"12")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='NotEqualTo']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Country']").click()
        time.sleep(3)


# %%
def test_Filter_ID_Country_GreaterThan_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_Country_ID_StartsWith(driver,"12")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='GreaterThan']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Country']").click()
        time.sleep(3)



# %%
def test_Filter_ID_Country_LessThan_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_Country_ID_StartsWith(driver,"12")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='LessThan']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Country']").click()
        time.sleep(3)


# %%
def test_Filter_ID_Country_LessThanOrEqualTo_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_Country_ID_StartsWith(driver,"12")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='LessThanOrEqualTo']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Country']").click()
        time.sleep(3)
    


# %%
def test_Filter_ID_Country_isNull_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_Country_ID_StartsWith(driver,"12")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='isNull']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Country']").click()
        time.sleep(3)


# %%
def test_Filter_ID_Country_isNotNull_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_Country_ID_StartsWith(driver,"12")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='isNotNull']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Country']").click()
        time.sleep(3)



# %%
def test_Filter_ID_Country_NoFilter_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_Country_ID_StartsWith(driver,"12")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='No Filter']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Country']").click()
        time.sleep(3)



# %%
def test_Filter_ID_Country_GreaterThanOrEqualTo_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_Country_ID_StartsWith(driver,"12")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='GreaterThanOrEqualTo']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Country']").click()
        time.sleep(3)

# %%
def test_Filter_Country_Pagination_15_Success(driver):
        ele=driver.find_element(By.XPATH,"//select[@name='currentPages']")
        d=Select(ele)
        d.select_by_visible_text('15')
        time.sleep(2)
        driver.find_element(By.XPATH,"//button[normalize-space()='2']").click()
        time.sleep(2)


# %%
def test_Filter_Country_Pagination_25_Success(driver):
        ele=driver.find_element(By.XPATH,"//select[@name='currentPages']")
        d=Select(ele)
        d.select_by_visible_text('25')
        time.sleep(2)
        driver.find_element(By.XPATH,"//button[normalize-space()='2']").click()
        time.sleep(2)


# %%
def test_Filter_Country_Pagination_50_Success(driver):
        ele=driver.find_element(By.XPATH,"//select[@name='currentPages']")
        d=Select(ele)
        d.select_by_visible_text('50')
        time.sleep(2)


# %%
def test_Country_Refresh_Success(driver):
        driver.find_element(By.XPATH,"//p[normalize-space()='Refresh']").click()
        time.sleep(2)


# %%
def test_Country_Download_Success(driver):
        driver.find_element(By.XPATH,"//p[normalize-space()='Download']").click()
        time.sleep(2)
        driver.find_element(By.XPATH,"//p[normalize-space()='Download as Excel']").click()
        time.sleep(2)


# %%
def test_Country_return_Success(driver):
        driver.find_element(By.XPATH,"//img[@src='/src/assets/back.png']").click()
        time.sleep(2)


# %%
def test_Country_Countryname_ascending(driver):
        driver.find_element(By.XPATH,"//body/div/div/div/div/div/div/div/div[2]/p[1]/button[1]/span[1]").click()
        time.sleep(2)


# %%
def test_Country_Countryname_descending(driver):
        driver.find_element(By.XPATH,"//body/div/div/div/div/div/div/div/div[2]/p[1]/button[1]/span[1]").click()
        time.sleep(2)


# %%
def test_Country_ID_descending(driver):
        driver.find_element(By.XPATH,"//body/div/div/div/div/div/div/div/div[1]/p[1]/button[1]/span[1]").click()
        time.sleep(2)


# %%
def test_Country_ID_ascending(driver):
        driver.find_element(By.XPATH,"//body/div/div/div/div/div/div/div/div[1]/p[1]/button[1]/span[1]").click()
        time.sleep(2)


# %%
def Country_Webpage():
    try:
        driver = login_and_navigate_Country("ruderaw", "abcdefg", "9632")
        test_Country_Countryname_ascending(driver)
        test_Country_Countryname_descending(driver)
        test_Country_ID_ascending(driver)
        test_Country_ID_descending(driver)
        test_Filter_Country_StartsWith_Success(driver)
        test_Filter_Country_Contains_Success(driver)
        test_Filter_Country_DoesNotContains_Success(driver)
        test_Filter_Country_EndsWith_Success(driver)
        test_Filter_Country_EqualsTo_Success(driver)
        test_Filter_Country_isNotNull_Success(driver)
        test_Filter_Country_isNull_Success(driver)
        test_Filter_Country_Nofilter_Success(driver)
        test_Filter_ID_Country_Equalto_Success(driver)
        test_Filter_ID_Country_NotEqualto_Success(driver)
        test_Filter_ID_Country_GreaterThan_Success(driver)
        test_Filter_ID_Country_LessThan_Success(driver)
        test_Filter_ID_Country_LessThanOrEqualTo_Success(driver)
        test_Filter_ID_Country_isNull_Success(driver)
        test_Filter_ID_Country_isNotNull_Success(driver)
        test_Filter_ID_Country_GreaterThanOrEqualTo_Success(driver)
        test_Filter_ID_Country_NoFilter_Success(driver)
        test_Filter_Country_Pagination_15_Success(driver)
        test_Filter_Country_Pagination_25_Success(driver)
        test_Filter_Country_Pagination_50_Success(driver)
        test_Add_New_Country_Success(driver)
        test_Edit_Country_Success(driver)
        test_Country_Refresh_Success(driver)
        test_Country_Download_Success(driver)
        test_Country_return_Success(driver)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

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

# %%
def test_Add_New_Locality_Success(driver):
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
        time.sleep(2)
        driver.find_element(By.XPATH,"//button[normalize-space()='Add']").click()
        time.sleep(2)
        driver.find_element(By.XPATH,"//button[normalize-space()='Add']").click()
        time.sleep(2)
        driver.find_element(By.XPATH,"//input[@type='text']").clear()
        time.sleep(2)
        driver.find_element(By.XPATH,"//input[@type='text']").send_keys("India")
        time.sleep(2)
        driver.find_element(By.XPATH,"//img[@alt='search-icon']").click()
        time.sleep(2)
        driver.find_element(By.XPATH,"//body[1]/div[1]/div[1]/div[1]/div[2]/div[3]/div[2]/div[1]/div[2]/div[2]/button[2]/img[1]").click()
        time.sleep(2)
        driver.find_element(By.XPATH,"//button[normalize-space()='Delete']").click()
        time.sleep(2)


# %%
def test_Edit_Locality_Success(driver):
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
        time.sleep(2)
        driver.find_element(By.XPATH,"//button[normalize-space()='Add']").click()
        time.sleep(2)
        driver.find_element(By.XPATH,"//button[normalize-space()='Add']").click()
        time.sleep(2)
        # driver.find_element(By.XPATH,"//input[@type='text']").clear()
        # time.sleep(2)
        # driver.find_element(By.XPATH,"//input[@type='text']").send_keys("India")
        # time.sleep(2)
        driver.find_element(By.XPATH,"//img[@alt='search-icon']").click()
        time.sleep(2)
        driver.find_element(By.XPATH,"//div//div//div//div//div//div[1]//div[2]//div[2]//button[1]//img[1]").click()
        driver.find_element(By.XPATH,"//input[@name='empName']").clear()
        driver.find_element(By.XPATH,"//input[@name='empName']").send_keys("ashish")
        driver.find_element(By.XPATH,"//button[normalize-space()='Save']").click()
        time.sleep(4)
        driver.find_element(By.XPATH,"//input[@type='text']").clear()
        time.sleep(2)
        driver.find_element(By.XPATH,"//input[@type='text']").send_keys("ashish")
        time.sleep(2)
        driver.find_element(By.XPATH,"//img[@alt='search-icon']").click()
        time.sleep(2)
        driver.find_element(By.XPATH,"//img[@alt='trash']").click()
        time.sleep(2)
        driver.find_element(By.XPATH,"//button[normalize-space()='Delete']").click()
        time.sleep(2)
        


# %%
def test_filter_Locality_CountryName_StartsWith(driver,send_letter):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").send_keys(send_letter)
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        time.sleep(2)

# %%
def test_Filter_Locality_Country_name_StartsWith_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_Locality_CountryName_StartsWith(driver,"i")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='StartsWith']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)
        


# %%
def test_Filter_Locality_Country_name_Contains_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_Locality_CountryName_StartsWith(driver,"i")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='Contains']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)
        


# %%
def test_Filter_Locality_Country_name_DoesNotContains_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_Locality_CountryName_StartsWith(driver,"i")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='DoesNotContain']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)
        


# %%
def test_Filter_Locality_Country_name_EndsWith_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_Locality_CountryName_StartsWith(driver,"i")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='EndsWith']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)
        


# %%
def test_Filter_Locality_Country_name_EqualsTo_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_Locality_CountryName_StartsWith(driver,"i")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='EqualTo']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)
    


# %%
def test_Filter_Locality_Country_name_isNotNull_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_Locality_CountryName_StartsWith(driver,"i")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='isNotNull']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)


# %%
def test_Filter_Locality_Country_name_isNull_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_Locality_CountryName_StartsWith(driver,"i")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='isNull']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)


# %%
def test_Filter_Locality_Country_name_NoFilter_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_Locality_CountryName_StartsWith(driver,"i")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='No Filter']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)


# %%
def test_filter_Locality_StateName_StartsWith(driver,send_letter):
        driver.find_element(By.CSS_SELECTOR,"div:nth-child(3) div:nth-child(1) input:nth-child(1)").send_keys(send_letter)
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        time.sleep(2)

# %%
def test_Filter_Locality_State_name_StartsWith_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"div:nth-child(3) div:nth-child(1) input:nth-child(1)").clear()
        test_filter_Locality_StateName_StartsWith(driver,"m")
        time.sleep(2)     
        driver.find_element(By.XPATH,"//h1[normalize-space()='StartsWith']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)


# %%
def test_Filter_Locality_State_name_Contains_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"div:nth-child(3) div:nth-child(1) input:nth-child(1)").clear()
        test_filter_Locality_StateName_StartsWith(driver,"m")
        time.sleep(2) 
        driver.find_element(By.XPATH,"//h1[normalize-space()='Contains']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)
    


# %%
def test_Filter_Locality_State_name_DoesNotContains_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"div:nth-child(3) div:nth-child(1) input:nth-child(1)").clear()
        test_filter_Locality_StateName_StartsWith(driver,"m")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='DoesNotContain']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)
    


# %%
def test_Filter_Locality_State_name_EndsWith_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"div:nth-child(3) div:nth-child(1) input:nth-child(1)").clear()
        test_filter_Locality_StateName_StartsWith(driver,"m")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='EndsWith']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)


# %%
def test_Filter_Locality_State_name_EqualsTo_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"div:nth-child(3) div:nth-child(1) input:nth-child(1)").clear()
        test_filter_Locality_StateName_StartsWith(driver,"m")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='EqualTo']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)
    


# %%
def test_Filter_Locality_State_name_isNotNull_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"div:nth-child(3) div:nth-child(1) input:nth-child(1)").clear()
        test_filter_Locality_StateName_StartsWith(driver,"m")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='isNotNull']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)
        


# %%
def test_Filter_Locality_State_name_isNull_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"div:nth-child(3) div:nth-child(1) input:nth-child(1)").clear()
        test_filter_Locality_StateName_StartsWith(driver,"m")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='isNull']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)
        


# %%
def test_Filter_Locality_State_name_NoFilter_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"div:nth-child(3) div:nth-child(1) input:nth-child(1)").clear()
        test_filter_Locality_StateName_StartsWith(driver,"m")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='No Filter']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)



# %%
def test_filter_Locality_CityName_StartsWith(driver,send_letter):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)").send_keys(send_letter)
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        time.sleep(2)

# %%
def test_Filter_Locality_City_name_StartsWith_Success(driver): 
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_Locality_CityName_StartsWith(driver,"p")
        time.sleep(2)      
        driver.find_element(By.XPATH,"//h1[normalize-space()='StartsWith']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)
        


# %%
def test_Filter_Locality_City_name_Contains_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_Locality_CityName_StartsWith(driver,"p")
        time.sleep(2)  
        driver.find_element(By.XPATH,"//h1[normalize-space()='Contains']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)


# %%
def test_Filter_Locality_City_name_DoesNotContains_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_Locality_CityName_StartsWith(driver,"p")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='DoesNotContain']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)
        


# %%
def test_Filter_Locality_City_name_EndsWith_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_Locality_CityName_StartsWith(driver,"p")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='EndsWith']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)


# %%
def test_Filter_Locality_City_name_EqualsTo_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_Locality_CityName_StartsWith(driver,"p")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='EqualTo']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)
    


# %%
def test_Filter_Locality_City_name_isNotNull_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_Locality_CityName_StartsWith(driver,"p")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='isNotNull']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)
    


# %%
def test_Filter_Locality_City_name_isNull_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_Locality_CityName_StartsWith(driver,"p")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='isNull']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)
        


# %%
def test_Filter_Locality_City_name_NoFilter_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_Locality_CityName_StartsWith(driver,"p")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='No Filter']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)
    


# %%
def test_filter_Locality_LocalityName_StartsWith(driver,send_letter):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(5) > div:nth-child(1) > input:nth-child(1)").send_keys(send_letter)
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(5) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        time.sleep(2)

# %%
def test_Filter_Locality_name_StartsWith_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(5) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_Locality_LocalityName_StartsWith(driver,"a")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='StartsWith']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)
        


# %%
def test_Filter_Locality_name_Contains_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(5) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_Locality_LocalityName_StartsWith(driver,"a")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='Contains']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)
    


# %%
def test_Filter_Locality_name_DoesNotContains_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(5) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_Locality_LocalityName_StartsWith(driver,"a")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='DoesNotContain']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)
    


# %%
def test_Filter_Locality_name_EndsWith_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(5) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_Locality_LocalityName_StartsWith(driver,"a")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='EndsWith']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)
    


# %%
def test_Filter_Locality_name_EqualsTo_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(5) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_Locality_LocalityName_StartsWith(driver,"a")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='EqualTo']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)


# %%
def test_Filter_Locality_name_isNotNull_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(5) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_Locality_LocalityName_StartsWith(driver,"a")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='isNotNull']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)
    


# %%
def test_Filter_Locality_name_isNull_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(5) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_Locality_LocalityName_StartsWith(driver,"a")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='isNull']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)
    


# %%
def test_Filter_Locality_name_NoFilter_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(5) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_Locality_LocalityName_StartsWith(driver,"a")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='No Filter']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)


# %%
def test_filter_Locality_LocalityID_StartsWith(driver,send_letter):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").send_keys(send_letter)
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > button:nth-child(2) > img:nth-child(1)").click()
        time.sleep(2)

# %%
def test_Filter_Locality_ID_EqualsTo_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_Locality_LocalityID_StartsWith(driver,"16")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='EqualTo']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)


# %%
def test_Filter_Locality_ID_NotEqualTo_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_Locality_LocalityID_StartsWith(driver,"16")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='NotEqualTo']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)
    

# %%
def test_Filter_Locality_ID_GreaterThan_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_Locality_LocalityID_StartsWith(driver,"16")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='GreaterThan']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)


# %%
def test_Filter_Locality_ID_LessThan_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_Locality_LocalityID_StartsWith(driver,"16")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='LessThan']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)
    


# %%
def test_Filter_Locality_ID_GreaterThanOrEqualTo_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_Locality_LocalityID_StartsWith(driver,"16")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='GreaterThanOrEqualTo']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)


# %%
def test_Filter_Locality_ID_LessThanOrEqualTo_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_Locality_LocalityID_StartsWith(driver,"16")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='LessThanOrEqualTo']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)
        


# %%
def test_Filter_Locality_ID_isNull_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_Locality_LocalityID_StartsWith(driver,"16")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='isNull']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)
        


# %%
def test_Filter_Locality_ID_isNotNull_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_Locality_LocalityID_StartsWith(driver,"16")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='isNotNull']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)
    


# %%
def test_Filter_Locality_ID_NoFilter_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)").clear()
        test_filter_Locality_LocalityID_StartsWith(driver,"16")
        time.sleep(2)
        driver.find_element(By.XPATH,"//h1[normalize-space()='No Filter']").click()
        driver.find_element(By.XPATH,"//h1[normalize-space()='Locality']").click()
        time.sleep(2)
        


# %%
def test_Filter_Locality_Pagination_15_Success(driver):
        ele=driver.find_element(By.XPATH,"//select[@name='currentPages']")
        d=Select(ele)
        d.select_by_visible_text('15')
        time.sleep(2)
        driver.find_element(By.XPATH,"//button[normalize-space()='2']").click()
        time.sleep(2)


# %%
def test_Filter_Locality_Pagination_25_Success(driver):
        ele=driver.find_element(By.XPATH,"//select[@name='currentPages']")
        d=Select(ele)
        d.select_by_visible_text('25')
        time.sleep(2)
        driver.find_element(By.XPATH,"//button[normalize-space()='2']").click()
        time.sleep(2)


# %%
def test_Filter_Locality_Pagination_50_Success(driver):
        ele=driver.find_element(By.XPATH,"//select[@name='currentPages']")
        d=Select(ele)
        d.select_by_visible_text('50')
        time.sleep(2)


# %%
def test_Filter_Locality_Refresh_Success(driver):
        driver.find_element(By.XPATH,"//p[normalize-space()='Refresh']").click()
        time.sleep(2)


# %%
def test_Locality_Download_Success(driver):
        driver.find_element(By.XPATH,"//p[normalize-space()='Download']").click()
        time.sleep(2)
        driver.find_element(By.XPATH,"//p[normalize-space()='Download as Excel']").click()
        time.sleep(2)


# %%
def test_Locality_Return_Success(driver):
        driver.find_element(By.CSS_SELECTOR,"body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > a:nth-child(1) > img:nth-child(1)").click()
        time.sleep(2)
        


# %%
def test_Locality_Country_ascending(driver):
    driver.find_element(By.XPATH,"//body/div/div/div/div/div/div/div/div[2]/p[1]/button[1]/span[1]").click()
    time.sleep(2)

# %%
def test_Locality_Country_descending(driver):
    driver.find_element(By.XPATH,"//body/div/div/div/div/div/div/div/div[2]/p[1]/button[1]/span[1]").click()
    time.sleep(2)
    

# %%
def test_Locality_State_descending(driver):
    driver.find_element(By.XPATH,"//div//div//div//div//div//div[3]//p[1]//button[1]//span[1]").click()
    time.sleep(2)
    

# %%
def test_Locality_State_ascending(driver):
    driver.find_element(By.XPATH,"//div//div//div//div//div//div[3]//p[1]//button[1]//span[1]").click()
    time.sleep(2)
    

# %%
def test_Locality_City_ascending(driver):
    driver.find_element(By.XPATH,"//div[4]//p[1]//button[1]//span[1]").click()
    time.sleep(2)
    

# %%
def test_Locality_City_descending(driver):
    driver.find_element(By.XPATH,"//div[4]//p[1]//button[1]//span[1]").click()
    time.sleep(2)
    

# %%
def test_Locality_Localityname_descending(driver):
    driver.find_element(By.XPATH,"//div[5]//p[1]//button[1]//span[1]").click()
    time.sleep(2)
    

# %%
def test_Locality_Localityname_ascending(driver):
    driver.find_element(By.XPATH,"//div[5]//p[1]//button[1]//span[1]").click()
    time.sleep(2)
    

# %%
def test_Locality_ID_ascending(driver):
    driver.find_element(By.XPATH,"//body/div/div/div/div/div/div/div/div[1]/p[1]/button[1]/span[1]").click()
    time.sleep(2)
    

# %%
def test_Locality_ID_descending(driver):
    driver.find_element(By.XPATH,"//body/div/div/div/div/div/div/div/div[1]/p[1]/button[1]/span[1]").click()
    time.sleep(2)
    

# %%
def Locality_Webpage():
    try:
        driver=login_and_navigate_Locality("ruderaw", "abcdefg", "9632")
        test_Locality_Country_ascending(driver)
        test_Locality_Country_descending(driver)
        test_Locality_State_ascending(driver)
        test_Locality_State_descending(driver)
        test_Locality_City_ascending(driver)
        test_Locality_City_descending(driver)
        test_Locality_Localityname_ascending(driver)
        test_Locality_Localityname_descending(driver)
        test_Locality_ID_ascending(driver)
        test_Locality_ID_descending(driver)
        test_Filter_Locality_Country_name_StartsWith_Success(driver)
        test_Filter_Locality_Country_name_Contains_Success(driver)
        test_Filter_Locality_Country_name_DoesNotContains_Success(driver)
        test_Filter_Locality_Country_name_EndsWith_Success(driver)
        test_Filter_Locality_Country_name_EqualsTo_Success(driver)
        test_Filter_Locality_Country_name_isNotNull_Success(driver)
        test_Filter_Locality_Country_name_isNull_Success(driver)
        test_Filter_Locality_Country_name_NoFilter_Success(driver)
        test_Filter_Locality_State_name_StartsWith_Success(driver)
        test_Filter_Locality_State_name_Contains_Success(driver)
        test_Filter_Locality_State_name_DoesNotContains_Success(driver)
        test_Filter_Locality_State_name_EndsWith_Success(driver)
        test_Filter_Locality_State_name_EqualsTo_Success(driver)
        test_Filter_Locality_State_name_isNotNull_Success(driver)
        test_Filter_Locality_State_name_isNull_Success(driver)
        test_Filter_Locality_State_name_NoFilter_Success(driver)
        test_Filter_Locality_City_name_StartsWith_Success(driver)
        test_Filter_Locality_City_name_Contains_Success(driver)
        test_Filter_Locality_City_name_DoesNotContains_Success(driver)
        test_Filter_Locality_City_name_EndsWith_Success(driver)
        test_Filter_Locality_City_name_EqualsTo_Success(driver)
        test_Filter_Locality_City_name_isNotNull_Success(driver)
        test_Filter_Locality_City_name_isNull_Success(driver)
        test_Filter_Locality_City_name_NoFilter_Success(driver)
        test_Filter_Locality_name_StartsWith_Success(driver)
        test_Filter_Locality_name_Contains_Success(driver)
        test_Filter_Locality_name_DoesNotContains_Success(driver)
        test_Filter_Locality_name_EndsWith_Success(driver)
        test_Filter_Locality_name_EqualsTo_Success(driver)
        test_Filter_Locality_name_isNotNull_Success(driver)
        test_Filter_Locality_name_isNull_Success(driver)
        test_Filter_Locality_name_NoFilter_Success(driver)
        test_Filter_Locality_ID_EqualsTo_Success(driver)
        test_Filter_Locality_ID_NotEqualTo_Success(driver)
        test_Filter_Locality_ID_GreaterThan_Success(driver)
        test_Filter_Locality_ID_LessThan_Success(driver)
        test_Filter_Locality_ID_GreaterThanOrEqualTo_Success(driver)
        test_Filter_Locality_ID_LessThanOrEqualTo_Success(driver)
        test_Filter_Locality_ID_isNull_Success(driver)
        test_Filter_Locality_ID_isNotNull_Success(driver)
        test_Filter_Locality_ID_NoFilter_Success(driver)
        test_Filter_Locality_Pagination_15_Success(driver)
        test_Filter_Locality_Pagination_25_Success(driver)
        test_Filter_Locality_Pagination_50_Success(driver)
        test_Add_New_Locality_Success(driver)
        test_Edit_Locality_Success(driver)
        test_Filter_Locality_Refresh_Success(driver)
        test_Locality_Download_Success(driver)
        test_Locality_Return_Success(driver)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit() 

Locality_Webpage()



