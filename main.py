from fastapi import FastAPI
import uvicorn
from store import db
from mltoolkit import apriori

app = FastAPI()

def run_init():
    try:
        import env
        env.init()
    except (e) as e:
        print(e)
    db.init()

def run_tests():
    # print(db.get_all_shops().data)
    return


@app.get('/')
async def hello():
    return {'message': 'go to /docs to test the routes'}


@app.get('/frequent_patterns')
async def frequent_patterns():
    frequent_patterns = apriori.get_frequent_patterns()
    return frequent_patterns



if __name__ == '__main__':
    # run_init()
    run_tests()
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)