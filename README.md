LocustRunner
==============================

What Is This?
-------------

This is a simple Python library intended to run locust script asynchronously.


How To Use This
---------------

1. import locust_runner library to the test script file.

    example:
    ```python
   from locust_runner import run_locust, get_locust_data, display_data, close_loop, wait_locust_run_to_complete 
   ```

Testing
-------
1. Get absolute path of locust conf file and the locust py files which needs to be executed.
    
    example:
    ```python
   import os
   path = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'locust_script'
   conf_file = os.path.join(path, 'locust_streaming.conf')
   locust_py_file_to_run = os.path.join(path, 'locust_script.py') 
   ```
2. Start the locust file.
     ```python
   run_locust(conf_file, locust_py_file_to_run) 
   ```
3. The above step is asynchronous call, control will come directly to next line, where you can perform specific actions.

4. PSB for the complete sample test case to execute the file.

    ```python
   import os
   import time

   from locust_runner import run_locust, get_locust_data, display_data, close_loop, wait_locust_run_to_complete


   def test_load_example_script():
       path = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'locust_script'
       conf_file = os.path.join(path, 'locust_streaming.conf')
       locust_py_file_to_run = os.path.join(path, 'locust_script.py')
    
       print("Start my locust script in separate process")
    
       run_locust(conf_file, locust_py_file_to_run)
    
       __do_my_work()
    
       # This line will wait for locust thread to complete its task.
       wait_locust_run_to_complete()
       
       # Get the data size of locust executed job.
       locust_data_size = get_locust_data().qsize()
    
       print("Locust input request Size :: ", locust_data_size)
    
       print("Displaying locust data")
    
       # Simple display function for locust.
       display_data()
    
       # Close the loop with thread safe
       close_loop()


   def __do_my_work():
       for my_work in range(10):
           print("Performing my task during locust run")
           time.sleep(1)
   ```

