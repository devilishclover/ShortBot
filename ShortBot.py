import pyautogui
import time
import random
import requests
from bs4 import BeautifulSoup
from win32gui import GetForegroundWindow, GetWindowText
import win32clipboard
from difflib import SequenceMatcher
from ollama import chat
import re
from collections import Counter

brainrot = ["relatable", "💀", "fypage", "fypviral", "goodvibes", "squidgame2", "squidgame", "netflix", "funny", "fypシ゚viral", 
"roblox", "troll face", "among us", "memes", "prank", "pranks", "tiktok", "tik tok", "tiktoks", "tik toks", "tiktokers", "tik tokers", "tiktokers", "tik tokers",
"Sigma", "viral" , "fypシ", "fyp", "satisfying", "trendingshorts", "copyright", "Bro", "🤫", "☠️", "motivation", "leadership", "Moments Before Disaster", "clip", 
"🗿", "respect", "skibidi", "aura", "capcut", "kdrama", "fromtman", "thanos", "celevrity", "salesman", "kdramaedit", "squid", "squidgameedit", "military"
"fouryou", "gongyoo", "leebyunghun"]

with open('rabbit-hole-block-list.txt', 'r', encoding='utf-8') as f:
    rabbit_hole_block_list = f.read().splitlines()

def sort_words_by_frequency(words):
    word_counts = Counter(words)
    sorted_words = sorted(word_counts.items(), key=lambda item: item[1], reverse=True)
    return sorted_words

def subtract_lists(list1, list2):
    set2 = set(list2)
    result = [item for item in list1 if item not in set2]
    return result

def read_words_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        words = content.split()
        words = [word[1:] if word.startswith('#') else word for word in words]
        words = [word.replace('-', '').replace('.', '') for word in words]
        words = [word for word in words if word and re.match("^[a-z]+$", word)]
        return words


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
        # Run prompt twice for each interest
        for _ in range(2):
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

    # Remove duplicates while preserving order
    interest_list = list(dict.fromkeys(interest_list))
    
    # Add hashtag versions and remove duplicates again
    hashtag_versions = ['#' + query if not query.startswith('#') else query for query in interest_list.copy()]
    interest_list.extend(hashtag_versions) 
    interest_list = list(dict.fromkeys(interest_list))

    # Remove duplicates while preserving order
    interest_list = list(dict.fromkeys(interest_list))
    print(f"Expanded interests: {interest_list}")

    print("Auto-scroll started. Press Ctrl+C to stop.")

    try:
        count = 0
        while True:
            count += 1

            if count % 50 == 0:
                
                file_path = 'brainrot.txt'
                words_list = read_words_from_file(file_path)
                interest_titles_path = 'interest-titles.txt'
                interest_titles_list = read_words_from_file(interest_titles_path)

                prompt = f"""our task is to analyze the provided list of topics from a YouTube Shorts tuning bot. 
                The algorithm is being tuned for the following interests: {initial_interests}
                Your job is to identify topics that are too specific or do not align well with these broad interests.
                Ignore generic words such as 'a,' 'the,' 'shorts,' 'video,' 'for,' 'to,' 'on,' and similar filler words. 
                Focus on identifying topics that are overly niche or could lead the algorithm down an unintended rabbit hole.

                Return your answer as a plain list of specific words that should be blocked, with no commentary or explanation.
                the following is the list of words: 
                {sort_words_by_frequency(subtract_lists(words_list, interest_titles_list))}
                """
                rabbit_hole_block_response = chat(model='llama3.2', messages=[{'role': 'user', 'content': prompt}])
                rabbit_hole_block_list.extend(rabbit_hole_block_response['message']['content'].split('\n'))
                rabbit_hole_block_list = list(dict.fromkeys(rabbit_hole_block_list))
                print(f"Updated rabbit hole block list: {rabbit_hole_block_list}")
                with open('rabbit-hole-block-list.txt', 'w', encoding='utf-8') as f:
                    f.write('\n'.join(rabbit_hole_block_list))
                


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
                                sleep_time += 5
                                break
                            
                # write to files
                with open('titles.txt', 'a', encoding='utf-8') as f:
                    f.write(title(soup) + str(sleep_time) + '\n')
                with open('descriptions.txt', 'a', encoding='utf-8') as f:
                    f.write(description(soup) + str(sleep_time) + '\n')

                if any(similar(interest, word) for interest in interest_list 
                    for word in title(soup).lower().split() + description(soup).lower().split()):
                    with open('interest-titles.txt', 'a', encoding='utf-8') as f:
                     f.write(title(soup) + str(sleep_time) + '\n')
                    with open('interest-descriptions.txt', 'a', encoding='utf-8') as f:
                     f.write(description(soup) + str(sleep_time) +'\n')


                if any(word.lower() in (title(soup).lower() + ' ' + description(soup).lower()) for word in brainrot):
                    print("Brainrot content detected")
                    with open('brainrot.txt', 'a', encoding='utf-8') as f:
                        f.write(title(soup) + str(sleep_time) + '\n')
                    dislike()
                    print("disliked")
                    sleep_time = 0

                if any(word.lower() in (title(soup).lower() + ' ' + description(soup).lower()) for word in rabbit_hole_block_list):
                    print("Rabbit hole content detected")
                    dislike()
                    with open('rabbit-hole.txt', 'a', encoding='utf-8') as f:
                        f.write(title(soup) + str(sleep_time) + '\n')
                    print("disliked")
                    sleep_time = 0

                if sleep_time > 5:
                    like()
                    print("Liked")
                print(f"Watching for {sleep_time} seconds")
                time.sleep(sleep_time)


                
                
            
    except KeyboardInterrupt:
        print("Program stopped by user")
