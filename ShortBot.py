import pyautogui
import time
import random
import requests
from bs4 import BeautifulSoup
from win32gui import GetForegroundWindow, GetWindowText
import win32clipboard
from difflib import SequenceMatcher
from ollama import chat

brainrot = ["relatable", "💀", "fypage", "fypviral", "trending", "goodvibes", "squidgame2", "squidgame", "netflix", "funny", "fypシ゚viral", 
"roblox", "troll face", "among us", "memes", "prank", "pranks", "tiktok", "tik tok", "tiktoks", "tik toks", "tiktokers", "tik tokers", "tiktokers", "tik tokers",
"Sigma", "viral" , "fypシ", "fyp", "satisfying", "trendingshorts", "copyright", "Bro", "🤫", "☠️", "motivation", "leadership", "Moments Before Disaster", "clip", 
"🗿", "respect", "skibidi", "aura", "capcut"]

def like():
    pyautogui.moveTo(789, 625)
    pyautogui.click()

def dislike():
    pyautogui.moveTo(784, 730)
    pyautogui.click()

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
    initial_interests = [x.strip() for x in interests.split(',')]
    interest_list = []

    for interest in initial_interests:
        prompt = f"""Generate a list of highly related words and direct synonyms based on this interest: {interest}

            Rules:
            - Return only close variations and direct synonyms
            - Each word should be on a new line
            - Include singular/plural forms
            - Include common compound words
            - Keep words simple and search-friendly
            - Start with the most relevant variations
            
            Do not include:
            - Hashtags or symbols
            - Tangentially related topics
            - Punctuation or special characters
            - Generic or unrelated terms
            - Any explanatory text
            - numberd lists or bullet points"""
        response = chat(model='llama3.2', messages=[{'role': 'user', 'content': prompt}])
        search_queries = response['message']['content'].split('\n')
        interest_list.extend([query.strip() for query in search_queries if query.strip()])
        interest_list.append(interest)
        hashtag_versions = ['#' + query for query in interest_list.copy()]
        interest_list.extend(hashtag_versions)

    # Remove duplicates while preserving order
    interest_list = list(dict.fromkeys(interest_list))
    print(f"Expanded interests: {interest_list}")

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
                    
                sleep_time = 1
                if title(soup).__contains__("Blurry:") or title(soup).__contains__("Vertical:") or title(soup).__contains__("EM ") or title(soup).__contains__("WT ") or title(soup).__contains__("1080x1920"):
                    print("AD")
                    #write to file
                    with open('ads.txt', 'a', encoding='utf-8') as f:
                        f.write(title(soup) + '\n')
                    sleep_time = 0
                else:
                    def similar(a, b, threshold=0.9):
                        return SequenceMatcher(None, a.lower(), b.lower()).ratio() > threshold
                    
                    for interest in interest_list:
                        for word in title(soup).lower().split() + description(soup).lower().split():
                            if similar(interest, word):
                                print(f"Interest found: {interest}")
                                print(f"Matching word: {word}")
                                sleep_time += 10
                                break
                            
                # write to files
                with open('titles.txt', 'a', encoding='utf-8') as f:
                    f.write(title(soup) + '\n')
                with open('descriptions.txt', 'a', encoding='utf-8') as f:
                    f.write(description(soup) + '\n')

                if any(similar(interest, word) for interest in interest_list 
                    for word in title(soup).lower().split() + description(soup).lower().split()):
                    with open('interest-titles.txt', 'a', encoding='utf-8') as f:
                     f.write(title(soup) + '\n')
                    with open('interest-descriptions.txt', 'a', encoding='utf-8') as f:
                     f.write(description(soup) + '\n')


                if any(word.lower() in (title(soup).lower() + ' ' + description(soup).lower()) for word in brainrot):
                    print("Brainrot content detected")
                    with open('brainrot.txt', 'a', encoding='utf-8') as f:
                        f.write(title(soup) + '\n')
                    dislike()
                    print("disliked")
                    sleep_time = 0

                if sleep_time > 5:
                    like()
                    print("Liked")
                print(f"Watching for {sleep_time} seconds")
                time.sleep(sleep_time)


                
                
            
    except KeyboardInterrupt:
        print("Program stopped by user")
