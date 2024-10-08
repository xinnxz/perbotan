import json,time,asyncio,websockets,requests, os, sys, threading
from concurrent.futures import ThreadPoolExecutor
from core.headers import headers
from core.info import get_user_dao, get_token, get_username, get_info_energy, get_info_coin, config
from datetime import datetime

energy_global = None
coins_global = None
class Task:
    def __init__(self, tokens):
        self.tokens = tokens
        self.user_dao = [None] * len(tokens)
        self.socket_tokens = [None] * len(tokens)
        self.counter = [0] * len(tokens)
        self.info = [{} for _ in range(len(tokens))]  # Initialize self.info as a list of dictionaries
    
    def clear_terminal(self):
        """Clears the terminal screen."""
        if os.name == 'nt':
            os.system('cls')  # For Windows
        else:
            os.system('clear')  # For Linux/Unix
    
    def check_energy(self):
        now = datetime.now()
        dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
        while True:
            for i in range(len(self.tokens)):
                energy = get_info_energy(self.tokens[i])
                coins = get_info_coin(self.tokens[i])
                self.info[i]['energy'] = energy
                print(f"{dt_string}   Real-time Check: (Energy:{energy}, Coins:{coins})")
                if energy < 5:
                    print(f"Energy is too low, stopping mining for this token.")
                    os.execl(sys.executable, *sys.orig_argv)
                    time.sleep(10)  # Check every 10 seconds
                # self.clear_terminal()
                time.sleep(10)  # Check every 10 seconds
            
    def apply_changes(self, account_index, msg):
        if 'rpc' not in msg:
            return
        self.info[account_index]['energy'] = msg['rpc']['data'].get('energy', 0)
        self.info[account_index]['coins'] = msg['rpc']['data'].get('coins', 0)
        self.info[account_index]['profit'] = msg['rpc']['data'].get('dao_coins', 0)

    def auth_message(self, account_index):
        self.counter[account_index] += 1
        return json.dumps({
            "connect": {
                "token": self.socket_tokens[account_index],
                "name": "js"
            },
            "id": self.counter[account_index]
        })

    def click_message(self, account_index):
        self.counter[account_index] += 1
        return json.dumps({
            "publish": {
                "channel": f"dao:{self.user_dao[account_index]['id']}",
                "data": {}
            },
            "id": self.counter[account_index]
        })

    def display_message(self, account_index):
        self.counter[account_index] += 1
        return json.dumps({
            "rpc": {
                "method": "sync",
                "data": {}
            },
            "id": self.counter[account_index]
        })

    async def start_async_mining(self, account_index):
        uri = 'wss://ws.production.tonxdao.app/ws'
        now = datetime.now()
        dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
        async with websockets.connect(uri) as websocket:
            while True:
                await websocket.send(self.auth_message(account_index))
                response = await websocket.recv()
                # print(f"detail:{response}")
                await websocket.send(self.click_message(account_index))

                time.sleep(config('delay_in_sending_message', .02))

                for _ in range(config('number_of_display_message', 2)):
                    await websocket.send(self.display_message(account_index))
                    response = await websocket.recv()
                    response_data = json.loads(response)
                    if 'rpc' in response_data:
                        global energy_global
                        global coins_global
                        energy_global = response_data["rpc"]["data"]["energy"]
                        coins_global = response_data["rpc"]["data"]["coins"]
                        print(f"{dt_string} Energy: {energy_global} Coins: {coins_global}")
                    self.apply_changes(account_index, json.loads(response))
                    
                if energy_global < 5:
                    print(f"Energy is too low ({energy_global}). Stopping mining for this token.")
                    return False 

    def run_websocket(self, account_index):
        asyncio.run(self.start_async_mining(account_index))

    def __mining(self):
        while True:
            try:
                with ThreadPoolExecutor(max_workers=len(self.tokens)) as executor:
                    futures = [executor.submit(self.run_websocket, account_index) for account_index in range(len(self.tokens))]
                    for future in futures:
                        future.result()
                        # print(f"future:{future}") 
                if energy_global > 5:
                    input()
                else:
                    return False

            except KeyboardInterrupt:
                break
            except Exception as E:
                # print(E)
                pass
            

    def start_mining(self):
        # Start a thread to check energy in real-time
        # energy_thread = threading.Thread(target=self.check_energy)
        # energy_thread.daemon = True  # This allows the thread to exit when the main program does
        # energy_thread.start()
        
        for i in range(len(self.tokens)):
            self.user_dao[i] = get_user_dao(self.tokens[i])
            time.sleep(1)

        for i in range(len(self.tokens)):
            self.socket_tokens[i] = get_token(self.tokens[i])
            self.info[i]['name'] = get_username(self.tokens[i])
            energy = get_info_energy(self.tokens[i])
            time.sleep(1)
            # if(get_info_energy(self.tokens[i]) < 611):
            #     time.sleep(1)
            #     self.clear_terminal()
           
                
        self.__mining()
    
    