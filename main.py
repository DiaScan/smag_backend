from fastapi import FastAPI
import uvicorn
from store import db

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


if __name__ == '__main__':
    run_init()
    run_tests()
    uvicorn.run(app, host="0.0.0.0", port=8000)