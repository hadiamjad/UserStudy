from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
import time
# from pyvirtualdisplay import Display
import pandas as pd
import requests
import zlib


# virtual display
# display = Display(visible=0, size=(800, 600))
# display.start()

#df = pd.read_csv(r'9.csv')
df = pd.DataFrame([['Mama.cn']], columns=['website'])

dic = {}

for i in df.index:
    #try:
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
        #driver.get(r'file:///Users/haadi/Desktop/UserStudy/extension/basic.html')
        # sleep
        time.sleep(20)
        # saving logs in dictionary
        pagedata = {
            "top_level_url": df['website'][i],
            "console_errors":driver.get_log('browser'),
            "page_source": zlib.compress(bytes(driver.page_source, 'utf-8')),
            "Blocking_level": None
        }
        requests.post("http://localhost:3000/logs", data=pagedata)
        # a = zlib.compress(a)
        # zlib.decompress(a.encode())
            
        driver.quit()

        with open("logs.txt","w") as log: log.write(str(i)); log.close()
        print(r'Completed: '+ str(i)+ ' website: '+ df['website'][i])
    #except:
        #print(r'Crashed: '+ str(i) + ' website: '+ df['website'][i])