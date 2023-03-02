from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait

import time
import requests
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys

import re
import random
import sqlite3


chrome_options = webdriver.ChromeOptions()

driver = webdriver.Chrome(chrome_options=chrome_options)

#gets proxy and port api link
driver.get("https://geonode.com/free-proxy-list")

link=(driver.find_element("xpath",'//*[@id="__next"]/div/div/div[2]/div/section[2]/div/div[2]/div[3]/div/div[1]/div[2]/div[1]/div[2]/div/div/span/div/div/input')).get_attribute("value")

#use the api link to get proxy as response
response = requests.get(link)

scraped_proxies=response.json()

#loop the dict and get proxy ip,port and protocol
proxy_list=[]
for i in scraped_proxies["data"]:
    if i["speed"] <= 2:
        proxys={}
        proxys["proxy"] = i["ip"]+":"+i["port"]
        protocols = str(i["protocols"])
        proxys["protocols"] = re.sub(r"[\[\]']", "", protocols)
        proxy_list.append(proxys)

valid_proxies=[]

# test proxy function that gets proxy and type of protocal as argument to test does it works
def test_proxy(proxy,protocolss):
    try:
        response = requests.get('https://geonode.com/free-proxy-list', proxies={protocolss:proxy}, timeout=2)
        if response.status_code == 200:
            return True
        else:
            return False
    except:
        return False    

# loop through each proxy and check if it's working
for proxy in proxy_list:
    if proxy["protocols"]=="http":
        if test_proxy(("http://" + proxy["proxy"]),proxy["protocols"]):
            valid_proxies.append("http://" + proxy["proxy"])


    elif proxy["protocols"]=="https":
        if test_proxy(("https://" + proxy["proxy"]),proxy["protocols"]):
            valid_proxies.append("https://" + proxy["proxy"])
  

    elif proxy["protocols"]=="socks4":
        if test_proxy(("socks4://" + proxy["proxy"]),proxy["protocols"]):
            valid_proxies.append("socks4://" + proxy["proxy"])


    elif proxy["protocols"]=="socks5":
        if test_proxy(("socks5://" + proxy["proxy"]),proxy["protocols"]):
            valid_proxies.append("socks5://" + proxy["proxy"])

            
    else:
        print("Proxy {} not working".format(proxy["proxy"]))



links=[]

#get the proxy randomly from the list
PROXY = random.choice(valid_proxies)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=%s' % PROXY)
driver = webdriver.Chrome(chrome_options=chrome_options)

driver.get("https://rocketreach.co/company?start=1&pageSize=10&geo%5B%5D=Australia")

driver.maximize_window()

wait = WebDriverWait(driver, 25)
wait.until(EC.presence_of_element_located(("xpath","/html/body/div[1]/div/div/div/rr-signup-form-v2-directive/div/div/form/div/p[2]/a")))

driver.find_element("xpath", "/html/body/div[1]/div/div/div/rr-signup-form-v2-directive/div/div/form/div/p[2]/a").click()

# Locate the username and password fields
driver.find_element("xpath","//*[@id='id_email']").send_keys("machinelearning791@gmail.com")
driver.find_element("xpath","//*[@id='id_password']").send_keys("Ha@03011999")

time.sleep(4)

# Click the login button
driver.find_element("xpath","//*[@id='user-signup']/div[1]/fieldset/button").click()

time.sleep(5)

# Skip the pop up page
WebDriverWait(driver, 25).until(EC.presence_of_element_located(("xpath","//*[@id='blur-container']/div[4]/div/div/div[1]/div[1]/a")))
driver.find_element("xpath","//*[@id='blur-container']/div[4]/div/div/div[1]/div[1]/a").click()

# click the company button
WebDriverWait(driver, 25).until(EC.presence_of_element_located(("xpath","//*[@id='blur-container']/div[4]/div[1]/div[2]/div[1]/div[2]/div[2]/ng-include/div/div/button[2]")))
driver.find_element("xpath","//*[@id='blur-container']/div[4]/div[1]/div[2]/div[1]/div[2]/div[2]/ng-include/div/div/button[2]").click()


#iterate through pages
for page in range(2,4):
    wait = WebDriverWait(driver, 25)
    wait.until(EC.presence_of_element_located(("xpath","//*[@id='blur-container']/div[4]/div[1]/div[2]/div[2]/div/div[2]/rr-unified-search-results/div/div[3]/div/div")))
    driver.find_element("xpath", '//*[@id="blur-container"]/div[4]/div[1]/div[2]/div[2]/div/div[2]/rr-unified-search-results/div/div[3]/div/div/ul/li[{}]/button'.format(page)).click()

    #get the href link of each company
    time.sleep(10)
    for i in range(1,11):
        link=(driver.find_element("xpath","//*[@id='blur-container']/div[4]/div[1]/div[2]/div[2]/div/div[2]/rr-unified-search-results/div/div[3]/div/ul/li[{}]/rr-company-search-result/div/div[1]/div[1]/div[2]/a".format(i))).get_attribute("href")
        links.append(link)

# Connect to the database (create it if it doesn't exist)
conn = sqlite3.connect('company.db')

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Check if the table exists
table_check = "SELECT name FROM sqlite_master WHERE type='table' AND name='Company'"
cursor.execute(table_check)
result = cursor.fetchone()

# If the table exists, drop it
if result:
    drop_table = "DROP TABLE Company"
    cursor.execute(drop_table)
    conn.commit()
    print("Existing table dropped")

# Create the Company table
cursor.execute('''
CREATE TABLE Company (
    company_name varchar(255),
    Website varchar(255),
    Ticker varchar(10),
    Revenue decimal(18,2),
    Employees int,
    Founded date,
    Address varchar(255),
    Phone varchar(20),
    Fax varchar(20),
    Technologies varchar(255),
    Category varchar(255),
    SIC varchar(10),
    NAICS varchar(10),
    E_mail varchar(255),
    Employee varchar(255)
)
''')

#iterrate through all company href links
for each_comapny in links:

    driver.get(str(each_comapny))

    company_name=driver.find_element("xpath","//*[@id='blur-container']/div[4]/div/div[3]/div[1]/div/div/div[1]/div/div/div[1]/div[1]/div/h1/a").text

    PARTIAL_LINK_TEXT = "partial link text"
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "headline-summary")))
    time.sleep(10)

    #Size of the table

    number_of_rows=(driver.find_elements("xpath","//table/tbody/tr"))
    size_of_table=(len(number_of_rows))+1


    data={}
    data["company_name"]="NIL"
    data["Website"]="NIL"
    data["Ticker"]="NIL"
    data["Revenue"] ="NIL"
    data["Employees"]="NIL"
    data["Founded"]="NIL"
    data["Address"]="NIL"
    data["Phone"]="NIL"
    data["Fax"] ="NIL"
    data["Technologies"]="NIL"
    data["Category"]="NIL"
    data["SIC"]="NIL"
    data["NAICS"]="NIL"
    data["E_mail"]="NIL"
    data["Employee"]="NIL"

    data["company_name"]=company_name[:-11]

    for i in range(1,size_of_table+1):

        #Iterate to each row
        
        try:
            name=(driver.find_element("xpath","(//table[@class='table']/tbody/tr)[{}]/td/strong".format(i)).text)

            #website and ticker has different pattern of xpath
            if name in ("Website","Ticker"):
                data[name]=(driver.find_element("xpath","(//table[@class='table']/tbody/tr)[{}]/td/a".format(i)).text)
            else:
                data[name]=(driver.find_element("xpath","((//table[@class='table']/tbody/tr)[{}]/td)[2]".format(i)).text)
        
        except:

            pass

    #clicks the email button

    email_button = driver.find_element("xpath", "//*[@id='blur-container']/div[4]/div/div[3]/div[1]/div/ul/li[2]/a")

    email_button.click()

    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "company-header__cta-container")))

    #check the table size
    get_table=(driver.find_elements("xpath","//table/tbody/tr"))
    size_of_table=(len(get_table))+1

    E_mail=[]

    #iterrate through the rows
    for i in range(1,size_of_table):
        nested_dict={}

        nested_dict["Email-format"]=(driver.find_element("xpath","(//table[@class='table']/tbody/tr)[{}]/td[1]".format(i)).text)

        nested_dict["Email-example"]=(driver.find_element("xpath","(//table[@class='table']/tbody/tr)[{}]/td[2]".format(i)).text)

        nested_dict["Email-success-percentage"]=(driver.find_element("xpath","(//table[@class='table']/tbody/tr)[{}]/td[3]/div/span".format(i)).text)

        E_mail.append(nested_dict)
    data["E_mail"]=str(E_mail)
        

    try:

        #press the management button
        driver.find_element("xpath", "//*[@id='blur-container']/div[4]/div/div[3]/div[1]/div/ul/li[3]").click()

    #if pop is appeared
    except ElementClickInterceptedException as e:
        popup=driver.find_element("xpath", "//*[@id='modal-upgrade']/div/div/div/a")
        popup.click()
        time.sleep(3)
        managment_button=driver.find_element("xpath", "//*[@id='blur-container']/div[4]/div/div[3]/div[1]/div/ul/li[3]")
        managment_button.click()

    #wait until page loads
    wait = WebDriverWait(driver, 25)
    wait.until(EC.presence_of_element_located(("xpath","//*[@id='blur-container']/div[4]/div/div[3]/div[1]/div/div/div[1]/div/div/div[2]/div/div/div[2]/ul/button")))

    employee={}

    try:
        #click and get the number in the show more integer to iterate the number of employees
        show_more_button=driver.find_element("xpath","//*[@id='blur-container']/div[4]/div/div[3]/div[1]/div/div/div[1]/div/div/div[2]/div/div/div[2]/ul/button")
        number_of_employee=show_more_button.text
        show_more_button.click()
        numbers = int((re.findall(r'\d+', number_of_employee))[0])

        #get the root employee
        first_level=(driver.find_element("xpath", "//*[@id='blur-container']/div[4]/div/div[3]/div[1]/div/div/div[1]/div/div/div[2]/div/div/div[2]/div/div[1]/ng-include/div/a/div[3]").text)
        first_level_designation=(driver.find_element("xpath","//*[@id='blur-container']/div[4]/div/div[3]/div[1]/div/div/div[1]/div/div/div[2]/div/div/div[2]/div/div[1]/ng-include/div/a/div[4]").text)
        employee[first_level]=first_level_designation

        #iterate through each employee

        for i in range(1,numbers+5):
            second_level=(driver.find_element("xpath","//*[@id='blur-container']/div[4]/div/div[3]/div[1]/div/div/div[1]/div/div/div[2]/div/div/div[2]/ul/li[{}]/ng-include/div/a/div[3]".format(i)).text)
            second_level_designation=(driver.find_element("xpath","//*[@id='blur-container']/div[4]/div/div[3]/div[1]/div/div/div[1]/div/div/div[2]/div/div/div[2]/ul/li[{}]/ng-include/div/a/div[4]".format(i)).text)
            department=(driver.find_element("xpath","//*[@id='blur-container']/div[4]/div/div[3]/div[1]/div/div/div[1]/div/div/div[2]/div/div/div[2]/ul/li[{}]/ng-include/div/a/div[1]/span/span[1]".format(i)).text)
            employee[second_level]=second_level_designation +" "+ "({})".format(department)
    
        
    except ElementClickInterceptedException as e:

        #if pop appears
        popup=driver.find_element("xpath", "//*[@id='modal-upgrade']/div/div/div/a")
        popup.click()
        time.sleep(3)
        #click and get the number in the show more integer
        show_more_button=driver.find_element("xpath","//*[@id='blur-container']/div[4]/div/div[3]/div[1]/div/div/div[1]/div/div/div[2]/div/div/div[2]/ul/button")
        number_of_employee=show_more_button.text
        show_more_button.click()
        numbers = int((re.findall(r'\d+', number_of_employee))[0])

        first_level=(driver.find_element("xpath", "//*[@id='blur-container']/div[4]/div/div[3]/div[1]/div/div/div[1]/div/div/div[2]/div/div/div[2]/div/div[1]/ng-include/div/a/div[3]").text)
        first_level_designation=(driver.find_element("xpath","//*[@id='blur-container']/div[4]/div/div[3]/div[1]/div/div/div[1]/div/div/div[2]/div/div/div[2]/div/div[1]/ng-include/div/a/div[4]").text)
        employee[first_level]=first_level_designation

        #iterate through each employee

        for i in range(1,numbers+5):
            second_level=(driver.find_element("xpath","//*[@id='blur-container']/div[4]/div/div[3]/div[1]/div/div/div[1]/div/div/div[2]/div/div/div[2]/ul/li[{}]/ng-include/div/a/div[3]".format(i)).text)
            second_level_designation=(driver.find_element("xpath","//*[@id='blur-container']/div[4]/div/div[3]/div[1]/div/div/div[1]/div/div/div[2]/div/div/div[2]/ul/li[{}]/ng-include/div/a/div[4]".format(i)).text)
            department=(driver.find_element("xpath","//*[@id='blur-container']/div[4]/div/div[3]/div[1]/div/div/div[1]/div/div/div[2]/div/div/div[2]/ul/li[{}]/ng-include/div/a/div[1]/span/span[1]".format(i)).text)
            employee[second_level]=second_level_designation +" "+ "({})".format(department)

    data["Employee"]=str(employee)

    #using regex to clean the employee string
    data["Employees"]=re.sub(r"\n\([^\)]*\)", "", data["Employees"])

    conn = sqlite3.connect('company.db')

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Define the SQL query with placeholders for the column values
    sql = '''
    INSERT INTO Company
        (company_name, Website, Ticker, Revenue, Employees, Founded, Address, Phone, Fax, Technologies, Category, SIC, NAICS, E_mail, Employee)
    VALUES
        (:company_name, :Website, :Ticker, :Revenue, :Employees, :Founded, :Address, :Phone, :Fax, :Technologies, :Category, :SIC, :NAICS, :E_mail, :Employee)
    '''

    # Execute the SQL query with the values from the dictionary
    cursor.execute(sql, data)

    # Save changes to the database
    conn.commit()

    # Close the connection to the database
    conn.close()
