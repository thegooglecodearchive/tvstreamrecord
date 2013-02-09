# coding=UTF-8
"""
    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 3 of the License,
    or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, see <http://www.gnu.org/licenses/>.

    @author: pavion
"""

from bottle import CherryPyServer
from bottle import route, run, template, post, request
from bottle import static_file, redirect
from datetime import datetime, timedelta, time, date
import config
from sql import sqlRun, sqlCreateAll, purgeDB
import xmltv
import json
import urllib2
import threading 
from mylogging import logInit, logRenew, logStop

records = []    
localdatetime = "%d.%m.%Y %H:%M:%S"
localtime = "%H:%M"
localdate = "%d.%m.%Y"
dayshown = datetime.combine(date.today(), time.min)
version = '0.4.4' 

@route('/log.txt')
def server_static7():
    return static_file("/log.txt", root='')
@route('/js/<filename>')
def server_static1(filename):
    return static_file(filename, root='./js')
@route('/css/smoothness/<filename>')
def server_static2(filename):
    return static_file(filename, root='./css/smoothness')
@route('/css/<filename>')
def server_static3(filename):
    return static_file(filename, root='./css')
@route('/css/smoothness/images/<filename>')
def server_static4(filename):
    return static_file(filename, root='./css/smoothness/images')
@route('/images/<filename>')
def server_static5(filename):
    return static_file(filename, root='./images')

#------------------------------- Recurring records -------------------------------
weekdays = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']
def getWeekdays(i):
    if i==0: i=127
    l = []
    s = bin(i)[2:]
    while len(s)<7: s = '0'+s
    s = s[::-1]    
    for c in s: l.append(c=='1')
    return l

#------------------------------- Main menu -------------------------------

@route('/')
def main_s():
    return records_s()

@route('/about')
def about_s():    
    return template('about', ver = version)

#------------------------------- Logging -------------------------------
        

logInit()    

print "Starting tvstreamrecord v.%s" % version
print "Logging output initialized"

@post('/resetlog')
def log_reset():
    logRenew()
    return

@route('/log')
def log_s():
    return template('log')

@route('/logget')
def log_get():
    l = list()
    lfile = open("log.txt", "r")
    for lline in lfile:
        if len(lline)>24:
            l.append([ lline[0:19], lline[20:23], lline[24:] ])
    lfile.close()    
    return json.dumps({"aaData": l } )

#------------------------------- Channel List -------------------------------

@route('/channellist')
def chanlist():
    l = []
    rows=sqlRun('SELECT channels.rowid, cname, cpath, cenabled FROM channels')    
    for row in rows:
        l.append([row[0], row[1], row[2], row[3]])
    return json.dumps({"aaData": l } )

@route('/list')
def list_s():
    return template('list')
    
@post('/list')
def list_p():
    what = request.forms.get("what")
    myid = request.forms.get("myid")
    if what=="-1":
        sqlRun("DELETE FROM channels WHERE channels.rowid=%s" % (myid))
    else: 
        sqlRun("UPDATE channels SET cenabled=%s WHERE channels.rowid=%s" % (what, myid))            
    setRecords()
    return

#------------------------------- Channel creation -------------------------------


@post('/create_channel')
def createchannel():
    cname = request.forms.cname
    cpath = request.forms.cpath
    aktiv = getBool(request.forms.aktiv)
    sqlRun("INSERT INTO channels VALUES (?, ?, ?)", (cname, cpath, aktiv))
    return
    
@post('/upload')
def upload_p():
    print "M3U upload parsing started"
    retl = []
    upfile = request.files.upfile
    header = upfile.file.read(7)
    if header.startswith("#EXTM3U"):
        how = getBool(request.forms.get("switch00"))
        upfilecontent = upfile.file.read()        
        if how==0:
            sqlRun('DELETE FROM channels')
        lines = upfilecontent.splitlines()
        i = 0
        name = ""
        for line in lines:
            i = i + 1
            if i>1:
                if i % 2 == 0: 
                    name = line.split(",",1)[1]
                if i % 2 == 1:
                    retl.append([name, line]) 
                    name = ""
        sqlRun("INSERT OR IGNORE INTO channels VALUES (?, ?, '1')", retl, 1)             
            
    redirect("/list") 

#------------------------------- Configuration -------------------------------
    
@post('/config')
def config_p():    
    attrl = []
    dicts = config.getDict()
    for d in dicts:
        val = request.forms.get(d)
        attrl.append([d, val])
    config.setConfig(attrl)
    redirect("/config") 

@route('/config')
def config_s():    
    return template('config', rows=sqlRun("SELECT * FROM config WHERE param<>'cfg_version'"))

#------------------------------- EPG -------------------------------
    
@post('/getepg')
def getepg():
    thread = epgthread() 
    thread.start()
    return 

class epgthread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        xmltv.getProgList(version)

@post('/epg')
def epg_p():    
    day = request.forms.datepicker3
    global dayshown
    dayshown = datetime.strptime(day,localdate)
    redirect("/epg") 

@route('/epg')
def epg_s():    
    widthq = 0.8
    ret = list()
    rtemp = list()
    w = 0.0
    for i in range(24):
        t = time(i)
        x = i * 100.0 / 24.0 * widthq
        w =  1.0 / 24.0 * widthq * 100.0 
        rtemp.append([-1, x, w, t.strftime("%H:%M"), "", "", -1, ""])
    ret.append(rtemp)    
    
    global dayshown    
    todaysql = datetime.strftime(dayshown, "%Y-%m-%d %H:%M:%S")
    d_von = dayshown    
    rows=sqlRun("SELECT guide.g_id, channels.rowid, channels.cname FROM guide, guide_chan, channels WHERE channels.cenabled=1 AND channels.cname=guide_chan.g_name AND guide.g_id=guide_chan.g_id AND (date(g_start)=date('%s') OR date(g_stop)=date('%s')) GROUP BY guide.g_id" % (todaysql, todaysql))
    for row in rows:
        cid=row[1]
        rtemp = list()
        #y+=1 
        c_rows=sqlRun("SELECT g_title, g_start, g_stop, g_desc, guide.rowid FROM guide WHERE (date(g_start)=date('%s') OR date(g_stop)=date('%s')) AND g_id='%s' ORDER BY g_start" % (todaysql, todaysql, row[0]))
        for event in c_rows:
            d_von = datetime.strptime(event[1],"%Y-%m-%d %H:%M:%S")
            d_bis = datetime.strptime(event[2],"%Y-%m-%d %H:%M:%S")
            fulltext = "<b>"+event[0]+": "+datetime.strftime(d_von, localtime) + " - " + datetime.strftime(d_bis, localtime) + "</b><BR><BR>"+event[3]
            title = fulltext
            if len(title)>300:
                title = title[:297]+"..."
                try:
                    title.decode("UTF-8")
                except:
                    title = title[:296]+"..."
                    pass
            if d_von.date() < dayshown.date():
                d_von = dayshown
            if d_bis.date() > dayshown.date():
                d_bis=datetime.combine(d_bis.date(),time.min)
            x = d_von - datetime.combine(d_von.date(),time.min)
            w = d_bis - d_von
            rtemp.append ([cid, x.total_seconds()/86400.0*100.0*widthq, w.total_seconds()/86400.0*100.0*widthq, event[0], title, fulltext, event[4], row[2]])
        ret.append(rtemp)
    return template('epg', curr=datetime.strftime(d_von, localdate), rowss=ret)            

#------------------------------- Record List -------------------------------

@route('/getrecordlist')
def getrecordlist():
    l = []
    rows=sqlRun("SELECT recname, cname, strftime('"+"%"+"d."+"%"+"m."+"%"+"Y "+"%"+"H:"+"%"+"M', rvon), strftime('"+"%"+"d."+"%"+"m."+"%"+"Y "+"%"+"H:"+"%"+"M', rbis), rmask, renabled, 100*(strftime('%s','now', 'localtime')-strftime('%s',rvon)) / (strftime('%s',rbis)-strftime('%s',rvon)), records.rowid, rvon, rbis FROM channels, records where channels.rowid=records.cid ORDER BY rvon")     
    for row in rows:
        rec = ""
        if row[4]==0: 
            rec = "no"
        else: 
            wd = getWeekdays(row[4])
            for index, item in enumerate(wd): 
                if item: 
                    rec += weekdays[index]
        l.append([row[0], row[1], row[2], row[3], rec, row[5], row[6], row[7], row[8], row[9]])
    return json.dumps({"aaData": l } )

@route('/records')
def records_s():    
    return template('records', rows2=sqlRun('SELECT rowid, cname FROM channels where cenabled=1'))

@post('/records')
def records_p():
    what = request.forms.get("what")
    myid = request.forms.get("myid")
    if what=="-2":
        sqlRun("DELETE FROM records WHERE datetime(rbis)<datetime('now', 'localtime') AND NOT rmask>0")
    if what=="-1":
        sqlRun("DELETE FROM records WHERE records.rowid=%s" % (myid))
    else: 
        sqlRun("UPDATE records SET renabled=%s WHERE rowid=%s" % (what, myid))            
    setRecords()
    return

#------------------------------- Record creation -------------------------------
    
@post('/createepg')
def createepg():
    sqlRun("INSERT INTO records SELECT guide.g_title, channels.rowid, datetime(guide.g_start, '-%s minutes'), datetime(guide.g_stop, '+%s minutes'), 1, 0 FROM guide, guide_chan, channels WHERE guide.g_id = guide_chan.g_id AND channels.cname = guide_chan.g_name AND guide.rowid=%s" % (config.cfg_delta_for_epg, config.cfg_delta_for_epg, request.forms.ret))
    setRecords()        
    redirect("/records")
    return 

@post('/create')
def create_p():
    recname = request.forms.recname
    sender = request.forms.Sender
    von = request.forms.von
    bis = request.forms.bis
    am = request.forms.am
    aktiv = getBool(request.forms.aktiv)    
    recurr = request.forms.recurr
    #print recurr

    d_von = datetime.strptime(am + " " + von, "%d.%m.%Y %H:%M")
    d_bis = datetime.strptime(am + " " + bis, "%d.%m.%Y %H:%M")
    delta = timedelta(days=1)
    if d_bis < d_von:
        d_bis = d_bis + delta         
    
    sqlRun("INSERT INTO records VALUES (?, ?, ?, ?, ?, ?)", (recname, sender, d_von, d_bis, aktiv, recurr))
    
    setRecords()
    
    return 
   
def getBool(stri):
    r = 0
    if stri == "on" or stri == "1" or stri == "delete" or stri==1:
        r = 1
    return r

    
class record(threading.Thread):
    running = 0
    id = -1
    stopflag = 0 
    timer = None
    name = ""
    mask = 0
        
    def __init__(self, row):
        threading.Thread.__init__(self)
        self.id = row[0]
        self.von = datetime.strptime(row[2],"%Y-%m-%d %H:%M:%S")
        self.bis = datetime.strptime(row[3],"%Y-%m-%d %H:%M:%S")        
        self.name = row[5]        
        self.url = row[1]
        self.mask = row[6]
        if self.mask > 0:
            w = self.bis.weekday()
            if not (self.bis>=datetime.now() and getWeekdays(self.mask)[w]):
                delta = timedelta(days=1)
                while not (self.bis>=datetime.now() and getWeekdays(self.mask)[w]):
                    self.von = self.von + delta
                    self.bis = self.bis + delta
                    w = self.bis.weekday()    
                print "Recurrent record '%s' moved to %s" % (self.name, self.von)
                sqlRun("UPDATE records SET rvon='%s', rbis='%s' WHERE rowid=%d" % (datetime.strftime(self.von,"%Y-%m-%d %H:%M:%S"), datetime.strftime(self.bis,"%Y-%m-%d %H:%M:%S"), self.id ) )    
    
    def run(self): 
        td = self.von-datetime.now()
        deltas = td.total_seconds()
        self.timer = threading.Timer(deltas, self.doIt)
        self.timer.start()
        if deltas>0:
            print "\nRecord: Thread timer for '%s' started for %d seconds" % (self.name, deltas)
        
    def doIt(self):
        self.running = 1
        block_sz = 8192
        print "\nRecord: '%s' started" % (self.name)
        u = urllib2.urlopen(self.url)
        fn = config.cfg_recordpath+datetime.now().strftime("%Y%m%d%H%M%S") + " - "        
        fn = fn + "".join([x if x.isalnum() else "_" for x in self.name])
        #print fn
        try:
            f = open(fn+config.cfg_file_extension, 'wb')
        except:
            print "\nOutput file %s can't be created. Please check your settings." % (fn+".mkv")  
            pass
        else:
            while self.bis > datetime.now() and self.stopflag==0:
                mybuffer = u.read(block_sz)
                if not mybuffer:
                    break
                f.write(mybuffer)
            f.close()
            print "\nRecord: '%s' ended" % (self.name)
            if self in records: records.remove(self) 
            if self.mask > 0:
                print (self in records)
                rectimer = threading.Timer(5, setRecords)
                rectimer.start()
    
    def stop(self):
        if self.running==0:
            self.timer.cancel()
        self.stopflag = 1
        print "\nRecord: Stopflag for '%s' received" % (self.name)
   
def setRecords():    
    #print "doof"
    rows=sqlRun("SELECT records.rowid, cpath, rvon, rbis, cname, records.recname, records.rmask FROM channels, records where channels.rowid=records.cid AND (datetime(rbis)>=datetime('now', 'localtime') OR rmask>0) AND renabled = 1 ORDER BY datetime(rvon)")
    for row in rows: 
        chk = False
        for t in records:
            if t.id == row[0]:
                chk = True
                break
        if chk == False:
            thread = record(row) 
            thread.start()
            records.append(thread)
        
    for index, t in enumerate(records[:]):
        chk = False
        for row in rows: 
            if t.id == row[0]:
                chk = True
                break
        if chk == False:
            t.stop()
            del records[index]

           
print "Initializing database..."
sqlCreateAll(version)
purgeDB()          
print "Initializing config..."
config.loadConfig()
print "Initializing records..."
setRecords()
    
print "Starting server on: %s:%s" % (config.cfg_server_bind_address, config.cfg_server_port)
run(host=config.cfg_server_bind_address, port=config.cfg_server_port, server=CherryPyServer, quiet=True)

print "Server aborted. Stopping all records before exiting"
for t in records:
    t.stop()

print "tvstreamrecord v.%s: bye-bye" % version
logStop()
    