import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from src.jobs.update_video_importance import conf_job


def init_jobs(app):
    app.logger.debug("Init jobs scheduler")
    global scheduler
    scheduler = BackgroundScheduler(timezone="UTC", daemon=True)
    conf_job(app, scheduler)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())
    app.logger.debug("End jobs scheduler")
