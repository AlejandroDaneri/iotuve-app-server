from src.models.video import Video


def conf_job(app, scheduler):
    app.logger.info("Add job update_video_importance to scheduler")
    update_interval = 5 * 60  # 5 min
    scheduler.add_job(func=run, coalesce=True, max_instances=1, trigger="interval",
                      seconds=update_interval, id="app_server_update_video_importance",
                      replace_existing=True, args=[app])


def run(app):
    try:
        app.logger.info("Start job update_video_importance")
        Video.update_videos_importance()
        app.logger.info("End job update_video_importance")
    except Exception as e:
        app.logger.error("Error job update_video_importance", e)
