# Black Myth Wukong

This project is an automated API client for the Black Myth Wukong game. The client allows users to automatically log in, perform daily check-ins, and claim coins for multiple accounts.

## Features

- Automatic login
- Daily check-in
- Coin and energy claiming
- Multi-account handling

## Requirements

- Node.js (version 12 or higher)
- NPM (Node Package Manager)

## Installation

1. Clone this repository:

   ```
   git clone https://github.com/Galkurta/BlackMythWukong-BOT.git
   cd BlackMythWukong-BOT
   ```

2. Install dependencies:

   ```
   npm install
   ```

## Usage

1. Account registration:
   Before using this client, you need to register a [BlackMythWukong](https://t.me/bwcwukong_bot/Play?startapp=6944804952)

2. Set up the `data.txt` file:
   Edit `data.txt` file in the project's root directory. Each line should contain account data in the following format:

   ```
   user=
   query_id=
   ```

3. Run the application:
   ```
   node main.js
   ```

The application will run continuously, processing each account in the `data.txt` file and waiting for 10 minutes before starting a new cycle.

## Warning

Using bots or automated clients may violate the Terms of Service. Use at your own risk.

## Contributing

Contributions are always welcome. Please make a pull request or open an issue for suggestions and improvements.

## License

[MIT License](LICENSE)
