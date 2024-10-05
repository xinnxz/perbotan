from colorama import *
from datetime import UTC, datetime, timedelta
from fake_useragent import FakeUserAgent
from faker import Faker
from telethon.errors import (
    AuthKeyUnregisteredError,
    UserDeactivatedError,
    UserDeactivatedBanError,
    UnauthorizedError
)
from telethon.functions import messages
from telethon.sync import TelegramClient
from telethon.types import AppWebViewResultUrl
from requests import (
    JSONDecodeError,
    RequestException,
    Session
)
from urllib.parse import parse_qs, unquote
import asyncio
import json
import os
import sys

class Timefarm:
    def __init__(self) -> None:
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
        self.api_id = int(config['api_id'])
        self.api_hash = config['api_hash']
        self.faker = Faker()
        self.headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Host': 'tg-bot-tap.laborx.io',
            'Origin': 'https://timefarm.app',
            'Pragma': 'no-cache',
            'Referer': 'https://timefarm.app/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': FakeUserAgent().random
        }

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
            except (AuthKeyUnregisteredError, UnauthorizedError, UserDeactivatedError, UserDeactivatedBanError) as e:
                raise e

            webapp_response: AppWebViewResultUrl = await client(messages.RequestWebViewRequest(
                peer='TimeFarmCryptoBot',
                bot=await client.get_input_entity('TimeFarmCryptoBot'),
                platform='ios',
                url='https://tg-bot-tap.laborx.io/'
            ))
            query = unquote(string=webapp_response.url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0])

            await client.disconnect()
            return query
        except Exception as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {session} Unexpected Error While Generating Query With Telethon: {str(e)} ]{Style.RESET_ALL}")
            await client.disconnect()
            return None

    async def generate_queries(self, sessions):
        tasks = [self.generate_query(session) for session in sessions]
        results = await asyncio.gather(*tasks)
        return [result for result in results if result is not None]

    async def generate_token(self, query: str):
        url = 'https://tg-bot-tap.laborx.io/api/v1/auth/validate-init/v2'
        payload = {'initData':query,'platform':'ios'}
        headers = {
            **self.headers,
            'Content-Length': str(len(payload)),
            'Content-Type': 'application/json'
        }
        try:
            with Session().post(url=url, headers=headers, json=payload) as response:
                response.raise_for_status()
                parsed_query = parse_qs(query)
                user_data_json = parsed_query['user'][0]
                user_data = json.loads(user_data_json)
                username = user_data['username'] if user_data else self.faker.user_name()
                return (response.json(), username)
        except (Exception, JSONDecodeError, RequestException):
            return None

    async def generate_tokens(self, queries):
        tasks = [self.generate_token(query) for query in queries]
        results = await asyncio.gather(*tasks)
        return [result for result in results if result is not None]

    async def complete_onboarding_me(self, token: str):
        url = 'https://tg-bot-tap.laborx.io/api/v1/me/onboarding/complete'
        payload = {}
        headers = {
            **self.headers,
            'Authorization': f"Bearer {token}",
            'Content-Length': str(len(payload)),
            'Content-Type': 'application/json'
        }
        try:
            with Session().post(url=url, headers=headers, json=payload) as response:
                response.raise_for_status()
                return True
        except (Exception, JSONDecodeError, RequestException):
            return False

    async def info_farming(self, token: str):
        url = 'https://tg-bot-tap.laborx.io/api/v1/farming/info'
        headers = {
            **self.headers,
            'Authorization': f"Bearer {token}"
        }
        try:
            with Session().get(url=url, headers=headers) as response:
                response.raise_for_status()
                return response.json()
        except RequestException as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Fetching Info Farming: {str(e)} ]{Style.RESET_ALL}")
            return None
        except (Exception, JSONDecodeError) as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Fetching Info Farming: {str(e)} ]{Style.RESET_ALL}")
            return None

    async def start_farming(self, token: str):
        url = 'https://tg-bot-tap.laborx.io/api/v1/farming/start'
        payload = {}
        headers = {
            **self.headers,
            'Authorization': f"Bearer {token}",
            'Content-Length': str(len(payload)),
            'Content-Type': 'application/json'
        }
        try:
            with Session().post(url=url, headers=headers, json=payload) as response:
                response.raise_for_status()
                start_farming = response.json()
                return self.print_timestamp(f"{Fore.GREEN + Style.BRIGHT}[ Farming Started And Can Be Claim At {(datetime.strptime(start_farming['activeFarmingStartedAt'], '%Y-%m-%dT%H:%M:%S.%fZ') + timedelta(seconds=start_farming['farmingDurationInSec'])).astimezone().strftime('%x %X %Z')} ]{Style.RESET_ALL}")
        except RequestException as e:
            if e.response.status_code == 403:
                error_start_farming = e.response.json()
                if error_start_farming['error']['message'] == 'Farming already started':
                    return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Farming Already Started ]{Style.RESET_ALL}")
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Start Farming: {str(e)} ]{Style.RESET_ALL}")
        except (Exception, JSONDecodeError) as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Start Farming: {str(e)} ]{Style.RESET_ALL}")

    async def finish_farming(self, token: str, farming_reward: int):
        url = 'https://tg-bot-tap.laborx.io/api/v1/farming/finish'
        payload = {}
        headers = {
            **self.headers,
            'Authorization': f"Bearer {token}",
            'Content-Length': str(len(payload)),
            'Content-Type': 'application/json'
        }
        try:
            with Session().post(url=url, headers=headers, json=payload) as response:
                response.raise_for_status()
                self.print_timestamp(f"{Fore.GREEN + Style.BRIGHT}[ You\'ve Got {farming_reward} From Farming ]{Style.RESET_ALL}")
                return await self.start_farming(token=token)
        except RequestException as e:
            if e.response.status_code == 403:
                error_finish_farming = e.response.json()
                if error_finish_farming['error']['message'] == 'Too early to finish farming':
                    return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Too Early To Finish Farming ]{Style.RESET_ALL}")
                elif error_finish_farming['error']['message'] == 'Farming didn\'t start':
                    return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Farming Didn\'t Start ]{Style.RESET_ALL}")
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Finish Farming: {str(e)} ]{Style.RESET_ALL}")
        except (Exception, JSONDecodeError) as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Finish Farming: {str(e)} ]{Style.RESET_ALL}")

    async def claim_referral_balance(self, token: str, available_balance: int):
        url = 'https://tg-bot-tap.laborx.io/api/v1/balance/referral/claim'
        payload = {}
        headers = {
            **self.headers,
            'Authorization': f"Bearer {token}",
            'Content-Length': str(len(payload)),
            'Content-Type': 'application/json'
        }
        try:
            with Session().post(url=url, headers=headers, json=payload) as response:
                response.raise_for_status()
                self.print_timestamp(f"{Fore.GREEN + Style.BRIGHT}[ You\'ve Got {available_balance} From Referral ]{Style.RESET_ALL}")
                return await self.start_farming(token=token)
        except RequestException as e:
            if e.response.status_code == 403:
                error_claim_referral = e.response.json()
                if error_claim_referral['error']['message'] == 'Nothing to claim':
                    return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Nothing To Claim From Referral ]{Style.RESET_ALL}")
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Claim Referral: {str(e)} ]{Style.RESET_ALL}")
        except (Exception, JSONDecodeError) as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Claim Referral: {str(e)} ]{Style.RESET_ALL}")

    async def tasks(self, token: str):
        url = 'https://tg-bot-tap.laborx.io/api/v1/tasks'
        headers = {
            **self.headers,
            'Authorization': f"Bearer {token}"
        }
        try:
            with Session().get(url=url, headers=headers) as response:
                response.raise_for_status()
                tasks = response.json()
                for task in tasks:
                    if task['type'] == 'ADSGRAM': continue
                    if not 'submission' in task or task['submission']['status'] == 'REJECTED':
                        await self.submissions_tasks(token=token, task_id=task['id'], task_title=task['title'], task_reward=task['reward'])
                    elif task['submission']['status'] == 'COMPLETED':
                        await self.claims_tasks(token=token, task_id=task['id'], task_title=task['title'], task_reward=task['submission']['reward'])
        except RequestException as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Fetching Tasks: {str(e)} ]{Style.RESET_ALL}")
        except (Exception, JSONDecodeError) as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Fetching Tasks: {str(e)} ]{Style.RESET_ALL}")

    async def submissions_tasks(self, token: str, task_id: str, task_title: str, task_reward: int):
        url = f'https://tg-bot-tap.laborx.io/api/v1/tasks/{task_id}/submissions'
        payload = {}
        headers = {
            **self.headers,
            'Authorization': f"Bearer {token}",
            'Content-Length': str(len(payload)),
            'Content-Type': 'application/json'
        }
        try:
            with Session().post(url=url, headers=headers, json=payload) as response:
                response.raise_for_status()
                submissions_tasks = response.json()
                if submissions_tasks['result']['status'] == 'COMPLETED':
                    return await self.claims_tasks(token=token, task_id=task_id, task_title=task_title, task_reward=task_reward)
        except RequestException as e:
            if e.response.status_code == 400:
                error_submissions_tasks = e.response.json()
                if error_submissions_tasks['error']['message'] == 'Already submitted':
                    return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {task_title} Already Submitted ]{Style.RESET_ALL}")
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Submissions Tasks: {str(e)} ]{Style.RESET_ALL}")
        except (Exception, JSONDecodeError) as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Submissions Tasks: {str(e)} ]{Style.RESET_ALL}")

    async def claims_tasks(self, token: str, task_id: str, task_title: str, task_reward: int):
        url = f'https://tg-bot-tap.laborx.io/api/v1/tasks/{task_id}/claims'
        payload = {}
        headers = {
            **self.headers,
            'Authorization': f"Bearer {token}",
            'Content-Length': str(len(payload)),
            'Content-Type': 'application/json'
        }
        try:
            with Session().post(url=url, headers=headers, json=payload) as response:
                response.raise_for_status()
                if response.ok:
                    return self.print_timestamp(f"{Fore.GREEN + Style.BRIGHT}[ You\'ve Got {task_reward} From {task_title} ]{Style.RESET_ALL}")
        except RequestException as e:
            if e.response.status_code == 400:
                error_claim_tasks = e.response.json()
                if error_claim_tasks['error']['message'] == 'Failed to claim reward':
                    return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Failed To Claim {task_title} ]{Style.RESET_ALL}")
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Claims Tasks: {str(e)} ]{Style.RESET_ALL}")
        except (Exception, JSONDecodeError) as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Claims Tasks: {str(e)} ]{Style.RESET_ALL}")

    async def upgrade_level(self, token: str):
        url = 'https://tg-bot-tap.laborx.io/api/v1/me/level/upgrade'
        payload = {}
        headers = {
            **self.headers,
            'Authorization': f"Bearer {token}",
            'Content-Length': str(len(payload)),
            'Content-Type': 'application/json'
        }
        try:
            with Session().post(url=url, headers=headers, json=payload) as response:
                response.raise_for_status()
                upgrade_level = response.json()
                return self.print_timestamp(f"{Fore.GREEN + Style.BRIGHT}[ Successfully Upgrade Level To {upgrade_level['level']} ]{Style.RESET_ALL}")
        except RequestException as e:
            if e.response.status_code == 403:
                error_upgrade_level = e.response.json()
                if error_upgrade_level['error']['message'] == 'Not enough balance':
                    return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Not Enough Balance To Upgrade Level ]{Style.RESET_ALL}")
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Upgrade Level: {str(e)} ]{Style.RESET_ALL}")
        except (Exception, JSONDecodeError) as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Upgrade Level: {str(e)} ]{Style.RESET_ALL}")

    async def staking(self, token: str, option_id: int, amount: int):
        url = 'https://tg-bot-tap.laborx.io/api/v1/staking'
        payload = {'optionId':str(option_id),'amount':str(amount)}
        headers = {
            **self.headers,
            'Authorization': f"Bearer {token}",
            'Content-Length': str(len(payload)),
            'Content-Type': 'application/json'
        }
        try:
            with Session().post(url=url, headers=headers, json=payload) as response:
                response.raise_for_status()
        except RequestException as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Staking: {str(e)} ]{Style.RESET_ALL}")
        except (Exception, JSONDecodeError) as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Staking: {str(e)} ]{Style.RESET_ALL}")

    async def answer_daily_questions(self):
        url = 'https://raw.githubusercontent.com/Shyzg/timefarm/refs/heads/main/answer.json'
        try:
            with Session().get(url=url) as response:
                response.raise_for_status()
                answer_daily_questions = json.loads(response.text)
                return answer_daily_questions
        except (Exception, JSONDecodeError, RequestException):
            return None

    async def get_daily_questions(self, token: str):
        url = 'https://tg-bot-tap.laborx.io/api/v1/daily-questions'
        headers = {
            **self.headers,
            'Authorization': f"Bearer {token}"
        }
        try:
            with Session().get(url=url, headers=headers) as response:
                response.raise_for_status()
                daily_questions = response.json()
                if 'answer' in daily_questions:
                    if daily_questions['answer']['isCorrect']:
                        return self.print_timestamp(f"{Fore.MAGENTA + Style.BRIGHT}[ Daily Questions Already Answered ]{Style.RESET_ALL}")
                answer_daily_questions = await self.answer_daily_questions()
                if datetime.fromtimestamp(answer_daily_questions['expires']).astimezone().timestamp() >= datetime.now().astimezone().timestamp():
                    return await self.post_daily_questions(token=token, answer=answer_daily_questions['answer'], reward=daily_questions['reward'])
        except RequestException as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Fetching Daily Questions: {str(e)} ]{Style.RESET_ALL}")
        except (Exception, JSONDecodeError) as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Fetching Daily Questions: {str(e)} ]{Style.RESET_ALL}")

    async def post_daily_questions(self, token: str, answer: str, reward: int):
        url = 'https://tg-bot-tap.laborx.io/api/v1/daily-questions'
        payload = {'answer':answer}
        headers = {
            **self.headers,
            'Authorization': f"Bearer {token}",
            'Content-Length': str(len(payload)),
            'Content-Type': 'application/json'
        }
        try:
            with Session().post(url=url, headers=headers, json=payload) as response:
                response.raise_for_status()
                daily_questions = response.json()
                if daily_questions['isCorrect']:
                    return self.print_timestamp(f"{Fore.GREEN + Style.BRIGHT}[ You\'ve Got {reward} From Daily Questions ]{Style.RESET_ALL}")
                return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Your Daily Question Answer Is Wrong ]{Style.RESET_ALL}")
        except RequestException as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Staking: {str(e)} ]{Style.RESET_ALL}")
        except (Exception, JSONDecodeError) as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Staking: {str(e)} ]{Style.RESET_ALL}")

    async def main(self):
        while True:
            try:
                sessions = [file.replace('.session', '') for file in os.listdir('sessions/') if file.endswith('.session')]
                if not sessions:
                    return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ No Session Files Found In The Folder! Please Make Sure There Are '*.session' Files In The Folder. ]{Style.RESET_ALL}")
                queries = await self.generate_queries(sessions=sessions)
                accounts = await self.generate_tokens(queries=queries)
                restart_times = []
                total_balance = 0

                for (account, username) in accounts:
                    self.print_timestamp(
                        f"{Fore.WHITE + Style.BRIGHT}[ Home ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.CYAN + Style.BRIGHT}[ {username} ]{Style.RESET_ALL}"
                    )
                    await self.complete_onboarding_me(token=account['token'])
                    self.print_timestamp(
                        f"{Fore.BLUE + Style.BRIGHT}[ Balance {account['balanceInfo']['balance']} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT}[ Clocks Level {account['info']['level']} ]{Style.RESET_ALL}"
                    )
                    info_farming = await self.info_farming(token=account['token'])
                    if info_farming is not None:
                        if 'activeFarmingStartedAt' in info_farming:
                            end_farm = (datetime.strptime(info_farming['activeFarmingStartedAt'], "%Y-%m-%dT%H:%M:%S.%fZ") + timedelta(seconds=info_farming['farmingDurationInSec'])).replace(tzinfo=UTC).astimezone()
                            if datetime.now().astimezone() >= end_farm:
                                await self.finish_farming(token=account['token'], farming_reward=info_farming['farmingReward'])
                            else:
                                restart_times.append(end_farm.timestamp())
                                self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ Farming Can Be Claim At {end_farm.strftime('%x %X %Z')} ]{Style.RESET_ALL}")
                        else:
                            await self.start_farming(token=account['token'])
                    if 'availableBalance' in account['balanceInfo']['referral'] and account['balanceInfo']['referral']['availableBalance'] != 0:
                        await self.claim_referral_balance(token=account['token'], available_balance=account['balanceInfo']['referral']['availableBalance'])
                    await self.upgrade_level(token=account['token'])
                    await self.get_daily_questions(token=account['token'])

                for (account, username) in accounts:
                    self.print_timestamp(
                        f"{Fore.WHITE + Style.BRIGHT}[ Tasks ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.CYAN + Style.BRIGHT}[ {username} ]{Style.RESET_ALL}"
                    )
                    await self.tasks(token=account['token'])

                for (account, username) in accounts:
                    total_balance += account['balanceInfo']['balance']

                if restart_times:
                    wait_times = [farming - datetime.now().astimezone().timestamp() for farming in restart_times if farming > datetime.now().astimezone().timestamp()]
                    if wait_times:
                        sleep_time = min(wait_times)
                    else:
                        sleep_time = 15 * 60
                else:
                    sleep_time = 15 * 60

                self.print_timestamp(
                    f"{Fore.CYAN + Style.BRIGHT}[ Total Account {len(accounts)} ]{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                    f"{Fore.GREEN + Style.BRIGHT}[ Total Balance {total_balance} ]{Style.RESET_ALL}"
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
        timefarm = Timefarm()
        asyncio.run(timefarm.main())
    except (ValueError, IndexError, FileNotFoundError) as e:
        timefarm.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {str(e)} ]{Style.RESET_ALL}")
    except KeyboardInterrupt:
        sys.exit(0)