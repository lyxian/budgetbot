# Budgets Bot

##Packages
Flask
Redis
pendulum
matplotlib
marshmallow
cryptography
PyTelegramBotAPI
##Packages

## TO-DO

- simulate local DB commands
  - structures :
    - { user : { date : { time , type , cost } } }
    - { user : id } , { date : { id , time , type , cost} }
  - handle single dict (hset>mapping)
  - handle nested dict (not allowed)
  - possible input :
    - .
  - implement with marshmallow
  - how to edit/delete records
- manage bot commands
  - subscription
  - add budget
  - manual :
    - choose date (HARD)
      - calendar
    - choose category
    - input cost
- manage backend bot server
  - dev
    - flask
  - prod
    - gunicorn
    - waitress

## Bot Configuration

- bot command
- get calendar
  - undo/cancel
  - selection
- get category
