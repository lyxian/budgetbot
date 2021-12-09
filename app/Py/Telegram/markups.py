from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils import CalendarObject, WEEKDAYS, CATEGORIES
import pendulum

def createMarkupCalendar(n=0):
    current = CalendarObject(pendulum.now().add(months=n))

    markup = InlineKeyboardMarkup(row_width=7)
    # Add Month
    markup.add(
        InlineKeyboardButton(text=f'{current.monthName}-{current.year}', callback_data="Ignore")
    )
    # Add Weekdays
    markup.add(
        *[InlineKeyboardButton(text=day, callback_data="Ignore") for day in WEEKDAYS]
    )
    # Add Days
    for row in current.days:
        markup.add(
            *[InlineKeyboardButton(text=val, callback_data=f"{current.month}-{val}-{current.year}") if val else InlineKeyboardButton(text="-", callback_data="Ignore") for val in row]
        )
    # Commands
    markup.add(
        InlineKeyboardButton("Back", callback_data=f"Back {n}"),
        InlineKeyboardButton("Cancel", callback_data="Cancel"),
        InlineKeyboardButton("Next", callback_data=f"Next {n}")
    )
    return markup

def createMarkupCategory(date):
    markup = InlineKeyboardMarkup(row_width=3)
    # Add First Row
    markup.add(
        *[InlineKeyboardButton(text=category, callback_data=' '.join([date, category, ''])) for category in CATEGORIES[:3]]
    )
    # Add Second Row
    markup.add(
        *[InlineKeyboardButton(text=category, callback_data=' '.join([date, category, ''])) for category in CATEGORIES[3:]]
    )
    return markup

def createMarkupPrice(digits=''):
    # Options
    markup = InlineKeyboardMarkup(row_width=3)
    nums = [str(i) for i in range(1,10)]
    if '.' not in digits:
        dot = digits + '.'
    else:
        dot = 'INVALID'
    if digits[-1] == ' ':
        clear = 'IGNORE'
        enter = 'IGNORE'
        dot = digits + '0.'
    else:
        clear = 'DEL {}'
        enter = 'ENTER {}'
    # Add Inline
    markup.add(
        *[InlineKeyboardButton(text=num, callback_data=digits+num) for num in nums[:3]]
    )
    markup.add(
        *[InlineKeyboardButton(text=num, callback_data=digits+num) for num in nums[3:6]]
    )
    markup.add(
        *[InlineKeyboardButton(text=num, callback_data=digits+num) for num in nums[6:]]
    )
    markup.add(
        InlineKeyboardButton(text='.', callback_data=dot),
        InlineKeyboardButton(text='0', callback_data=digits+'0'),
        InlineKeyboardButton(text="C", callback_data=clear.format(digits))
    )
    markup.add(
        InlineKeyboardButton(text="Enter", callback_data=enter.format(digits))
    )
    return markup

# selective (bool, optional) –
# Use this parameter if you want to force reply from specific users only. Targets:
# Users that are @mentioned in the text of the telegram.Message object.
# If the bot’s message is a reply (has reply_to_message_id), sender of the original message.