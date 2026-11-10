import pyautogui
import time
import pyperclip
import openpyxl
import os
import mss
from datetime import datetime

# Configure PyAutoGUI safety settings
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5   

print("=== Starting PyAutoGUI Daily Report Bot ===")
time.sleep(3)

# Date formatting
now = datetime.now()
today_time = now.strftime("%d-%m-%y %H:%M:%S")
today_date = now.strftime("%d-%m-%y")

# 1. Open Google Chrome
print("1. Opening Chrome...")
pyautogui.hotkey('win', 'r')
time.sleep(1)
pyautogui.write('chrome --profile-directory="Profile 4"', interval=0.05)
time.sleep(1)
pyautogui.press('enter')
time.sleep(3)

pyautogui.hotkey('ctrl', 't')  # Open a new tab
time.sleep(1)
pyautogui.write('https://news.google.com/home?hl=en-IN&gl=IN&ceid=IN%3Aen', interval=0.05)
pyautogui.press('enter')
time.sleep(5)  # Wait for page to load

# 2. Extract news text from page clipboard
print("2. Copying the news content...")
pyautogui.hotkey('win', 'up')  # Maximize window
time.sleep(1)   
pyautogui.hotkey('ctrl', 'a')  # Select all text
time.sleep(1)
pyautogui.hotkey('ctrl', 'c')  # Copy selected text
time.sleep(1)

fetched_news = pyperclip.paste().strip()
if not fetched_news:    
    print("Error: No news content copied. Exiting.")
    exit(1)

clean_news = fetched_news.replace('\n', ' ')[:200]    
print(f"   Fetched News Data: '{clean_news}'")
pyautogui.hotkey('ctrl', 'w')  # Close news tab
time.sleep(1)

# 3. Create Excel workbook report via openpyxl
print("3. Creating report data with Date/Time, Fetched Info, and Comment...")
comment = "Good News"
xlsx_filename = f"daily_report_{today_date}.xlsx"
xlsx_file_path = os.path.abspath(xlsx_filename)

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Daily Summary"

# Append Header and Data rows
ws.append(["Date & Time", "Fetched Information", "Comment"])
ws.append([today_time, clean_news, comment])

# Save workbook
wb.save(xlsx_file_path)
print(f"   Saved Excel file: {xlsx_file_path}")

# 4. Open generated spreadsheet
print("4. Opening spreadsheet application (Excel)...")
os.startfile(xlsx_file_path)
time.sleep(5)  # Allow Excel to load completely

pyautogui.hotkey('win', 'up')
time.sleep(2)

# 5. Capture desktop screenshot
print("5. Taking screenshot of the final Excel sheet...")
screenshot_filename = f"screenshot_{today_date}.png"

# Fixed: Formatted properly as a dynamic path including the .png extension
save_path = os.path.join(r"D:\GENAI PROGRAM\screenshots", screenshot_filename)
os.makedirs(os.path.dirname(save_path), exist_ok=True)

# Save screenshot via pyautogui
pyautogui.screenshot(save_path)

# Save high-res screenshot via mss to the same path
with mss.mss() as sct:
    sct.shot(output=save_path)

print(f"Screenshot successfully saved to: {save_path}")
print("\n=== Bot Execution Successfully Finished! ===")