import asyncio
import os
from threading import Thread
from queue import Queue

q = Queue()
t = Thread()


class __SubprocessProtocol(asyncio.SubprocessProtocol):
    """Private class which inherits asyncio Subprocess protocol, and receives subprocess PIPE data."""

    def pipe_data_received(self, fd, data):
        """Called when the subprocess writes data into stdout/stderr pipe.

        fd is int file descriptor.
        data is bytes object.
        """
        if fd == 1:  # got stdout data (bytes)
            decoded_data = data.decode()
            q.put(decoded_data)
            print("STDOUT", data)

    def connection_lost(self, exc):
        """Called when a file descriptor associated with the child process is
               closed.
        """
        loop.stop()  # end loop.run_forever()


loop = asyncio.new_event_loop()


def run_locust(locust_conf_file: str, locust_py_file: str):
    """Method to run the locust file , Non-blocking call

    :param locust_conf_file locust conf file absolute path.
        example file content:
            headless = true
            users = 1
            spawn-rate = 1
            run-time = 1m
    :param locust_py_file .py file execute the locust, absolute path of py file.

    :return None """

    if not os.path.exists(locust_conf_file):
        print("Invalid conf file, expected absolute path of conf file")
        raise FileNotFoundError("Invalid conf file, expected absolute path of conf file")
    if not os.path.exists(locust_py_file):
        print("Invalid py file, expected absolute path of py file")
        raise FileNotFoundError("Invalid .py file, expected absolute path of .py file")

    try:
        global t
        # Create subprocess execution task.
        loop.create_task(loop.subprocess_exec(__SubprocessProtocol,
                                              "locust", "-f", locust_py_file, "--config=" + locust_conf_file))
        t = Thread(target=loop.run_forever)
        t.start()
    except Exception as e:
        print(str(e))


def wait_locust_run_to_complete(time_out=60):
    """This method will wait for the running locust thread to complete.

    :param time_out max timeout for thread to complete."""

    try:
        print("waiting locust thread to complete")
        if t: t.join(timeout=time_out)
    except Exception as e:
        print(e)


def close_loop():
    """Close the running event loop, this can be called
    at the end of execution for smooth close of event loop. """

    try:
        global t
        if t:
            t.join()
        loop.close()
    except Exception as e:
        print(str(e))


def get_locust_data():
    """Get complete queue data of locust file execution."""

    return q


def display_data():
    """Method to display the queue data, this will be popping the elements from queue."""
    while not q.empty():
        print("****** QUEUE DATA ****** \n", q.get())


if __name__ == '__main__':
    path = os.path.dirname(os.path.abspath(__file__))
    conf_file = os.path.join(path, 'locust_streaming.conf')
    locust_py_file_to_run = os.path.join(path, 'locust_streaming.py')
    run_locust(conf_file, locust_py_file_to_run)
    data = get_locust_data()
    display_data()
    print("completed")
