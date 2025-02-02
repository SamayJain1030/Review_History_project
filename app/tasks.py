from sqlalchemy.orm import Session
from app.models.redis_model import AccessLog
from app.database.redisdb import redis_client
import json
import ssl
from celery import Celery

redis_url = "redis://user:pd@host:port"

celery_app = Celery("tasks", 
                    broker=redis_url,
                    backend=redis_url,
                    broker_use_ssl = {
        'ssl_cert_reqs': ssl.CERT_NONE
     },
     redis_backend_use_ssl = {
        'ssl_cert_reqs': ssl.CERT_NONE
     })


@celery_app.task
def log_activity(endpoint: str, timestamp: str):
    log_entry = {
        "endpoint": endpoint,
        "timestamp": timestamp
    }
    redis_client.lpush("access_logs", json.dumps(log_entry))

 