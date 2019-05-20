## Telegram Dutch Tax Calculation Bot
https://t.me/nl_taxes_bot  
**@nl_taxes_bot**

Based on Web version:  
https://thetax.nl  
(**author**: Stepan Suvorov) 
https://github.com/stevermeister/dutch-tax-income-calculator


### Dependencies

**Python 3.6** and above.  
**python-telegram-bot** 


### Running program locally
`python3 app.py`

### Deploying on Heroku
`heroku login`  
`git push heroku master`  
`heroku ps:scale bot=1`  

### Environment variables
**ADMIN_ID** -  Admin user ID. Got from telegram.  
**BOT_TOKEN** - Telegram bot access token. Got from botfather.  
**ENV** - "dev", "prod" set proper config for specified environment.
