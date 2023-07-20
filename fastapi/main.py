import json
from pydantic import BaseModel
from fastapi import FastAPI
from broker import celery

app = FastAPI()

class Item(BaseModel):
    number: int


@app.post("/cpu_task/")
async def cpu_task(item: Item):
    task_name = "cpu.task"
    task = celery.send_task(task_name, args=[item.number], kwargs={}, queue='cpu_task')
    return dict(id=task.id, url='localhost:8000/check_task/{}'.format(task.id))


@app.post("/gpu_tast/")
async def gpu_tast(item: Item):
    task_name = "gpu.task"
    task = celery.send_task(task_name, args=[item.number], kwargs={}, queue='gpu_task')
    return dict(id=task.id, url='localhost:8000/check_task/{}'.format(task.id))

@app.get("/check_task/{id}")
def check_task(id: str):
    task = celery.AsyncResult(id)
    if task.state == 'SUCCESS':
        response = {
            'status': task.state,
            'result': task.result,
            'task_id': id
        }
    elif task.state == 'FAILURE':
        response = json.loads(task.backend.get(task.backend.get_key_for_task(task.id)).decode('utf-8'))
        del response['children']
        del response['traceback']
    else:
        response = {
            'status': task.state,
            'result': task.info,
            'task_id': id
        }
    return response