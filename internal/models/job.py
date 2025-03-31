class Job:
    def __init__(self, job_id, reference_id, title, location, url, description):
        self.job_id = job_id
        self.reference_id = reference_id
        self.title = title
        self.location = location
        self.location_id = []
        self.url = url
        self.description = description
        self.job_type = '1'
        self.commercial_name = '0'
        self.bullet1 = ''
        self.bullet2 = ''
        self.bullet3 = ''
        self.show_salary = 'False'
        self.skills = []
        self.salary_prediction = []
        self.salary_min = 0
        self.salary_max = 0

