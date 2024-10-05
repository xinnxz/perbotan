import aiohttp
import asyncio
import json
import os
from colorama import *
from datetime import datetime
import pytz

wib = pytz.timezone('Asia/Jakarta')


class Cats:
    def __init__(self) -> None:
        self.headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Origin': 'https://cats-frontend.tgapps.store',
            'Priority': 'u=1, i',
            'Referer': 'https://cats-frontend.tgapps.store/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'
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
        {Fore.GREEN + Style.BRIGHT}Auto Claim {Fore.BLUE + Style.BRIGHT}Cats - BOT
            """
            f"""
        {Fore.GREEN + Style.BRIGHT}Rey? {Fore.YELLOW + Style.BRIGHT}<INI WATERMARK>
            """
        )

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

    async def user(self, query: str):
        url = 'https://api.catshouse.club/user'
        headers = self.headers.copy()
        headers.update({
            'Authorization': f'tma {query}',
            'Content-Type': 'application/json'
        })

        for attempt in range(5):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, headers=headers) as response:
                        result = await response.json()
                        if response.status == 200:
                            return result
                        else:
                            return None
            except (aiohttp.ClientError, aiohttp.ContentTypeError) as e:
                print(
                    f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}[{Style.RESET_ALL}"
                    f"{Fore.RED + Style.BRIGHT} Gagal terhubung ke server {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT} Mencoba Ulang... {attempt + 1}/{5} {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}] : {e}{Style.RESET_ALL}",
                    end="\r",
                    flush=True
                )
                await asyncio.sleep(3)
        self.log(f"{Fore.RED+Style.BRIGHT}Semua percobaan gagal. Token mungkin sudah mati atau ada masalah koneksi.{Style.RESET_ALL}")
        return None

    async def get_tasks(self, query: str):
        url = 'https://api.catshouse.club/tasks/user?group=cats'
        headers = self.headers.copy()
        headers.update({
            'Authorization': f'tma {query}',
            'Content-Type': 'application/json'
        })

        for attempt in range(5):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, headers=headers) as response:
                        result = await response.json()
                        if response.status == 200:
                            return result['tasks']
                        else:
                            return None
            except (aiohttp.ClientError, aiohttp.ContentTypeError) as e:
                print(
                    f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}[{Style.RESET_ALL}"
                    f"{Fore.RED + Style.BRIGHT} Gagal terhubung ke server {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT} Mencoba Ulang... {attempt + 1}/{5} {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}] : {e}{Style.RESET_ALL}",
                    end="\r",
                    flush=True
                )
                await asyncio.sleep(3)
        self.log(f"{Fore.RED+Style.BRIGHT}Semua percobaan gagal. Token mungkin sudah mati atau ada masalah koneksi.{Style.RESET_ALL}")
        return None

    async def complete_tasks(self, query: str, task_id: str):
        url = f'https://api.catshouse.club/tasks/{task_id}/complete'
        data = json.dumps({})
        headers = self.headers.copy()
        headers.update({
            'Authorization': f'tma {query}',
            'Content-Type': 'application/json'
        })

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, data=data) as response:
                    result = await response.json()
                    if response.status == 200:
                        return result
                    else:
                        return None
        except (aiohttp.ClientError, aiohttp.ContentTypeError) as e:
            self.log(f"{Fore.YELLOW+Style.BRIGHT}[ Terputus dari server ] : {e}{Style.RESET_ALL}")

    async def process_query(self, query: str):
        try:
            user = await self.user(query)
            if user:
                self.log(
                    f"{Fore.MAGENTA+Style.BRIGHT}[ Nama{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {user['firstName']} {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} | {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}[ Balance{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {user['totalRewards']} {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}CATS ]{Style.RESET_ALL}                                   "
                )
            else:
                self.log(f"{Fore.YELLOW+Style.BRIGHT}[ User Info not Found ]{Style.RESET_ALL}")

            print(f"{Fore.YELLOW + Style.BRIGHT}[ Getting Tasks........ ]{Style.RESET_ALL}", end="\r", flush=True)
            await asyncio.sleep(3)
            tasks = await self.get_tasks(query)
            if tasks:
                manual_task = False

                for task in tasks:
                    task_id = task['id']

                    if not task['allowCheck'] and not task['completed'] and task['progress'] is None:
                        print(
                            f"{Fore.YELLOW + Style.BRIGHT}[ Starting Task........ ]{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT}[{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} {task['title']} {Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}",
                            end="\r",
                            flush=True
                        )
                        await asyncio.sleep(3)
                        complete_tasks = await self.complete_tasks(query, task_id)
                        if complete_tasks and complete_tasks['success']:
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}[ Task{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {task['title']} {Style.RESET_ALL}"
                                f"{Fore.GREEN+Style.BRIGHT}Sukses {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} | {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}[ Reward{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {task['rewardPoints']} {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}CATS ]{Style.RESET_ALL}"
                            )
                        else:
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}[Task{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {task['title']} {Style.RESET_ALL}"
                                f"{Fore.RED+Style.BRIGHT}Gagal {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                            )
                    else:
                        manual_task = True

                if manual_task:
                    self.log(f"{Fore.YELLOW+Style.BRIGHT}[ Tersisa Manual Task ]{Style.RESET_ALL}")
            else:
                self.log(f"{Fore.YELLOW+Style.BRIGHT}[ Gagal Mendapatkan List Task ]{Style.RESET_ALL}")

        except (aiohttp.ClientError, aiohttp.ContentTypeError) as e:
            self.log(f"{Fore.RED+Style.BRIGHT}Error: {e}")
            return None

    async def main(self):
        try:
            with open('query.txt', 'r') as file:
                content = file.read()
                queries = [query.strip() for query in content.splitlines() if query.strip()]

            while True:
                self.clear_terminal()
                self.welcome()
                self.log(
                    f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{len(queries)}{Style.RESET_ALL}"
                )
                self.log(f"{Fore.CYAN + Style.BRIGHT}---------------------------------------------------{Style.RESET_ALL}")

                for query in queries:
                    print(f"{Fore.YELLOW + Style.BRIGHT}[ Getting User Token... ]{Style.RESET_ALL}", end="\r", flush=True)
                    await asyncio.sleep(5)
                    await self.process_query(query)
                    self.log(f"{Fore.CYAN + Style.BRIGHT}---------------------------------------------------{Style.RESET_ALL}")

                seconds = 3
                while seconds > 0:
                    formatted_time = self.format_seconds(seconds)
                    print(
                        f"{Fore.CYAN+Style.BRIGHT}[ Wait for{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {formatted_time} {Style.RESET_ALL}"
                        f"{Fore.CYAN+Style.BRIGHT}... ]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    await asyncio.sleep(1)
                    seconds -= 1

        except FileNotFoundError:
            print(f"{Fore.RED}File 'query.txt' tidak ditemukan.{Style.RESET_ALL}")
            return
        except Exception as e:
            self.log(f"{Fore.RED+Style.BRIGHT}Error: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        cat_bot = Cats()
        asyncio.run(cat_bot.main())
    except KeyboardInterrupt:
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{Fore.RED + Style.BRIGHT}[ EXIT ] Cats - BOT{Style.RESET_ALL}",                                       
        )