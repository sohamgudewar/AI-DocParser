"""Celery worker entry point: python worker.py or celery -A worker worker --loglevel=info"""

from modules.tasks import celery_app

if __name__ == "__main__":
    celery_app.start()
