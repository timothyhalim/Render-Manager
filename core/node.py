import os
import time
import re
import glob
import getpass
import subprocess
import platform
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString
from pathlib import Path

def unc_drive(file_path):
    return str(Path(file_path).resolve())
    
import win32wnet
from PySide.QtCore import *

def getUNC(filepath):
	drive, path = os.path.splitdrive(filepath)
	try:
		drive = win32wnet.WNetGetUniversalName(drive, 1)
	except:
		pass
	path = os.path.normpath(os.path.join(drive, path))
	return path.replace("\\",'/')

def normalizeFramePath(filePath):
	fileName = os.path.basename(filePath)
	fileDir = os.path.dirname(filePath)
	# Replace "%??d" expression
	pattern = "[\%][0-9]+[d]"
	matchPattern = {}
	for m in re.finditer(pattern, fileName):
		matchPattern[m.group(0)] = [m.start(), m.end()]
	newfilePath = ""
	start = 0
	for k in matchPattern.keys():
		newfilePath += fileName[start:matchPattern[k][0]]
		newfilePath += "{{frame:{digit}d}}".format(digit=k[1:-1])
		start = matchPattern[k][1]
	newfilePath += fileName[start:len(fileName)]
	fileName = newfilePath
	# Replace "#" symbol
	hashtagList = [s for s in [item[0] for item in re.findall(r"((.)\2*)", fileName)] if "#" in s]
	for r in sorted(hashtagList, reverse = True):
		fileName = fileName.replace(r, "{{frame:0{digit}d}}".format(digit=len(r)))
	return os.path.normpath(os.path.join(fileDir, fileName)).replace("\\",'/')

def deleteFrames(outputFile, frameList=[]):
	for frame in frameList:
		deleteFiles = glob.glob(outputFile.format(frame=frame)+"*")
		tryCount = 0
		while deleteFiles and tryCount < 3:
			try:
				for df in deleteFiles:
					if os.path.exists(df):
						os.remove(df)
					deleteFiles.remove(df)
					print (df, "Deleted")
			except:
				time.sleep(1)
				tryCount += 1
		else:
			if deleteFiles:
				print ("Fail to delete", deleteFiles)

def generateFrameList(frameStart, frameEnd, frameIncrement):
	frameList = [frame for frame in range(int(frameStart), int(frameEnd)+1) if (frame+int(frameIncrement)-1) % int(frameIncrement) == 0]
	return frameList

def exportJobData(xmlPath, id, priority, worker, submitter, nukeApp, pythonScript, nukeFile, writeName, outputFile, status, frameList=[], frameRendered=[], frameError=[]):
	if xmlPath:
		xmlPath = str(xmlPath)
		if not os.path.exists(os.path.dirname(xmlPath)):
			os.makedirs(os.path.dirname(xmlPath))
		if os.path.isdir("/".join(xmlPath.split("/")[0:-1])):
			root = ET.Element("NukeRenderJob")
			ET.SubElement(root, "id").attrib["value"] = str(id)
			ET.SubElement(root, "priority").attrib["value"] = str(priority)
			ET.SubElement(root, "worker").attrib["value"] = str(worker)
			ET.SubElement(root, "submitter").attrib["value"] = submitter
			ET.SubElement(root, "nukeApp").attrib["value"] = nukeApp
			ET.SubElement(root, "pythonScript").attrib["value"] = pythonScript
			ET.SubElement(root, "nukeFile").attrib["value"] = nukeFile
			ET.SubElement(root, "writeName").attrib["value"] = writeName
			ET.SubElement(root, "outputFile").attrib["value"] = outputFile
			ET.SubElement(root, "status").attrib["value"] = status
			ET.SubElement(root, "frameList").attrib["value"] = str("[{list}]".format(list=",".join([str(n) for n in frameList])))
			ET.SubElement(root, "frameRendered").attrib["value"] = str("[{list}]".format(list=",".join([str(n) for n in frameRendered])))
			ET.SubElement(root, "frameError").attrib["value"] = str("[{list}]".format(list=",".join([str(n) for n in frameError])))
			
			tostring = ET.tostring(root)
			domObject = parseString(tostring)
			domObject.toprettyxml(encoding='utf-8')
			with open(xmlPath, "wb") as xmlFile:
				domObject.writexml(xmlFile, addindent='\t', newl='\n')
			

def importJobData(xmlPath):
	if xmlPath:
		if os.path.exists(xmlPath):
			jobData = {}
			xmlRoot = None
			try:
				tree = ET.parse(xmlPath)
				root = tree.getroot()
				xmlRoot = root.getchildren()
			except Exception, e:
				raise Exception("%s is not a valid xml file" % xmlPath)
			
			for xmlNode in xmlRoot:
				tag = xmlNode.tag
				value = xmlNode.attrib.get("value")
				jobData [tag] = value
			
			return jobData

def workerJobCommand(nukeExe, workerCount, renderThreads, pythonScript, nukeFile, writeName, outputFile, frameList):
	outputFilename = os.path.basename(outputFile)
	search = "[{]frame:[0-9]+[d][}]"
	multipleFrame = True if (re.search(search, outputFilename) or "#" in outputFilename) else False
	# Filter for video file
	if not multipleFrame:
		renderThreads = workerCount
		workerCount = 1 
	workerCount = workerCount if workerCount < len(frameList) else len(frameList)
	
	cmdList = []
	for worker in range(workerCount):
		workerFrames = sorted([frame for i, frame in enumerate(frameList) if (i+worker) %(workerCount) == 0])
		flags = [
			"{nukeExe}".format(nukeExe=nukeExe), 
			"-i", # Use interactive license
			"-f", # Full Resolution not using Proxy
			"-m", "{renderThreads}".format(renderThreads=renderThreads), # Number of Thread Used
			"-t", "{pythonScript}".format(pythonScript=pythonScript), # Python Script For Rendering
			# Below would be the argument for python script
			"{nukeFile}".format(nukeFile=nukeFile), # NukeScriptFile for Python Argument
			"{writeName}".format(writeName=writeName), # Render Specific Write Node
			"{workerFrames}".format(workerFrames=workerFrames), # Frame List
			"{skip}".format(skip=True) # Skip existing frame
		]
		cmdList.append(flags)
	
	return cmdList

class RenderThread(QThread):
	workerDone = Signal(int)
	workerSignal = Signal(str)
	
	def __init__(self, cmd, logFile=None, parent=None):
		super(RenderThread, self).__init__()
		self.cmd = cmd
		self.frameLeft = eval(self.cmd[-2])
		self.logFile = logFile
		self.workerError = False
		self.pid = None
	
	def __del__(self):
		self.running = self.process.poll() is None
		if self.running:
			self.stop()
	
	def saveLog(self, message):
		with open(self.logFile, "a") as file:
			file.write("{message}".format(message=message)) # log
	
	def emitSignal(self):
		self.workerSignal.emit( "Worker {pid:^6} {status}".format(pid=self.pid, status=self.workerStatus) )
	
	def stop(self):
		if self.pid:
			operatingSystem = platform.system()
			if operatingSystem == "Windows":
				subprocess.Popen("taskkill /F /T /PID {pid}".format(pid=self.pid), shell=True)
				self.workerStatus = "Killed"
				self.emitSignal()
	
	def run(self):
		self.process = subprocess.Popen(self.cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		self.pid = int(self.process.pid)
		self.workerCurrent = self.frameLeft[0]
		
		a = self.process.stdout.readline()
		self.workerStatus = "Running"
		self.emitSignal()
		while a:
			message = "{id}:{message}".format(id=self.pid, message=a)
			if self.logFile:
				self.saveLog(message)
			if all(word in a for word in ["Frame", "rendering"]):
				self.workerCurrent = int(a.split(" ")[1])
				self.workerStatus = "Rendering frame {frame}".format(frame=self.workerCurrent)
				self.emitSignal()
			
			if all(word in a for word in ["Frame", "rendered"]):
				self.workerCurrent = int(a.split(" ")[1])
				self.workerDone.emit(self.workerCurrent)
				self.frameLeft.remove(self.workerCurrent)
				self.workerStatus = "Done rendering frame {frame}".format(frame=self.workerCurrent)
				self.emitSignal()
				
				self.workerCurrent = None
			a = self.process.stdout.readline()
		
		e = self.process.stderr.readline()
		while e:
			if "error" in e.lower():
				self.workerError = True
				self.frameLeft.remove(self.workerCurrent)
				self.workerStatus = "Error\n{message}".format(message=e)
				self.emitSignal()
			message = "{id}:{message}".format(id=self.pid, message=e)
			if self.logFile:
				self.saveLog(message)
			e = self.process.stderr.readline()
			
		prg = self.process.returncode
		if prg == None:
			self.workerStatus = "Finished"
			self.emitSignal()

class RenderNode(QObject):
	statusSignal = Signal(str)
	percentSignal = Signal(float)
	prioritySignal = Signal(str)
	workerSignal = Signal(int)
	jobMessage = Signal(dict)
	
	def __init__(self):
		super(RenderNode, self).__init__()
		self.infoFile = ""
		self.id = 0
		self.priority = 1
		self.submitter = "User"
		self.nukeApp = ""
		self.workerCount = 1
		self.renderThreads = 1
		self.pythonScript = ""
		self.nukeFile = ""
		self.writeName = ""
		self.outputFile = ""
		self.frameList = []
		self.frameRendered = []
		self.frameError = []
		# statusList = ["Waiting", "Running", "Disabled", "Finished", "Deleted"]
		self.status = "Waiting"
		self.percentage = 0.0
		self.workers = []
	
	def __del__(self):
		if self.workers:
			self.stopRender()
	
	def emitStatus(self):
		self.statusSignal.emit( self.status )
	
	def emitPriority(self):
		self.prioritySignal.emit( str(self.priority) )
		
	def getInfo(self):
		# print ("getInfo")
		if self.infoFile:
			jobData = importJobData(self.infoFile)
			if jobData:
				self.id = jobData["id"] 
				self.priority = int(jobData["priority"])
				self.workerCount = int(jobData["workerCount"]) if "workerCount" in jobData.keys() else 1
				self.submitter = jobData["submitter"] 
				self.logFile = os.path.normpath(os.path.join(os.path.dirname(self.infoFile), "jobLogs", "{id}_log.txt".format(id=self.id)))
				self.nukeApp = jobData["nukeApp"]
				self.pythonScript = jobData["pythonScript"]
				self.nukeFile = jobData["nukeFile"]
				self.writeName = jobData["writeName"]
				self.outputFile = jobData["outputFile"]
				self.status = jobData["status"]
				self.frameList = eval(jobData["frameList"])
				self.frameRendered = eval(jobData["frameRendered"]) if "frameRendered" in jobData.keys() else []
				self.frameError = eval(jobData["frameError"]) if "frameError" in jobData.keys() else []
				self.percentage = (float(len(self.frameRendered))/len(self.frameList))*100
			
			self.emitStatus()
			self.emitPriority()
			self.percentSignal.emit( self.percentage )
	
	def updateInfo(self):
		# print("updateInfo")
		self.frameList.sort()
		self.frameRendered.sort()
		self.frameError.sort()
		
		exportJobData(
			self.infoFile, self.id, self.priority, self.workerCount,
			self.submitter, self.nukeApp, self.pythonScript, 
			self.nukeFile, self.writeName, self.outputFile, self.status, 
			self.frameList, self.frameRendered, self.frameError
		)
	
	def createCommand(self, workerCount=1, renderFrameList=[]):
		commands = workerJobCommand(
			self.nukeApp,
			workerCount, 
			self.renderThreads, 
			self.pythonScript,
			self.nukeFile, 
			self.writeName, 
			self.outputFile, 
			renderFrameList
		)
		return commands
	
	def updateProgress(self, value = None):
		if not value is None:
			self.frameRendered.append(value)
		frameCount = len(self.frameList)
		frameDone = len(self.frameRendered)
		self.percentage = (float(frameDone)/frameCount)*100
		self.percentSignal.emit( self.percentage )
		if not value is None:
			self.jobMessage.emit( {"id":self.id, "message":"Frame {frame} done! [{done}/{total}] {percent:0.2f} %".format(frame=value, done=frameDone, total=frameCount, percent=self.percentage), "level":"info"} )
		if frameDone >= frameCount:
			self.stopRender()
	
	def updateStatus(self, status):
		level = "info"
		if "Rendering" in status:
			if self.status != "Running":
				self.status = "Running"
				self.updateInfo()
		elif "Finished" in str(status):
			for worker in self.workers:
				if str(worker.pid) in status:
					self.workers.remove(worker)
		elif "Error" in str(status):
			for worker in self.workers:
				if worker.workerError and str(worker.pid) in status:
					if worker.workerCurrent:
						if not worker.workerCurrent in self.frameError:
							self.frameError.append(worker.workerCurrent)
							self.frameError.sort()
							cmd = self.createCommand(workerCount=1, renderFrameList=worker.frameLeft)[0]
							self.startWorker(cmd)
							self.updateInfo()
					level = "error"
		
		self.jobMessage.emit( {"id":self.id, "message":status, "level":level} )
		if not self.workers:
			self.stopRender()
	
	def startWorker(self, cmd):
		self.worker = RenderThread(cmd, logFile=self.logFile)
		self.worker.workerDone.connect(self.updateProgress)
		self.worker.workerSignal.connect(self.updateStatus)
		self.workers.append(self.worker)
		time.sleep(0.02)
		
		self.worker.start()
		time.sleep(0.02)
	
	def startRender(self):
		self.status = "Starting"
		self.updateInfo()
		
		renderFrameList = sorted([frame for frame in self.frameList if not frame in self.frameRendered and not frame in self.frameError])
		commands = self.createCommand(workerCount=self.workerCount, renderFrameList=renderFrameList)
		for cmd in commands:
			self.startWorker(cmd)
		self.jobMessage.emit( {"id":self.id, "message":"Job Started by {user}".format(user=getpass.getuser()), "level":"info"} )
	
	def stopRender(self):
		if self.workers:
			tmps = []
			while len(self.workers):
				for worker in self.workers:
					worker.stop()
					if worker.workerCurrent:
						self.jobMessage.emit( {"id":self.id, "message":"Frame {frame} not finished".format(frame=worker.workerCurrent), "level":"info"} )
						failedFile = self.outputFile.format(frame=worker.workerCurrent)
						tmps += glob.glob(failedFile+"*tmp")
					self.workers.remove(worker)
					worker.terminate()
			else:
				self.frameError.sort()
				frameLeft = sorted([f for f in self.frameList if f not in self.frameRendered])
				
				if len(self.frameRendered) >= len(self.frameList):
					self.status = "Finished"
				elif self.frameError == frameLeft:
					self.status = "Disabled"
				else:
					self.status = "Waiting"
			self.updateInfo()
			self.jobMessage.emit( {"id":self.id, "message":"Job Stopped by {user}".format(user=getpass.getuser()), "level":"info"} )
			
			tryCount = 0
			while tmps and tryCount < 5:
				for tmp in tmps:
					if os.path.exists(tmp):
						try:
							os.remove(tmp)
							tmps.remove(tmp)
						except:
							time.sleep(1)
							tryCount += 1
	
	def checkJob(self):
		frameRendered = []
		for frame in self.frameList:
			checkFile = self.outputFile.format(frame=frame)
			if os.path.exists(checkFile):
				if not frame in frameRendered:
					frameRendered.append(frame)
		self.frameRendered = frameRendered
		if len(self.frameRendered) >= len(self.frameList):
			self.status = "Finished"
		else:
			if self.frameError:
				self.status = "Disabled"
			if self.status in ["Finished"]:
				self.status = "Waiting"
		self.updateInfo()
		self.jobMessage.emit( {"id":self.id, "message":"Job Check by {user}".format(user=getpass.getuser()), "level":"info"} )
		
	def enableJob(self):
		if not self.status in ["Finished", "Waiting"]:
			self.frameError = []
			if len(self.frameRendered) >= len(self.frameList):
				self.status = "Finished"
			else:
				self.status = "Waiting"
			self.updateInfo()
			self.jobMessage.emit( {"id":self.id, "message":"Job Enabled by {user}".format(user=getpass.getuser()), "level":"info"} )
		
	def disableJob(self):
		if self.status != "Disabled":
			self.stopRender()
			self.status = "Disabled"
			self.updateInfo()
			self.jobMessage.emit( {"id":self.id, "message":"Job Disabled by {user}".format(user=getpass.getuser()), "level":"info"} )
		
	def resetJob(self):
		self.jobMessage.emit( {"id":self.id, "message":"Job Reset by {user}".format(user=getpass.getuser()), "level":"info"} )
		deleteFrames(self.outputFile, self.frameList)
		self.frameRendered = []
		self.enableJob()
		self.checkJob()
	
	def deleteJob(self):
		# print("deleteJob")
		self.status = "Deleted"
		self.stopRender()
		while os.path.exists(str(self.infoFile)):
			os.remove(str(self.infoFile))
		while os.path.exists(str(self.logFile)):
			os.remove(str(self.logFile))
		self.jobMessage.emit( {"id":self.id, "message":"Job Deleted by {user}".format(user=getpass.getuser()), "level":"info"} )
	
	def openFolder(self):
		filePath = os.path.normpath(os.path.dirname(self.outputFile))
		if os.path.exists(filePath):
			os.startfile(filePath)