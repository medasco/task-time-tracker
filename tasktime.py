
import json

from dateutil import parser


class TimeInput:
    def __init__(self, start_time, end_time, days, hours, minutes, seconds):
        self.start_time = start_time
        self.end_time = end_time
        self.total_time = end_time - start_time
        self.days = days
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
    
    def get_time_details(self):
        self.days, self.seconds = self.total_time.days, self.total_time.seconds
        self.hours = self.days * 24 + self.seconds // 3600 
        self.minutes = (self.seconds % 3600) // 60
        self.seconds = self.seconds % 60

    def publish(self):
        return {
            "start_time": self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "end_time": self.end_time.strftime("%Y-%m-%d %H:%M:%S"),
            "days": self.days,
            "hours": self.hours,
            "minutes": self.minutes,
            "seconds": self.seconds
        }

    
class Task:
    def __init__(self, title, time_in):
        self.title = title
        self.time_in = time_in
        
    def create_time_inputs_to_json(self):
        time_in_list = []
        for input_time in self.time_in:
            time_in_list.append(input_time.publish())
        return time_in_list

    def publish(self):
        return  {
            "title": self.title,
            "time_in": self.create_time_inputs_to_json()
        }


class TaskRecord:
    def __init__(self, tasks):
        self.tasks = tasks

    def set_task_record(self):
        task_record = TaskRecord([])
        with open("tasks.json", "r") as f:  
            data = json.load(f)
            task_record = TaskRecord(
                tasks = self.get_tasks_from_json(data)
            )
        return task_record
    
    def get_tasks_from_json(self, data):
        data_record = []
        for item in data["tasks"]:
            data_record.append(
                Task(
                    title = item["title"],
                    time_in = self.get_time_inputs_from_json(item)
                )
            )
        self.tasks = data_record
        return data_record
    
    def get_time_inputs_from_json(self, data):
        data_record = []
        for item in data["time_in"]:
            data_record.append(
                TimeInput(
                    start_time = parser.parse(item["start_time"]),
                    end_time = parser.parse(item["end_time"]),
                    days = item["days"],
                    hours = item["hours"],
                    minutes = item["minutes"],
                    seconds = item["seconds"],
                )
            )
        self.time_in = data_record
        return data_record

    def create_tasks_to_json(self):
        tasks_record = []
        for task in self.tasks:
            tasks_record.append(task.publish())
        
        return tasks_record

    def publish(self):
        return {
            "tasks": self.create_tasks_to_json()
        }
