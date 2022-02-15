from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
import time
from pyvirtualdisplay import Display
import pandas as pd
import requests


# virtual display
display = Display(visible=0, size=(800, 600))
display.start()

df = pd.read_csv(r'9.csv')
#df = pd.DataFrame([['sisaketimmigration.com'], ['home.hipac.cn/shop/login.html']], columns=['website'])

dic = {}

for i in df.index:
    try:
        # dictionary collecting logs
        # 1: Logs 2: PageSource 
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
        driver.get(r'https://'+ df['website'][i])
        #driver.get(r'file:///Users/haadi/Desktop/UserStudy/extension/basic.html')
        
        # sleep
        time.sleep(10)
        # saving logs in dictionary
        # saving logs in dictionary
        dic[df['website'][i]].append(driver.get_log('browser'))
        dic[df['website'][i]].append(driver.page_source)

        # driver.quit   
        driver.quit()
        # saving it in csv
        pd.DataFrame(dic).to_csv('output.csv')

        with open("logs.txt","w") as log: log.write(str(i)); log.close()
        print(r'Completed: '+ str(i)+ ' website: '+ df['website'][i])
    except:
        try:
            driver.quit()
        except: 
            pass
        print(r'Crashed: '+ str(i) + ' website: '+ df['website'][i])