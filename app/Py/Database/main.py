import pendulum
import redis
import logging
logging.getLogger().setLevel(logging.INFO)

# TO-DO
# - no validation, push to DB
# - model validation with marshmallow

# REDIS - (only object str key-pair allowed)
# DB.users : 
# - props : username, chat_id, pk_list, pk_count
# - model : userName:chatId > userName, chatId, totalCount, netSpending, createdAt
# DB.records : 
# - props : pk/transaction , time, date. categpry. price
# - model : uid:pid > pid, uid, time, date, category, price
# - uid = username:chatId

DB_USER_ID = 1
DB_RECORD_ID = 2

def pushToDb(message, data):
    db_user = redis.Redis(db=DB_USER_ID, decode_responses=True)
    db_record = redis.Redis(db=DB_RECORD_ID, decode_responses=True)

    # PAYLOAD: 5;Food;12-8-2021;Oooo
    headers = ['price', 'category', 'date', 'description']
    data_dict = dict(zip(headers, data))

    uid = '{1}:{2}'.format(message.chat.username, message.chat.id)
    # Check if User in DB_USERS
    if not db_user.exists(uid):
        user_data = {
            uid: {
                'userName': message.chat.username,
                'chatId': message.chat.id,
                'totalCount': 0,
                'netSpending': 0,
                'createdAt': pendulum.now.format('YYYY-MM-DDTHH:mm:ssZZ')
            }
        }
        # Add User if not exists
        db_user.hset(name=uid, mapping=user_data)
        logging.info(f'{uid} has been added to DB_USER')
    else:
        user_data = db_user.hgetall(uid)
        logging.info(f'{uid} exists in DB_USER')
        
    pid = eval(f"{user_data['totalCount']}+1")
    record_id = f'{uid}:{pid}'
    record_data = {
        record_id: {
            'pid': pid,
            'uid': uid,
            'time': pendulum.now().format('HH:mm:ss'),
            **data_dict
        }
    }
    # Check if Record in DB_RECORDS
    if not db_record.exists(record_id):
        # Add Record
        db_record.hset(name=record_id, mapping=record_data)
        logging.info(f'{record_id} has been added to DB_RECORD')
        # Increment User "totalCount", "netSpending"
        db_user.hincrby(name=uid, key='totalCount', amount=1)
        db_user.hincrby(name=uid, key='netSpending', amount=record_data['price'])
        logging.info(f'{uid} updated!')
    else:
        logging.info(f'{record_id} cannot be added to DB_RECORD')


sampleUser = {
    'lyxian:2': {
        'userName': 'lyxian',
        'chatId': 2,
        'totalCount': 0,
        'netSpending': 0,
        'createdAt': 1
    }
}
sampleRecord = {
    'lyxian:2:1': {
        'pid': 1,
        'uid': 'lyxian:2',
        'time': 0,
        'date': '12-10-2021',
        'category': 'Food',
        'price': 10
    },
    'lyxian:2:2': {
        'pid': 2,
        'uid': 'lyxian:2',
        'time': 0,
        'date': '12-10-2021',
        'category': 'Food',
        'price': 15
    },
    'lyxian:2:3': {
        'pid': 2,
        'uid': 'lyxian:2',
        'time': 0,
        'date': '12-10-2021',
        'category': 'Food',
        'price': 20
    }
}

if __name__ == '__main__':
    db_user = redis.Redis(db=DB_USER_ID)
    db_record = redis.Redis(db=DB_RECORD_ID)
    
    user_test = next(iter(sampleUser))
    # Check if User in DB_USERS
    # if f'{user_test}:{chat_test}'.encode('utf-8') not in db_user.keys():
    if not db_user.exists(user_test):
        # Add User if not exists
        for k,v in sampleUser.items():
            db_user.hset(name=k, mapping=v)
        logging.info(f'{user_test} has been added to DB_USER')
    else:
        logging.info(f'{user_test} exists in DB_USER')
        
    for k,v in sampleRecord.items():
        # Check if Record in DB_RECORDS
        record_id = k
        if not db_record.exists(k):
            # Add Record
            db_record.hset(name=k, mapping=v)
            logging.info(f'{record_id} has been added to DB_RECORD')

            # Increment User "totalCount", "netSpending"
            db_user.hincrby(name=v['uid'], key='totalCount', amount=1)
            db_user.hincrby(name=v['uid'], key='netSpening', amount=v['price'])
            logging.info(f'{v["uid"]} updated! CHANGES=...')
        else:
            logging.info(f'{record_id} cannot be added to DB_RECORD')

    # Increment totalCount for User
    
    # r.bgsave()

# r = redis.Redis(db=1)
# r.bgsave()

# From redis/client.py
# class Redis(object):
#     def __init__(self, host='localhost', port=6379,
#                  db=0, password=None, socket_timeout=None,
#                  # ...