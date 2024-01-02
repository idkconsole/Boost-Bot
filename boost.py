import aiohttp
import asyncio
import tasksio
import sys, os
import datetime

async def boost_server(guildid, token):
    headers = {
        "Authorization": token,
        "accept": "*/*",
        "accept-language": "en-US",
        "connection": "keep-alive",
        "cookie": f'__cfduid={os.urandom(43).hex()}; __dcfduid={os.urandom(32).hex()}; locale=en-US',
        "DNT": "1",
        "origin": "https://discord.com",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "referer": "https://discord.com/channels/@me",
        "TE": "Trailers",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9001 Chrome/83.0.4103.122 Electron/9.3.5 Safari/537.36",
        "X-Super-Properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDAxIiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDIiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiY2xpZW50X2J1aWxkX251bWJlciI6ODMwNDAsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9"
    }
    async with aiohttp.ClientSession(headers=headers) as ClientSession:
        async with ClientSession.get(f"https://discord.com/api/v9/users/@me/guilds/premium/subscription-slots") as nvmmm:
            if nvmmm.status == 200:
                idk_var = await nvmmm.json()
                for varr in idk_var:
                    id__ = varr['id']
                    payload = {"user_premium_guild_subscription_slot_ids": [id__]}
                    async with ClientSession.put(f"https://discord.com/api/v9/guilds/{guildid}/premium/subscriptions", json=payload) as boost_req:
                        btxt = await boost_req.text()
                        if "id" in btxt:
                            time = datetime.datetime.now().strftime("%H:%M:%S")
                            print(f"{time} | Successfully Boosted -> {guildid}")
                        else:
                            print(f"{time} | Failed To Boost -> {guildid}: Reason -> {btxt}")

async def start_boost(guild_id, tokens):
    async with tasksio.TaskPool(10_000) as pool:
        for token in tokens:
            await pool.put(boost_server(guild_id, token))

guild_id = sys.argv[1]
tokens_string = sys.argv[2]
tokens = tokens_string.split(',')

asyncio.run(start_boost(guild_id, tokens))
