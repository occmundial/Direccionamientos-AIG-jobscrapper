from abc import ABC, abstractmethod


class JobFunctionaliter(ABC):
    @abstractmethod
    def download_s3_file(self):
        pass

    @abstractmethod
    def get_data_from_file(self):
        pass

    @abstractmethod
    def process_information(self):
        pass