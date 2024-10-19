#	Make with Love 


import requests
import base64
import json
import os
import time 
from log import Log 
from fake_useragent import UserAgent

#   Read Configs

config_path = "config.json"

with open(config_path, 'r') as json_file:
    config = json.load(json_file)

DevMode = config.get("DevMode")
ScrapeTokenInfos = config.get("ScrapeTokenInfos")
SaveTokenInfos = config.get("SaveTokenInfos")

#   Intialize Logger

log = Log()

#   Gen Headers

class Header:

    def __init__(self):
        user_agent_generator = UserAgent() 
        self.user_agent = user_agent_generator.random  

    def create_headers(self, token):
        x_super_properties_data = {
            "os": "Windows",
            "browser": "Chrome",
            "device": "",
            "system_locale": "en-US", 
            "browser_user_agent": self.user_agent,
            "browser_version": "129.0.0.0",
            "os_version": "10",
            "referrer": "https://www.google.com",  
            "referring_domain": "google.com",  
            "release_channel": "stable",
            "client_build_number": 336973,
            "client_event_source": None
        }

        x_super_properties = base64.b64encode(json.dumps(x_super_properties_data).encode()).decode()

        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9", 
            "authorization": token,
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://www.google.com",  
            "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": self.user_agent, 
            "x-debug-options": "bugReporterEnabled",
            "x-discord-locale": "en-US",
            "x-discord-timezone": "America/New_York",  
            "x-super-properties": x_super_properties
        }

        return headers 
    
#   Main Check Token Func

def check(token, file):

    header = Header()

    headers = header.create_headers(token)

    r = requests.get("https://discord.com/api/v10/users/@me", headers=headers)

    if r.status_code == 200:

        file.write(f"{token}\n")

        r = r.json()

        email = r.get("email")
        phone = r.get("phone")
        verified = r.get("verified")

        if email and phone:
            log.suc(f"Full Verified | Phone: {phone} | Email: {email} | Token: {token[:20]}*****")
        elif email:
            log.suc(f"Email Verified | Email: {email} | Token: {token[:20]}*****")
        elif phone: 
            log.suc(f"Phone Verified | Phone: {phone} | Token: {token[:20]}*****")
        else:
            if verified is False or verified is None:
                log.suc(f"Unclaimed Token | Token: {token[:20]}*****")

        if ScrapeTokenInfos == True: 

            email = r.get("email")
            id = r.get("id")
            username = r.get("username")
            global_name = r.get("global_name")
            premium_type = r.get("premium_type")
            verified = r.get("verified")
            phone = r.get("phone")
            linked_users = r.get("linked_users")
            bio = r.get("bio")
            authenticator_types = r.get("authenticator_types")
            public_flags = r.get("public_flags")
            flags = r.get("flags")   

            log.suc(f"Token Infos Scraped! | Token: {token} | Id: {id} | Global_Name: {global_name} | Username: {username} | Nitro: {premium_type} | Flags : {flags+public_flags}") 

            if SaveTokenInfos == True:
                with open ("tokens_infos.txt","a") as file:
                    file.write(f'''
                               
Global Infos!                               

Token : {token}
Globalname : {global_name}
Username : {username}
ID : {id}

Nitro Infos!

Nitro : {premium_type}

Flags!

Flags : {flags+public_flags}
------------------------------
''')
                    log.suc("Saved Infos in token_infos.txt")



    elif r.status_code == 401:
        log.error(f"Invalid Token | Token: {token[:20]}*****")

    elif r.status_code == 403:
        log.error(f"Access Forbidden | Token: {token[:20]}*****")
    
    else:
        log.fatal(f"Request Error | Response: {r.text} | Status Code: {r.status_code}")

#   Main Start Func!

def main():
    os.system("cls")
    log.inf("Made with Love :)")
    time.sleep(1)
    log.inf("I made this during the time to learn py!")
    time.sleep(1)
    os.system("cls")
    with open('tokens.txt', 'r') as file:
        lines = file.readlines()
        if not lines:
            log.fatal("No Tokens Available in /tokens.txt")
        else:
            with open('valid_tokens.txt', 'a') as valid_file:
                for line in lines:
                    token = line.strip()
                    if token:
                        check(token, valid_file)

main()
input("End of Code")
