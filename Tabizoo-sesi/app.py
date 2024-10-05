from colorama import *
from datetime import datetime, timedelta
from fake_useragent import FakeUserAgent
from faker import Faker
from requests import (
    JSONDecodeError,
    RequestException,
    Session
)
from telethon.errors import (
    AuthKeyUnregisteredError,
    UserDeactivatedError,
    UserDeactivatedBanError,
    UnauthorizedError
)
from telethon.functions import messages
from telethon.sync import TelegramClient
from telethon.types import InputBotAppShortName, AppWebViewResultUrl
from urllib.parse import unquote
import asyncio, json, os, sys

class TabiZoo:
    def __init__(self) -> None:
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
        self.api_id = int(config['api_id'])
        self.api_hash = config['api_hash']
        self.faker = Faker()
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Host': 'api.tabibot.com',
            'Origin': 'https://miniapp.tabibot.com',
            'Pragma': 'no-cache',
            'Referer': 'https://miniapp.tabibot.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': FakeUserAgent().random
        }
        self.play_spin_multiplier = 3

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_timestamp(self, message):
        print(
            f"{Fore.BLUE + Style.BRIGHT}[ {datetime.now().astimezone().strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{message}",
            flush=True
        )

    async def generate_query(self, session: str):
        try:
            client = TelegramClient(session=f'sessions/{session}', api_id=self.api_id, api_hash=self.api_hash)
            try:
                await client.connect()
                me = await client.get_me()
                username = me.username if me.username is not None else self.faker.user_name()
            except (AuthKeyUnregisteredError, UnauthorizedError, UserDeactivatedBanError, UserDeactivatedError) as e:
                raise e

            webapp_response: AppWebViewResultUrl = await client(messages.RequestAppWebViewRequest(
                peer='tabizoobot',
                app=InputBotAppShortName(bot_id=await client.get_input_entity('tabizoobot'), short_name='tabizoo'),
                platform='ios',
                write_allowed=True,
                start_param='6094625904'
            ))
            query = unquote(string=webapp_response.url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0])

            await client.disconnect()
            return (query, username)
        except Exception as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {session} Unexpected Error While Generating Query With Telethon: {str(e)} ]{Style.RESET_ALL}")
            await client.disconnect()
            return None

    async def generate_queries(self, sessions):
        tasks = [self.generate_query(session) for session in sessions]
        results = await asyncio.gather(*tasks)
        return [result for result in results if result is not None]

    async def onboarding_task(self, query: str):
        url = 'https://api.tabibot.com/api/task/v1/onboarding'
        headers = {
            **self.headers,
            'rawdata': query
        }
        try:
            with Session().post(url=url, headers=headers) as response:
                response.raise_for_status()
                return True
        except (Exception, JSONDecodeError, RequestException):
            return False

    async def profile_user(self, query: str):
        url = 'https://api.tabibot.com/api/user/v1/profile'
        headers = {
            **self.headers,
            'rawdata': query
        }
        try:
            with Session().get(url=url, headers=headers) as response:
                response.raise_for_status()
                profile_user = response.json()
                if profile_user['code'] == 200 and profile_user['message'] == 'success':
                    return profile_user['data']['user']
                return None
        except RequestException as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Fetching Profile: {str(e)} ]{Style.RESET_ALL}")
            return None
        except (Exception, JSONDecodeError) as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Fetching Profile: {str(e)} ]{Style.RESET_ALL}")
            return None

    async def check_in_user(self, query: str):
        url = 'https://api.tabibot.com/api/user/v1/check-in'
        headers = {
            **self.headers,
            'Content-Length': '0',
            'rawdata': query
        }
        try:
            with Session().post(url=url, headers=headers) as response:
                response.raise_for_status()
                check_in_user = response.json()
                if check_in_user['code'] == 200 and check_in_user['message'] == 'success':
                    if check_in_user['data']['check_in_status'] == 1:
                        return self.print_timestamp(f"{Fore.GREEN + Style.BRIGHT}[ You\'ve Got {check_in_user['data']['check_in_reward']} From Check In ]{Style.RESET_ALL}")
                    elif check_in_user['data']['check_in_status'] == 2:
                        return self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ Check In Already Claimed ]{Style.RESET_ALL}")
        except RequestException as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Fetching Profile: {str(e)} ]{Style.RESET_ALL}")
        except (Exception, JSONDecodeError) as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Fetching Profile: {str(e)} ]{Style.RESET_ALL}")

    async def level_up_user(self, query: str):
        url = 'https://api.tabibot.com/api/user/v1/level-up'
        headers = {
            **self.headers,
            'Content-Length': '0',
            'rawdata': query
        }
        while True:
            try:
                with Session().post(url=url, headers=headers) as response:
                    response.raise_for_status()
                    level_up_user = response.json()
                    if level_up_user['code'] == 200 and level_up_user['message'] == 'success':
                        self.print_timestamp(f"{Fore.GREEN + Style.BRIGHT}[ Successfully Upgrade Level {level_up_user['data']['user']['level']} ]{Style.RESET_ALL}")
                    elif level_up_user['code'] == 400 or level_up_user['message'] == 'coin not enough':
                        return self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ Not Enough Coin To Upgrade Level ]{Style.RESET_ALL}")
                    else:
                        return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Error While Level Up User: {level_up_user['message']} ]{Style.RESET_ALL}")
            except RequestException as e:
                return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Level Up User: {str(e)} ]{Style.RESET_ALL}")
            except (Exception, JSONDecodeError) as e:
                return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Level Up User: {str(e)} ]{Style.RESET_ALL}")

    async def info_mining(self, query: str):
        url = 'https://api.tabibot.com/api/mining/v1/info'
        headers = {
            **self.headers,
            'rawdata': query
        }
        try:
            with Session().get(url=url, headers=headers) as response:
                response.raise_for_status()
                info_mining = response.json()
                if info_mining['code'] == 200 and info_mining['message'] == 'success':
                    return info_mining['data']['mining_data']
                return None
        except RequestException as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Fetching Info Mining: {str(e)} ]{Style.RESET_ALL}")
            return None
        except (Exception, JSONDecodeError) as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Fetching Info Mining: {str(e)} ]{Style.RESET_ALL}")
            return None

    async def claim_mining(self, query: str, mining_coins: int):
        url = 'https://api.tabibot.com/api/mining/v1/claim'
        headers = {
            **self.headers,
            'Content-Length': '0',
            'rawdata': query
        }
        try:
            with Session().post(url=url, headers=headers) as response:
                response.raise_for_status()
                claim_mining = response.json()
                if claim_mining['code'] == 200 and claim_mining['message'] == 'success':
                    if claim_mining['data']:
                        self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ You\'ve Got {mining_coins} From Mining ]{Style.RESET_ALL}")
                        info_mining = await self.info_mining(query=query)
                        if info_mining is not None:
                            self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ Mining Can Be Claim At {datetime.fromisoformat(info_mining['next_claim_time'].replace('Z', '+00:00')).astimezone().strftime('%x %X %Z')} ]{Style.RESET_ALL}")
        except RequestException as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Claim Mining: {str(e)} ]{Style.RESET_ALL}")
        except (Exception, JSONDecodeError) as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Claim Mining: {str(e)} ]{Style.RESET_ALL}")

    async def info_spin(self, query: str):
        url = 'https://api.tabibot.com/api/spin/v1/info'
        headers = {
            **self.headers,
            'Content-Length': '0',
            'rawdata': query
        }
        try:
            with Session().post(url=url, headers=headers) as response:
                response.raise_for_status()
                info_spin = response.json()
                if info_spin['code'] == 200 and info_spin['message'] == 'success':
                    self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Your Energy {info_spin['data']['energy']['energy']} ]{Style.RESET_ALL}")
                    await self.play_spin(query=query, multiplier=self.play_spin_multiplier)
        except RequestException as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Fetching Info Spin: {str(e)} ]{Style.RESET_ALL}")
        except (Exception, JSONDecodeError) as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Fetching Info Spin: {str(e)} ]{Style.RESET_ALL}")

    async def play_spin(self, query: str, multiplier: int):
        url = 'https://api.tabibot.com/api/spin/v1/play'
        data = json.dumps({'multiplier':multiplier})
        headers = {
            **self.headers,
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json',
            'rawdata': query
        }
        while True:
            try:
                with Session().post(url=url, headers=headers, data=data) as response:
                    response.raise_for_status()
                    play_spin = response.json()
                    if play_spin['code'] == 200 and play_spin['message'] == 'success':
                        self.print_timestamp(f"{Fore.GREEN + Style.BRIGHT}[ You\'ve Got {play_spin['data']['prize']['amount'] * play_spin['data']['prize']['multiplier']} {play_spin['data']['prize']['prize_type']} From Spin ]{Style.RESET_ALL}")
                    elif play_spin['code'] == 400 and play_spin['message'] == 'not enough energy':
                        return self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ Not Enough Energy To Play Spin ]{Style.RESET_ALL}")
                    else:
                        return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Error While Play Spin: {play_spin['message']} ]{Style.RESET_ALL}")
            except RequestException as e:
                return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Play Spin: {str(e)} ]{Style.RESET_ALL}")
            except (Exception, JSONDecodeError) as e:
                return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Play Spin: {str(e)} ]{Style.RESET_ALL}")

    async def sign_in_user(self, query: str):
        url = 'https://api.tabibot.com/api/user/v1/sign-in'
        data = json.dumps({'referral':6094625904})
        headers = {
            **self.headers,
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json',
            'rawdata': query
        }
        try:
            with Session().post(url=url, headers=headers, data=data) as response:
                response.raise_for_status()
                return True
        except (Exception, JSONDecodeError, RequestException):
            return False

    async def mine_project_task(self, query: str):
        url = 'https://api.tabibot.com/api/task/v1/project/mine'
        headers = {
            **self.headers,
            'rawdata': query
        }
        try:
            with Session().get(url=url, headers=headers) as response:
                response.raise_for_status()
                data = response.json()
                if data['code'] == 200 and data['message'] == 'success':
                    for project in data['data']:
                        await self.mine_task(query=query, project_tag=project['project_tag'])
                        await self.project_verify_task(query=query, project_tag=project['project_tag'], project_name=project['project_name'], project_reward=project['reward'])
        except RequestException as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Fetching Mine Project Task: {str(e)} ]{Style.RESET_ALL}")
            return None
        except (Exception, JSONDecodeError) as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Fetching Mine Project : {str(e)} ]{Style.RESET_ALL}")
            return None

    async def mine_task(self, query: str, project_tag: str):
        url = f'https://api.tabibot.com/api/task/v1/mine?project_tag={project_tag}'
        headers = {
            **self.headers,
            'rawdata': query
        }
        try:
            with Session().get(url=url, headers=headers) as response:
                response.raise_for_status()
                data = response.json()
                if data['code'] == 200 and data['message'] == 'success':
                    for task in data['data']['list']:
                        await self.go_report_task(query=query, task_tag=task['task_tag'], task_name=task['task_name'], task_reward=task['reward'])
        except RequestException as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Fetching Mine Task: {str(e)} ]{Style.RESET_ALL}")
            return None
        except (Exception, JSONDecodeError) as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Fetching Mine Task: {str(e)} ]{Style.RESET_ALL}")
            return None

    async def list_task(self, query: str):
        url = 'https://api.tabibot.com/api/task/v1/list'
        headers = {
            **self.headers,
            'rawdata': query
        }
        try:
            with Session().get(url=url, headers=headers) as response:
                response.raise_for_status()
                data = response.json()
                if data['code'] == 200 and data['message'] == 'success':
                    for task_list in data['data']:
                        if task_list['project_tag'] not in ['task_special', 'task_daily_reward']:
                            for task in task_list['task_list']:
                                await self.go_report_task(query=query, task_tag=task['task_tag'], task_name=task['task_name'], task_reward=task['reward'])
        except RequestException as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Fetching Task: {str(e)} ]{Style.RESET_ALL}")
            return None
        except (Exception, JSONDecodeError) as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Fetching Task: {str(e)} ]{Style.RESET_ALL}")
            return None

    async def go_report_task(self, query: str, task_tag: str, task_name: str, task_reward: int):
        url = 'https://api.tabibot.com/api/task/v1/report/go'
        data = json.dumps({'task_tag':task_tag})
        headers = {
            **self.headers,
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json',
            'rawdata': query
        }
        try:
            with Session().post(url=url, headers=headers, data=data) as response:
                response.raise_for_status()
                await self.task_verify_task(query=query, task_tag=task_tag, task_name=task_name, task_reward=task_reward)
        except RequestException as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Go Report Task: {str(e)} ]{Style.RESET_ALL}")
        except (Exception, JSONDecodeError) as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Go Report Task: {str(e)} ]{Style.RESET_ALL}")

    async def task_verify_task(self, query: str, task_tag: str, task_name: str, task_reward: int):
        url = 'https://api.tabibot.com/api/task/v1/verify/task'
        data = json.dumps({'task_tag':task_tag})
        headers = {
            **self.headers,
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json',
            'rawdata': query
        }
        try:
            with Session().post(url=url, headers=headers, data=data) as response:
                response.raise_for_status()
                task_verify_task = response.json()
                if task_verify_task['code'] == 200 and task_verify_task['message'] == 'success':
                    if task_verify_task['data']['verify'] and task_verify_task['data']['status'] == 1:
                        return self.print_timestamp(f"{Fore.GREEN + Style.BRIGHT}[ You\'ve Got {task_reward} From {task_name} ]{Style.RESET_ALL}")
                elif task_verify_task['code'] == 200 and task_verify_task['message'] == 'Task Not Completed':
                    return self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ {task_name} Isn\'t Completed ]{Style.RESET_ALL}")
        except RequestException as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Task Verify Task: {str(e)} ]{Style.RESET_ALL}")
        except (Exception, JSONDecodeError) as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Task Verify Task: {str(e)} ]{Style.RESET_ALL}")

    async def project_verify_task(self, query: str, project_tag: str, project_name: str, project_reward: int):
        url = 'https://api.tabibot.com/api/task/v1/verify/project'
        data = json.dumps({'project_tag':project_tag})
        headers = {
            **self.headers,
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json',
            'rawdata': query
        }
        try:
            with Session().post(url=url, headers=headers, data=data) as response:
                response.raise_for_status()
                task_verify_task = response.json()
                if task_verify_task['code'] == 200 and task_verify_task['message'] == 'success':
                    if task_verify_task['data']['verify'] and task_verify_task['data']['status'] == 1:
                        return self.print_timestamp(f"{Fore.GREEN + Style.BRIGHT}[ You\'ve Got {project_reward} From {project_name} ]{Style.RESET_ALL}")
                elif task_verify_task['code'] == 200 and task_verify_task['message'] == 'Task Not Completed':
                    return self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ {project_name} Isn\'t Completed ]{Style.RESET_ALL}")
        except RequestException as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Project Verify Task: {str(e)} ]{Style.RESET_ALL}")
        except (Exception, JSONDecodeError) as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Project Verify Task: {str(e)} ]{Style.RESET_ALL}")

    async def main(self):
        while True:
            try:
                sessions = [file.replace('.session', '') for file in os.listdir('sessions/') if file.endswith('.session')]
                if not sessions:
                    return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ No Session Files Found In The Folder! Please Make Sure There Are '*.session' Files In The Folder. ]{Style.RESET_ALL}")
                accounts = await self.generate_queries(sessions)
                total_balance = 0
                restart_times = []

                for (query, username) in accounts:
                    self.print_timestamp(
                        f"{Fore.WHITE + Style.BRIGHT}[ Shiro ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.CYAN + Style.BRIGHT}[ {username} ]{Style.RESET_ALL}"
                    )
                    await self.sign_in_user(query=query)
                    await self.onboarding_task(query=query)
                    profile = await self.profile_user(query=query)
                    if profile is not None:
                        self.print_timestamp(
                            f"{Fore.GREEN + Style.BRIGHT}[ Level {profile['level']} ]{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                            f"{Fore.BLUE + Style.BRIGHT}[ Ton Balance {profile['coins']} ]{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                            f"{Fore.YELLOW + Style.BRIGHT}[ Streak {profile['streak']} ]{Style.RESET_ALL}"
                        )
                        self.print_timestamp(
                            f"{Fore.GREEN + Style.BRIGHT}[ Coins {profile['coins']} ]{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                            f"{Fore.BLUE + Style.BRIGHT}[ Zoo Coins {profile['zoo_coins']} ]{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                            f"{Fore.YELLOW + Style.BRIGHT}[ Crystal Coins {profile['crystal_coins']} ]{Style.RESET_ALL}"
                        )
                    info_mining = await self.info_mining(query=query)
                    if info_mining is not None:
                        if info_mining['current'] == info_mining['top_limit'] or datetime.now().astimezone().timestamp() >= datetime.fromisoformat(info_mining['next_claim_time'].replace('Z', '+00:00')).astimezone().timestamp():
                            await self.claim_mining(query=query, mining_coins=info_mining['current'])
                        else:
                            restart_times.append(datetime.fromisoformat(info_mining['next_claim_time'].replace('Z', '+00:00')).astimezone().timestamp())
                            self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ Mining Can Be Claim At {datetime.fromisoformat(info_mining['next_claim_time'].replace('Z', '+00:00')).astimezone().strftime('%x %X %Z')} ]{Style.RESET_ALL}")

                for (query, username) in accounts:
                    self.print_timestamp(
                        f"{Fore.WHITE + Style.BRIGHT}[ Spin ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.CYAN + Style.BRIGHT}[ {username} ]{Style.RESET_ALL}"
                    )
                    await self.info_spin(query=query)

                for (query, username) in accounts:
                    self.print_timestamp(
                        f"{Fore.WHITE + Style.BRIGHT}[ Task & Mine ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.CYAN + Style.BRIGHT}[ {username} ]{Style.RESET_ALL}"
                    )
                    await self.list_task(query=query)
                    await self.mine_project_task(query=query)

                for (query, username) in accounts:
                    self.print_timestamp(
                        f"{Fore.WHITE + Style.BRIGHT}[ Level Up ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.CYAN + Style.BRIGHT}[ {username} ]{Style.RESET_ALL}"
                    )
                    await self.level_up_user(query=query)
                    profile = await self.profile_user(query=query)
                    total_balance += profile['coins'] if profile else 0

                if restart_times:
                    wait_times = [mining - datetime.now().astimezone().timestamp() for mining in restart_times if mining > datetime.now().astimezone().timestamp()]
                    if wait_times:
                        sleep_time = min(wait_times)
                    else:
                        sleep_time = 15 * 60
                else:
                    sleep_time = 15 * 60

                self.print_timestamp(
                    f"{Fore.CYAN + Style.BRIGHT}[ Total Account {len(accounts)} ]{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                    f"{Fore.GREEN + Style.BRIGHT}[ Total Coins {total_balance} ]{Style.RESET_ALL}"
                )
                self.print_timestamp(f"{Fore.CYAN + Style.BRIGHT}[ Restarting At {(datetime.now().astimezone() + timedelta(seconds=sleep_time)).strftime('%x %X %Z')} ]{Style.RESET_ALL}")

                await asyncio.sleep(sleep_time)
                self.clear_terminal()
            except Exception as e:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {str(e)} ]{Style.RESET_ALL}")
                continue

if __name__ == '__main__':
    try:
        init(autoreset=True)
        tabizoo = TabiZoo()
        asyncio.run(tabizoo.main())
    except (ValueError, IndexError, FileNotFoundError) as e:
        tabizoo.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {str(e)} ]{Style.RESET_ALL}")
    except KeyboardInterrupt:
        sys.exit(0)