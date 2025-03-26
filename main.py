from comnd.mid import middleware
from internal.app.jobs import jobs_controller
import logging.config


if __name__ == '__main__':
    middleware.setup_middleware()
    logging.info("Inicio del proceso AIG publish jobs - *ASPEND* V1")
    jobs_controller.JobsController().run()