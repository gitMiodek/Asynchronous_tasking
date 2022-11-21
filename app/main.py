import time
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from celery import Celery
from celery.result import AsyncResult
from dotenv import dotenv_values
from redis import Redis

config = {**dotenv_values(".env")}

celery = Celery(__name__, backend=config['BACKEND'], broker=config['BROKER'])

redis = Redis(host=config['REDIS_LOCALHOST'])

app = FastAPI()


# LONG TASK SIMULATOR
@celery.task()
def task_simulator(t: int) -> str:
    """
    Function symulationg long running proccess
    """
    start = time.time()
    for i in range(t):
        time.sleep(i)
    return f"FINISHED in {time.time() - start} s"


@app.get("/")
async def description() -> JSONResponse:
    return JSONResponse({"[INFO]": "This app is a demo of integrating fastAPI with celery, rabbitmq and redis"})


@app.post("/api/tasks", status_code=201)
async def create_task(t: int) -> JSONResponse:
    process = task_simulator.delay(t)
    return JSONResponse({"task_id": process.id})


@app.get("/api/tasks/{task_id}")
async def get_task_info(task_id: str) -> JSONResponse:
    task = AsyncResult(task_id)
    d = {"ID": task_id,
         "STATUS": task.status,
         "RESULT": task.result}
    return JSONResponse(d)


@app.get("/api/tasks")
async def get_tasks_ids() -> list:
    """
    function that get keys from redis
    and modify them to get task id
    [INFO]
    Only finished tasks!!!
    :return:
    list of those ids
    """
    ids = redis.keys('*')
    lst = []
    for id in ids:
        id = id.decode("utf-8")
        id = id.split("-")
        id = "-".join(id[3:])
        lst.append(id)

    return lst

