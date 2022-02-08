from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import concurrent.futures
import pandas as pd
import itertools 
import os



pages = list(range(1,144))


ROOT = os.getcwd()
s=Service(f'{ROOT}/driver/chromedriver')


chrome_options = Options()
chrome_options.add_argument("--headless")



# url = "https://thehub.io/startups/donkey-republic"
# driver = webdriver.Chrome(service=s,options=chrome_options)
# driver.get(url)
# person_linkedin_id = driver.find_elements(By.CLASS_NAME,'card-person__linkedin')
# linkedin_id = [ i.get_attribute("href") for i in person_linkedin_id]
# person_positions = driver.find_elements(By.CLASS_NAME,'card-person__position')
# position = [ i.text for i in person_positions]
# person_names = driver.find_elements(By.CLASS_NAME,'card-person__name')
# names = [ i.text for i in person_names]
# for (a,b,c) in itertools.zip_longest(names,position,linkedin_id):
#         print(f"{a},{b},{c}")

# for person_name in person_names:
    # print(person_id.get_attribute("href"))
    # print(person_position.text)
    # print(person_name.text)



company_links = []


def urls(page):
    url = f"https://thehub.io/startups?countryCodes=SE&page={page}" 
    print(url)
    driver = webdriver.Chrome(service=s,options=chrome_options)
    driver.get(url)
    elements = list(driver.find_elements(By.XPATH,'//div[@class="col-lg-9"]/content/div[1]/div/div/a'))
    company_links.extend([element.get_attribute("href") for element in elements])

    driver.close()


with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
    executor.map(urls,pages)


company_details = []

def scrap(link):
    driver = webdriver.Chrome(service=s, options=chrome_options)
    driver.get(link)
    try:
        company_name = driver.find_element(By.CLASS_NAME,'startup-header__name').text
        location = driver.find_element(By.XPATH,'//*[@id="__layout"]/div/div[1]/div/div/content/div/div/div/section[1]/div/div/div/content/div/div[2]/table/tbody/tr[1]/td[2]/b').text
        website = driver.find_element(By.XPATH,'//*[@id="__layout"]/div/div[1]/div/div/content/div/div/div/section[1]/div/div/div/content/div/div[2]/table/tbody/tr[2]/td[2]/a').get_attribute("href")
        founded = driver.find_element(By.XPATH,'//*[@id="__layout"]/div/div[1]/div/div/content/div/div/div/section[1]/div/div/div/content/div/div[2]/table/tbody/tr[3]/td[2]/b').text
        employess = driver.find_element(By.XPATH,'//*[@id="__layout"]/div/div[1]/div/div/content/div/div/div/section[1]/div/div/div/content/div/div[2]/table/tbody/tr[4]/td[2]/b').text
        industries = driver.find_element(By.XPATH,'//*[@id="__layout"]/div/div[1]/div/div/content/div/div/div/section[1]/div/div/div/content/div/div[2]/table/tbody/tr[5]/td[2]/b').text
        stage = driver.find_element(By.XPATH,'//*[@id="__layout"]/div/div[1]/div/div/content/div/div/div/section[1]/div/div/div/content/div/div[2]/table/tbody/tr[6]/td[2]/b').text
        business_model = driver.find_element(By.XPATH,'//*[@id="__layout"]/div/div[1]/div/div/content/div/div/div/section[1]/div/div/div/content/div/div[2]/table/tbody/tr[7]/td[2]/b').text
        funding_state = driver.find_element(By.XPATH,'//*[@id="__layout"]/div/div[1]/div/div/content/div/div/div/section[1]/div/div/div/content/div/div[2]/table/tbody/tr[8]/td[2]/b').text
        person_linkedin_id = driver.find_elements(By.CLASS_NAME,'card-person__linkedin')
        linkedin_id = [ i.get_attribute("href") for i in person_linkedin_id]
        person_position = driver.find_elements(By.CLASS_NAME,'card-person__position')
        position = [ i.text for i in person_position]
        person_name = driver.find_elements(By.CLASS_NAME,'card-person__name')
        names = [ i.text for i in person_name]
    
    except Exception as e:
        print(e.message,"Something went Wrong !!!!")

    final_details = []
    for (a,b,c) in itertools.zip_longest(names,position,linkedin_id):
        final_details.append([a,b,c])        

    details = {
        "company_name":company_name,
        "location_site" : location,
        "website":website,
        "founded":founded,
        "employess":employess,
        "industries":industries,
        "stage":stage,
        "business_model":business_model,
        "funding_state":funding_state,
        "person_details":final_details
    }
    company_details.append(details)

    print(company_details)

    driver.close()



with concurrent.futures.ThreadPoolExecutor(max_workers=25) as executor:
    executor.map(scrap,company_links)


dataframe = pd.DataFrame(company_details)
file_name = 'Sweden_compnay_details.xlsx'
dataframe.to_excel(file_name)
print("Data Extraction Completed !!!")


