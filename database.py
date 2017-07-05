# -*- coding:utf-8 -*-
import MySQLdb
import os
username='root'
password='PI*32767*i*e'
def connect(dbname,sqlstring,procedure=0):
    db=MySQLdb.connect(host="localhost", user=username, passwd=password, db=dbname,charset="utf8")
    #c=db.cursor()
    c = db.cursor(cursorclass = MySQLdb.cursors.DictCursor)
    c.execute('SET NAMES \'utf8\';')
    c.execute(sqlstring)
    if procedure==0:
        db.commit()
    rows=c.fetchall()
    return rows
#connect("iGraffiti","INSERT INTO PasteQueues VALUES (null,'/home/mysite/static')")
'''n=1
rows=connect("iGraffiti","select insert_PasteQueue("+str(n)+")")
row=rows[0]
print(row['insert_PasteQueue('+str(n)+')'])
'''
'''rows=connect("iGraffiti","select * from PasteQueues")
maxID=0
for row in rows:
	maxID=max(maxID,row['ImageID'])
saveName=str(maxID+1)
connect("iGraffiti","insert into PasteQueues values (null,'"+saveName+".png')")
rows=connect("iGraffiti","select * from PasteQueues")
for row in rows:
    print(row)
'''
import json
from datetime import date
from datetime import datetime

class JsonExtendEncoder(json.JSONEncoder):
    """
        This class provide an extension to json serialization for datetime/date.
    """
    def default(self, o):
        """
            provide a interface for datetime/date
        """
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(o, date):
            return o.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, o)

if __name__ == '__main__':
    rows=connect('iGraffiti','select insert_Wall(\'wall2\',\'public\',null,\'info\',1)')
    row = rows[0]
    print(row[row.keys()[0]])
    d = {'now': datetime.now(), 'today': date.today(), 'i': 100}
    ds = json.dumps(d, cls=JsonExtendEncoder)
    print "ds type:", type(ds), "ds:", ds
    l = json.loads(ds)
    print "l  type:", type(l), "ds:", l
