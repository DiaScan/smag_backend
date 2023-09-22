import os
import postgrest
from supabase import create_client, Client

SUPABASE_PUBLIC_URL: str = ''
SUPABASE_SERVICE_ROLE: str = ''

supabase: Client = None


def init_client():
    global SUPABASE_PUBLIC_URL, SUPABASE_SERVICE_ROLE, supabase
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


def add_new_user(username: str, password: str):
    init_client()
    try:
        if user_exists(username):
            return "user already exists"

        supabase.table('user').insert({
            'username': username,
            'password': password
        }).execute()

        return "user successfully added"
    except postgrest.exceptions.APIError as err:
        print(err.message)
        return "error adding user"
