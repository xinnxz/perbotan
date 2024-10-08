# Gradient Bot

<div align="center">
  <img src="./images/console.png" alt="Gradient Bot Console" width="600"/>
</div>

## Overview

Gradient Bot is an advanced automation tool designed to streamline account registration and farming processes on Gradient Network. With its powerful features and user-friendly interface, it offers a seamless experience for users looking to maximize their efficiency on the platform.

**Purchase: [https://t.me/gradient_network_bot](https://t.me/gradient_network_bot)**

**Price: $120**

---

## 🚀 Features

- ✅ Automatic account registration
- 🌾 Automated farming
- 🔄 Automated farming with auto-swap proxy
- 🔁 Automated re-verification of accounts
- 🧩 Captcha solving
- 📧 Email verification
- 🎟️ Invite code binding
- 📊 Export statistics to CSV
- 🧵 Multi-threaded support for registration, export stats, and re-verify accounts
- 📤 Auto-export unverified/unregistered accounts

---

## 💻 Requirements

- Windows operating system
- Internet connection
- Valid email accounts for registration
- Valid proxies

---

## 🛠️ Setup

1. Download the EXE file.
2. Run the EXE file and login. It will automatically bind to your PC (the bind will disappear automatically if you close all sessions).
3. Prepare the configuration files as described below.

---

## ⚙️ Configuration

### settings.yaml

This file contains general settings for the bot:

```yaml
threads: 3 # Number of threads for registration and export stats (min 1)
invite_code: "DOIFI8" # Your invite code
capsolver_api_key: "CAP" # Your CapSolver API key

delay_before_start:
  min: 5 # Minimum delay before starting registration (in seconds)
  max: 10 # Maximum delay before starting registration (in seconds)

imap_settings: # IMAP settings for email providers
  rambler.ru: imap.rambler.ru
  hotmail.com: imap-mail.outlook.com
  outlook.com: imap-mail.outlook.com
  mail.ru: imap.mail.ru
  gmail.com: imap.gmail.com
  gmx.com: imap.gmx.com
  yahoo.com: imap.mail.yahoo.com
  gmx.net: imap.gmx.net
  gmx.de: imap.gmx.net
```

### Other Configuration Files

#### 📁 farm.txt
Contains accounts for farming.
```
Format:
email:password
email:password
...
```

#### 📁 register.txt
Contains accounts to register.
```
Format:
email:password
email:password
...
```

#### 📁 verify.txt
Contains accounts to re-verify.
```
Format:
email:password
email:password
...
```

#### 📁 multiple_proxies.txt
For auto-swap proxy module (especially for residential proxies).
```
Format:
http://user:pass@ip:port
http://ip:port:user:pass
http://ip:port@user:pass
http://user:pass:ip:port
...
```

#### 📁 proxies.txt
For regular proxy usage.
```
Format:
http://user:pass@ip:port
http://ip:port:user:pass
http://ip:port@user:pass
http://user:pass:ip:port
...
```

---

## 🚀 Usage

1. Ensure all configuration files are set up correctly.
2. Run the EXE file.

---

## ⚠️ Important Notes

- The script is limited to 2 active sessions. For example, you can use 2 sessions on one PC or 1 session on 2 PCs.
- Make sure your email providers are correctly configured in the `imap_settings` section of `settings.yaml`.
- The bot uses CapSolver for solving captchas. Ensure you have sufficient balance in your CapSolver account.

---

## 🔧 Troubleshooting

- **Email Verification Issues**: Check your email provider's IMAP settings and ensure they match the configuration in `settings.yaml`.
- **Captcha Problems**: Verify your CapSolver API key and account balance.
- **Unexpected Farming Stops**: Check the console output for error messages and ensure your account credentials are correct.

---
