import sys
import json
import requests
from datetime import datetime, time as datetime_time
from colorama import init, Fore, Style
from urllib.parse import unquote
import cloudscraper
import hashlib
import random
from zoneinfo import ZoneInfo
from settings import config
from functions import calculate_bet, calculate_best_skill, improve_possible, number_short, calculate_tap_power
import time

from pydantic import BaseModel, Field


init(autoreset=True)


class FundHelper(BaseModel):
    funds: set = Field(default_factory=set)
    youtube: dict


def time_now():
    return int(time.time())


class Data:
    def __init__(self, apiKey_us, username, id_us):
        self.apiKey = apiKey_us
        self.username = username
        self.id = id_us


class PixelTod:
    def __init__(self):
        self.scraper = cloudscraper.create_scraper()
        self.DEFAULT_COUNTDOWN = config.SLEEP_ALL
        self.INTERVAL_DELAY = config.SLEEP_MULT 
        self.base_headers = {
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9,ru;q=0.8",
            "Content-Type": "application/json",
            "Origin": "https://game.xempire.io",
            "Referer": "https://game.xempire.io/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Linux; Android 9; SM-N971N Build/PQ3B.190801.07101020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/124.0.6367.82 Safari/537.36",
            "X-Requested-With": "org.telegram.messenger.web",
        }

        self.level = 0
        self.gmt_timezone = ZoneInfo('GMT')
        self.dbData = {}
        self.balance = 0
        self.mph = 0
        self.taps_limit = False
        self.taps_limit_date = ''


    def data_parsing(self, data):
        return {key: value for key, value in (i.split('=') for i in unquote(data).split('&'))}

    def main(self):
        with open("initdata.txt", "r") as file:
            datas = file.read().splitlines()

        self.log(f'{Fore.LIGHTYELLOW_EX}Accounts detected: {len(datas)}')
        if not datas:
            self.log(f'{Fore.LIGHTYELLOW_EX}Please, enter your data in initdata.txt')
            sys.exit()
        print('-' * 50)
        while True:
            for no, data in enumerate(datas):
                self.log(f'{Fore.LIGHTYELLOW_EX}Number Accountа: {Fore.LIGHTWHITE_EX}{no + 1}')
                data_parse = self.data_parsing(data)
                user = json.loads(data_parse['user'])
                username = user.get('first_name')
                id_us = user.get('id')
                apiKey_us = data_parse.get('hash')
                chat_instance = data_parse.get('chat_instance')
                sender = data_parse.get('sender')

                utm_bot_inline = data_parse.get('utm_bot_inline')

                self.log(f'{Fore.LIGHTYELLOW_EX}Account: {Fore.LIGHTWHITE_EX}{username} ')

                url = "https://api.xempire.io/telegram/auth"
                payload = {
                    "data": {
                        "chatId": "",
                        "chatInstance": f"{chat_instance}",
                        "chatType": f"{sender}",
                        "initData": f"{data}",
                        "platform": "android",
                        "startParam": f"{utm_bot_inline}",
                    }
                }
                headers = self.base_headers.copy()
                self.api_call(url, data=json.dumps(payload), headers=headers, method='POST')
                Data(apiKey_us, username, id_us)

                self.process_account(apiKey=apiKey_us, id_data=id_us)
                print('-' * 50)
                self.countdown(self.INTERVAL_DELAY)
            self.countdown(self.DEFAULT_COUNTDOWN)

    def process_account(self, apiKey: str, id_data):
        full_profile = self.get_profile(full=True, apiKey=apiKey)
        self.dbData = full_profile.get('dbData', {})
        if self.dbData:
            del full_profile['dbData']
        hero_data = full_profile.get('hero')
        self.balance = int(full_profile['hero']['money'] or 0)
        self.update_level(level=int(full_profile['hero']['level'] or 0))
        self.mph = int(full_profile['hero']['moneyPerHour'] or 0)
        offline_bonus = int(full_profile['hero']['offlineBonus'] or 0)
        if offline_bonus > 0:
            time.sleep(random.randint(1, 2))
            if self.get_offline_bonus(apiKey=apiKey):
                self.log(f"{Fore.LIGHTYELLOW_EX}Offline bonus: {Fore.LIGHTWHITE_EX}+{number_short(value=offline_bonus)}")
        else:
            self.log(f"{Fore.LIGHTRED_EX}Офлайн бонуса нету")

        time.sleep(random.randint(2, 4))
        profile = self.get_profile(full=False, apiKey=apiKey)
        self.update_level(level=int(profile['hero']['level'] or 0))
        self.balance = int(profile['hero']['money'] or 0)
        self.mph = int(profile['hero']['moneyPerHour'] or 0)
        self.level = int(profile['hero']['level'] or 0)
        self.log(f"{Fore.LIGHTYELLOW_EX}Level: {Fore.LIGHTWHITE_EX}{self.level} | "
                 f"{Fore.LIGHTYELLOW_EX}Balance: {Fore.LIGHTWHITE_EX}+{number_short(value=self.balance)} "
                 f"{Fore.LIGHTYELLOW_EX}Income per hour: {Fore.LIGHTWHITE_EX}+{number_short(value=self.mph)}")

        cur_time_gmt = datetime.now(self.gmt_timezone)
        cur_time_gmt_s = cur_time_gmt.strftime('%Y-%m-%d')
        new_day_gmt = cur_time_gmt.replace(hour=7, minute=0, second=0, microsecond=0)

        daily_rewards = full_profile['dailyRewards']
        daily_index = None
        for day, status in daily_rewards.items():
            if status == 'canTake':
                daily_index = day
                break
        if daily_index is not None:
            time.sleep(random.randint(2, 4))
            daily_claimed = self.daily_reward(index=daily_index, apiKey=apiKey)
            if daily_claimed:
                self.log(f"{Fore.LIGHTYELLOW_EX}Claimed daily reward")

        else:
            self.log(f"{Fore.LIGHTRED_EX}Daily reward unavailable")

        unrewarded_quests = [quest['key'] for quest in full_profile['quests'] if not quest['isRewarded']]
        if unrewarded_quests:
            self.log(f"{Fore.LIGHTYELLOW_EX}There are available quests")
            time.sleep(random.randint(2, 4))
            for quest in unrewarded_quests:
                time.sleep(random.randint(1, 2))
                if self.quest_reward(quest=quest, apiKey=apiKey):
                    self.log(f"{Fore.LIGHTYELLOW_EX}Quest reward {Fore.LIGHTWHITE_EX}{quest} {Fore.LIGHTYELLOW_EX}получена")

        time.sleep(random.randint(2, 4))
        self.daily_quests(apiKey=apiKey)

        time.sleep(random.randint(2, 4))
        self.open_boxes(apiKey=apiKey)

        time.sleep(random.randint(2, 4))
        unrewarded_friends = [int(friend['id']) for friend in full_profile['friends'] if friend['bonusToTake'] > 0]
        if unrewarded_friends:
            self.log(f"{Fore.LIGHTYELLOW_EX}Reward for friend available")

            while len(unrewarded_friends) >= 10:
                success, friends = self.friend_reward(batch=True, apiKey=apiKey)
                if success:
                    self.log(f"{Fore.LIGHTYELLOW_EX}Награда за 10 друзей получена")
                    unrewarded_friends = [int(friend['id']) for friend in friends if friend['bonusToTake'] > 0]
                time.sleep(random.randint(2, 4))

            for friend in unrewarded_friends:
                success, _ = self.friend_reward(batch=False, friend=friend, apiKey=apiKey)
                if success:
                    self.log(f"{Fore.LIGHTYELLOW_EX}Reward for friend {Fore.LIGHTWHITE_EX}{friend} {Fore.LIGHTYELLOW_EX}получена")
                time.sleep(random.randint(1, 2))

        quests_completed = 0
        for dbQuest in self.dbData['dbQuests']:
            if quests_completed >= 2:
                break
            if dbQuest['isArchived']:
                continue
            if dbQuest['checkType'] != 'fakeCheck':
                continue
            if not any(dbQuest['key'] in quest['key'] for quest in full_profile['quests']):
                if self.quest_reward(quest=dbQuest['key'], apiKey=apiKey):
                    quests_completed += 1
                    self.log(f"{Fore.LIGHTYELLOW_EX}Quest reward {Fore.LIGHTWHITE_EX}{dbQuest['key']} {Fore.LIGHTYELLOW_EX}получена")
                    time.sleep(random.randint(10, 20))

        quiz_key = ''
        quiz_answer = ''
        quiz_req_level = 0
        rebus_key = ''
        rebus_answer = ''
        rebus_req_level = 0
        for quest in self.dbData['dbQuests']:
            if quest['isArchived']:
                continue
            date_start = datetime.strptime(quest['dateStart'], '%Y-%m-%d %H:%M:%S') if quest.get('dateStart') else None
            date_end = datetime.strptime(quest['dateEnd'], '%Y-%m-%d %H:%M:%S') if quest.get('dateEnd') else None
            if date_start:
                date_start = date_start.replace(tzinfo=self.gmt_timezone)
            if date_end:
                date_end = date_end.replace(tzinfo=self.gmt_timezone)
            if date_start and date_end and not (date_start <= cur_time_gmt <= date_end):
                continue
            if 'riddle' in quest['key']:
                quiz_key = quest['key']
                quiz_answer = quest['checkData']
                quiz_req_level = int(quest['requiredLevel'] or 0)
            if 'rebus' in quest['key']:
                rebus_key = quest['key']
                rebus_answer = quest['checkData']
                rebus_req_level = int(quest['requiredLevel'] or 0)

        need_quiz = bool(quiz_key and quiz_answer) and not any(
            quiz_key in quest['key'] for quest in full_profile['quests'])
        need_rebus = bool(rebus_key and rebus_answer) and not any(
            rebus_key in quest['key'] for quest in full_profile['quests'])

        if need_quiz:
            day_end = datetime_time(random.randint(22, 23), random.randint(0, 59))
            self.log(f"{Fore.LIGHTYELLOW_EX}Tonight, the night period will begin at {Fore.LIGHTWHITE_EX}{str(day_end)}")
            if self.level >= quiz_req_level:
                time.sleep(random.randint(2, 4))
                if self.complete_quest(quest=quiz_key, code=quiz_answer, apiKey=apiKey):

                    self.log(f"{Fore.LIGHTYELLOW_EX}Награда за ежедневный квиз получена")
        if need_rebus:
            day_start = datetime_time(random.randint(8, 9), random.randint(0, 59))
            self.log(f"{Fore.LIGHTYELLOW_EX}Tomorrow, the day period will begin at {Fore.LIGHTWHITE_EX}{str(day_start)}")
            if self.level >= rebus_req_level:
                time.sleep(random.randint(2, 4))
                if self.complete_quest(quest=rebus_key, code=rebus_answer, apiKey=apiKey):

                    self.log(f"{Fore.LIGHTYELLOW_EX}Награда за ежедневный ребус получена")

        if config.INVEST_ENABLED:
            helper = self.get_helper(apiKey=apiKey)
            if cur_time_gmt >= new_day_gmt and cur_time_gmt_s in helper:
                helper = helper[cur_time_gmt_s]
                if 'funds' in helper:
                    regular_funds = helper['funds'].get('regular', [])
                    special_fund = helper['funds'].get('special', None)
                    special_fund = special_fund if any(
                        fund['key'] == special_fund for fund in self.dbData['dbFunds']) else None
                    current_funds = self.get_funds_info(apiKey=apiKey)
                    time.sleep(random.randint(4, 8))

                    if regular_funds and 'funds' in current_funds and not current_funds['funds']:
                        funds_to_invest = [special_fund] if special_fund else []
                        funds_to_invest += regular_funds[:2] if special_fund else regular_funds
                        for fund in funds_to_invest:
                            self.invest(fund=fund, apiKey=apiKey, amount=calculate_bet(level=self.level, mph=self.mph, balance=self.balance))
                            time.sleep(random.randint(2, 4))

        if config.MINING_SKILLS_LEVEL > 0:
            my_skills = full_profile['skills']
            friends_count = int(full_profile['profile']['friends'] or 0)
            for skill in self.dbData['dbSkills']:
                if skill['category'] != 'mining':
                    continue
                if skill['key'] in my_skills:
                    if my_skills[skill['key']]['level'] >= config.MINING_SKILLS_LEVEL:
                        continue
                possible_skill = improve_possible(skill, my_skills, self.level, self.balance, friends_count)
                if possible_skill is not None:
                    if self.balance - possible_skill['price'] >= config.PROTECTED_BALANCE:
                        time.sleep(random.randint(1, 2))
                        improve_data = self.improve_skill(skill=possible_skill['key'], apiKey=apiKey)
                        if improve_data is not None:
                            self.log(
                                f"{Fore.LIGHTYELLOW_EX}Gathering skill {Fore.LIGHTWHITE_EX}{possible_skill['key']} {Fore.LIGHTYELLOW_EX}Upgraded to level {Fore.LIGHTWHITE_EX}{possible_skill['newlevel']}")
                        else:
                            break

        if config.SKILLS_COUNT > 0:
            improved_skills = 0
            improve_data = None
            while improved_skills < config.SKILLS_COUNT:
                skill = calculate_best_skill(skills=self.dbData['dbSkills'], ignored_skills=config.IGNORED_SKILLS,
                                             profile=full_profile, level=self.level, balance=self.balance,
                                             improve=improve_data)
                if skill is None:
                    break
                if self.balance - skill['price'] < config.PROTECTED_BALANCE:
                    self.log(f"{Fore.LIGHTYELLOW_EX}Skill improvement stopped (balance protection)")
                    break
                time.sleep(random.randint(2, 4))
                improve_data = self.improve_skill(skill=skill['key'], apiKey=apiKey)
                if improve_data is None:
                    break
                improved_skills += 1
                self.log(f"{Fore.LIGHTYELLOW_EX}Skill {Fore.LIGHTWHITE_EX}{skill['key']} {Fore.LIGHTYELLOW_EX}Upgraded to level {Fore.LIGHTWHITE_EX}{skill['newlevel']}")

        time.sleep(random.randint(2, 4))
        profile = self.get_profile(full=False, apiKey=apiKey)
        self.update_level(level=int(profile['hero']['level'] or 0))
        self.balance = int(profile['hero']['money'] or 0)
        self.mph = int(profile['hero']['moneyPerHour'] or 0)
        self.log(f"{Fore.LIGHTYELLOW_EX}Level: {Fore.LIGHTWHITE_EX}{self.level} | "
                 f"{Fore.LIGHTYELLOW_EX}Balance: {Fore.LIGHTWHITE_EX}{number_short(value=self.balance)} | "
                 f"{Fore.LIGHTYELLOW_EX}Income per hour: {Fore.LIGHTWHITE_EX}+{number_short(value=self.mph)}")

        if config.PVP_ENABLED:
            if self.dbData:
                league_data = None
                selected_league = None
                for league in self.dbData['dbNegotiationsLeague']:
                    if config.PVP_LEAGUE == 'auto':
                        if self.level >= league['requiredLevel'] and self.level <= league['maxLevel']:
                            if league_data is None or league['requiredLevel'] < league_data['requiredLevel']:
                                league_data = league
                    else:
                        if league['key'] == config.PVP_LEAGUE:
                            selected_league = league
                            if self.level >= league['requiredLevel'] and self.level <= league['maxLevel']:
                                league_data = league
                                break

                if config.PVP_LEAGUE != 'auto' and league_data is None:
                    if selected_league:
                        if config.PVP_UPGRADE_LEAGUE:
                            for league in self.dbData['dbNegotiationsLeague']:
                                if league['requiredLevel'] > selected_league['requiredLevel'] and self.level >= league['requiredLevel']:
                                    league_data = league
                                    break
                            self.log(
                                f"{Fore.LIGHTYELLOW_EX}Выбранная лига больше недоступна. Новая лига: {Fore.LIGHTWHITE_EX}{league_data['key']}.")
                        else:
                            config.PVP_ENABLED = False
                            self.log(
                                f"{Fore.LIGHTRED_EX}Выбранная лига больше недоступна. PvP отключены")
                    else:
                        config.PVP_ENABLED = False
                        self.log(f"{Fore.LIGHTRED_EX}PVP_LEAGUE parameter is invalid. PvP disabled")

                if league_data is not None:
                    self.strategies = [strategy['key'] for strategy in self.dbData['dbNegotiationsStrategy']]
                    if config.PVP_STRATEGY == 'random' or config.PVP_STRATEGY in self.strategies:
                        time.sleep(random.randint(2, 4))
                        self.perform_pvp(league=league_data, strategy=config.PVP_STRATEGY, count=config.PVP_COUNT, apiKey=apiKey, id_data=id_data)
                    else:
                        config.PVP_ENABLED = False
                        self.log(f"{Fore.LIGHTRED_EX}Параметр PVP_STRATEGY недействителен. PvP отключены")
            else:
                self.log(f"{Fore.LIGHTRED_EX}База данных отсутствует. PvP на этот раз будут пропущены")

        if config.TAPS_ENABLED:
            per_tap = int(profile['hero']['earns']['task']['moneyPerTap'] or 0)
            max_energy = int(profile['hero']['earns']['task']['limit'] or 0)
            energy = int(profile['hero']['earns']['task']['energy'] or 0)
            bonus_chance = float(profile['hero']['earns']['task']['bonusChance'] or 0)
            bonus_mult = float(profile['hero']['earns']['task']['bonusMultiplier'] or 0)
            if energy == max_energy and not self.taps_limit:
                time.sleep(random.randint(2, 4))
                self.perform_taps(per_tap=per_tap, energy=energy, bonus_chance=bonus_chance, bonus_mult=bonus_mult, apiKey=apiKey)
                time.sleep(random.randint(2, 4))

    def countdown(self, t):
        while t:
            one, two = divmod(t, 3600)
            three, four = divmod(two, 60)
            print(f"{Fore.LIGHTWHITE_EX}Ожидание до {one:02}:{three:02}:{four:02} ", flush=True, end="\r")
            t -= 1
            time.sleep(1)
        print("                          ", flush=True, end="\r")

    def api_call(self, url, data=None, headers=None, method='GET'):
        while True:
            try:
                if method == 'GET':
                    res = self.scraper.get(url, headers=headers)
                elif method == 'POST':
                    res = self.scraper.post(url, headers=headers, data=data)
                else:
                    raise ValueError(f'Не поддерживаемый метод: {method}')

                if res.status_code == 401:
                    self.log(f'{Fore.LIGHTRED_EX}{res.text}')

                return res
            except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout, requests.exceptions.Timeout):
                self.log(f'{Fore.LIGHTRED_EX}Ошибка подключения соединения!')
                break

    def set_sign_headers(self, data: dict, apiKey: str) -> dict:
        time_string = str(int(time_now()))
        json_string = json.dumps(data)
        hash_object = hashlib.md5()
        hash_object.update(f"{time_string}_{json_string}".encode('utf-8'))
        hash_string = hash_object.hexdigest()
        headers = self.base_headers.copy()
        headers["Api-Key"] = f"{apiKey}"
        headers["Api-Time"] = f"{time_string}"
        headers["Api-Hash"] = f"{hash_string}"
        return headers

    def get_profile(self, full: bool, apiKey: str) -> dict:
        full_url = 'https://api.xempire.io/user/data/all'
        after_url = 'https://api.xempire.io/user/data/after'
        sync_url = 'https://api.xempire.io/hero/balance/sync'

        try:
            if full:
                json_data = {'data': {}}

                headers = self.set_sign_headers(data=json_data, apiKey=apiKey)

                response = self.api_call(full_url, headers=headers, data=json.dumps(json_data), method='POST')

                response_text = response.text
                response_json = json.loads(response_text)

                data = response_json['data']

                lang = data.get('settings', {}).get('lang', 'en')
                json_data2 = {'data': {'lang': f"{lang}"}}
                headers2 = self.set_sign_headers(data=json_data2, apiKey=apiKey)
                response2 = self.api_call(after_url, headers=headers2, data=json.dumps(json_data2),  method='POST')


                response_text2 = response2.text
                response_json2 = json.loads(response_text2)
                data.update(response_json2['data'])

                return data
            else:
                json_data = {}

                headers = self.set_sign_headers(data=json_data, apiKey=apiKey)
                response = self.api_call(sync_url, headers=headers, data=json.dumps(json_data), method='POST')
                response.raise_for_status()
                response_text = response.text

                response_json = json.loads(response_text)

                return response_json['data']

        except Exception as error:
            self.log(f"{Fore.LIGHTRED_EX}Profile data error: {error}")
            time.sleep(3)
            return {}

    def update_level(self, level: int) -> None:
        if self.level > 0 and level > self.level:
            self.log(f"{Fore.LIGHTYELLOW_EX}New level gained: {level}")
            self.level = level

    def get_offline_bonus(self, apiKey: str) -> bool:
        url = 'https://api.xempire.io/hero/bonus/offline/claim'
        try:
            json_data = {}
            headers = self.set_sign_headers(data=json_data, apiKey=apiKey)
            response = self.api_call(url, headers=headers, data=json.dumps(json_data), method='POST')
            response.raise_for_status()
            response_text = response.text

            response_json = json.loads(response_text)
            success = response_json.get('success', False)
            if success:
                self.update_level(level=int(response_json['data']['hero']['level']))
                self.balance = int(response_json['data']['hero']['money'])
                self.mph = int(response_json['data']['hero']['moneyPerHour'])
                return True
            else:
                return False

        except Exception as error:
            self.log(f"{Fore.LIGHTRED_EX}Offline bonus error: {error}")
            time.sleep(3)
            return False

    def daily_reward(self, index: int, apiKey: str) -> bool:
        url = 'https://api.xempire.io/quests/daily/claim'
        try:
            json_data = {'data': f"{index}"}
            headers = self.set_sign_headers(data=json_data, apiKey=apiKey)
            response = self.api_call(url, headers=headers, data=json.dumps(json_data), method='POST')
            response.raise_for_status()
            response_text = response.text
            response_json = json.loads(response_text)
            success = response_json.get('success', False)
            if success:
                self.update_level(level=int(response_json['data']['hero']['level']))
                self.balance = int(response_json['data']['hero']['money'])
                self.mph = int(response_json['data']['hero']['moneyPerHour'])
                return True
            else:
                return False

        except Exception as error:
            self.log(f"{Fore.LIGHTRED_EX}Daily reward error: {str(error)}")
            return False

    def quest_reward(self, apiKey: str, quest: str, code: str = None) -> bool:
        url = 'https://api.xempire.io/quests/claim'
        try:
            json_data = {'data': [quest, code]}
            headers = self.set_sign_headers(data=json_data, apiKey=apiKey)
            response = self.api_call(url, headers=headers, data=json.dumps(json_data), method='POST')
            response.raise_for_status()
            response_text = response.text
            response_json = json.loads(response_text)
            success = response_json.get('success', False)
            if success:
                self.update_level(level=int(response_json['data']['hero']['level']))
                self.balance = int(response_json['data']['hero']['money'])
                self.mph = int(response_json['data']['hero']['moneyPerHour'])
                return True
            else:
                return False

        except Exception as error:
            self.log(f"{Fore.LIGHTRED_EX}Quest error: {str(error)}")
            return False

    def daily_quests(self, apiKey: str) -> None:
        url = 'https://api.xempire.io/quests/daily/progress/all'
        try:
            json_data = {}
            headers = self.set_sign_headers(data=json_data, apiKey=apiKey)
            response = self.api_call(url, headers=headers, data=json.dumps(json_data), method='POST')
            response.raise_for_status()
            response_text = response.text
            response_json = json.loads(response_text)
            success = response_json.get('success', False)
            if success:
                for name, quest in response_json['data'].items():

                    if 'youtube' in name and not quest["isRewarded"]:
                        continue

        except Exception as error:
            self.log(f"{Fore.LIGHTRED_EX}Ошибка ежедневного квеста: {str(error)}")

    def daily_quest_reward(self, apiKey: str, quest: str, code: str = None) -> bool:
        url = 'https://api.xempire.io/quests/daily/progress/claim'
        try:
            json_data = {'data': {'quest': quest, 'code': code}}
            headers = self.set_sign_headers(data=json_data, apiKey=apiKey)
            response = self.api_call(url, headers=headers, data=json.dumps(json_data), method='POST')
            response.raise_for_status()
            response_text = response.text
            response_json = json.loads(response_text)
            success = response_json.get('success', False)
            if success:
                self.update_level(level=int(response_json['data']['hero']['level']))
                self.balance = int(response_json['data']['hero']['money'])
                self.mph = int(response_json['data']['hero']['moneyPerHour'])
                return True
            else:
                return False

        except Exception as error:
            self.log(f"{Fore.LIGHTRED_EX}Ошибка награды за ежедневный квест: {str(error)}")
            return False

    def open_boxes(self, apiKey: str) -> None:
        url_list = 'https://api.xempire.io/box/list'
        url_open = 'https://api.xempire.io/box/open'
        try:
            json_data = {}
            headers = self.set_sign_headers(data=json_data, apiKey=apiKey)
            response = self.api_call(url_list, headers=headers, data=json.dumps(json_data), method='POST')
            response.raise_for_status()
            response_text = response.text
            response_json = json.loads(response_text)
            success = response_json.get('success', False)
            if success and response_json['data']:
                for name, _ in response_json['data'].items():
                    json_data = {'data': name}
                    headers2 = self.set_sign_headers(data=json_data, apiKey=apiKey)
                    res = self.api_call(url_open, headers=headers2, data=json.dumps(json_data), method='POST')
                    res.raise_for_status()
                    res_text = res.text
                    res_json = json.loads(res_text)
                    success = res_json.get('success', False)
                    if success and res_json['data']['loot']:
                        self.log(f"Box {name} opened")

        except Exception as error:
            self.log(f"{Fore.LIGHTRED_EX}Error opening boxes: {str(error)}")

    def friend_reward(self, apiKey: str, batch: bool = False, friend: int = 0) -> tuple[bool, list]:
        url_claim = 'https://api.xempire.io/friends/claim'
        url_batch = 'https://api.xempire.io/friends/claim/batch'
        try:
            if batch:
                json_data = {}
                url = url_batch
            else:
                json_data = {'data': friend}
                url = url_claim
            headers = self.set_sign_headers(data=json_data, apiKey=apiKey)
            response = self.api_call(url, headers=headers, data=json.dumps(json_data), method='POST')
            response.raise_for_status()
            response_text = response.text
            response_json = json.loads(response_text)
            success = response_json.get('success', False)
            if success:
                self.update_level(level=int(response_json['data']['hero']['level']))
                self.balance = int(response_json['data']['hero']['money'])
                self.mph = int(response_json['data']['hero']['moneyPerHour'])
                return True, response_json['data']['friends']
            else:
                return False, []

        except Exception as error:
            self.log(f"{Fore.LIGHTRED_EX}Ошибка награды за друга: {str(error)}")
            return False, []

    def complete_quest(self, quest: str, code: str, apiKey: str) -> bool:
        url = 'https://api.xempire.io/quests/check'
        try:
            json_data = {'data': [quest, code]}
            headers = self.set_sign_headers(data=json_data, apiKey=apiKey)
            response = self.api_call(url, headers=headers, data=json.dumps(json_data), method='POST')
            response.raise_for_status()
            response_text = response.text
            response_json = json.loads(response_text)
            if response_json.get('success', False) and response_json['data'].get('result', False):
                time.sleep(2)
                if self.quest_reward(quest=quest, code=code, apiKey=apiKey):
                    return True
            return False

        except Exception as error:
            self.log(f"{Fore.LIGHTRED_EX}Ошибка выполнения квеста: {str(error)}")
            return False

    def get_helper(self, apiKey: str) -> dict:
        url = 'https://eeyjey.pro/crypto/x-empire/data/'
        try:
            json_data = {'data': 'eeyjey'}
            headers = self.set_sign_headers(data=json_data, apiKey=apiKey)
            response = self.api_call(url, headers=headers, data=json.dumps(json_data), method='POST')
            print(f'{response}')
            if response.status_code in {200, 400, 401, 403}:
                response_json = response.json()
                print(f'{response_json}')
                success = response_json.get('success', False)
                print(f'{success}')
                if success:
                    return response_json.get('result', {})
                else:
                    self.log(
                        f"{Fore.LIGHTRED_EX}Ошибка хелпера: {response.status_code} {response_json.get('message', '')}")
                    return {}
        except Exception as error:
            self.log(f"{Fore.LIGHTRED_EX}Ошибка хелпера: {str(error)}")
            return {}

    def get_funds_info(self, apiKey: str) -> dict:
        url = 'https://api.xempire.io/fund/info'
        try:
            json_data = {}
            headers = self.set_sign_headers(data=json_data, apiKey=apiKey)
            response = self.api_call(url, headers=headers, data=json.dumps(json_data), method='POST')
            response.raise_for_status()
            response_text = response.text
            response_json = json.loads(response_text)
            return response_json['data']

        except Exception as error:
            self.log(f"{Fore.LIGHTRED_EX}Ошибка инвестиций: {error}")
            time.sleep(3)
            return {}

    def invest(self, fund: str, amount: int, apiKey: str) -> None:
        url = 'https://api.xempire.io/fund/invest'
        if self.balance < amount:
            self.log(f"{Fore.LIGHTRED_EX}No money for investments")
            return
        if self.balance - amount < config.PROTECTED_BALANCE:
            self.log(f"{Fore.LIGHTRED_EX}Skipping investment (Balance protection))")
            return
        try:
            json_data = {'data': {'fund': fund, 'money': amount}}
            headers = self.set_sign_headers(data=json_data, apiKey=apiKey)
            response = self.api_call(url, headers=headers, data=json.dumps(json_data), method='POST')
            response.raise_for_status()
            response_text = response.text
            response_json = json.loads(response_text)
            success = response_json.get('success', False)
            if success:
                self.update_level(level=int(response_json['data']['hero']['level']))
                self.balance = int(response_json['data']['hero']['money'])
                self.mph = int(response_json['data']['hero']['moneyPerHour'])
                for fnd in response_json['data']['funds']:
                    if fnd['fundKey'] == fund:
                        money = fnd['moneyProfit']
                        money_str = f"{Fore.LIGHTYELLOW_EX}Profit: +{number_short(value=money)}" if money > 0 else (
                            f"{Fore.LIGHTRED_EX}Loss: {number_short(value=money)}" if money < 0 else "Profit: 0")
                        self.log(
                            f"{Fore.LIGHTYELLOW_EX}Инвестировал {Fore.LIGHTWHITE_EX}{number_short(value=amount)} {Fore.LIGHTYELLOW_EX}в {Fore.LIGHTWHITE_EX}{fund} {money_str}")
                        break

        except Exception as error:
            self.log(f"{Fore.LIGHTRED_EX}Ошибка инвестиций: {str(error)}")

    def improve_skill(self, skill: str, apiKey: str) -> dict | None:
        url = 'https://api.xempire.io/skills/improve'
        try:
            json_data = {'data': skill}
            headers = self.set_sign_headers(data=json_data, apiKey=apiKey)
            response = self.api_call(url, headers=headers, data=json.dumps(json_data), method='POST')
            response.raise_for_status()
            response_text = response.text
            response_json = json.loads(response_text)
            success = response_json.get('success', False)
            if success:
                self.update_level(level=int(response_json['data']['hero']['level']))
                self.balance = int(response_json['data']['hero']['money'])
                self.mph = int(response_json['data']['hero']['moneyPerHour'])
                return response_json['data']
            else:
                return None

        except Exception as error:
            self.log(f"{Fore.LIGHTRED_EX}Skill improvement error: {str(error)}")
            return None

    def perform_pvp(self, league: dict, strategy: str, count: int, apiKey: str, id_data: Data) -> None:
        url_fight = 'https://api.xempire.io/pvp/start/fight'
        url_cancel = 'https://api.xempire.io/pvp/fight/cancel'
        url_claim = 'https://api.xempire.io/pvp/claim'
        self.log(f"{Fore.LIGHTYELLOW_EX}Началось PvP. Лига: {Fore.LIGHTWHITE_EX}{league['key']} {Fore.LIGHTYELLOW_EX}Стратегия: {Fore.LIGHTWHITE_EX}{strategy}")
        time.sleep(3)
        curent_strategy = strategy
        money = 0
        search_attempts = 0
        while count > 0:
            if self.balance < int(league['maxContract']):
                money_str = f"Profit: +{number_short(value=money)}" if money > 0 else (
                    f"Loss: {number_short(value=money)}" if money < 0 else "Profit: 0")
                self.log(f"{Fore.LIGHTRED_EX}PvP stopped (no money) {Fore.LIGHTWHITE_EX}{money_str}")
                break
            if self.balance - int(league['maxContract']) < config.PROTECTED_BALANCE:
                money_str = f"Profit: +{number_short(value=money)}" if money > 0 else (
                    f"Loss: {number_short(value=money)}" if money < 0 else "Profit: 0")
                self.log(f"{Fore.LIGHTRED_EX}PvP остановлен (защита Balanceа) {Fore.LIGHTWHITE_EX}{money_str}")
                break

            if strategy == 'random':
                curent_strategy = random.choice(self.strategies)

            self.log(f"SПоиск оппонента...")
            try:
                search_attempts += 1
                json_data = {'data': {'league': league['key'], 'strategy': curent_strategy}}
                headers = self.set_sign_headers(data=json_data, apiKey=apiKey)
                response = self.api_call(url_fight, headers=headers, data=json.dumps(json_data), method='POST')
                response.raise_for_status()
                response_text = response.text
                response_json = json.loads(response_text)
                success = response_json.get('success', False)
                op = response_json['data']
                op2 = response_json["data"].get("opponent")
                print(f"{op}")
                print(f"{op2}")
                if success:
                    if response_json['data']['opponent'] is None:

                        if search_attempts > 2:
                            json_data = {}
                            headers = self.set_sign_headers(data=json_data, apiKey=apiKey)
                            self.api_call(url_cancel, headers=headers, data=json.dumps(json_data),
                                                     method='POST')
                            search_attempts = 0
                            self.log(f"Поиск закрыт")
                        time.sleep(random.randint(5, 10))
                        continue

                    time.sleep(random.randint(6, 7))
                    count -= 1
                    search_attempts = 0
                    if int(response_json['data']['fight']['player1']) == id_data.id:
                        opponent_strategy = response_json['data']['fight']['player2Strategy']
                    else:
                        opponent_strategy = response_json['data']['fight']['player1Strategy']
                    money_contract = response_json['data']['fight']['moneyContract']
                    money_profit = response_json['data']['fight']['moneyProfit']
                    winner = int(response_json['data']['fight']['winner'])
                    if winner == id_data.id:
                        money += money_profit
                        self.log(f"{Fore.LIGHTYELLOW_EX}Сумма на кону: {Fore.LIGHTWHITE_EX}{number_short(value=money_contract)} | "
                                    f"{Fore.LIGHTYELLOW_EX}Твоя стратегия: {Fore.LIGHTWHITE_EX}{curent_strategy} | "
                                    f"{Fore.LIGHTYELLOW_EX}Стратегия опоонента: {Fore.LIGHTWHITE_EX}{opponent_strategy} | "
                                    f"{Fore.LIGHTYELLOW_EX}ПОБЕДИЛ {Fore.LIGHTWHITE_EX}(+{number_short(value=money_profit)})")
                    else:
                        money -= money_contract
                        self.log(f"{Fore.LIGHTYELLOW_EX}Сумма на кону: {Fore.LIGHTWHITE_EX}{number_short(value=money_contract)} | "
                                    f"{Fore.LIGHTYELLOW_EX}Твоя стратегия: {Fore.LIGHTWHITE_EX}{curent_strategy} | "
                                    f"{Fore.LIGHTYELLOW_EX}Стратегия опоонента: {Fore.LIGHTWHITE_EX}{opponent_strategy} | "
                                    f"{Fore.LIGHTRED_EX}ПРОИГРАЛ {Fore.LIGHTWHITE_EX}(-{number_short(value=money_contract)})")

                    json_data = {}
                    headers = self.set_sign_headers(data=json_data, apiKey=apiKey)
                    response = self.api_call(url_claim, headers=headers, data=json.dumps(json_data), method='POST')
                    response.raise_for_status()
                    response_text = response.text
                    response_json = json.loads(response_text)
                    success = response_json.get('success', False)
                    if success:
                        self.update_level(level=int(response_json['data']['hero']['level']))
                        self.balance = int(response_json['data']['hero']['money'])
                        self.mph = int(response_json['data']['hero']['moneyPerHour'])

                    time.sleep(random.randint(3, 5))

            except Exception as error:
                self.log(f"PvP error: {str(error)}")
                time.sleep(3)
            time.sleep(random.randint(15, 20))
        money_str = f"Profit: +{number_short(value=money)}" if money > 0 else (
            f"Loss: {number_short(value=money)}" if money < 0 else "Profit: 0")
        self.log(f"{Fore.LIGHTYELLOW_EX}PvP ended {Fore.LIGHTWHITE_EX}{money_str}")

    def get_tap_limit(self) -> int:
        for level_info in self.dbData['dbLevels']:
            if level_info['level'] == self.level:
                return int(level_info['tapLimit'] or 0)
        return 0

    def perform_taps(self, per_tap: int, energy: int, bonus_chance: float, bonus_mult: float, apiKey: str) -> None:
        url = 'https://api.xempire.io/hero/action/tap'
        self.log(f"{Fore.LIGHTYELLOW_EX}Started tapping. Coins per tap: {Fore.LIGHTWHITE_EX}{per_tap} | {Fore.LIGHTYELLOW_EX}Бонус: {Fore.LIGHTWHITE_EX}{bonus_chance:.2f} | {Fore.LIGHTYELLOW_EX}Multiplier: {Fore.LIGHTWHITE_EX}{bonus_mult:.2f}")
        tap_limit = self.get_tap_limit()
        taps_over = False
        last = False
        while not last:
            taps_per_second = random.randint(*config.TAPS_PER_SECOND)
            seconds = random.randint(4, 6)
            taps_sum = taps_per_second * seconds
            earned_money = 0
            for i in range(1, taps_sum + 1):
                tap_power = calculate_tap_power(per_tap, energy, bonus_chance, bonus_mult)
                earned_money += tap_power
                energy -= 0.7 * tap_power
            if energy < per_tap: last = True
            time.sleep(seconds)
            try:
                json_data = {
                    'data': {'data': {'task': {'amount': earned_money, 'currentEnergy': energy}}, 'seconds': seconds}}
                headers = self.set_sign_headers(data=json_data, apiKey=apiKey)
                response = self.api_call(url, headers=headers, data=json.dumps(json_data), method='POST')
                response.raise_for_status()
                response_text = response.text
                response_json = json.loads(response_text)
                success = response_json.get('success', False)
                error = response_json.get('error', '')
                if success:
                    self.update_level(level=int(response_json['data']['hero']['level']))
                    self.balance = int(response_json['data']['hero']['money'])
                    self.mph = int(response_json['data']['hero']['moneyPerHour'])
                    energy = int(response_json['data']['hero']['earns']['task']['energy'])
                    tapped_today = int(response_json['data']['tapped_today'])
                    self.log(f"{Fore.LIGHTYELLOW_EX}Received: {Fore.LIGHTWHITE_EX}+{number_short(value=earned_money)} {Fore.LIGHTYELLOW_EX}Energy remaining: {Fore.LIGHTWHITE_EX}{number_short(value=energy)}")
                    if tapped_today >= tap_limit:
                        taps_over = True
                    if last and not taps_over:
                        self.log(f"{Fore.LIGHTRED_EX}Tap stop (no energy)")
                elif 'too many taps' in error:
                    taps_over = True

                if taps_over:
                    self.log(f"{Fore.LIGHTRED_EX}Остановка тапов (Tap limit reached)")
                    self.taps_limit = True
                    cur_time_gmt = datetime.now(self.gmt_timezone)
                    self.taps_limit_date = cur_time_gmt.strftime('%Y-%m-%d')
                    last = True

            except Exception as error:
                self.log(f"Taps error: {str(error)}")
                break

    def log(self, message):
        now = datetime.now().isoformat(" ").split(".")[0]
        print(f"{Fore.LIGHTBLACK_EX}[{now}]{Style.RESET_ALL} {message}")


if Data is None:
    def log(message):
        now = datetime.now().isoformat(" ").split(".")[0]
        print(f"{Fore.LIGHTBLACK_EX}[{now}]{Style.RESET_ALL} {message}")


if __name__ == "__main__":
    try:
        app = PixelTod()
        app.main()
    except KeyboardInterrupt:
        sys.exit()
