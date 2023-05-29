import os
import sys
W = '\033[0m'   # White
L = '\033[90m'  # Grey

try:
    import time
    import requests
    import datetime
    from concurrent.futures import ThreadPoolExecutor
except ModuleNotFoundError:
    os.system("""
    pip install time
    pip install requests
    pip install datetime
    pip install concurrent
    """)

class console:
    def get_info():
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        return current_time

    def info(content: str):
        print(
                f" {W}[{L}{console.get_info()}{W}] " + content)

class main:
    os.system('cls' if os.name == 'nt' else 'clear')
    def __init__(self):
        sessions = requests.Session()

        with open("tokens.txt", "r") as file:
            tokens = file.read().strip().splitlines()

        if len(tokens) <= 1:
           console.info("No tokens in tokens.txt, please input you tokens.")
           time.sleep(2)
           sys.exit()

        self.message = input(" Message: ")
        self.title = input(" Title: ")
        self.channel = int(input(" Forum ID: "))
        self.aumunt = int(input(" Aumunt: "))
        self.threads = int(input(" Threads (1-10):"))
        
        if self.threads > 10:
            console.info("The maximum of threads is 10, try again")
            time.sleep(3)
            main()

        self.headers = {
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US",
            "referer": "https://discord.com/channels/@me",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9011 Chrome/91.0.4472.164 Electron/13.6.6 Safari/537.36",
            "x-debug-options": "bugReporterEnabled",
            "x-discord-locale": "en-US",
            "x-super-properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDExIiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDUiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTc5ODgyLCJuYXRpdmVfYnVpbGRfbnVtYmVyIjozMDMwNiwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbCwiZGVzaWduX2lkIjowfQ=="
        }

        def make_post(token, self):
            try:
                data = {
                    "name": self.title,
                    "auto_archive_duration": 60,
                    "message": {
                        "content": self.message
                    }
                }
                for i in range(self.aumunt):
                    self.session = sessions.post(f"https://discord.com/api/v9/channels/{self.channel}/threads?use_nested_fields=true", headers=self.headers, json=data)

                    if self.session.status_code == 201:
                        data1 = {
                            "content": self.message,
                            "tts": False
                        }
                        self.session1 = sessions.post(f"https://discord.com/api/v9/channels/{self.session.json()['id']}/messages", headers=self.headers, json=data1)

                        if self.session1.status_code == 200:
                            console.info(f"Sent post, Channel ID: {self.channel}")

                        else:
                            console.info("Failed to send post")

                    else:
                        console.info("Failed to send post")

            except Exception as e:
                console.info(str(e))

        executor = ThreadPoolExecutor(max_workers=int(self.threads))
        for token in tokens:
            self.headers.update({"authorization": token})
            executor.submit(make_post, token, self)

if __name__ == "__main__":
    main()

