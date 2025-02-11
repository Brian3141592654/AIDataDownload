#!/home/alilong/tf/bin/python3
# Install requirements
#!apt-get update
#!apt install chromium-chromedriver
#!cp /usr/lib/chromium-browser/chromedriver /usr/bin
#!pip install selenium

import os, cv2, random
# import matplotlib.pyplot as plt
# import numpy as np
import time #shutil, requests
import numpy as np
# import pandas as pd
from keras.models import load_model
import sys
sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')
from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from urllib.parse import urljoin
# import csv
from IPython.display import Image, display

from settings4 import BASEPATH, filename, num_rows_to_read


#存下載下來的驗證碼圖案
CAPTCHA_FOLDER = BASEPATH + "captcha/"

#做完前處理後的圖案
PROCESSED_FOLDER = BASEPATH + "processed/"

#AI的訓練權重
MODEL_FOLDER = "model.hdf5"

#下載下來後存在的檔案
DL_FOLDER = BASEPATH + "download/"

#Output Path
CSVPATH = BASEPATH + "csv/" 

#前處理裁切的大小
WIDTH = 200
HEIGHT = 60
CROP_LEFT = 10
CROP_TOP = 10
CROP_BOTTON = 10
allowedChars = 'ACDEFGHJKLNPQRTUVXYZ2346789';

#預測結果轉成字串
def one_hot_decoding(prediction, allowedChars):
    text = ''
    for predict in prediction:
        value = np.argmax(predict[0])
        text += allowedChars[value]
    return text

#前處理=>去噪 模糊 裁剪
def preprocessing(from_filename, to_filename):
    if not os.path.isfile(from_filename):
        print("file not found:", from_filename)
        return
    img = cv2.imread(from_filename)
    denoised = cv2.fastNlMeansDenoisingColored(img, None, 30, 30, 7, 21)

    kernel = np.ones((4,4), np.uint8)
    erosion = cv2.erode(denoised, kernel, iterations=1)
    burred = cv2.GaussianBlur(erosion, (5, 5), 0)

    edged = cv2.Canny(burred, 30, 150)
    dilation = cv2.dilate(edged, kernel, iterations=1)

    crop_img = dilation[CROP_TOP:HEIGHT - CROP_BOTTON, CROP_LEFT:WIDTH]

    cv2.imwrite(to_filename, crop_img)
    return

#猜驗證碼
def TakeGuess(filename, model):
    from_filename = DL_FOLDER+filename
    to_filename = CAPTCHA_FOLDER+filename

    preprocessing(from_filename, to_filename) #將要辨識的圖片做一次預處理
    #model = load_model(MODEL_FOLDER) #載入模型
    img = cv2.imread(to_filename)
    npary = np.array(img)/255.0
    npary = npary.reshape(40, 190, 3)
    npary = npary.reshape(-1, 40, 190, 3) #將預處理過的圖片轉成模型可接受的形式
    x = model.predict(npary) #預測結果
    result = one_hot_decoding(x, allowedChars) #預測結果轉成字串
    return result

# def read_excel_row_by_row(filename, num_rows=None):
#     df = pd.read_excel(filename)
#     integer_data = []
#     for i, row in df.iterrows():
#         if num_rows is not None and i >= num_rows:
#             break
#         row_data = []
#         for value in row:
#             try:
#                 row_data.append(int(value))
#             except ValueError:
#                 # Handle non-numeric values gracefully
#                 row_data.append(value)
#         integer_data.append(row_data)
#     return integer_data

def read_txt_row_by_row(filename, num_rows=0):
    row_data = []
    i = 0
    try:
        with open(filename, 'r') as file:
            print ("Stock Ticks: ", end="")
            for row in file:
                value = row.strip()
                row_data.append(value)
                print (value, end=" ", flush=True)
                # time.sleep (0.01)
                i+=1
                if num_rows!=0 and i>=num_rows:
                    break
    except Exception as e:
        print(f"Error: {e}")
    return row_data    
    
# # dl_captch deprecated!!!
# # Download Captcha and save the image from 'image_url' to 'to_file'
# # return True: fail;    False: success
# def dl_captcha (image_url, to_file):
#       response = requests.get(image_url, stream=False)  # Stream download
#       if response.status_code == 200:
#           # Get the filename from the response headers (optional)
#           #filename = image_url.split("=")[-1]  # Assuming filename is the last part of URL
#           #print(f"filename={filename}")
#           # Save the image
#           with open(to_file, 'wb') as f:
#               for chunk in response.iter_content(1024):
#                   f.write(chunk)
#           # print(f"Downloaded captcha: {to_file}")
#           return False
#       else:
#           print(f"Failed to download captcha {response.status_code}")
#           time.sleep(2)
#           return True
      
def click_by_NAME(driver, name):
    ele = driver.find_element(By.NAME, name)
    ActionChains(driver).click(ele).perform()

def clear_by_NAME(driver, name):
    ele = driver.find_element(By.NAME, name)
    ele.clear()

def submit_captcha(driver, vcode):
    captcha_input = WebDriverWait(driver, 10).until (
    EC.presence_of_element_located((By.NAME, "CaptchaControl1"))
    )
    # Submit captcha
    captcha_input.send_keys(vcode)
    time.sleep(0.5+random.random())
    # captcha_input.send_keys(Keys.ENTER)
    click_by_NAME (driver, "btnOK")

def csv_click_action(driver):
    try:
        # Find the download link
        dlcsv = WebDriverWait(driver, timeout=10, poll_frequency=1.1).until(
            EC.presence_of_element_located((By.ID, "HyperLink_DownloadCSV"))
        )
        # Check if the link is both displayed and enabled (clickable)
        if dlcsv.is_displayed() and dlcsv.is_enabled():
            # print("Download link found and enabled!, click the download link")
            ActionChains(driver).click(dlcsv).perform()
            return False
        else:
            print("Download link not found or not enabled!")
            time.sleep (5)
            return True
    except (NoSuchElementException, TimeoutException) as e:
        # Handle both NoSuchElementException and TimeoutException
        print("csv_click_action Error:", e)
        return True

def get_vcode (model):
    captcha_filename = "001.png"
    captcha_filepathname = DL_FOLDER+captcha_filename 
    
    panel_element = driver.find_element(By.CSS_SELECTOR, "#Panel_bshtm")
    image_element = panel_element.find_element(By.TAG_NAME, "img")
    
    image_element.screenshot(captcha_filepathname)
    display (Image(filename=captcha_filepathname))
    print ("analyze..")
    vcode = TakeGuess(captcha_filename, model)
    print(f"captcha={vcode}", flush=True)
    return vcode
    
    
def get_csv (driver, row):
    stock_num = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "TextBox_Stkno"))
    )
    stock_num.send_keys(row)
    # time.sleep(random.randint(0,1))
    if stock_num.get_attribute("value") != row:
        print("Text not successfully typed")
        return True #fail

    # image_url = image_element.get_attribute("src")
    # if not image_url.startswith("http"):
    #     image_url = urljoin(driver.current_url, image_url)
    
    vcode = get_vcode(model)
    submit_captcha(driver, vcode)
    
    # click on save csv button
    if csv_click_action(driver):
        print ("get_csv: Captcha wrong answer.  Try again")
        time.sleep(3)
        print ("analyze")
        vcode = get_vcode(model)
        print ("End of analyze")
        submit_captcha(driver, vcode)
        if csv_click_action(driver):
            print (f"get_csv: Download {row} Fail.")
            return True # fail probably on captcha recognition.
    
    print(f"Downloaded {row}.CSV.\n")
    return 0  # success

#----------------------------------------------------------#


## Begin of Main Program
print (f"Reading stock tick symbol from {filename}.")
integer_data = read_txt_row_by_row(filename, num_rows_to_read)
if integer_data == []:
    print ("FATAL: Read_txt_row_by_row Fail!!!")
    exit(1)
    

#Saving Path
prefs = {"download.default_directory" : CSVPATH,
#         "profile.managed_default_content_settings.images": 2,
         };

model = load_model(MODEL_FOLDER) #載入模型

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("prefs",prefs);
#chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--window-size=800,600")
driver = webdriver.Chrome(options=chrome_options)


datalen = len(integer_data)
print (f"\n\n\n===Total {datalen} Stocks")
T = 10
t = 1
for row in integer_data:

  time.sleep(0.1)
  if (t%T)==1:
      driver.get("https://bsr.twse.com.tw/bshtm/bsMenu.aspx")
      print ("Loading")
      # print ("Driver.get")
  else:
      #click_by_NAME(driver, "Button_Reset")
      #print ("Reset")
      clear_by_NAME(driver, "TextBox_Stkno")
  time.sleep(0.5)
  print(f"---Stock:{row}  {t}/{datalen}---", flush=True)
  if get_csv(driver, row):
      print (f"Retry {row}.", flush=True)
      time.sleep(1)
      click_by_NAME(driver, "Button_Reset")
      if get_csv(driver, row):
          integer_data.append(row)   #retrieve fail, append for retry
          print (f"Fail Again. Retry {row} at the end!", flush=True) # fail
      else:
          print ("Suceed after retry")
          t += 1  #succeed
  else:
      t+=1  #succeed
time.sleep(1)
driver.close()
time.sleep(1)
driver.quit()
