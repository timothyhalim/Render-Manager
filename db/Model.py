from enum import unique
import os
import peewee as pw
import datetime

db = pw.DatabaseProxy()

class BaseModel(pw.Model):
    class Meta:
        database = db

class User(BaseModel):
    name = pw.CharField(unique=True, constraints=[pw.SQL('COLLATE NOCASE')])

    def jobs(self):
        jobs = Job.select().where(Job.submitter == self.id)
        return jobs

class Status(BaseModel):
    name = pw.CharField(unique=True, constraints=[pw.SQL('COLLATE NOCASE')])
    # Idle, Wait for, Running, Disabled, Finished

class Client(BaseModel):
    name = pw.CharField(unique=True, constraints=[pw.SQL('COLLATE NOCASE')])
    enabled = pw.BooleanField()

    def task(self):
        return ClientTask.get(ClientTask.client == self.id).task


class Job(BaseModel):
    code = pw.CharField(unique=True)
    weight = pw.IntegerField(default=1)
    submit_date = pw.DateTimeField(default=datetime.datetime.now)
    submitter = pw.ForeignKeyField(User)
    file_path = pw.CharField()
    layer = pw.CharField()
    app = pw.CharField()
    max_client = pw.IntegerField(default=1)
    executor = pw.CharField()

    def frames(self):
        return Frame.select().where(Frame.job == self.id)
    
    def status(self):
        return Frame.select().where(Frame.job == self.id).order_by(Frame.status).first().status

    def avg_time(self):
        frames_time = [frame.render_time() for frame in self.frames().where(Frame.finished_date.is_null(False)) if frame.render_time is not None]
        if frames_time:
            return sum(frames_time)/len(frames_time) 
        else:
            return None
    
    def frame_left(self):
        return self.frames().where(Frame.status != 7)

    def clients(self):
        return list(set([frame.client().name for frame in self.frames()]))

    def eta(self):
        avg = self.avg_time()
        frame_left = len(self.frame_left())
        clients = len(self.clients())
        if clients == 0:
            return avg * frame_left
        else:
            return avg * frame_left / clients

class Frame(BaseModel):
    job = pw.ForeignKeyField(Job)
    number = pw.IntegerField()
    status = pw.ForeignKeyField(Status, default=1)
    submit_date = pw.DateTimeField(default=datetime.datetime.now)
    start_date = pw.DateTimeField(null=True)
    finished_date = pw.DateTimeField(null=True)

    def render_time(self):
        if self.finished_date is not None:
            return (self.finished_date-self.start_date).total_seconds()
        else:
            return None

    def client(self):
        return ClientTask.get(ClientTask.job == self.id).client

class ClientTask(BaseModel):
    client = pw.ForeignKeyField(Client)
    job = pw.ForeignKeyField(Frame, unique=True)

    class Meta:
        primary_key = pw.CompositeKey('client', 'job')