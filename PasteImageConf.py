#coding=utf-8
import os,time
import MySQLdb
import Image
from apns import APNs, Frame, Payload
import sys
reload(sys)
sys.setdefaultencoding('utf8')
apns = APNs(use_sandbox=True, cert_file='/home/myscript/APNs-Cer/cert2.pem', key_file='/home/myscript/APNs-Cer/key2.pem')
username=''
password=''
def connect(dbname,sqlstring,uncmt=0):
    db=MySQLdb.connect(host="localhost", user=username, passwd=password, db=dbname,charset="utf8")
    c = db.cursor(cursorclass = MySQLdb.cursors.DictCursor)
    c.execute('SET NAMES \'utf8\';')
    c.execute(sqlstring)
    if uncmt==0:
        db.commit()
    rows=c.fetchall()
    return rows
while True:
    rows=connect("iGraffiti","select ImageID,ImageLocation,WallName,WallLocation,TargetWallID from PasteQueue inner join Wall on PasteQueue.TargetWallID=Wall.WallID")
    for row in rows:
        try:
            imid=row['ImageID']
            imlocation=row['ImageLocation']
            walllocation=row['WallLocation']
            im=Image.open(imlocation)
            bgim=Image.open(walllocation)
            im.load()
            im=im.convert('RGBA')
            r,g,b,alpha=im.split()
            box=(0,0)
            bgim.paste(im,box,mask=alpha)
            bgim.save(walllocation)
            filename=imlocation
            os.remove(filename)
            notiwallid=row['TargetWallID']
            notiwallname=row['WallName']
            trows=connect("iGraffiti","call select_NotiToken('"+str(notiwallid)+"')",1)
            print(trows)
            for trow in trows:
                token_hex=trow["DeviceToken"]
                if token_hex=="":
                    continue
                payload = Payload(alert="你关注的墙有更新！", sound="default", badge=1,custom={'WallID':notiwallid,'WallName':notiwallname})
                apns.gateway_server.send_notification(token_hex, payload)
        except:
            localtime=time.asctime(time.localtime(time.time()))
            errorlog=localtime+"  "+imlocation+" PasteImage Error -PasteImageConf.py\n"
            print(errorlog)
            logfile = open('/home/logfile', 'a')
            logfile.write(errorlog)
            logfile.close()
        connect("iGraffiti","delete from PasteQueue where ImageId="+str(imid)+"")
    time.sleep(1)
    
