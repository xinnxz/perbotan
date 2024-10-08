import time
from colorama import *
import concurrent.futures
from utils.queries import MUTATION_GAME_PROCESS_TAPS_BATCH
from utils.utils import (
    cek_stat,cek_user, claim_combo, activate_energy_recharge_booster, 
    activate_booster ,set_next_boss, submit_taps, _number
    )
from utils.helpers import (
    clear_screen, countdown_timer,
    log, htm,pth,hju,bru,mrh,kng,print_banner,
    generate_random_nonce, read_config
    )

init(autoreset=True)
config = read_config()

def main():
    clear_screen()
    print_banner()
    energy_booster = config.get('energy_booster', False)
    turbo_booster = config.get('turbo_booster', False)
    auto_claim_combo = config.get('auto_claim_combo', False)
    crazy_damage = config.get('crazy_damage',False)
    ACCOUNT_DELAY = config.get('ACCOUNT_DELAY', 0)
    LOOP_COUNTDOWN = config.get('LOOP_COUNTDOWN', 10)

    with open('query_id.txt', 'r') as file:
        account_lines = file.readlines()

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:  
        future_to_index = {executor.submit(cek_user, index): index for index in range(len(account_lines))}

        for future in concurrent.futures.as_completed(future_to_index):
            index = future_to_index[future]
            try:
                result = future.result()
                if result:
                    user_name = result.get('username', 'Unknown')
                    first_name = result.get('firstName', 'Unknown')
                    league = result.get('league', 'Unknown')
                    headers = {'Authorization': f'Bearer {result}'}
                    stat_result = cek_stat(index, headers)
                    if stat_result:
                        user_data = stat_result
                    log(bru + f"Account number : {pth}{index + 1}")
                    log(pth + "~" * 40)
                    log(kng + f"{user_name} {hju}in {pth}{league} {hju}league")
                    log(hju + f"Total balance {kng}{_number(stat_result['coinsAmount'])} {hju}coins")
                    log(hju + f"Have Free : {pth}{stat_result['freeBoosts']['currentTurboAmount']} {hju}TURBO {kng}& {pth}{stat_result['freeBoosts']['currentRefillEnergyAmount']} {hju}ENERGY")
                    log(hju + f"Boss lv. {pth}{stat_result['currentBoss']['level']} {hju}/ id {kng}({stat_result['currentBoss']['_id']})")
                    log(hju + f"Boss health {mrh}{_number(stat_result['currentBoss']['currentHealth'])} {kng}/ {hju}{_number(stat_result['currentBoss']['maxHealth'])}")
                else:
                    log(hju + f"{first_name} {kng}League {league}{mrh} failed          ", end="\r", flush=True)
                    log(htm + "~" * 40)

                level_bos = user_data['currentBoss']['level']
                bos_health = user_data['currentBoss']['currentHealth']

                if auto_claim_combo == True:
                    claim_combo(index, headers)

                while bos_health > 0:
                    current_energy = user_data['currentEnergy']
                    max_energy = user_data['maxEnergy']
                    damage = user_data['weaponLevel'] + 1
                    total_tap = current_energy // damage
                    hit_boss = current_energy - damage
                    
                    tap_payload = {
                        "operationName": "MutationGameProcessTapsBatch",
                        "variables": {
                            "payload": {
                                "nonce": generate_random_nonce(),
                                "tapsCount": total_tap
                            }
                        },
                        "query": MUTATION_GAME_PROCESS_TAPS_BATCH
                    }
                    tap_result = submit_taps(index, tap_payload)
                    if tap_result is not None:
                        bos_health -= hit_boss
                        stat_result = cek_stat(index, headers)
                        user_data = stat_result
                        current_energy = user_data['currentEnergy']
                        log(hju + f"Fight with Level {pth}{user_data['currentBoss']['level']} {hju}boss")
                        log(hju + f"Gave a total {mrh}{_number(hit_boss)} HIT {hju}to boss")
                        log(hju + f"Boss health after {mrh}{_number(bos_health)}")
                        time.sleep(1)

                    if energy_booster == True:
                        if current_energy < 0.25 * max_energy:
                            gasken = user_data['freeBoosts']['currentRefillEnergyAmount'] > 0
                            if gasken :
                                log(hju + f"Energy {bru}depleted, {hju}recharging Booster ")
                                activate_energy_recharge_booster(index, headers)
                                stat_result = cek_stat(index, headers)
                                user_data = stat_result
                                current_energy = user_data['currentEnergy']
                                time.sleep(1)
                            else:
                                log(kng + f"Energy depleted, no booster available", flush=True)
                                break
                    else:
                        log(kng + f"Energy Booster is not activate", flush=True)
                        break
                    
                    if current_energy < damage:
                        log(kng + "Insufficient energy to continue, exiting loop.")
                        break

                    if level_bos == 13 and bos_health == 0:
                        log(kng + f"{hju}waiting {kng}dev add boss level {pth}{user_data['currentBoss']['level'] + 1}")
                        break

                    if bos_health == 0:
                        log(hju + f"lv. {pth}{user_data['currentBoss']['level']} {hju}boss die, looking for the next boss.", flush=True)
                        set_next_boss(index, headers)
                        log(hju + f"Success found new lvl {pth}{user_data['currentBoss']['level']} {hju}boss", flush=True)
                        break

                if turbo_booster == True: 
                    if user_data['freeBoosts']['currentTurboAmount'] > 0:
                        activate_booster(index, headers)
                    else :
                        log(kng + f"Turbo booster is not available", flush=True)
                        
                if crazy_damage == True:  
                    if user_data['freeBoosts']['currentTurboAmount'] > 0:
                        activate_booster(index, headers)
                    else :
                        log(kng + f"Turbo booster is not available", flush=True)
                        
            except Exception as exc:
                log(mrh + f"Account {pth}{index + 1} {mrh}generated an exception: {pth}{exc}")
            log(htm + f"~" * 40)
            countdown_timer(ACCOUNT_DELAY)
        log(pth + f"All warriors have been processed..")
        countdown_timer(LOOP_COUNTDOWN)  

if __name__ == '__main__':
    main()
