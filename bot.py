from aiohttp import (
    ClientResponseError,
    ClientSession,
    ClientTimeout
)
from colorama import *
from datetime import datetime
from fake_useragent import FakeUserAgent
import asyncio, random, json, os, pytz

wib = pytz.timezone('Asia/Jakarta')

class RedactedAirways:
    def __init__(self) -> None:
        self.headers = {
            'Accept': '*/*',
            'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'no-cache',
            'Host': 'quest.redactedairways.',
            'Content-Type': 'application/json',
            'Origin': 'https://quest.redactedairways.com',
            'Pragma': 'no-cache',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': FakeUserAgent().random
        }

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def welcome(self):
        print(
            f"""
        {Fore.GREEN + Style.BRIGHT}Auto Claim {Fore.BLUE + Style.BRIGHT}RedactedAirways Quests - BOT
            """
            f"""
        {Fore.GREEN + Style.BRIGHT}Rey? {Fore.YELLOW + Style.BRIGHT}<INI WATERMARK>
            """
        )

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

    async def user_revalidate(self, token: str):
        url = 'https://quest.redactedairways.com/ecom-gateway/revalidate'
        headers = {
            **self.headers,
            'Authorization': f'Bearer {token}',
            'Content-Length': '0',
            'Referer': 'https://quest.redactedairways.com/login',
        }
        try:
            async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                async with session.post(url=url, headers=headers) as response:
                    response.raise_for_status()
                    result = await response.json()
                    return result["token"]
        except (Exception, ClientResponseError) as e:
            return None
        
    async def revalidate_if_needed(self, token: str, auth_token: str, user_revalidate_func):
        if not auth_token:
            self.log(
                f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} {auth_token} {Style.RESET_ALL}"
                f"{Fore.RED + Style.BRIGHT}Is Expired{Style.RESET_ALL}"
                f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
                f"{Fore.YELLOW + Style.BRIGHT}Revalidating...{Style.RESET_ALL}"
                f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
            )
            return await user_revalidate_func(token)
        return auth_token
        
    async def user_auth(self, auth_token: str):
        url = 'https://quest.redactedairways.com/ecom-gateway/auth'
        headers = {
            **self.headers,
            'Authorization': f'Bearer {auth_token}',
            'Referer': 'https://quest.redactedairways.com/home',
        }
        try:
            async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                async with session.get(url=url, headers=headers) as response:
                    response.raise_for_status()
                    return await response.json()
        except (Exception, ClientResponseError) as e:
            return None
        
    async def user_info(self, auth_token: str):
        url = 'https://quest.redactedairways.com/ecom-gateway/user/info'
        headers = {
            **self.headers,
            'Authorization': f'Bearer {auth_token}',
            'Referer': 'https://quest.redactedairways.com/home',
        }
        try:
            async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                async with session.get(url=url, headers=headers) as response:
                    response.raise_for_status()
                    result = await response.json()
                    return result["userData"]
        except (Exception, ClientResponseError) as e:
            return None
        
    async def task_lists(self, auth_token: str):
        url = 'https://quest.redactedairways.com/ecom-gateway/task/list'
        headers = {
            **self.headers,
            'Authorization': f'Bearer {auth_token}',
            'Referer': 'https://quest.redactedairways.com/home',
        }
        try:
            async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                async with session.get(url=url, headers=headers) as response:
                    response.raise_for_status()
                    result = await response.json()
                    return result["list"]
        except (Exception, ClientResponseError) as e:
            return None
        
    async def task_lists(self, auth_token: str):
        url = 'https://quest.redactedairways.com/ecom-gateway/task/list'
        headers = {
            **self.headers,
            'Authorization': f'Bearer {auth_token}',
            'Referer': 'https://quest.redactedairways.com/home',
        }
        try:
            async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                async with session.get(url=url, headers=headers) as response:
                    response.raise_for_status()
                    result = await response.json()
                    return result["list"]
        except (Exception, ClientResponseError) as e:
            return None
        
    async def complete_tasks(self, auth_token: str, task_id: str, task: dict):
        url = f'https://quest.redactedairways.com/ecom-gateway/task/{task["task_action"]}'
        if "tweet_id" in task and task["tweet_id"]:
            key = "tweetId"
            action_id = task["tweet_id"]
        elif "twitter_id" in task and task["twitter_id"]:
            key = "twitterId"
            action_id = task["twitter_id"]
        else:
            return None

        data = json.dumps({"taskId": task_id, key: action_id})
        headers = {
            **self.headers,
            'Authorization': f'Bearer {auth_token}',
            'Referer': 'https://quest.redactedairways.com/home',
        }
        try:
            async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                async with session.post(url=url, headers=headers, data=data) as response:
                    response.raise_for_status()
                    return await response.json()
        except (Exception, ClientResponseError) as e:
            return None
        
    async def partner_tasks(self, auth_token: str):
        url = 'https://quest.redactedairways.com/ecom-gateway/partners'
        headers = {
            **self.headers,
            'Authorization': f'Bearer {auth_token}',
            'Referer': 'https://quest.redactedairways.com/home',
        }
        try:
            async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                async with session.get(url=url, headers=headers) as response:
                    response.raise_for_status()
                    result = await response.json()
                    return result["data"]
        except (Exception, ClientResponseError) as e:
            return None
        
    async def complete_partner(self, auth_token: str, partner_id: str, task_type: str):
        url = 'https://quest.redactedairways.com/ecom-gateway/partnerActivity'
        data = json.dumps({'partnerId':partner_id, 'taskType':task_type})
        headers = {
            **self.headers,
            'Authorization': f'Bearer {auth_token}',
            'Referer': 'https://quest.redactedairways.com/home',
        }
        try:
            async with ClientSession(timeout=ClientTimeout(total=20)) as session:
                async with session.post(url=url, headers=headers, data=data) as response:
                    response.raise_for_status()
                    return await response.json()
        except (Exception, ClientResponseError) as e:
            return None
        
    async def process_accounts(self, token: str):
        auth_token = await self.user_revalidate(token)
        if not auth_token:
            self.log(
                f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} {token} {Style.RESET_ALL}"
                f"{Fore.RED + Style.BRIGHT}Failed to Login{Style.RESET_ALL}"
                f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
            )
            return
        
        if auth_token:
            auth = await self.user_auth(auth_token)
            user = await self.user_info(auth_token)
            auth_token = await self.revalidate_if_needed(token, auth_token if auth and user else None, self.user_revalidate)

            if auth and user:
                self.log(
                    f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {user['username']} {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}] [ Balance{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {user['overall_score']} Points {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                )

                basic_tasks = await self.task_lists(auth_token)
                auth_token = await self.revalidate_if_needed(token, auth_token if auth and user else None, self.user_revalidate)

                if basic_tasks:
                    completed = False
                    for task in basic_tasks:
                        task_id = task['_id']
                        is_completed = task['completed']

                        if task and not is_completed:
                            if task['task_action'] == 'telegram-auth':
                                self.log(
                                    f"{Fore.MAGENTA + Style.BRIGHT}[ Basic Task{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} {task['task_name']} {Style.RESET_ALL}"
                                    f"{Fore.YELLOW + Style.BRIGHT}Is Skipped{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                                )
                                continue

                            complete = await self.complete_tasks(auth_token, task_id, task)
                            if complete:
                                self.log(
                                    f"{Fore.MAGENTA + Style.BRIGHT}[ Basic Task{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} {task['task_name']} {Style.RESET_ALL}"
                                    f"{Fore.GREEN + Style.BRIGHT}Is Completed{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT} ] [ Reward{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} {complete['points']} Points {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                                )
                            else:
                                self.log(
                                    f"{Fore.MAGENTA + Style.BRIGHT}[ Basic Task{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} {task['task_name']} {Style.RESET_ALL}"
                                    f"{Fore.RED + Style.BRIGHT}Isn't Completed{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                                )
                            await asyncio.sleep(5)

                        else:
                            completed = True

                    if completed:
                        self.log(
                            f"{Fore.MAGENTA + Style.BRIGHT}[ Basic Task{Style.RESET_ALL}"
                            f"{Fore.GREEN + Style.BRIGHT} Is Completed {Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                        )
                    await asyncio.sleep(1)

                partner_tasks = await self.partner_tasks(auth_token)
                auth_token = await self.revalidate_if_needed(token, auth_token if auth and user else None, self.user_revalidate)

                if partner_tasks:
                    completed = False
                    for partner in partner_tasks:
                        partner_id = partner['_id']
                        sub_tasks = partner['tasks']

                        if partner:
                            sub_completed = False
                            for task in sub_tasks:
                                task_type = task['task_type']
                                status = task['status']

                                if task and status == 'incomplete':
                                    complete = await self.complete_partner(auth_token, partner_id, task_type)
                                    if complete:
                                        self.log(
                                            f"{Fore.MAGENTA + Style.BRIGHT}[ Partner Task{Style.RESET_ALL}"
                                            f"{Fore.WHITE + Style.BRIGHT} {partner['partner_name']} {Style.RESET_ALL}"
                                            f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                                            f"{Fore.WHITE + Style.BRIGHT} {task['text']} {Style.RESET_ALL}"
                                            f"{Fore.GREEN + Style.BRIGHT}Is Completed{Style.RESET_ALL}"
                                            f"{Fore.MAGENTA + Style.BRIGHT} ] [ Reward{Style.RESET_ALL}"
                                            f"{Fore.WHITE + Style.BRIGHT} {complete['status']} Points {Style.RESET_ALL}"
                                            f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                                        )
                                    else:
                                        self.log(
                                            f"{Fore.MAGENTA + Style.BRIGHT}[ Partner Task{Style.RESET_ALL}"
                                            f"{Fore.WHITE + Style.BRIGHT} {partner['partner_name']} {Style.RESET_ALL}"
                                            f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                                            f"{Fore.WHITE + Style.BRIGHT} {task['text']} {Style.RESET_ALL}"
                                            f"{Fore.RED + Style.BRIGHT}Isn't Completed{Style.RESET_ALL}"
                                            f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                                        )
                                    await asyncio.sleep(5)

                                else:
                                    sub_completed = True

                            if sub_completed:
                                self.log(
                                    f"{Fore.MAGENTA + Style.BRIGHT}[ Partner Task{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} {partner['partner_name']} {Style.RESET_ALL}"
                                    f"{Fore.GREEN + Style.BRIGHT}Is Completed{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                                )
                            await asyncio.sleep(3)

                        else:
                            completed = True

                    if completed:
                        self.log(
                            f"{Fore.MAGENTA + Style.BRIGHT}[ Partner Task{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} {partner['partner_name']} {Style.RESET_ALL}"
                            f"{Fore.GREEN + Style.BRIGHT}Is Completed{Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
                        )
                
    async def main(self):
        try:
            with open('tokens.txt', 'r') as file:
                tokens = [line.strip() for line in file if line.strip()]

            while True:
                self.clear_terminal()
                self.welcome()
                self.log(
                    f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{len(tokens)}{Style.RESET_ALL}"
                )
                self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"*75)
                
                for token in tokens:
                    token = token.strip()
                    if token:
                        await self.process_accounts(token)
                        self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"*75)
                        seconds = random.randint(15, 30)
                        while seconds > 0:
                            formatted_time = self.format_seconds(seconds)
                            print(
                                f"{Fore.CYAN+Style.BRIGHT}[ Wait for{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {formatted_time} {Style.RESET_ALL}"
                                f"{Fore.CYAN+Style.BRIGHT}... ]{Style.RESET_ALL}",
                                end="\r"
                            )
                            await asyncio.sleep(1)
                            seconds -= 1

                seconds = 28800
                while seconds > 0:
                    formatted_time = self.format_seconds(seconds)
                    print(
                        f"{Fore.CYAN+Style.BRIGHT}[ Wait for{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {formatted_time} {Style.RESET_ALL}"
                        f"{Fore.CYAN+Style.BRIGHT}... ]{Style.RESET_ALL}",
                        end="\r"
                    )
                    await asyncio.sleep(1)
                    seconds -= 1

        except FileNotFoundError:
            self.log(f"{Fore.RED}File 'tokens.txt' tidak ditemukan.{Style.RESET_ALL}")
            return
        except Exception as e:
            self.log(f"{Fore.RED+Style.BRIGHT}Error: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        bot = RedactedAirways()
        asyncio.run(bot.main())
    except KeyboardInterrupt:
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{Fore.RED + Style.BRIGHT}[ EXIT ] RedactedAirways Quests - BOT{Style.RESET_ALL}                                       "                              
        )