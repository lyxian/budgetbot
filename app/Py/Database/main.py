import redis
import logging
logging.getLogger().setLevel(logging.INFO)


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