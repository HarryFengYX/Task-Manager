import tkinter as tk
import logging
END = "end"
RETURN = "<Return>"
DOUBLE_CLICK = '<Double-Button-1>'

class Application(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super(Application, self).__init__(master, **kwargs)
        self.master = master
        self.pack(expand=1, fill=tk.BOTH)
        self.master.geometry("%dx%d"%(300, 700))
        self.create_widgets()

    def create_widgets(self):
        self.createTaskButton = tk.Button(self, text="Create Task", command=self.createTask)
        self.createTaskButton.pack()
        self.deleteTaskButton = tk.Button(self, text="Delete Task", command=self.deleteTask)
        self.deleteTaskButton.pack()
        self.finishTaskButton = tk.Button(self, text="Finish Task", command=self.finishTask)
        self.finishTaskButton.pack()

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")
        self.taskListbox = TaskListbox(self)
        self.taskListbox.pack()

    def createTask(self):
        tc = TaskCreation(self.master, self.taskListbox)

    def deleteTask(self):
        # print(list(self.taskListbox.curselection()))
        for i in sorted(list(self.taskListbox.curselection()), reverse=True):
            self.taskListbox.delete(i)

    def finishTask(self):
        print("finish task")

class MyListbox(tk.Listbox):
    def __init__(self, master=None, pack=True, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        if pack: self.pack()

class TaskListbox(MyListbox):
    def __init__(self, master=None, listbox=[], **kwargs):
        super().__init__(master, selectmode=tk.EXTENDED, **kwargs)
        self.listbox = listbox
        self.bind()

    def addTask(self, task):
        if type(task) != Task:
            logging.critical("Task list adding not task error")
        else:
            self.listbox.append(task)
            self.insert(END, task.name)

class TaskCreation(tk.Toplevel):
    def __init__(self, master=None, taskListbox=None):
        super().__init__(master)
        self.taskListbox = taskListbox
        self.nameEntry = tk.Entry(self)
        self.taskTypeEntry = tk.Entry(self)
        self.createTask = tk.Button(self, text="Create Subtask", command=self.createSubtask)
        self.subtaskListbox = TaskListbox(self, pack=False)
        self.subtaskList = []
        self.timeEntry = tk.Entry(self)

        # packing
        tk.Label(self, text="Name:").pack()
        self.nameEntry.pack()
        tk.Label(self, text="Type:").pack()
        self.taskTypeEntry.pack()
        tk.Label(self, text="Subtasks").pack()
        self.createTask.pack()
        self.subtaskListbox.pack()
        self.bind(RETURN, self.addToTaskListbox)

    def addToTaskListbox(self, event):
        if self.taskListbox == None:
            logging.critical("No task list specified for task creation")
        else:
            newTask = Task(self.nameEntry.get(), self.subtaskList, self.taskTypeEntry.get())
            self.taskListbox.addTask(newTask)

    def createSubtask(self, ):
        TaskCreation(self, taskListbox=self.subtaskListbox)

class Task:
    def __init__(self, name=None, subTasks=[], taskType=None):
        self.name = name # how do we call this
        self.subTasks = subTasks # smaller tasks that makes this task
        self.taskType = taskType # relaxing? workout? brain-intensive?

    def __str__(self, ):
        return "(%s, %s)" % (self.name, self.taskType)

logging.basicConfig(filename='taskManager.log', level=logging.DEBUG, format='%(asctime)-15s %(message)s')
root = tk.Tk()
app = Application(master=root)
tk.mainloop()
