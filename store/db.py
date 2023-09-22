import os
from supabase import create_client, Client

SUPABASE_PUBLIC_URL : str = ''
SUPABASE_SERVICE_ROLE : str = ''
supabase: Client = None


def init():
    global SUPABASE_PUBLIC_URL, SUPABASE_SERVICE_ROLE, supabase
    SUPABASE_PUBLIC_URL = os.environ.get('SUPABASE_PUBLIC_URL')
    SUPABASE_SERVICE_ROLE = os.environ.get('SUPABASE_SERVICE_ROLE')
    supabase = create_client(supabase_url=SUPABASE_PUBLIC_URL, supabase_key=SUPABASE_SERVICE_ROLE)


def get_all_shops():
    shop_records = supabase.table('shop').select("*").execute()
    return shop_records




