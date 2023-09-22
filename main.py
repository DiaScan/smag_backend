from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from mltoolkit import apriori
from store import db


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
    print(db.get_all_shops().data)
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


class User(BaseModel):
    username: str
    password: str


@app.post('/register_user')
async def register_user(user: User):
    res = db.add_new_user(user.username, user.password)
    return {"message": res}


@app.post('/login_user')
async def login_user(user: User):
    res = db.login(user.username, user.password)
    return {"message": res}

@app.get('/transactions')
async def get_all_transactions():
    return db.get_all_transactions()

@app.post('/file')
async def upload_file(file: UploadFile):
    # file_data = parse_file(file.file)
    pass

@app.get('/shops')
async def get_shops(user_id):
    user_shops = db.get_all_shops(user_id)
    return user_shops

if __name__ == '__main__':
    run_init()
    # run_tests()
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
