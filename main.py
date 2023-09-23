from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from mltoolkit import apriori, frequency_metric
from store import db
from utils import csv_parser
from wrapper import gpt
import datetime as dt



class User(BaseModel):
    username: str
    password: str

class Shop(BaseModel):
    user_id: str
    shop_name: str
    district: str
    state: str


app = FastAPI()

origins = [
    "*"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def run_init():
    try:
        import env
        print('Running init')
        env.init()
    except:
        print("NO ENV")
    db.init_client()


def run_tests():
    print(db.get_all_shops_of_user().data)
    print(db.get_all_users().data)
    return


@app.get('/')
async def hello():
    return {'message': 'go to /docs to test the routes'}


@app.get('/frequent_patterns')
async def frequent_patterns():
    transactions = db.get_all_transactions()
    frequent_patterns = apriori.get_frequent_patterns(transactions)
    return frequent_patterns


@app.get('/get_suggested_patterns')
async def frequent_pattterns_by_shop(shop_id):
    shop_details = db.get_shop_details(shop_id)
    transactions = db.get_all_transactions_of_shop(shop_id)
    frequent_patterns = apriori.get_frequent_patterns(transactions)
    return {'shop_details': shop_details, 'buy_patterns' : frequent_patterns}

@app.post('/register_user')
async def register_user(user: User):
    res = db.add_new_shop(user.username, user.password)
    return {"message": res}


@app.post('/login_user')
async def login_user(user: User):
    res = db.login(user.username, user.password)
    return {"message": res}

@app.get('/transactions')
async def get_all_transactions():
    return db.get_all_transactions()

@app.post('/add_transactions')
async def upload_file(file: UploadFile, shop_id):
    file_data = csv_parser.parse_file(file)
    db.insert_transactions(shop_id, file_data)
    return {"message": file_data}

@app.get('/shops')
async def get_shops(user_id):
    user_shops = db.get_all_shops_of_user(user_id)
    return user_shops

@app.get('/shop')
async def get_shop_details(shop_id):
    shop_details = db.get_shop_details(shop_id)
    return {'shop_details': shop_details}

@app.get('/top_items_by_location')
async def get_top_items_by_location(location: str):
    transactions = db.get_transactions_by_location(location)
    res = frequency_metric.get_top_k_most_sold_items(3, transactions)
    return { 'top_sold_items': res, 'location': location }


@app.get('/top_items_by_store')
async def top_items_by_store(shop_id):
    transactions = db.get_all_transactions_of_shop(shop_id)
    res = frequency_metric.get_top_k_most_sold_items(3, transactions)
    shop_details = db.get_shop_details(shop_id)
    return {'top_sold_items': res, 'shop_details': shop_details }


@app.get('/top_items_by_time')
async def get_top_items_by_time(time: str):
    year, month, date = time.split('-')
    lower_date, upper_date = max(1, int(date) - 5), min(30, int(date) + 5)
    lower_full_date = ('-').join([str(lower_date), month, year])
    upper_full_date = ('-').join([str(upper_date), month, year])

    ld = dt.datetime.strptime(lower_full_date, "%d-%m-%Y")
    ld = ld.date()
    ld = ld.isoformat()

    ud = dt.datetime.strptime(upper_full_date, "%d-%m-%Y")
    ud = ud.date()
    ud = ud.isoformat()


    # print(upper_full_date, lower_full_date)
    transactions = db.get_transactions_in_range(ld, ud)
    if transactions is None: return {'messsage': 'insufficient data'}
    res = frequency_metric.get_top_k_most_sold_items(3, transactions)
    return {'top_sold_items': res}


@app.post('/shop')
async def add_shop(shop: Shop):
    res = db.add_new_shop(shop.shop_name, shop.district, shop.state, shop.user_id)
    return {'message': res}

@app.get('/improve_top_product_sales')
async def add_improve_top_product_sales(product_name: str):
    res = gpt.improve_top_product_sales(product_name)
    return {'strategy': res}

@app.get('/improve_low_product_sales')
async def add_improve_low_product_sales(product_name: str):
    res = gpt.improve_low_product_sales(product_name)
    return {'strategy': res}

if __name__ == '__main__':
    run_init()
    # run_tests()
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
