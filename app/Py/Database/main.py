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

def pushToDb(message, data, current):
    db_user = redis.Redis(host='redis', port=6379, db=DB_USER_ID, decode_responses=True)
    db_record = redis.Redis(host='redis', port=6379, db=DB_RECORD_ID, decode_responses=True)

    # PAYLOAD: 5;Food;12-8-2021;Oooo
    headers = ['price', 'category', 'date', 'description']
    data_dict = dict(zip(headers, data))

    uid = '{}:{}'.format(message.chat.username, message.chat.id)
    # Check if User in DB_USERS
    if not db_user.exists(uid):
        user_data = {
            'userName': message.chat.username,
            'chatId': message.chat.id,
            'totalCount': 0,
            'netSpending': 0,
            'createdAt': current.format('YYYY-MM-DDTHH:mm:ssZZ')
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
        'pid': pid,
        'uid': uid,
        'time': current.format('HH:mm:ss'),
        **data_dict
    }
    # Check if Record in DB_RECORDS
    if not db_record.exists(record_id):
        # Add Record
        db_record.hset(name=record_id, mapping=record_data)
        logging.info(f'{record_id} has been added to DB_RECORD')
        # Increment User "totalCount", "netSpending"
        db_user.hincrby(name=uid, key='totalCount', amount=1)
        db_user.hincrbyfloat(name=uid, key='netSpending', amount=record_data['price'])
        logging.info(f'{uid} updated!')
    else:
        logging.info(f'{record_id} cannot be added to DB_RECORD')

if __name__ == '__main__':
    pass