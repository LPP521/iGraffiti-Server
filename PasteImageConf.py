import os,time
import MySQLdb
import Image
username=''
password=''
def connect(dbname,sqlstring):
    db=MySQLdb.connect(host="localhost", user=username, passwd=password, db=dbname)
    c = db.cursor(cursorclass = MySQLdb.cursors.DictCursor)
    c.execute(sqlstring)
    db.commit()
    rows=c.fetchall()
    return rows
while True:
    rows=connect("iGraffiti","select ImageID,ImageLocation,WallLocation from PasteQueue inner join Wall on PasteQueue.TargetWallID=Wall.WallID")
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
        except:
            localtime=time.asctime(time.localtime(time.time()))
            errorlog=localtime+"  "+imlocation+" PasteImage Error -PasteImageConf.py\n"
            print(errorlog)
            logfile = open('/home/logfile', 'a')
            logfile.write(errorlog)
            logfile.close()
        connect("iGraffiti","delete from PasteQueue where ImageId="+str(imid)+"")
    time.sleep(1)
