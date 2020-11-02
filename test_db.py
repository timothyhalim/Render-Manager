import os
from db import Controller

db_path = os.path.join( __file__, "..", "RenderManager.db" )
Controller.init(db_path)

# Create Job

job = Controller.create_job( 
        r"J:\UCG\Episodes\Scenes\EP100\SH002.00A\UCG_EP100_SH002.00A_CMP.nk", 
        "WRITE_IMG", 
        r"J:\UCG\UCG_Nuke10.bat", 
        "renderNuke.py", 
        frames=[i for i in range(100)]
    )

# Query Job

JobList = Controller.Job.select()
for job in JobList:
    print("Job", job.code)
    print("Status", job.status().name)
    print("Left", len([frame.number for frame in job.frame_left()]))
    print("Avg", job.avg_time())
    print("Eta", job.eta())
    print("Clients", job.clients())
    print()
    # for frame in job.frames():
    #     print("Frame", frame.number)
