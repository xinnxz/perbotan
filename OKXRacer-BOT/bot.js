const fs = require('fs');
const path = require('path');
const axios = require('axios');
const colors = require('colors');
const readline = require('readline');

class OKX_RACER {
    headers() {
        return {
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9",
            "App-Type": "web",
            "Content-Type": "application/json",
            "Origin": "https://www.okx.com",
            "Referer": "https://www.okx.com/mini-app/racer?tgWebAppStartParam=linkCode_114965710",
            "Sec-Ch-Ua": '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127", "Microsoft Edge WebView2";v="127"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0",
            "X-Cdn": "https://www.okx.com",
            "X-Locale": "en_US",
            "X-Utc": "7",
            "X-Zkdex-Env": "0"
        };
    }

    async sendRequest(extUserId, extUserName, queryId) {
        const url = `https://www.okx.com/priapi/v1/affiliate/game/racer/info?t=${Date.now()}`;
        const headers = { ...this.headers(), 'X-Telegram-Init-Data': queryId };
        const payload = {
            "extUserId": extUserId,
            "extUserName": extUserName,
            "gameId": 1,
            "linkCode": "114965710"
        };

        return axios.post(url, payload, { headers });
    }

    async getCheckin(extUserId, queryId) {
        const url = `https://www.okx.com/priapi/v1/affiliate/game/racer/tasks?t=${Date.now()}`;
        const headers = { ...this.headers(), 'X-Telegram-Init-Data': queryId };
        try {
            const response = await axios.get(url, { headers });
            const tasks = response.data.data;
            const dailyCheckInTask = tasks.find(task => task.id === 4);
            if (dailyCheckInTask) {
                if (dailyCheckInTask.state === 0) {
                    console.log(`[      Checkin      ]:`.green + ` Mulai check-in...`.yellow);
                    await this.doCheckin(extUserId, dailyCheckInTask.id, queryId);
                } else {
                    console.log(`[      Checkin      ]:`.green + ` Anda sudah check-in hari ini!`.yellow);
                }
            }
        } catch (error) {
            console.log(`Error saat memeriksa hadiah harian: ${error.message}`);
        }
    }

    async doCheckin(extUserId, taskId, queryId) {
        const url = `https://www.okx.com/priapi/v1/affiliate/game/racer/task?t=${Date.now()}`;
        const headers = { ...this.headers(), 'X-Telegram-Init-Data': queryId };
        const payload = {
            "extUserId": extUserId,
            "id": taskId
        };

        try {
            await axios.post(url, payload, { headers });
            console.log(`[      Checkin      ]:`.green + ` Check-in harian berhasil!`.green);
        } catch (error) {
            console.log(`Error: ${error.message}`);
        }
    }

    async processTasks(extUserId, queryId) {
        const url = `https://www.okx.com/priapi/v1/affiliate/game/racer/group-tasks?t=${Date.now()}`
        const headers = { ...this.headers(), 'X-Telegram-Init-Data': queryId };

        try {

            const response = await axios.get(url, { headers });
            const taskGroups = response.data.data.taskGroups;

            for (const group of taskGroups) {

                console.log(`[     Group Task    ]: ${`Sedang menyelesaikan task pada group ${group.groupName.cyan}`.yellow}`.green);
    
                for (const task of group.tasks) {
                    if (task.state === 0) {
                        console.log(`[        Task       ]: Memproses task ${task.context.name.cyan}`.yellow);
                        await this.completeTask(extUserId, task.id, queryId);
                    } else {
                        console.log(`[        Task       ]: Task ${task.context.name.cyan} ${`sudah selesai`.green}`.green);
                    }
                }
            }
        } catch (error) {
            console.log(`[        Task       ]: Error saat menyelesaikan task ${task.context.name.cyan}: ${error.message}`.red);
        }
    }

    async completeTask(extUserId, taskId, queryId) {
        const url = `https://www.okx.com/priapi/v1/affiliate/game/racer/group-tasks?t=${Date.now()}`
        const headers = { ...this.headers(), 'X-Telegram-Init-Data': queryId };
    
        try {
            const response = await axios.get(url, { headers });
            const taskGroups = response.data.data.taskGroups;

            let taskName = 'Unknown';
    
            for (const group of taskGroups) {
                const task = group.tasks.find(task => task.id === taskId);
                if (task) {
                    taskName = task.context.name;
                    break;
                }
            }

            await axios.post(`https://www.okx.com/priapi/v1/affiliate/game/racer/task?t=${Date.now()}`, { extUserId, id: taskId }, { headers });
            console.log(`[        Task       ]: Task ${taskName.cyan} ${`berhasil diselesaikan`.green}`.green);

            await new Promise(resolve => setTimeout(resolve, 2000));
            const { data: { data: { taskGroups: updatedTaskGroups } } } = await axios.get(`https://www.okx.com/priapi/v1/affiliate/game/racer/group-tasks?t=${Date.now()}`, { headers });
    
            let taskCompleted = false;
            for (const group of updatedTaskGroups) {
                const task = group.tasks.find(task => task.id === taskId);
                if (task && task.state === 1) {
                    taskCompleted = true;
                    break;
                }
            }
    
            if (taskCompleted) {
                console.log(`[        Task       ]: Task ${taskName.cyan} ${`dikonfirmasi telah selesai`.green}`.green);
            } else {
                console.log(`[        Task       ]: Task ${taskName.cyan} ${`dikonfirmasi belum selesai`.red}`.red);
            }
        } catch (error) {
            console.log(`[        Task       ]: Error saat menyelesaikan task ${taskName.cyan}: ${error.message}`.red);
        }
    }

    async getBoosts(queryId) {
        const url = `https://www.okx.com/priapi/v1/affiliate/game/racer/boosts?t=${Date.now()}`;
        const headers = { ...this.headers(), 'X-Telegram-Init-Data': queryId };
    
        try {
            const response = await axios.get(url, { headers });
            const boosts = response.data.data;
    
            boosts.forEach(boost => {
                switch (boost.id) {
                    case 8:
                        console.log(`[    Auto-Driving   ]: ${`${boost.curStage}`.cyan} / ${`${boost.totalStage}`.cyan}`.green);
                        break;
                    case 1:
                        console.log(`[  Reload Fuel Tank ]: ${`${boost.curStage}`.cyan} / ${`${boost.totalStage}`.cyan}`.green);
                        break;
                    case 2:
                        console.log(`[      Fuel Tank    ]: ${`${boost.curStage}`.cyan} / ${`${boost.totalStage}`.cyan}`.green);
                        break;
                    case 3:
                        console.log(`[    Turbo Charger  ]: ${`${boost.curStage}`.cyan} / ${`${boost.totalStage}`.cyan}`.green);
                        break;
                    default:
                        console.log(`[    ${boost.context.name}   ]: ${`${boost.curStage}`.cyan} / ${`${boost.totalStage}`.cyan}`.green);
                        break;
                }
            });
    
            return boosts;
        } catch (error) {
            console.log(`Error mengambil informasi boosts: ${error.message}`);
            return [];
        }
    }

    async useBoost(queryId) {
        const url = `https://www.okx.com/priapi/v1/affiliate/game/racer/boost?t=${Date.now()}`;
        const headers = { ...this.headers(), 'X-Telegram-Init-Data': queryId };
        const payload = { id: 1 };

        try {
            const response = await axios.post(url, payload, { headers });
            if (response.data.code === 0) {
                console.log(`\n${`===================`.blue} ${`[ Reload Fuel Tank Berhasil ]`.yellow} ${`===================`.blue}\n`);
                await this.Countdown(5);
            } else {
                console.log(`Error Reload Fuel Tank: ${response.data.msg}`.red);
            }
        } catch (error) {
            console.log(`Error: ${error.message}`.red);
        }
    }

    async upgradeFuelTank(queryId) {
        const url = `https://www.okx.com/priapi/v1/affiliate/game/racer/boost?t=${Date.now()}`;
        const headers = { ...this.headers(), 'X-Telegram-Init-Data': queryId };
        const payload = { id: 2 };
    
        try {
            const response = await axios.post(url, payload, { headers });
            if (response.data.code === 0) {
                console.log(`[    Up Fuel Tank   ]: `.green + `Upgrade Fuel Tank Berhasil`.cyan);
            } else {
                console.log(`[    Up Fuel Tank   ]: `.red + ` ${response.data.msg}`.red);
            }
        } catch (error) {
            console.log(`Error: ${error.message}`.red);
        }
    }

    async upgradeTurboCharger(queryId) {
        const url = `https://www.okx.com/priapi/v1/affiliate/game/racer/boost?t=${Date.now()}`;
        const headers = { ...this.headers(), 'X-Telegram-Init-Data': queryId };
        const payload = { id: 3 };
    
        try {
            const response = await axios.post(url, payload, { headers });
            if (response.data.code === 0) {
                console.log(`[  Up Turbo Charger ]: `.green + `Upgrade Turbo Charger Berhasil`.cyan);
            } else {
                console.log(`[  Up Turbo Charger ]: `.red + `${response.data.msg}`.red);
            }
        } catch (error) {
            console.log(`Error: ${error.message}`.red);
        }
    }

    async getCurrentPrice() {
        const url = 'https://www.okx.com/api/v5/market/ticker?instId=BTC-USDT';
        try {
            const response = await axios.get(url);
            if (response.data.code === '0' && response.data.data && response.data.data.length > 0) {
                return parseFloat(response.data.data[0].last);
            } else {
                throw new Error('Error saat mengambil harga saat ini');
            }
        } catch (error) {
            throw new Error(`Error mengambil harga saat ini: ${error.message}`);
        }
    }

    async assessPrediction(extUserId, predict, queryId) {
        const url = `https://www.okx.com/priapi/v1/affiliate/game/racer/assess?t=${Date.now()}`;
        const headers = { ...this.headers(), 'X-Telegram-Init-Data': queryId };
        const payload = {
            "extUserId": extUserId,
            "predict": predict,
            "gameId": 1
        };

        return axios.post(url, payload, { headers });
    }

    async sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    async waitWithCountdown(seconds) {
        for (let i = seconds; i >= 3; i--) {
            readline.cursorTo(process.stdout, 0);
            process.stdout.write(`===== Semua akun telah selesai, tunggu ${`${i}`.yellow} detik untuk melanjutkan =====`);
            await new Promise(resolve => setTimeout(resolve, 1000));
        }
        console.log('');
    }

    async Countdown(seconds) {
        for (let i = seconds; i >= 0; i--) {
            readline.cursorTo(process.stdout, 0);
            process.stdout.write(`${`================`.blue} ${`Tunggu ${`${i}`.yellow} detik untuk melanjutkan...`.white} ${`================`.blue}`);
            await new Promise(resolve => setTimeout(resolve, 1000));
        }
        console.log('');
    }

    extractUserData(queryId) {
        const urlParams = new URLSearchParams(queryId);
        const user = JSON.parse(decodeURIComponent(urlParams.get('user')));
        return {
            extUserId: user.id,
            extUserName: user.username
        };
    }
    
    askQuestion(query) {
        const rl = readline.createInterface({
            input: process.stdin,
            output: process.stdout
        });

        return new Promise(resolve => rl.question(query, ans => {
            rl.close();
            resolve(ans);
        }));
    }

    printWelcomeMessage() {
        console.log(`
┌─────────────────────────────────────────────────────┐
│██╗   ██╗ ██████╗ ███╗   ██╗███████╗███████╗██╗   ██╗│
│██║   ██║██╔═══██╗████╗  ██║██╔════╝██╔════╝╚██╗ ██╔╝│
│██║   ██║██║   ██║██╔██╗ ██║███████╗███████╗ ╚████╔╝ │
│╚██╗ ██╔╝██║   ██║██║╚██╗██║╚════██║╚════██║  ╚██╔╝  │
│ ╚████╔╝ ╚██████╔╝██║ ╚████║███████║███████║   ██║   │
│  ╚═══╝   ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚══════╝   ╚═╝   │
└─────────────────────────────────────────────────────┘
              `.magenta.bold);
        console.log(`${'OKX Racer BOT'}`.yellow.bold);
        console.log(`${`Update Link: ${'https://github.com/vonssy/OKXRacer-BOT'.cyan.underline}`}`.green.bold);
        console.log(`${`Donate? ${'081328733023'.cyan.underline} ${`- DANA`.green}`}`.green.bold);
        console.log(`${'NOT FOR SALE ! Edit Boleh, Rename Jangan :)\n\n'}`.yellow.bold);
    }

    async main() {
        const dataFile = path.join(__dirname, 'query.txt');
        const userData = fs.readFileSync(dataFile, 'utf8')
            .replace(/\r/g, '')
            .split('\n')
            .filter(Boolean);

        const checkin = await this.askQuestion('Auto Checkin? (y/n): ');
        const shouldCheckin = checkin.toLowerCase() === 'y';
        const clearTask = await this.askQuestion('Auto Completed Task? (y/n): ');
        const shouldClearTask = clearTask.toLowerCase() === 'y';
        const upgradeFuelTank = await this.askQuestion('Auto Upgrade Fuel Tank? (y/n): ');
        const shouldUpgradeFuelTank = upgradeFuelTank.toLowerCase() === 'y';
        const upgradeTurboCharger = await this.askQuestion('Auto Upgrade Turbo Charger? (y/n): ');
        const shouldUpgradeTurboCharger = upgradeTurboCharger.toLowerCase() === 'y';
    
        while (true) {
            this.printWelcomeMessage()
            for (let i = 0; i < userData.length; i++) {
                const queryId = userData[i];
                const { extUserId, extUserName } = this.extractUserData(queryId);
                try {
                    console.log(`\n=======================`.blue + `[   Akun ${i + 1} | ${extUserName}   ]`.cyan + `=======================\n`.blue);
                    const response = await this.sendRequest(extUserId, extUserName, queryId);
                    const balancePoints = response.data.data.balancePoints;
                    const numChances = response.data.data.numChances;
                    console.log(`[     Saldo Poin    ]: ${`${balancePoints}`.cyan}`.green);
                    console.log(`[     Kesempatan    ]: ${`${numChances}`.cyan}`.green);
                    
                    if (shouldCheckin) {
                        await this.getCheckin(extUserId, queryId);
                    } else {
                        console.log(`[      Checkin      ]: ${`Skipping Auto Checkin`.yellow}.`.green);
                    }
                    
                    if (shouldClearTask) {
                        await this.processTasks(extUserId, queryId);
                    } else {
                        console.log(`[        Task       ]: ${`Skipping Auto Completed Task`.yellow}.`.green);
                    }

                    let boosts = await this.getBoosts(queryId);
    
                    let reloadFuelTank = boosts.find(boost => boost.id === 1);
                    let fuelTank = boosts.find(boost => boost.id === 2);
                    let turbo = boosts.find(boost => boost.id === 3);
    
                    if (fuelTank && shouldUpgradeFuelTank) {
                        const balanceResponse = await this.sendRequest(extUserId, extUserName, queryId);
                        const balancePoints = balanceResponse.data.data.balancePoints;
                        if (fuelTank.curStage < fuelTank.totalStage && balancePoints > fuelTank.pointCost) {
                            await this.upgradeFuelTank(queryId);
                    
                            boosts = await this.getBoosts(queryId);
                            const updatedFuelTank = boosts.find(boost => boost.id === 2);
                            const updatedBalanceResponse = await this.sendRequest(extUserId, extUserName, queryId);
                            const updatedBalancePoints = updatedBalanceResponse.data.data.balancePoints;
                    
                            if (updatedFuelTank.curStage >= fuelTank.totalStage || updatedBalancePoints < fuelTank.pointCost) {
                                console.log(`[    Up Fuel Tank   ]: `.red + `Saldo Kurang Atau Sudah Lv. Max`.yellow);
                            }
                        } else {
                            console.log(`[    Up Fuel Tank   ]: `.red + `Saldo Kurang Atau Sudah Lv. Max`.yellow);
                        }
                    } else {
                        console.log(`[    Up Fuel Tank   ]: ${`Skipping Auto Upgrade Fuel Tank`.yellow}.`.green);
                    }
                    
                    if (turbo && shouldUpgradeTurboCharger) {
                        const balanceResponse = await this.sendRequest(extUserId, extUserName, queryId);
                        const balancePoints = balanceResponse.data.data.balancePoints;
                        if (turbo.curStage < turbo.totalStage && balancePoints > turbo.pointCost) {
                            await this.upgradeTurboCharger(queryId);
                        
                            boosts = await this.getBoosts(queryId);
                            const updatedTurbo = boosts.find(boost => boost.id === 3);
                            const updatedBalanceResponse = await this.sendRequest(extUserId, extUserName, queryId);
                            const updatedBalancePoints = updatedBalanceResponse.data.data.balancePoints;
                    
                            if (updatedTurbo.curStage >= turbo.totalStage || updatedBalancePoints < turbo.pointCost) {
                                console.log(`[  Up Turbo Charger ]: `.red + `Saldo Kurang Atau Sudah Lv. Max`.yellow);
                            }
                        } else {
                            console.log(`[  Up Turbo Charger ]: `.red + `Saldo Kurang Atau Sudah Lv. Max`.yellow);
                        }
                    } else {
                        console.log(`[  Up Turbo Charger ]: ${`Skipping Auto Upgrade Turbo Charger`.yellow}.`.green);
                    }                    

                    console.log(`\n======================`.blue + `[ Prediction Processing ]`.cyan + `======================\n`.blue);
                    
                    while (true) {
                        const price1 = await this.getCurrentPrice();
                        await this.sleep(4000);
                        const price2 = await this.getCurrentPrice();

                        const padLength = 10;
                        let predict;
                        let actionPadded;

                        if (price1 > price2) {
                            predict = 0;
                            actionPadded = 'Jual'.padEnd(padLength).yellow;
                        } else {
                            predict = 1;
                            actionPadded = 'Beli'.padEnd(padLength).green;
                        }

                        const assessResponse = await this.assessPrediction(extUserId, predict, queryId);
                        const assessData = assessResponse.data.data;
                        const result = assessData.won ? 'Menang'.green : 'Kalah'.red;
                        const calculatedValue = assessData.basePoint * assessData.multiplier;

                        console.log(`${`[      Prediksi    ]:`.cyan} ${actionPadded} | ${`[      Hasil       ]:`.cyan} ${result.padEnd(padLength)} x ${assessData.multiplier}`);
                        console.log(`${`[       Saldo      ]:`.cyan} ${assessData.balancePoints.toString().padEnd(padLength)} | ${`[     Diperoleh    ]:`.cyan} ${calculatedValue.toString().padEnd(padLength)}`);
                        console.log(`${`[ Harga Sebelumnya ]:`.cyan} ${assessData.prevPrice.toString().padEnd(padLength)} | ${`[  Harga Saat Ini  ]:`.cyan} ${assessData.currentPrice.toString().padEnd(padLength)}`);
    
                        if (assessData.numChance > 0) {
                            await this.Countdown(1);
                        } else if (assessData.numChance <= 0 && reloadFuelTank && reloadFuelTank.curStage < reloadFuelTank.totalStage) {
                            
                            await this.useBoost(queryId);
                            console.log('\n')
                            boosts = await this.getBoosts(queryId);
                            reloadFuelTank = boosts.find(boost => boost.id === 1);
                            console.log(`\n======================`.blue + `[ Prediction Processing ]`.cyan + `======================\n`.blue);
                        } else {
                            break;
                        }
                    }
                } catch (error) {
                    console.log(`${'Error:'.red} ${error.message}`);
                }
            }
            await this.waitWithCountdown(1800);
        }
    }
}

if (require.main === module) {
    const okx = new OKX_RACER();
    okx.main().catch(err => {
        console.error(err.toString().red);
        process.exit(1);
    });
}