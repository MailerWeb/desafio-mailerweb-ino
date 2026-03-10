from celery import Celery
from libs.env import ENVS

celery_app = Celery(
    'booking_worker',
    broker=ENVS.CELERY_BROKER_URL,
    backend=ENVS.CELERY_RESULT_BACKEND,
    include=['tasks']
)
