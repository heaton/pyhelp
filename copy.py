# -*- coding:UTF-8 -*- 
import re,os,time,shutil
fromDir = r'D:/web/build/autobuild'
toDir = r'D:/web/dongze'
sqlDir = r'C:/Builds/1/oa'
doneSqlLogPath = r'D:/web/sqlLog/production'
doneSqlFileName = 'sqldone.txt'

oldDbStr = r'server=10.8.10.252;database=OfficeDev;uid=oadev;pwd=oadev;'
dbStr = r'server=localhost;database=MyOffice;uid=oa;pwd=oa123;'
timeformat = '%Y%m%d'
filePre = 'autobuild'

versionPath = filePre + '_' + time.strftime(timeformat,time.localtime(time.time())) + '.1'
if not(os.path.exists(fromDir+'/'+versionPath)):
	quit()

filePath = versionPath + '/_PublishedWebsites/Authority.UI'
#now = time.strftime(timeformat,time.localtime(time.time()))
os.chdir(fromDir)

myList = []

def search(path,list,without=[]):
	pathLen = len(path)
	for root, dirs, files in os.walk(path):
		#print root
		for name in files:
			p = root+"/"+name
			list.append(p[pathLen:].replace("\\","/"))
		for woDir in without:
			if woDir in dirs:
				dirs.remove(woDir)

def copyFiles(path,list,to,withPath=True):
	for name in list:
		fullname = to+name
		if not(withPath):
			fullname = to+name[name.rindex('/'):]
		fullpath = os.path.dirname(fullname)
		if not(os.path.exists(fullpath)):
			os.makedirs(fullpath)
		if os.path.exists(fullname):
			os.remove(fullname)
		shutil.copy(path+name,fullname)
		print 'copy '+name+' >> '+fullname

search(filePath,myList)

copyFiles(filePath,myList,toDir)

configData = open(toDir + "/web.config","r").read()
configData = re.sub(oldDbStr, dbStr, configData)
configFile = open(toDir + "/web.config","w")
configFile.write(configData)
configFile.close()

#execute sql
os.chdir(sqlDir)
filePath = filePre + '/Sources/sql'
sqlFileList = []
search(filePath,sqlFileList,['done'])

doneSqlLog = doneSqlLogPath+'/'+doneSqlFileName
doneSqls = open(doneSqlLog).readlines()
doneSqls = [s.strip() for s in doneSqls]
doneLogFile = open(doneSqlLog, 'a')
for sqlFile in sqlFileList:
	sqlFileName = sqlFile[sqlFile.rindex('/')+1:]
	#print doneSqls
	if(sqlFileName not in doneSqls):
		temp = sqlFileName[:sqlFileName.rindex('.')]
		cmd = 'sqlcmd -S localhost -U oaadmin -P "admin|999" -d MyOffice -i "'+sqlDir+'/'+filePath+sqlFile+'" -o "'+doneSqlLogPath+'/'+temp+'.log"'
		#print cmd
		os.system(cmd)
		doneLogFile.write(sqlFileName+'\n')
doneLogFile.close()

