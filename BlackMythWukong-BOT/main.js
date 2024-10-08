const axios = require("axios");
const fs = require("fs");
const path = require("path");
const readline = require("readline");
const winston = require("winston");
const { format } = require("winston");
const colors = require("colors/safe");

colors.setTheme({
  info: "cyan",
  warn: "yellow",
  success: "green",
  error: "red",
});

// Updated Winston logger setup
const logger = winston.createLogger({
  level: "info",
  format: format.combine(
    format.timestamp({ format: "YYYY-MM-DD HH:mm:ss" }),
    format.printf(({ timestamp, level, message }) => {
      let coloredMessage;
      switch (level) {
        case "info":
          coloredMessage = colors.info(message);
          break;
        case "warn":
          coloredMessage = colors.warn(message);
          break;
        case "error":
          coloredMessage = colors.error(message);
          break;
        case "success":
          coloredMessage = colors.success(message);
          break;
        default:
          coloredMessage = message;
      }
      return `[ ${timestamp} ] [ ${level
        .toUpperCase()
        .padEnd(7)} ] BWC - ${coloredMessage}`;
    })
  ),
  transports: [new winston.transports.Console()],
});

class BWC {
  constructor() {
    this.headers = {
      Accept: "*/*",
      "Accept-Encoding": "gzip, deflate, br",
      "Accept-Language":
        "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
      "Content-Type": "application/json",
      Origin: "https://blackwukong.lucky-mines.com",
      Referer: "https://blackwukong.lucky-mines.com/",
      "Sec-Ch-Ua":
        '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
      "Sec-Ch-Ua-Mobile": "?1",
      "Sec-Ch-Ua-Platform": '"Android"',
      "Sec-Fetch-Dest": "empty",
      "Sec-Fetch-Mode": "cors",
      "Sec-Fetch-Site": "same-site",
      "User-Agent":
        "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36",
    };
  }

  log(msg, type = "info") {
    switch (type.toLowerCase()) {
      case "success":
        logger.log("info", msg, { level: "success" });
        break;
      case "error":
        logger.error(msg);
        break;
      case "warning":
        logger.warn(msg);
        break;
      default:
        logger.info(msg);
    }
  }

  formatTime(seconds) {
    const m = Math.floor(seconds / 60)
      .toString()
      .padStart(2, "0");
    const s = (seconds % 60).toString().padStart(2, "0");
    return `${m}:${s}`;
  }

  async countdown(seconds) {
    for (let i = seconds; i >= 0; i--) {
      readline.cursorTo(process.stdout, 0);
      const message = `Waiting ${this.formatTime(i)} to continue the loop`;
      process.stdout.write(colors.cyan(message));
      await new Promise((resolve) => setTimeout(resolve, 1000));
    }
    readline.clearLine(process.stdout, 0);
    this.log("Countdown complete", "info");
  }

  async login(userData) {
    const url = "https://api-blackwukong.lucky-mines.com/v1/user/login";
    const payload = {
      tid: userData.id,
      parent_tid: userData.parent_tid,
      username: userData.username,
      is_premium: userData.is_premium || false,
      device: "android",
    };
    try {
      const response = await axios.post(url, payload, {
        headers: this.headers,
      });
      if (response.status === 200 && response.data.code === 200) {
        return {
          success: true,
          token: response.data.data.token,
          is_register: response.data.data.is_register,
        };
      } else {
        return { success: false, error: response.data.msg };
      }
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  async getBalance(token) {
    const url = "https://api-blackwukong.lucky-mines.com/v1/user/balance";
    const headers = { ...this.headers, "User-Auth": token };
    try {
      const response = await axios.post(url, {}, { headers });
      if (response.status === 200 && response.data.code === 200) {
        return {
          success: true,
          coins: response.data.data.coins,
          energy: response.data.data.energy,
        };
      } else {
        return { success: false, error: response.data.msg };
      }
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  async collectEnergy(token, userId) {
    const url = "https://api-blackwukong.lucky-mines.com/v1/ss/button_info";
    const headers = { ...this.headers, "User-Auth": token };
    const payload = {
      button_type: "collect",
      user_id: `${userId}`,
      devive: "android",
    };

    try {
      const response = await axios.post(url, payload, { headers });
      if (response.status === 200 && response.data.code === 200) {
        this.log("Claim successful", "success");
        return { success: true, data: response.data };
      } else {
        return { success: false, error: response.data.msg };
      }
    } catch (error) {
      this.log(`Claim unsuccessful: ${error.message}`, "error");
      if (error.response) {
        this.log(
          `Error occurred: ${JSON.stringify(error.response.data)}`,
          "error"
        );
      }
      return { success: false, error: error.message };
    }
  }

  async exchange(token) {
    const url = "https://api-blackwukong.lucky-mines.com/v1/user/exchange";
    const headers = { ...this.headers, "User-Auth": token };

    try {
      const response = await axios.post(url, {}, { headers });
      if (response.status === 200 && response.data.code === 200) {
        return {
          success: true,
          coins: response.data.data.coins,
          energy: response.data.data.energy,
          energy_update_at: response.data.data.energy_update_at,
        };
      } else {
        return { success: false, error: response.data.msg };
      }
    } catch (error) {
      this.log(`Exchange error: ${error.message}`, "error");
      if (error.response) {
        this.log(
          `Error response: ${JSON.stringify(error.response.data)}`,
          "error"
        );
      }
      return { success: false, error: error.message };
    }
  }

  async sign(token) {
    const url = "https://api-blackwukong.lucky-mines.com/v1/user/sign";
    const headers = { ...this.headers, "User-Auth": token };

    try {
      const response = await axios.post(url, {}, { headers });
      if (response.status === 200) {
        if (response.data.code === 200) {
          return {
            success: true,
            sign_times: response.data.data.sign_times,
            sign_time: response.data.data.sign_time,
            reward_record: response.data.data.reward_record,
          };
        } else if (
          response.data.code === 1003 &&
          response.data.msg === "signed"
        ) {
          return {
            success: true,
            alreadySigned: true,
          };
        } else {
          return { success: false, error: response.data.msg };
        }
      } else {
        return {
          success: false,
          error: `Unexpected response status: ${response.status}`,
        };
      }
    } catch (error) {
      this.log(`Check-in error: ${error.message}`, "error");
      if (error.response) {
        this.log(
          `Error occurred: ${JSON.stringify(error.response.data)}`,
          "error"
        );
      }
      return { success: false, error: error.message };
    }
  }

  parseQueryString(queryString) {
    const params = {};
    const pairs = queryString.split("&");
    for (const pair of pairs) {
      const [key, value] = pair.split("=");
      params[decodeURIComponent(key)] = decodeURIComponent(value);
    }
    return params;
  }

  async main() {
    const dataFile = path.join(__dirname, "data.txt");
    const data = fs
      .readFileSync(dataFile, "utf8")
      .replace(/\r/g, "")
      .split("\n")
      .filter(Boolean);

    while (true) {
      for (let i = 0; i < data.length; i++) {
        try {
          const queryString = data[i];
          const parsedQuery = this.parseQueryString(queryString);

          let userDataParsed;
          if (parsedQuery.user) {
            userDataParsed = JSON.parse(parsedQuery.user);
          } else {
            const userParam = queryString.match(/user=([^&]+)/);

            if (!userParam) {
              throw new Error("Invalid data format");
            }

            userDataParsed = JSON.parse(decodeURIComponent(userParam[1]));
          }

          const userData = {
            id: userDataParsed.id,
            username: userDataParsed.username,
            parent_tid: 6944804952,
            is_premium: userDataParsed.is_premium || false,
          };

          this.log(`Account ${i + 1} | ${userDataParsed.first_name}`, "info");

          this.log(`Logging in to account ${userData.id}...`, "info");
          const loginResult = await this.login(userData);
          if (loginResult.success) {
            this.log("Login successful!", "success");
            const token = loginResult.token;

            const balanceResult = await this.getBalance(token);
            if (balanceResult.success) {
              this.log(`Coins: ${balanceResult.coins}`, "info");
              this.log(`Energy: ${balanceResult.energy}`, "info");

              this.log("Performing check-in...", "info");
              const signResult = await this.sign(token);
              if (signResult.success) {
                if (signResult.alreadySigned) {
                  this.log("You've already checked in today", "warning");
                } else {
                  this.log("Check-in successful", "success");
                  this.log(`Check-in times: ${signResult.sign_times}`, "info");
                  this.log(
                    `Check-in time: ${new Date(
                      signResult.sign_time * 1000
                    ).toLocaleString()}`,
                    "info"
                  );
                  this.log(`Reward: ${signResult.reward_record}`, "info");
                }
              } else {
                this.log(`Check-in failed: ${signResult.error}`, "error");
              }

              if (balanceResult.energy > 0) {
                this.log("Claiming coin...", "info");
                const collectResult = await this.collectEnergy(
                  token,
                  userData.id
                );
                if (collectResult.success) {
                  const exchangeResult = await this.exchange(token);
                  if (exchangeResult.success) {
                    this.log(
                      `Coins & Energy after claim: ${exchangeResult.coins} | Energy: ${exchangeResult.energy}`,
                      "info"
                    );
                    this.log(
                      `Energy update at: ${new Date(
                        exchangeResult.energy_update_at * 1000
                      ).toLocaleString()}`,
                      "info"
                    );
                  } else {
                    this.log(
                      `Exchange failed: ${exchangeResult.error}`,
                      "error"
                    );
                  }
                } else {
                  this.log(
                    `Collect energy failed: ${collectResult.error}`,
                    "error"
                  );
                }
              }
            } else {
              this.log(
                `Could not retrieve account information: ${balanceResult.error}`,
                "error"
              );
            }
          } else {
            this.log(`Login unsuccessful! ${loginResult.error}`, "error");
          }
        } catch (error) {
          this.log(`User data processing error: ${error.message}`, "error");
        }

        await new Promise((resolve) => setTimeout(resolve, 1000));
      }

      await this.countdown(10 * 60);
    }
  }
}

const client = new BWC();
client.main().catch((err) => {
  client.log(err.message, "error");
  process.exit(1);
});
