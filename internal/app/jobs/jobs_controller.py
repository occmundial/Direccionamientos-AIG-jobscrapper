import internal.app.jobs.jobs_service as js

class JobsController:
    def __init__(self):
        self.service_publish_jobs = js.JobService()

    def run(self):
        if self.service_publish_jobs.s3conn is not None and self.service_publish_jobs.db_conn is not None:
            self.service_publish_jobs.Start()