# Celery Worker with Redis Integration

This package provides a simple implementation to register and manage tasks for a Celery worker, with Redis as the broker and result backend. It includes functionality for registering regular tasks, periodic tasks, and configuring various aspects of the Celery worker and Redis connection.

## Features

- Register and manage tasks with optional queues.
- Register periodic tasks with customizable schedules using crontab or timedelta.
- Configure Celery worker settings such as time zone, task serializers, result backend, and retry options.
- Set up Redis as the broker and backend with SSL support for secure connections.
- Automatically discover tasks for the Celery worker.

## Requirements

- Python 3.11+
- Celery
- dtpyredis

## Requirements

```bash
pip install dtpyworker
```

## Usage

### Define Tasks

To define tasks, create a Task object and register your routes:

```python
from dtpyworker.task import Task, crontab

task_manager = (
    Task()
    .register(route="my_task_route")
    .register_periodic_task(
        route="my_periodic_task_route",
        schedule=crontab(minute="*/5"),
        queue="default_queue"
    )
)
```

### Set Up Worker

Create a Worker instance, configure it with the Redis instance and registered tasks, and then create the Celery app

```python
from dtpyworker.worker import Worker
from dtpyredis.config import RedisConfig
from dtpyredis.connection import RedisInstance

# Initialize Redis connection
redis_config = RedisConfig()
redis_config.set_redis_host('localhost')
redis_config.set_redis_port(6379)
redis_config.set_redis_db(0)

redis_instance = RedisInstance(redis_config=redis_config)

# Initialize Worker and configure
worker = (
    Worker()
    .set_redis(redis_instance)
    .set_task(task_manager)
    .set_name("my_worker")
    .set_timezone("UTC")
)

# Create Celery app
celery_app = worker.create()
```

### Task Example

Define a simple task that can be executed by the worker:

```python
from dtpyworker.task import shared_task

@shared_task
def my_task():
    print("Executing my task!")
```

### Running the Worker

To start the Celery worker, run the following command in your terminal:

```bash
celery -A your_package.celery_app worker --loglevel=info
```

For periodic tasks, run the Celery Beat scheduler alongside the worker:

```bash
celery -A your_package.celery_app beat --loglevel=info
```
