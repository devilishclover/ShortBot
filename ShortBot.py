import pyautogui
import time
import random
import requests
from bs4 import BeautifulSoup
from win32gui import GetForegroundWindow, GetWindowText
import win32clipboard
from difflib import SequenceMatcher

def get_chrome_url():
    window = GetForegroundWindow()
    title = GetWindowText(window)
    
    if "- Google Chrome" in title:
        # Simulate Ctrl+L to select address bar
        pyautogui.hotkey('ctrl', 'l')
        # Small delay to ensure address bar is selected
        time.sleep(0.1)
        # Copy URL to clipboard
        pyautogui.hotkey('ctrl', 'c')
        # Small delay to ensure clipboard is updated
        time.sleep(0.1)
        # Return to previous position
        pyautogui.press('escape')
        
        # Get URL from clipboard
        try:
            win32clipboard.OpenClipboard()
            url = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            return url
        except:
            return None
    return None

def title(soup):
        link = soup.find_all(name="title")[0]
        title = str(link)
        title = title.replace("<title>","")
        title = title.replace("</title>","")
        return title

def description(soup):
        description = ""
        meta_desc = soup.find("meta", {"name": "description"})
        if meta_desc:
            description = meta_desc.get("content", "")
        return description


if __name__ == "__main__":
    interests = pyautogui.prompt('Enter your interests (separated by commas):')
    interest_list = [x.strip() for x in interests.split(',')]
    print(f"Interests: {interest_list}")

    print("Auto-scroll started. Press Ctrl+C to stop.")

    try:
        while True:
            pyautogui.scroll(-1)
            time.sleep(1)
            try:
                url = get_chrome_url()
            except:
                url = None
            if url:
                r = requests.get(url)
                soup = BeautifulSoup(r.text, 'html.parser')
                print(f"Title: {title(soup)}")
                print(f"Description: {description(soup)}")
                    
                sleep_time = random.randint(1, 5)
                if title(soup).__contains__("Blurry:") or title(soup).__contains__("Vertical:"):
                    print("AD")
                    sleep_time = 0
                else:
                    def similar(a, b, threshold=0.8):
                        return SequenceMatcher(None, a.lower(), b.lower()).ratio() > threshold or \
                            a.lower() in b.lower() or b.lower() in a.lower()  # Added substring check
                    
                    for interest in interest_list:
                        if any(similar(interest, word) for word in title(soup).lower().split()) or \
                        any(similar(interest, word) for word in description(soup).lower().split()):
                            print(f"Interest found: {interest}")
                            print(f"Interest found: {interest}")
                            sleep_time += 10
                time.sleep(sleep_time)
                
            
    except KeyboardInterrupt:
        print("Program stopped by user")
