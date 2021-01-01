import time
from locust import User, SequentialTaskSet, task, between


class ApiTask(SequentialTaskSet):
    wait_time = between(1, 5)

    def on_start(self):
        """ on_start is called when a Locust start
        before any task is scheduled """

        print("Locust On Start method.")

    def create_random_name(self):
        print("Random Name is created.")
        self._time_to_sync_object_creation()

    def rename_names(self):
        print("Rename is successful")
        self._time_to_sync_object_creation()

    def move_names_to_back(self):
        print("Names moved to original position")
        self._time_to_sync_object_creation()

    def delete_name(self):
        print("Deleted the name")
        self._time_to_sync_object_creation()

    def create_role(self):
        print("Role is created.")
        self._time_to_sync_object_creation()

    def delete_role(self):
        print("Role is deleted.")
        self._time_to_sync_object_creation()

    @staticmethod
    def _time_to_sync_object_creation(t=2):
        time.sleep(t)

    @task(1)
    def test_create_name(self):
        """This task will create a group"""
        self.create_random_name()

    @task(1)
    def test_delete_name(self):
        """This task will delete the created group"""
        self.delete_name()

    @task(1)
    def test_create_role(self):
        """This task will create a new role in account settings"""
        self.create_role()

    @task(1)
    def test_delete_role(self):
        """This task will create a new role in account settings"""
        self.delete_role()

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping
        Add some cleaning process for group deletions.
        """
        print("Locust On Stop method called.")


class ApiUser(User):
    wait_time = between(3, 5)
    tasks = [ApiTask]

