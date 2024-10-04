Here’s the complete code for the README file for your project:

```markdown
# Rise and Shine Challenge

## Overview

The Rise and Shine Challenge is a project designed to manage a daily challenge where participants submit their entries via a Microsoft Form. The project integrates with Google Sheets for data storage and uses a Telegram bot to facilitate communication and notifications.

## Table of Contents

- [Installation](#installation)
- [Requirements](#requirements)
- [Obtaining Secret Keys](#obtaining-secret-keys)
- [Running the Project](#running-the-project)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. **Clone the repository:**

   ```bash
   git clone <repository_url>
   cd rise-and-shine-challenge
   ```

2. **Install the required dependencies:**

   Make sure you have Python 3.6 or later installed. Then, create a virtual environment and install the required packages:

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

## Requirements

- Python 3.6 or later
- `requests` library
- `python-telegram-bot` library
- Access to Google Sheets API

## Obtaining Secret Keys

To run the project, you will need the following secret keys:

1. **Google Sheets API Credentials:**
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project or select an existing one.
   - Navigate to **APIs & Services > Credentials**.
   - Click on **Create Credentials** and select **Service Account**.
   - Fill in the necessary details and create the service account.
   - After creating the account, click on it and go to **Keys** to create a new key. Choose JSON format. This file contains your `private_key`, `client_email`, and other necessary information.

2. **Set Up Permissions:**
   - Share the Google Sheet (where you collect form submissions) with the service account email (e.g., `sheets-api-service-account@rise-and-shine-challenge.iam.gserviceaccount.com`).

3. **Telegram Bot Token:**
   - Create a new bot using [BotFather](https://t.me/botfather) on Telegram.
   - Follow the instructions to create your bot and obtain the **API token**.

4. **Environment Variables:**
   - Store your secret keys in a `.env` file in the root of your project:

     ```
     GOOGLE_SHEET_CREDENTIALS='YOUR_CREDENTIALS_JSON_CONTENT_HERE'
     TELEGRAM_BOT_TOKEN='YOUR_TELEGRAM_BOT_TOKEN'
     ```

## Running the Project

1. **Make sure the required services are running:**
   - Start your bot using the command:

   ```bash
   python your_bot_file.py
   ```

2. **Monitor the console for logs and errors.**

## Usage

- The Telegram bot will automatically send notifications and manage form submissions based on the defined rules.
- Participants can submit their entries between 5:00 AM and 6:00 AM to earn points.

## Contributing

If you would like to contribute to the project, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

### Instructions for Use

1. Replace `<repository_url>` with the URL of your project's repository.
2. Update any necessary details specific to your project, such as filenames or additional setup instructions.
3. Save this content in a file named `README.md` in your project directory.

This README provides clear and comprehensive instructions for users to set up and run the project effectively.