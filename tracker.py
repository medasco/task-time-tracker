
import time
import win32gui
import datetime
import uiautomation as auto

from tasktime import *


def main():
    active_window_title = ""
    task_title = ""

    time_start = datetime.datetime.now()
    task_logger = TaskRecord([])
    initial_task = True

    try:
        task_logger.set_task_record()
    except Exception:
        print("::: No JSON file yet, switch task window or tab to record :::")

    try:
        while True:
            new_window_title = get_active_window()
            if active_window_title != new_window_title:
                print(active_window_title)
                task_title = active_window_title

                if not initial_task:
                    time_end = datetime.datetime.now()
                    time_input = TimeInput(time_start, time_end, 0, 0, 0, 0)
                    time_input.get_time_details()

                    task_is_found = False
                    for task in task_logger.tasks:
                        if task.title == task_title:
                            task_is_found = True
                            task.time_in.append(time_input)
                    
                    if not task_is_found:
                        task_time = Task(task_title, [time_input])
                        task_logger.tasks.append(task_time)

                    with open("tasks.json", "w", encoding="utf-8") as jfile:
                        json.dump(task_logger.publish(), jfile, ensure_ascii=False, indent=2)
                        time_start = datetime.datetime.now()

                initial_task = False 
                active_window_title = new_window_title

            time.sleep(1)
    
    except KeyboardInterrupt:
        task_title = get_active_window()
        print(task_title)

        time_end = datetime.datetime.now()
        time_input = TimeInput(time_start, time_end, 0, 0, 0, 0)
        time_input.get_time_details()

        obtain = False
        for task in task_logger.tasks:
            if task.title == task_title:
                obtain = True
                task.time_in.append(time_input)
        
        if not obtain:
            task_time = Task(task_title, [time_input])
            task_logger.tasks.append(task_time)

        with open("tasks.json", "w", encoding="utf-8") as ofile:
            json.dump(task_logger.publish(), ofile, ensure_ascii=False, indent=2)
            time_start = datetime.datetime.now()
            
def get_active_window():
    window = win32gui.GetForegroundWindow()
    window_text = win32gui.GetWindowText(window)
    return window_text


if __name__ == "__main__":
    main()
