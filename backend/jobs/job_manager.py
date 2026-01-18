import uuid
from jobs.job_types import JobStatus

class Job:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.progress = 0
        self.status = JobStatus.queued
        self.result_url = None
        self.cancelled = False

class JobManager:
    def __init__(self):
        self.jobs = {}

    def create_job(self):
        job = Job()
        self.jobs[job.id] = job
        return job

    def get_job(self, job_id: str):
        return self.jobs.get(job_id)

    def cancel_job(self, job_id: str):
        job = self.get_job(job_id)
        if job:
            job.cancelled = True
            job.status = JobStatus.cancelled
        return job

job_manager = JobManager()
