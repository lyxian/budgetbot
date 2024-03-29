# Budgets Bot

## Changelogs

**To-Do**

- `simulate local DB commands`
  - implement with marshmallow
  - how to edit/delete records
- `manage backend bot server`
  - prod (gunicorn/waitress)
  - setup ENV

**Done**

- `simulate local DB commands`
  - structures :
    - { user : id } , { date : { id , time , type , cost} }
  - handle single dict (hset>mapping)
- ` manage bot commands`
  - subscription
  - add budget
  - manual :
    - choose date
      - calendar
    - choose category
    - input cost
  - include DEBUG_MODE
- `manage backend bot server`
  - dev (flask)

## Bugs

**To-Do**

- handle _unwanted_ plain message

**Done**

- .

## Bot Configuration

- bot command
- get calendar
  - undo/cancel
  - selection
- get category

## Cloud Configuration

- setup telebot on Heroku
- setup Redis on AWS

## Add-ons

- read/edit/remove past records
  - search by :
    - YEAR > MONTH > DAY > views records in a day
    - display up to \_ records with sidebar navigator
- main menu GUI
  - buttons :
    - add
    - analyze spending within time period
    - edit past records
- try docker-compose
  - flask--telebot
  - redis--container

## Packages

##Packages
Flask
Redis
pendulum
matplotlib
marshmallow
cryptography
PyTelegramBotAPI
##Packages
