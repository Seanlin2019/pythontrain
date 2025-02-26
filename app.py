from fastapi import FastAPI


app = FastAPI()


@app.get('/')
def home():
    return "Hello, Test App!"


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)
