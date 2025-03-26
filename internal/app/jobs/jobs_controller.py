import internal.app.jobs.jobs_service as js

class JobsController:
    def __init__(self):
        self._service_publish_jobs = js.JobService()

    def run(self):
        self._service_publish_jobs.Start()