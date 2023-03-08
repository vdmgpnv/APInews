
broker_url = 'redis://localhost:6379/0'
imports = ("tasks", )
worker_disable_rate_limits = True
timezone = 'Asia/Novosibirsk'
enable_utc = False
task_routes = {'tasks': {'queue': 'fetch_queue'}}

beat_schedule = {
    'parsing': {
        'task': 'tasks.tasks.parse_news',
        'schedule': 600.0
    }
}

