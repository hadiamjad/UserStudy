from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
import time
# from pyvirtualdisplay import Display
import pandas as pd
import requests
import csv

# virtual display
# display = Display(visible=0, size=(800, 600))
# display.start()

#df = pd.read_csv(r'9.csv')
df = pd.DataFrame([['biba.in']], columns=['website'])

dic = {}

for i in df.index:
    #try:
        # dictionary collecting logs
        # 1: Before Logs 2: Before PageSource 3: After Logs 4: After PageSource
        dic[df['website'][i]] = []
        # extension filepath
        ext_file = 'extension'

        opt = webdriver.ChromeOptions()
        # devtools necessary for complete network stack capture
        opt.add_argument("--auto-open-devtools-for-tabs")
        # loads extension
        opt.add_argument("load-extension=" + ext_file)
        # important for linux
        opt.add_argument('--no-sandbox')

        dc = DesiredCapabilities.CHROME
        dc['goog:loggingPrefs'] = { 'browser':'ALL' }

        driver = webdriver.Chrome(ChromeDriverManager().install(), options=opt, desired_capabilities=dc)
        requests.post(url = 'http://localhost:3000/complete', data = {'website': df['website'][i]})
        driver.get(r'https://www.'+ df['website'][i])
        # sleep
        time.sleep(1500)
        # saving logs in dictionary
        dic[df['website'][i]].append(driver.get_log('browser'))
        dic[df['website'][i]].append(driver.page_source)
            
        driver.quit()
        pd.DataFrame(dic).to_csv('output.csv')

        with open("logs.txt","w") as log: log.write(str(i)); log.close()
        print(r'Completed: '+ str(i)+ ' website: '+ df['website'][i])
    #except:
        #print(r'Crashed: '+ str(i) + ' website: '+ df['website'][i])