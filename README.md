
# Asynchronous tasking

This is a demo of an API which is able to handle long asynchronous tasks.

Stack used:

     FastAPI
     docker
     redis
     celery
     rabbitmq

Particular task was simulated by executing time.sleep function inside a loop



## Installation

Application requirements: docker

```bash
  cd src/
  docker-compose build
  docker-compose up
```
    
## API Reference

#### Add task to the queue

```http
  POST /api/tasks
```

| Parameter | Type     | Description                |
| :-------- | :-------  :------------------------- |
| `Number | integer| **Required**. Perform a task looped in range(1, Number).

Returns an id of a task

#### Get item

```http
  GET /api/tasks/${task_id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of task to preview the status and the result |

#### Preview all tasks

```http
GET /api/tasks
```
Returns a list of all given tasks


#### Function simulating long task
```
@celery.task()
def task_simulator(t: int) -> str:
    """
    Function symulationg long running proccess
    """
    start = time.time()
    for i in range(t):
        time.sleep(i)
    return f"FINISHED in {time.time() - start} s"
```

