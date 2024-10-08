# Diamore - automation of the crypto game “Diamore”

A program that automates actions in the crypto game “Diamore”

# Quick Start

*  Download [latest version from Releases page](https://github.com/Argona7/Diamore/releases), and **run the program as administrator**.

# How does it work 

**The program does automation with post queries, the actions it automatically performs:**

* Get daily reward
* Start game
* Claim points for game
* Automatic skill improvement

The program sends requests using an authorization token that is different for each account, and thanks to the token the authorization takes place.
[How to get "query"](#how-to-get-query)

# How to track a request

In order to trace the request you need to [run Diamore in web telegram and bypass the protection](https://www.youtube.com/watch?v=esgoT_wigDI). With the help of the ***DevTools*** in the ***Network*** section you will be able to find  the request that the Diamore sends

###

# How to use

Download [latest version from Releases page](https://github.com/Argona7/Diamore/releases) and run.
After that, the program will create a json document called **diamore** which must be filled in manually on the path **“C:\Users\ Your user.“**

* ### How the json file should be filled in:
```
{
    "accounts": {
        "@YouTelegramAccountName": {
            "query":"",
            "user-agent":""
        },
        "@YouTelegramAccountName": {
            "query":"",
            "user-agent":""
        },
        "@YouTelegramAccountName": {
            "query":"",
            "user-agent":""
        },
        "@YouTelegramAccountName": {
            "query":"",
            "user-agent":""
        }
    }
}
```
You should also record a different **user-agent** for each account for better security

## How to get "query"

You have to follow the same pattern as in [How to track a request](#how-to-track-a-request) . You need to trace any request Diamore sends out and look in the headers: **Authorization: Token "query"**

After that, once you have properly modified the file, restart the application
You will be prompted to exclude accounts from the automation list, simply type the account name or account names with a space.  
Enjoy the app!

**Who's not registered**: https://t.me/DiamoreCryptoBot/app?startapp=1087108725
