# 📈 AI Stock Data Downloader with Auto Captcha Recognition  

This project automates downloading stock data from [TWSE](https://bsr.twse.com.tw/bshtm/bsMenu.aspx) with **auto captcha recognition**. It is designed to streamline the data collection process with minimal manual intervention.  

---

## 🚀 Features  
- 🔐 **Auto Captcha Recognition**: Efficiently bypasses captcha challenges.  
- 📊 **Stock Data Collection**: Automatically downloads and syncs stock data from TWSE.  
- 🔄 **Automated Workflow**: Managed through a series of shell scripts for seamless execution.  

---

## 📁 File Execution Order  

The files should be run in the following order:  

1. **`run_all.sh`** - The main script to start the entire process.  
2. **`sync_from_net.sh`** - Syncs the latest data from the local files on the PC. (also deletes files)  
3. **`demo4.py`** - 💡 *Core Functionality*: Captcha recognition and data download.  
4. **`sync_to_net.sh`** - Reloads the downloaded data into the local files.  

```bash
# To run the entire process, simply use:
sh run_all.sh
