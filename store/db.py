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


def get_all_shops():
    shop_records = supabase.table('shop').select("*").execute()
    return shop_records


def get_all_users():
    user_records = supabase.table('user').select("*").execute()
    return user_records


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
            return "login successful"
    except:
        return "error login"