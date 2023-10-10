import tls_client, threading, os, requests
from base64 import b64encode
import json, time

__useragent__ = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
build_number = 165486
cv = "108.0.0.0"
__properties__ = b64encode(
  json.dumps(
    {
      "os": "Windows",
      "browser": "Chrome",
      "device": "PC",
      "system_locale": "en-GB",
      "browser_user_agent": __useragent__,
      "browser_version": cv,
      "os_version": "10",
      "referrer": "https://discord.com/channels/@me",
      "referring_domain": "discord.com",
      "referrer_current": "",
      "referring_domain_current": "",
      "release_channel": "stable",
      "client_build_number": build_number,
      "client_event_source": None
    },
    separators=(',', ':')).encode()).decode()

def get_headers(token):
  headers = {
    "Authorization": token,
    "Origin": "https://canary.discord.com",
    "Accept": "*/*",
    "X-Discord-Locale": "en-GB",
    "X-Super-Properties": __properties__,
    "User-Agent": __useragent__,
    "Referer": "https://canary.discord.com/channels/@me",
    "X-Debug-Options": "bugReporterEnabled",
    "Content-Type": "application/json"
  }
  return headers

os.system("cls" if os.name == "nt" else "clear")
tkn = ""
secret = ""
client_id =""
redirect = "http://localhost:8080" #dont change this
API_ENDPOINT = 'https://canary.discord.com/api/v9'
auth = f"https://canary.discord.com/api/oauth2/authorize?client_id={client_id}&redirect_uri={redirect}&response_type=code&scope=identify%20guilds.join"
guild = input("[!] Guild ID: ")
nickname = input("[!] Nickname: ")

def exchange_code(code):
  data = {
    'client_id': client_id,
    'client_secret': secret,
    'grant_type': 'authorization_code',
    'code': code,
    'redirect_uri': redirect
  }
  headers = {'Content-Type': 'application/x-www-form-urlencoded'}
  r = requests.post(str(API_ENDPOINT) + '/oauth2/token', data=data, headers=headers)
  print(r.text)
  if r.status_code in (200, 201, 204):
    return r.json()
  else:
    return False

def add_to_guild(access_token, userID):
  url = f"{API_ENDPOINT}/guilds/{guild}/members/{userID}"

  botToken = tkn
  data = {
    "access_token": access_token,
  }
  headers = {
    "Authorization": f"Bot {botToken}",
    'Content-Type': 'application/json'
  }
  r = requests.put(url=url, headers=headers, json=data)
  return r.status_code

def rename(tk):
    headers = get_headers(tk)
    client = tls_client.Session(client_identifier="firefox_102")
    client.headers.update(headers)
    r = client.patch(f"https://canary.discord.com/api/v9/guilds/{guild}/members/@me", json={"nick": nickname})
    if r.status_code in (200, 201, 204):
        print("[+] Nickname Changed to %s" % (nickname))
        return "ok"
    else:
        print("[-] Failed to Change Nickname")
        return "error"

def authorizer(tk):
    headers = get_headers(tk)
    r = requests.post(auth, headers=headers, json={"authorize": "true"})
    print(r.text)
    if r.status_code in (200, 201, 204):
        location = r.json()['location']
        code = location.replace("http://localhost:8080?code=", "")
        exchange = exchange_code(code)
        print("[+] Authorized Token")
        access_token = exchange['access_token']
        userid = get_user(access_token)
        add_to_guild(access_token, userid)
        print("[+] Added to Guild %s" % (guild))
        if not nickname == "":
          threading.Thread(target=rename, args=(tk,)).start()
        return "ok"

def get_user(access: str):
  endp = "https://canary.discord.com/api/v9/users/@me"
  r = requests.get(endp, headers={"Authorization": f"Bearer {access}"})
  rjson = r.json()
  return rjson['id']

def main(tk):
    authorizer(tk)
    headers = get_headers(tk)
    client = tls_client.Session(client_identifier="firefox_102")
    client.headers.update(headers)
    r = client.get(f"https://canary.discord.com/api/v9/users/@me/guilds/premium/subscription-slots")
    idk = r.json()
    for x in idk:
        id_ = x['id']
        payload = {"user_premium_guild_subscription_slot_ids": [id_]}
        r = client.put(f"https://canary.discord.com/api/v9/guilds/{guild}/premium/subscriptions", json=payload)
        if r.status_code in (200, 201, 204):
            print("[+] Boosted %s" % (guild))

f = open("tokens.txt", "r").readlines()
os.system("cls" if os.name == "nt" else "clear")
for tk in f:
    tk = tk.strip()
    tk = tk.split(":")[2]
    threading.Thread(target=main, args=(tk,)).start()
