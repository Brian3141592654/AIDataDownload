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
2. **`sync_from_net.sh`** - Syncs the latest data from the internet.  
3. **`demo4.py`** - 💡 *Core Functionality*: This is where the AI magic happens for captcha recognition and data extraction.  
4. **`sync_to_net.sh`** - Uploads the processed data for storage or further analysis.  

```bash
# To run the entire process, simply use:
sh run_all.sh
