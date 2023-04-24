from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from datetime import datetime, timedelta
import time, subprocess, sys

#inspired from https://stackoverflow.com/questions/12332975/how-can-i-install-a-python-module-within-code
#install selenium for user 
subprocess.check_call([sys.executable, "-m", "pip", "install", "selenium"])
print()

#input for zip code
user_zip = input("Enter zip code: ").strip()
#error handling for valid zip code
while(user_zip.isdigit() == False or len(user_zip) != 5):
    user_zip = input("Please enter a valid zip code: ")
#prompt for movie times to be printed
print("Available movie dates to be viewed: ")
#acquires todays date and finds all future dates for up to 11 days
today = datetime.now()
future_dates = list(range(12))
for x in range(12):
    future_dates[x] = today + timedelta(days=x) 
    future_dates[x] = str(future_dates[x])[5:10]
for x in range(len(future_dates)):
    #print future dates
    print(future_dates[x])

#dictionary of accepted user inputted dates
dates_dict = {
    future_dates[0]: "1",
    future_dates[1]: "2",
    future_dates[2]: "3",
    future_dates[3]: "4",
    future_dates[4]: "5",
    future_dates[5]: "6",
    future_dates[6]: "7",
    future_dates[7]: "8",
    future_dates[8]: "9",
    future_dates[9]: "10",
    future_dates[10]: "11",
    future_dates[11]: "12",
}
#user inputted dates
user_date = input("Enter the date of movie (month-day, ex. 01-31): ").strip()
#error handling for valid date
while (user_date not in dates_dict.keys()):
    user_date = input("Enter valid date: ").strip()
    continue
#if today is today's date, sends different x-path
if user_date == future_dates[0]:
    final_date = "//*[@id='showdatesCarousel']/li[1]/a[1]/div[1]"

#string splicing from https://stackoverflow.com/questions/4022827/insert-some-string-into-given-string-at-given-index
#string manipulation to send corresponding xpath of date
else:
    user_date_xpath = "//*[@id='showdatesCarousel']/li[]/a[1]/div[2]"
    index = user_date_xpath.find("]/a")
    final_date = user_date_xpath[:index] + dates_dict.get(user_date) + user_date_xpath[index:]

#driver creation and path
#service = Service(r"C:\Program Files (x86)\chromedriver.exe")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#driver = webdriver.Chrome(service = service)

# window size taken from https://stackoverflow.com/questions/12211781/how-to-maximize-window-in-chrome-using-webdriver-python
#set window size to max view
driver.set_window_size(1024, 600)
driver.maximize_window()
#Cinemark website
driver.get("https://www.cinemark.com/?gclid=Cj0KCQjw8e-gBhD0ARIsAJiDsaV9B9qAXoAteb5wqisEl31hxsJHOFPBn5YD1797IDRUdMi9h8LuEx8aAhEWEALw_wcB")
print(driver.title,"\n")

#try block inspired from https://www.w3docs.com/snippets/java/stale-element-reference-element-is-not-attached-to-the-page-document.html
#try blocks to handle StaleElementReferenceExceptions, I could not get explicit or implicit waits to work. Unfortunately, as a result, time.sleeps() were used
try:
    time.sleep(7)
    raise StaleElementReferenceException

except StaleElementReferenceException as Exception:
    #find and click zip icon
    zip = driver.find_element(By.ID, "UserLocationForm")
    zip.click()
    #find and click search bar
    search = driver.find_element(By.ID, "locationSearchInput")
    time.sleep(2)
    search.click()
    #enter user zip code and return
    search.send_keys(user_zip)
    search.send_keys(Keys.RETURN)

    try:
        time.sleep(5)
        raise StaleElementReferenceException

    except StaleElementReferenceException as Exception:
        #find and print theater name
        user_theater = driver.find_element(By.CLASS_NAME, "trunc")
        print("Closest movie theater:", user_theater.text)
        #find and click closest theater to zip code 
        theater = driver.find_element(By.CLASS_NAME, "theaterLink").click()
        time.sleep(3)
        #find and click user specified date
        date = driver.find_element(By.XPATH, final_date).click()
        time.sleep(3)
        #prompt to display movie titles and their showtimes
        print("Movies playing and their showtimes: \n")
        #find movie titles and show times
        theater_name = driver.find_element(By.ID, "showtimesInner")
        for x in theater_name.find_elements(By.TAG_NAME, "a"):
            #remove excessive links
            if x.text == "Details" or x.text == "Trailer" or x.text == "Add to Watch List":
                continue

            else:
                #inspired from https://www.geeksforgeeks.org/how-to-remove-blank-lines-from-a-txt-file-in-python/
                #remove blank lines
                if x.text.strip():
                    print(x.text)
        #prevent executable from closing
        driver.minimize_window()
        prevent_close = input("Enter any key to close: ")
#close browser
driver.quit()