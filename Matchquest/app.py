from colorama import *
from datetime import datetime, timedelta
from fake_useragent import FakeUserAgent
from faker import Faker
from requests import (
    JSONDecodeError,
    RequestException,
    Session
)
from urllib.parse import parse_qs
import asyncio
import json
import os
import sys
import random
import re

class MatchQuest:
    def __init__(self) -> None:
        self.session = Session()
        self.faker = Faker()
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Host': 'tgapp-api.matchain.io',
            'Origin': 'https://tgapp-api.matchain.io',
            'Pragma': 'no-cache',
            'Referer': 'https://tgapp-api.matchain.io/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
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

    def process_queries(self, lines_per_file: int):
        if not os.path.exists('queries.txt'):
            raise FileNotFoundError(f"File 'queries.txt' not found. Please ensure it exists.")

        with open('queries.txt', 'r') as f:
            queries = [line.strip() for line in f if line.strip()]
        if not queries:
            raise ValueError("File 'queries.txt' is empty.")

        existing_queries = set()
        for file in os.listdir():
            if file.startswith('queries-') and file.endswith('.txt'):
                with open(file, 'r') as qf:
                    existing_queries.update(line.strip() for line in qf if line.strip())

        new_queries = [query for query in queries if query not in existing_queries]
        if not new_queries:
            self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ No New Queries To Add ]{Style.RESET_ALL}")
            return

        files = [f for f in os.listdir() if f.startswith('queries-') and f.endswith('.txt')]
        files.sort(key=lambda x: int(re.findall(r'\d+', x)[0]) if re.findall(r'\d+', x) else 0)

        last_file_number = int(re.findall(r'\d+', files[-1])[0]) if files else 0

        for i in range(0, len(new_queries), lines_per_file):
            chunk = new_queries[i:i + lines_per_file]
            if files and len(open(files[-1], 'r').readlines()) < lines_per_file:
                with open(files[-1], 'a') as outfile:
                    outfile.write('\n'.join(chunk) + '\n')
                self.print_timestamp(f"{Fore.GREEN + Style.BRIGHT}[ Updated '{files[-1]}' ]{Style.RESET_ALL}")
            else:
                last_file_number += 1
                queries_file = f"queries-{last_file_number}.txt"
                with open(queries_file, 'w') as outfile:
                    outfile.write('\n'.join(chunk) + '\n')
                self.print_timestamp(f"{Fore.GREEN + Style.BRIGHT}[ Generated '{queries_file}' ]{Style.RESET_ALL}")

    def load_queries(self, file_path):
        with open(file_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]

    async def register_user(self, query: str):
        url = 'https://tgapp-api.matchain.io/api/tgapp/v1/user/register'
        try:
            parsed_query = parse_qs(query)
            user_data_json = parsed_query['user'][0]
            user_data = json.loads(user_data_json)
            uid = user_data.get('id')
            first_name = user_data.get('first_name', '')
            last_name = user_data.get('last_name', '')
            username = user_data.get('username', '')
            nickname = f"{self.faker.user_name()}{random.randint(1000, 9999)}"
            data = json.dumps({'uid':int(uid),'first_name':first_name,'last_name':last_name,'username':username,'nickname':nickname,'invitor':'799088ca289a5695366dedcce0c35bf3','tg_login_params':query})
            headers = {
                **self.headers,
                'Content-Length': str(len(data)),
                'Content-Type': 'application/json'
            }
            with Session().post(url=url, headers=headers, data=data) as response:
                response.raise_for_status()
                return None
        except (Exception, JSONDecodeError, RequestException):
            return None

    async def register_users(self, queries):
        tasks = [self.register_user(query) for query in queries]
        await asyncio.gather(*tasks)
        return None

    async def generate_token(self, query: str):
        url = 'https://tgapp-api.matchain.io/api/tgapp/v1/user/login'
        try:
            parsed_query = parse_qs(query)
            user_data_json = parsed_query['user'][0]
            user_data = json.loads(user_data_json)
            uid = user_data.get('id')
            first_name = user_data.get('first_name', '')
            last_name = user_data.get('last_name', '')
            username = user_data.get('username', '')
            data = json.dumps({'uid':uid,'first_name':first_name,'last_name':last_name,'username':username,'tg_login_params':query})
            headers = {
                **self.headers,
                'Content-Length': str(len(data)),
                'Content-Type': 'application/json'
            }
            with Session().post(url=url, headers=headers, data=data) as response:
                response.raise_for_status()
                generate_token = response.json()
                token = generate_token['data']['token']
                return (token, first_name, uid)
        except (Exception, JSONDecodeError, RequestException) as e:
            self.print_timestamp(
                f"{Fore.YELLOW + Style.BRIGHT}[ Failed To Process {query} ]{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                f"{Fore.RED + Style.BRIGHT}[ {str(e)} ]{Style.RESET_ALL}"
            )
            return None

    async def generate_tokens(self, queries):
        tasks = [self.generate_token(query) for query in queries]
        results = await asyncio.gather(*tasks)
        return [result for result in results if result is not None]

    async def profile_user(self, token: str, uid: int):
        url = 'https://tgapp-api.matchain.io/api/tgapp/v1/user/profile'
        data = json.dumps({'uid':uid})
        headers = {
            **self.headers,
            'Authorization': token,
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json'
        }
        try:
            with Session().post(url=url, headers=headers, data=data) as response:
                response.raise_for_status()
                return response.json()
        except RequestException as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Fetching Profile User: {str(e)} ]{Style.RESET_ALL}")
            return None
        except (Exception, JSONDecodeError) as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Fetching Profile User: {str(e)} ]{Style.RESET_ALL}")
            return None

    async def progress_quiz_daily(self, token: str):
        url = 'https://tgapp-api.matchain.io/api/tgapp/v1/daily/quiz/progress'
        headers = {
            **self.headers,
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        answer_result = {'answer_result':[]}
        try:
            with Session().get(url=url, headers=headers) as response:
                response.raise_for_status()
                progress_quiz_daily = response.json()
                if 'msg' in progress_quiz_daily:
                    if progress_quiz_daily['msg'] == 'Already answered today':
                        self.print_timestamp(f"{Fore.MAGENTA + Style.BRIGHT}[ Daily Quiz Already Answered Today ]{Style.RESET_ALL}")
                elif 'data' in progress_quiz_daily:
                    for quiz in progress_quiz_daily['data']:
                        quiz_id = quiz['Id']
                        correct_answer = None
                        for answer in quiz['items']:
                            if answer['is_correct']:
                                correct_answer = answer['number']
                                break
                        answer_result['answer_result'].append({'quiz_id':quiz_id,'selected_item':correct_answer,'correct_item':correct_answer})
                    await self.submit_quiz_daily(token=token, answer_result=answer_result)
        except RequestException as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Fetching Progress Quiz Daily: {str(e)} ]{Style.RESET_ALL}")
        except (Exception, JSONDecodeError) as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Fetching Progress Quiz Daily: {str(e)} ]{Style.RESET_ALL}")

    async def submit_quiz_daily(self, token: str, answer_result: dict):
        url = 'https://tgapp-api.matchain.io/api/tgapp/v1/daily/quiz/submit'
        data = json.dumps(answer_result)
        headers = {
            **self.headers,
            'Authorization': token,
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json'
        }
        try:
            with Session().post(url=url, headers=headers, data=data) as response:
                response.raise_for_status()
                submit_quiz_daily = response.json()
                if 'msg' in submit_quiz_daily:
                    if submit_quiz_daily['msg'] == 'OK':
                        return self.print_timestamp(f"{Fore.GREEN + Style.BRIGHT}[ Submitted Quiz Daily ]{Style.RESET_ALL}")
                elif 'err' in submit_quiz_daily:
                    if submit_quiz_daily['err'] == 'Already answered today':
                        return self.print_timestamp(f"{Fore.MAGENTA + Style.BRIGHT}[ Daily Quiz Already Answered Today ]{Style.RESET_ALL}")
        except RequestException as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Submit Quiz Daily: {str(e)} ]{Style.RESET_ALL}")
        except (Exception, JSONDecodeError) as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Submit Quiz Daily: {str(e)} ]{Style.RESET_ALL}")

    async def status_task_daily(self, token: str, uid: int):
        url = 'https://tgapp-api.matchain.io/api/tgapp/v1/daily/task/status'
        headers = {
            **self.headers,
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        try:
            with Session().get(url=url, headers=headers) as response:
                response.raise_for_status()
                status_task_daily = response.json()
                if 'data' in status_task_daily:
                    for status in status_task_daily['data']:
                        await self.purchase_task_daily(token=token, uid=uid, type_purchase=status['type'])
        except RequestException as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Fetching Status Task Daily: {str(e)} ]{Style.RESET_ALL}")
        except (Exception, JSONDecodeError) as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Fetching Status Task Daily: {str(e)} ]{Style.RESET_ALL}")

    async def purchase_task_daily(self, token: str, uid, type_purchase: str):
        url = 'https://tgapp-api.matchain.io/api/tgapp/v1/daily/task/purchase'
        data = json.dumps({'uid':uid,'type':type_purchase})
        headers = {
            **self.headers,
            'Authorization': token,
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json'
        }
        try:
            with Session().post(url=url, headers=headers, data=data) as response:
                response.raise_for_status()
                purchase_task_daily = response.json()
                if 'code' in purchase_task_daily:
                    if purchase_task_daily['code'] == 200:
                        if 'msg' in purchase_task_daily:
                            if ((purchase_task_daily['msg'] == 'Congratulations on receiving 3x') or
                                (purchase_task_daily['msg'] == 'Congratulations on receiving 2x') or
                                (purchase_task_daily['msg'] == 'Congratulations on receiving 1x')):
                                return self.print_timestamp(f"{Fore.GREEN + Style.BRIGHT}[ Successfully Purchase Daily Booster ]{Style.RESET_ALL}")
                            elif purchase_task_daily['msg'] == 'Booster successfully':
                                return self.print_timestamp(f"{Fore.GREEN + Style.BRIGHT}[ Successfully Purchase Daily Game Booster ]{Style.RESET_ALL}")
                    elif purchase_task_daily['code'] == 400:
                        if purchase_task_daily['msg'] == 'You\'ve already made a purchase. Buy again once you utilize the last chance.🫶':
                            return self.print_timestamp(f"{Fore.MAGENTA + Style.BRIGHT}[ Already Made A Purchase ]{Style.RESET_ALL}")
                        elif purchase_task_daily['msg'] == 'Oops! You\'ve reached purchase limit for today, buy again tomorrow! 🔥':
                            return self.print_timestamp(f"{Fore.MAGENTA + Style.BRIGHT}[ Reached Purchase Limit For Today, Buy Again Tomorrow ]{Style.RESET_ALL}")
                        elif purchase_task_daily['msg'] == 'Booster failed, Your Points is insufficient':
                            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Insufficient Points ]{Style.RESET_ALL}")
        except RequestException as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Purchase Task Daily: {str(e)} ]{Style.RESET_ALL}")
        except (Exception, JSONDecodeError) as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Purchase Task Daily: {str(e)} ]{Style.RESET_ALL}")

    async def rule_game(self, token: str):
        url = 'https://tgapp-api.matchain.io/api/tgapp/v1/game/rule'
        headers = {
            **self.headers,
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        try:
            with Session().get(url=url, headers=headers) as response:
                response.raise_for_status()
                rule_game = response.json()
                if 'code' in rule_game:
                    if rule_game['code'] == 200:
                        if 'data' in rule_game:
                            while rule_game['data']['game_count'] > 0:
                                await self.play_game(token=token)
                                rule_game['data']['game_count'] -= 1
        except RequestException as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Fetching Rule Game: {str(e)} ]{Style.RESET_ALL}")
        except (Exception, JSONDecodeError) as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Fetching Rule Game: {str(e)} ]{Style.RESET_ALL}")

    async def play_game(self, token: str):
        url = 'https://tgapp-api.matchain.io/api/tgapp/v1/game/play'
        headers = {
            **self.headers,
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        try:
            with Session().get(url=url, headers=headers) as response:
                response.raise_for_status()
                play_game = response.json()
                if 'code' in play_game:
                    if play_game['code'] == 200:
                        if 'data' in play_game:
                            self.print_timestamp(
                                f"{Fore.YELLOW + Style.BRIGHT}[ Game Started ]{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                                f"{Fore.BLUE + Style.BRIGHT}[ Please Wait ~30 Seconds ]{Style.RESET_ALL}"
                            )
                            await asyncio.sleep(30 + 3)
                            await self.claim_game(token=token, game_id=play_game['data']['game_id'])
        except RequestException as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Play Game: {str(e)} ]{Style.RESET_ALL}")
        except (Exception, JSONDecodeError) as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Play Game: {str(e)} ]{Style.RESET_ALL}")

    async def claim_game(self, token: str, game_id: str):
        url = 'https://tgapp-api.matchain.io/api/tgapp/v1/game/claim'
        data = json.dumps({'game_id':game_id,'point':220})
        headers = {
            **self.headers,
            'Authorization': token,
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json'
        }
        try:
            with Session().post(url=url, headers=headers, data=data) as response:
                response.raise_for_status()
                claim_game = response.json()
                if 'code' in claim_game:
                    if claim_game['code'] == 200:
                        return self.print_timestamp(f"{Fore.GREEN + Style.BRIGHT}[ Game Claimed ]{Style.RESET_ALL}")
                    elif claim_game['code'] == 400:
                        if 'err' in claim_game:
                            if claim_game['err'] == 'game does not exist, claim error.':
                                return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Game Does Not Exist, Claim Error ]{Style.RESET_ALL}")
                            elif claim_game['err'] == 'Claim failed':
                                return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Claim Failed ]{Style.RESET_ALL}")
        except RequestException as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Claim Game: {str(e)} ]{Style.RESET_ALL}")
        except (Exception, JSONDecodeError) as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Claim Game: {str(e)} ]{Style.RESET_ALL}")

    async def reward_point(self, token: str, uid: int):
        url = 'https://tgapp-api.matchain.io/api/tgapp/v1/point/reward'
        data = json.dumps({'uid':uid})
        headers = {
            **self.headers,
            'Authorization': token,
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json'
        }
        try:
            with Session().post(url=url, headers=headers, data=data) as response:
                response.raise_for_status()
                return response.json()
        except RequestException as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Fetching Reward Point: {str(e)} ]{Style.RESET_ALL}")
            return None
        except (Exception, JSONDecodeError) as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Fetching Reward Point: {str(e)} ]{Style.RESET_ALL}")
            return None

    async def farming_reward_point(self, token: str, uid: int):
        url = 'https://tgapp-api.matchain.io/api/tgapp/v1/point/reward/farming'
        data = json.dumps({'uid':uid})
        headers = {
            **self.headers,
            'Authorization': token,
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json'
        }
        try:
            with Session().post(url=url, headers=headers, data=data) as response:
                response.raise_for_status()
                farming_reward_point = response.json()
                if 'code' in farming_reward_point:
                    if farming_reward_point['code'] == 200:
                        return self.print_timestamp(f"{Fore.GREEN + Style.BRIGHT}[ Farming Started ]{Style.RESET_ALL}")
                    elif farming_reward_point['code'] == 400:
                        if 'err' in farming_reward_point:
                            if farming_reward_point['err'] == 'Has farming event wait claim':
                                return self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ Farming Already Started ]{Style.RESET_ALL}")
        except RequestException as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Farming Reward Point: {str(e)} ]{Style.RESET_ALL}")
        except (Exception, JSONDecodeError) as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Farming Reward Point: {str(e)} ]{Style.RESET_ALL}")

    async def claim_reward_point(self, token: str, uid: int):
        url = 'https://tgapp-api.matchain.io/api/tgapp/v1/point/reward/claim'
        data = json.dumps({'uid':uid})
        headers = {
            **self.headers,
            'Authorization': token,
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json'
        }
        try:
            with Session().post(url=url, headers=headers, data=data) as response:
                response.raise_for_status()
                claim_reward_point = response.json()
                if 'code' in claim_reward_point:
                    if claim_reward_point['code'] == 200:
                        self.print_timestamp(f"{Fore.GREEN + Style.BRIGHT}[ You Have Got {int(claim_reward_point['data'] / 1000)} From Farming ]{Style.RESET_ALL}")
                        return await self.farming_reward_point(token=token, uid=uid)
                    elif claim_reward_point['code'] == 400:
                        if 'err' in claim_reward_point:
                            if claim_reward_point['err'] == 'Farming event not finished':
                                return self.print_timestamp(f"{Fore.YELLOW + Style.BRIGHT}[ Farming Is Not Finished ]{Style.RESET_ALL}")
        except RequestException as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Claim Reward Point: {str(e)} ]{Style.RESET_ALL}")
        except (Exception, JSONDecodeError) as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Claim Reward Point: {str(e)} ]{Style.RESET_ALL}")

    async def list_task_point(self, token: str, uid: int):
        url = 'https://tgapp-api.matchain.io/api/tgapp/v1/point/task/list'
        data = json.dumps({'uid':uid})
        headers = {
            **self.headers,
            'Authorization': token,
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json'
        }
        try:
            with Session().post(url=url, headers=headers, data=data) as response:
                response.raise_for_status()
                list_task_point = response.json()
                if 'code' in list_task_point:
                    all_tasks = []
                    data_section = list_task_point.get('data', {})
                    for key in data_section.keys():
                        all_tasks.extend(data_section.get(key, []))
                    for task in all_tasks:
                        if not task['complete']:
                            await self.complete_task_point(token=token, uid=uid, task_name=task['name'], task_description=task['description'], task_points=task['points'])
        except RequestException as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Fetching List Task Point: {str(e)} ]{Style.RESET_ALL}")
        except (Exception, JSONDecodeError) as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Fetching List Task Point: {str(e)} ]{Style.RESET_ALL}")

    async def complete_task_point(self, token: str, uid: int, task_name: str, task_points: int, task_description: str):
        url = 'https://tgapp-api.matchain.io/api/tgapp/v1/point/task/complete'
        data = json.dumps({'uid':uid,'type':task_name})
        headers = {
            **self.headers,
            'Authorization': token,
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json'
        }
        try:
            with Session().post(url=url, headers=headers, data=data) as response:
                response.raise_for_status()
                complete_task_point = response.json()
                if 'code' in complete_task_point:
                    if complete_task_point['code'] == 200:
                        if complete_task_point['data']:
                            await asyncio.sleep(random.randint(3, 5))
                            await self.claim_task_point(token=token, uid=uid, task_name=task_name, task_points=task_points, task_description=task_description)
        except RequestException as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Complete Task Point: {str(e)} ]{Style.RESET_ALL}")
        except (Exception, JSONDecodeError) as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Complete Task Point: {str(e)} ]{Style.RESET_ALL}")

    async def claim_task_point(self, token: str, uid: int, task_name: str, task_points: int, task_description: str):
        url = 'https://tgapp-api.matchain.io/api/tgapp/v1/point/task/claim'
        data = json.dumps({'uid':uid,'type':task_name})
        headers = {
            **self.headers,
            'Authorization': token,
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json'
        }
        try:
            with Session().post(url=url, headers=headers, data=data) as response:
                response.raise_for_status()
                claim_task_point = response.json()
                if 'code' in claim_task_point:
                    if claim_task_point['code'] == 200:
                        if claim_task_point['data'] == 'success':
                            return self.print_timestamp(f"{Fore.GREEN + Style.BRIGHT}[ You\'ve Got {task_points} From {task_description} ]{Style.RESET_ALL}")
                    elif claim_task_point['code'] == 401:
                        if claim_task_point['err'] == 'task already claimed':
                            return self.print_timestamp(f"{Fore.GREEN + Style.BRIGHT}[ {task_description} Already Claimed ]{Style.RESET_ALL}")
        except RequestException as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Claim Task Point: {str(e)} ]{Style.RESET_ALL}")
        except (Exception, JSONDecodeError) as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Claim Task Point: {str(e)} ]{Style.RESET_ALL}")

    async def claim_invite_point(self, token: str, uid: int):
        url = 'https://tgapp-api.matchain.io/api/tgapp/v1/point/invite/claim'
        data = json.dumps({'uid':uid})
        headers = {
            **self.headers,
            'Authorization': token,
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json'
        }
        try:
            with Session().post(url=url, headers=headers, data=data) as response:
                response.raise_for_status()
                claim_invite_point = response.json()
                if 'code' in claim_invite_point:
                    if claim_invite_point['code'] == 200:
                        if claim_invite_point['data'] != 0:
                            return self.print_timestamp(f"{Fore.GREEN + Style.BRIGHT}[ You Have Got {int(claim_invite_point['data'] / 1000)} From Referral ]{Style.RESET_ALL}")
        except RequestException as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An HTTP Error Occurred While Claim Invite Point: {str(e)} ]{Style.RESET_ALL}")
        except (Exception, JSONDecodeError) as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ An Unexpected Error Occurred While Claim Invite Point: {str(e)} ]{Style.RESET_ALL}")

    async def main(self, queries):
        while True:
            try:
                await self.register_users(queries=queries)
                accounts = await self.generate_tokens(queries=queries)
                restart_times = []
                total_balance = 0

                for (token, first_name, uid) in accounts:
                    self.print_timestamp(
                        f"{Fore.WHITE + Style.BRIGHT}[ Home ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.CYAN + Style.BRIGHT}[ {first_name} ]{Style.RESET_ALL}"
                    )
                    await self.progress_quiz_daily(token=token)
                    await self.claim_invite_point(token=token, uid=uid)
                
                accounts = await self.generate_tokens(queries=queries)
                for (token, first_name, uid) in accounts:
                    self.print_timestamp(
                        f"{Fore.WHITE + Style.BRIGHT}[ Home/Farming ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.CYAN + Style.BRIGHT}[ {first_name} ]{Style.RESET_ALL}"
                    )
                    reward_point = await self.reward_point(token=token, uid=uid)
                    if reward_point is not None:
                        if 'code' in reward_point:
                            if reward_point['code'] == 200:
                                if reward_point['data']['next_claim_timestamp'] == 0:
                                    await self.farming_reward_point(token=token, uid=uid)
                                else:
                                    if datetime.now().astimezone() >= datetime.fromtimestamp(reward_point['data']['next_claim_timestamp'] / 1000).astimezone():
                                        await self.claim_reward_point(token=token, uid=uid)
                            else:
                                restart_times.append(datetime.fromtimestamp(int(reward_point['data']['next_claim_timestamp'] / 1000)).astimezone().timestamp())
                                self.print_timestamp(f"{Fore.BLUE + Style.BRIGHT}[ Farming Can Be Claim At {datetime.fromtimestamp(reward_point['data']['next_claim_timestamp'] / 1000).astimezone().strftime('%x %X %Z')} ]{Style.RESET_ALL}")
                    await self.status_task_daily(token=token, uid=uid)

                for (token, first_name, uid) in accounts:
                    self.print_timestamp(
                        f"{Fore.WHITE + Style.BRIGHT}[ Home/Game ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.CYAN + Style.BRIGHT}[ {first_name} ]{Style.RESET_ALL}"
                    )
                    await self.rule_game(token=token)

                for (token, first_name, uid) in accounts:
                    self.print_timestamp(
                        f"{Fore.WHITE + Style.BRIGHT}[ Tasks ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.CYAN + Style.BRIGHT}[ {first_name} ]{Style.RESET_ALL}"
                    )
                    await self.list_task_point(token=token, uid=uid)
                    profile_user = await self.profile_user(token=token, uid=uid)
                    total_balance += int(profile_user['data']['Balance'] / 1000) if profile_user else 0

                if restart_times:
                    now = datetime.now().astimezone().timestamp()
                    future_farming_times = [time - now for time in restart_times if time > now]
                    if future_farming_times:
                        sleep_time = min(future_farming_times) + 30
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
        matchquest = MatchQuest()
        
        queries_files = [f for f in os.listdir() if f.startswith('queries-') and f.endswith('.txt')]
        queries_files.sort(key=lambda x: int(re.findall(r'\d+', x)[0]) if re.findall(r'\d+', x) else 0)

        matchquest.print_timestamp(
            f"{Fore.MAGENTA + Style.BRIGHT}[ 1 ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT}[ Split Queries ]{Style.RESET_ALL}"
        )
        matchquest.print_timestamp(
            f"{Fore.MAGENTA + Style.BRIGHT}[ 2 ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT}[ Use Existing 'queries-*.txt' ]{Style.RESET_ALL}"
        )
        matchquest.print_timestamp(
            f"{Fore.MAGENTA + Style.BRIGHT}[ 3 ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT}[ Use 'queries.txt' Without Splitting ]{Style.RESET_ALL}"
        )
        initial_choice = int(input(
            f"{Fore.BLUE + Style.BRIGHT}[ {datetime.now().astimezone().strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{Fore.YELLOW + Style.BRIGHT}[ Select An Option ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
        ))

        if initial_choice == 1:
            accounts = int(input(
                f"{Fore.YELLOW + Style.BRIGHT}[ How Much Account That You Want To Process Each Terminal ]{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            ))
            matchquest.print_timestamp(f"{Fore.CYAN + Style.BRIGHT}[ Processing Queries To Generate Files ]{Style.RESET_ALL}")
            matchquest.process_queries(lines_per_file=accounts)

            queries_files = [f for f in os.listdir() if f.startswith('queries-') and f.endswith('.txt')]
            queries_files.sort(key=lambda x: int(re.findall(r'\d+', x)[0]) if re.findall(r'\d+', x) else 0)

            if not queries_files:
                raise FileNotFoundError("No 'queries-*.txt' Files Found")
        elif initial_choice == 2:
            if not queries_files:
                raise FileNotFoundError("No 'queries-*.txt' Files Found")
        elif initial_choice == 3:
            queries = [line.strip() for line in open('queries.txt') if line.strip()]
        else:
            raise ValueError("Invalid Initial Choice. Please Run The Script Again And Choose A Valid Option")

        if initial_choice in [1, 2]:
            matchquest.print_timestamp(f"{Fore.MAGENTA + Style.BRIGHT}[ Select The Queries File To Use ]{Style.RESET_ALL}")
            for i, queries_file in enumerate(queries_files, start=1):
                matchquest.print_timestamp(
                    f"{Fore.MAGENTA + Style.BRIGHT}[ {i} ]{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                    f"{Fore.CYAN + Style.BRIGHT}[ {queries_file} ]{Style.RESET_ALL}"
                )

            choice = int(input(
                f"{Fore.BLUE + Style.BRIGHT}[ {datetime.now().astimezone().strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                f"{Fore.YELLOW + Style.BRIGHT}[ Select 'queries-*.txt' File ]{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            )) - 1
            if choice < 0 or choice >= len(queries_files):
                raise ValueError("Invalid Choice. Please Run The Script Again And Choose A Valid Option")

            selected_file = queries_files[choice]
            queries = matchquest.load_queries(selected_file)
        asyncio.run(matchquest.main(queries))
    except (ValueError, IndexError, FileNotFoundError) as e:
        matchquest.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {str(e)} ]{Style.RESET_ALL}")
    except KeyboardInterrupt:
        sys.exit(0)