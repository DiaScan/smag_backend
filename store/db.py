import os
import postgrest
from supabase import create_client, Client
import bcrypt


SUPABASE_PUBLIC_URL: str = ''
SUPABASE_SERVICE_ROLE: str = ''

supabase: Client = None
salt = None


def init_client():
    global SUPABASE_PUBLIC_URL, SUPABASE_SERVICE_ROLE, supabase, salt
    SUPABASE_PUBLIC_URL = os.environ.get('SUPABASE_PUBLIC_URL')
    SUPABASE_SERVICE_ROLE = os.environ.get('SUPABASE_SERVICE_ROLE')
    supabase = create_client(
        supabase_url=SUPABASE_PUBLIC_URL, supabase_key=SUPABASE_SERVICE_ROLE)


def get_all_shops_of_user(user_id):
    init_client()
    shop_records = supabase.table('shop').select("*").eq('user_id', user_id).execute()
    return shop_records.data

def get_all_shops():
    init_client()
    shop_records = supabase.table('shop').select('*').execute()
    return shop_records.data

def get_all_transactions():
    init_client()
    transactions = supabase.table('transaction').select("*").execute()
    return transactions.data

def get_all_transactions_of_shop(shop_id):
    init_client()
    transactions = supabase.table('transaction').select("*").eq('shop_id', shop_id).execute()
    return transactions.data


def get_all_users():
    init_client()
    user_records = supabase.table('user').select("*").execute()
    return user_records.data

def get_shop_details(shop_id):
    init_client()
    shop_details = supabase.table('shop').select("*").eq('shop_id', shop_id).execute()
    res = shop_details.data[0]
    return {'shop_id': shop_id, 'shop_name': res['shop_name'], 'district': res['district'], 'state': res['state']}

def user_exists(username):
    try:
        response = supabase.table('user').select(
            '*').eq('username', username).execute()

        if len(response.data) != 0:
            return True
        else:
            return False
    except postgrest.exceptions.APIError as err:
        print(err.message)
        return False


def get_hashed_pwd(password: str):
    byte_pwd = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(byte_pwd, bcrypt.gensalt()).decode()

    return hashed_password
    
def is_valid_password(password, hashed_password):
    byte_pwd = password.encode('utf-8')
    return bcrypt.checkpw(byte_pwd, hashed_password.encode('utf-8'))

def add_new_user(username: str, password: str):
    init_client()
    try:
        if user_exists(username):
            return "user already exists"

        supabase.table('user').insert({
            'username': username,
            'password': get_hashed_pwd(password)
        }).execute()

        return "user successfully added"
    except postgrest.exceptions.APIError as err:
        print(err.message)
        return "error adding user"
    

def add_new_shop(shop_name: str, district: str, state: str, user_id: any):
    init_client()
    try:
        supabase.table('shop').insert({
            'shop_name': shop_name,
            'district': district.lower(),
            'state': state.lower(),
            'user_id': user_id
        }).execute()

        return "shop successfully added"
    except postgrest.exceptions.APIError as err:
        print(err.message)
        return "error adding shop"


def login(username: str, password: str):
    init_client()
    if not user_exists(username): return "user does not exist"

    try:
        res = supabase.table('user').select('*').eq('username', username).limit(1).execute()
        userdata = res.data
        db_password = userdata[0]['password']
        if not is_valid_password(password, db_password):
            return "invalid password"
        else:
            return {'user_id': userdata[0]['user_id'], 'message': 'login successful'}
    except:
        return "error login"
    
def insert_transactions(shop_id, transactions):
    init_client()
    try:
        for transaction in transactions:
            transaction['shop_id'] = shop_id
            res = supabase.table('transaction').insert(transaction).execute()
        return res
    except postgrest.exceptions.APIError as err:
        print(err)
        return "error inserting transaction"
    

def get_transactions_by_location(location):
    init_client()
    response = supabase.table('transaction').select("*").execute()
    transactions = response.data

    shop_details = get_all_shops()
    shop_to_location = {}
    for shop in shop_details:
        shop_to_location[shop['shop_id']] = shop['district']

    transactions_at_location = []
    for transaction in transactions:
        shop_id = transaction['shop_id']
        if shop_to_location[shop_id] == location: transactions_at_location.append(transaction)

    return transactions_at_location


def get_transactions_in_range(lower_time, upper_time):
    init_client()
    transactions_response = supabase.table('transaction').select('*').gte('date', lower_time).lte('date', upper_time).execute()
    return transactions_response.data
