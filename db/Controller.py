import datetime
import random
from peewee import SqliteDatabase

from .Model import db, User, Status, Job, Frame, Client, ClientTask
from . import Utils

# Init Connection

def init(db_path):
    db.initialize(SqliteDatabase(db_path))
    db.connect()
    db.create_tables([User, Status, Job, Frame, Client, ClientTask])
    for status in ("Idle", "Waiting For", "Ready", "Running", "Error", "Disabled", "Finished" ):
        create_status(status)
    return db

# Create Record

def create_user(name):
    return User.get_or_create(name=name)[0]

def create_status(name):
    return Status.get_or_create(name=name)[0]

def create_job( file_path, layer, app, executor, submitter=Utils.get_username(), code=Utils.code_generator(), weight=1, submit_date=datetime.datetime.now(), status="Idle", frames=[]):
    if isinstance(status, str):
        status = create_status(status)

    if not isinstance(submitter, User):
        submitter = create_user(submitter)
    job = Job.get_or_create(code=code, weight=weight, submit_date=submit_date, submitter=submitter, file_path=file_path, layer=layer, app=app, executor=executor)

    create_frames(job=job[0], frames=frames, status=status)

    return job[0]

def create_frames(job, frames, status):
    data = [ ]
    client = create_client()
    for frame in frames:
        start = datetime.datetime.now()+datetime.timedelta(seconds=random.randint(0, 60*60))
        render_time = datetime.timedelta(seconds=random.randint(0, 60*60))
        data.append({
            'job' : job, 
            'number': frame, 
            'status': random.choice(Status.select()), 
            'start_date' : start,
            'finished_date' : random.choice([start+render_time,None])
        })
    # data = [{'job':job, 'number':frame, 'status':status} for frame in frames]
    frames = Frame.insert_many(data).execute()
    assign_task(client, job.frames())
    return frames

def create_client(name=Utils.get_host(), enabled=False):
    return Client.get_or_create(name=name, enabled=enabled)[0]
    
def assign_task(client, jobs):
    data =[{'client':client, 'job':job} for job in jobs]
    tasks = ClientTask.insert_many(data).execute()
    return tasks

# Read

def get_all_job():
    return [job for job in Job.select()]

def get_job(code="", id=""):
    if code:
        return Job.get(Job.code == code)
    elif id:
        return Job.get(Job.id == id)

def get_host(name=Utils.get_host()):
    return Client.get(Client.name == name)

# Update

def update_job(code="", id="", **kwargs):
    job = get_job(code=code, id=id)
    query = job.update(**kwargs)
    query.execute()

def update_host(name=Utils.get_host(), enabled=True):
    host = get_host(name=name)
    query = host.update(enabled=enabled)
    query.execute()

# Delete

def delete_job(code="", id=""):
    if code:
        return Job.delete().where(Job.code == code)
    elif id:
        return Job.delete().where(Job.id == id)