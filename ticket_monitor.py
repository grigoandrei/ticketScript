#!/usr/bin/env python3
import requests
import time
import re
import os
from datetime import datetime

URL = "https://www.ticketmaster.de/artist/bts-tickets/958687"
CHECK_INTERVAL = 300  # 5 minutes

def play_notification():
    # Play system notification sound (macOS)
    os.system("afplay /System/Library/Sounds/Glass.aiff")
    # Alternative: terminal bell
    print("\a" * 5)  # Bell sound

def check_tickets():
    try:
        response = requests.get(URL, headers={'User-Agent': 'Mozilla/5.0'})
        content = response.text
        
        # Look for "Konzerte" followed by a number
        match = re.search(r'konzerte(\d+)', content.lower())
        if match:
            count = int(match.group(1))
            if count > 0:
                return True, f"TICKETS AVAILABLE! Konzerte count: {count}"
            else:
                return False, f"No concerts yet (Konzerte{count})"
        
        return False, "Konzerte pattern not found"
    
    except Exception as e:
        return False, f"Error: {e}"

def main():
    print(f"Monitoring BTS tickets at: {URL}")
    print(f"Checking every {CHECK_INTERVAL} seconds...")
    
    while True:
        available, message = check_tickets()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"[{timestamp}] {message}")
        
        if available:
            print("🎫 TICKETS ARE AVAILABLE! Check the website now!")
            play_notification()
            break
        
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
