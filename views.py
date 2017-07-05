from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import string
import Image
import os
from . import database as db

PASSWORD=""
@csrf_exempt
def paste_image(request):
    name=request.POST.get('name')
    pwd=request.POST.get('pwd')
    img=request.FILES.get('pic')
    if not img==None:
        im=Image.open(img)
        bgim=Image.open('/home/mysite/static/wall1.jpg')
        a=0
        b=0
        if not name==None:
            a=int(name)
        if not pwd==None:
            b=int(pwd)
        box=(a,b)
        bgim.paste(im,box)
        bgim.save('/home/mysite/static/wall1.jpg')
    ans="success!"
    return render(request, 'iGraffiti/templates/paste_image.html',{'ans':ans})

def wall1(request):
    name=request.POST.get('x_position')
    pwd=request.POST.get('y_position')
    img=request.FILES.get('pic')
    ans=""
    if not img==None:
	try:
            name=0
            #return HttpResponse("ERROR")
            pwd=0
            im=Image.open(img)
            bgim=Image.open('/home/mysite/static/wall1.jpg')
            im.load()
            im=im.convert('RGBA')
            r,g,b,alpha=im.split()
            a=0
            b=0
            if not name==None:
                a=int(name)
            if not pwd==None:
                b=int(pwd)
            box=(a,b)
            bgim.paste(im,box,mask=alpha)
            bgim.save('/home/mysite/static/wall1.jpg')
	except:
		ans="error1"
	#return HttpResponse("ACCEPT")
    return render(request, 'iGraffiti/templates/wall1.html',{'ans':ans})    
def paste(request):
    target=request.POST.get('target')
    img=request.FILES.get('pic')
    ans="noimage"
    if target==None:
        ans="notarget"
        return HttpResponse(ans)
    if not img==None:
        try:
            im=Image.open(img)
            target=str(target)
            rows=db.connect("iGraffiti","select insert_PasteQueue("+target+")")
            row=rows[0]
            imlocation=row["insert_PasteQueue("+target+")"]
            im.save(imlocation)
            ans="success"
        except:
            ans="error"
    return HttpResponse(ans)
def walldata(request):
    target=request.GET['target']
    pw=request.GET['password']
    response_data={}
    if target==None or pw==None or pw!=PASSWORD:
        response_data["ans"]="error"
        return HttpResponse(json.dumps(response_data, cls=db.JsonExtendEncoder), content_type="application/json")
    rows=db.connect("iGraffiti","call select_Wall("+str(target)+")",1)
    if rows==None:
        response_data["ans"]="error"
        return HttpResponse(json.dumps(response_data, cls=db.JsonExtendEncoder), content_type="application/json")
    response_data["ans"]="success"
    row=rows[0]
    response_data["data"]=row
    return HttpResponse(json.dumps(response_data, ensure_ascii=False, cls=db.JsonExtendEncoder), content_type="application/json; charset=utf-8")
def createwall(request):
    name=request.GET['name']
    wtype=request.GET['type']
    pw=request.GET['pw']
    info=request.GET['info']
    uid=request.GET['uid']
    opw=request.GET['opw']
    response_data={}
    if name==None or wtype==None or uid==None or opw!=PASSWORD:
        response_data["ans"]="error"
        return HttpResponse(json.dumps(response_data, cls=db.JsonExtendEncoder), content_type="application/json")
    rows=db.connect("iGraffiti","select insert_Wall('"+name+"','"+wtype+"','"+pw+"','"+info+"','"+str(uid)+"')")
    if rows==None:
        response_data["ans"]="error"
        return HttpResponse(json.dumps(response_data, cls=db.JsonExtendEncoder), content_type="application/json")
    row=rows[0]
    ans=row[row.keys()[0]]
    if ans!="SameWallName":
        imlocation="/home/mysite/static/emptywall1.jpg"
        im=Image.open(imlocation)
        im.save(ans)
    response_data["ans"]=ans
    return HttpResponse(json.dumps(response_data, ensure_ascii=False, cls=db.JsonExtendEncoder), content_type="application/json; charset=utf-8")
def searchwall(request):
    name=request.GET['name']
    opw=request.GET['opw']
    response_data={}
    if name==None or opw!=PASSWORD:
        response_data["ans"]="error"
        return HttpResponse(json.dumps(response_data, cls=db.JsonExtendEncoder), content_type="application/json")
    rows=db.connect("iGraffiti","call search_Wall('"+name+"')",1)
    db.connect("iGraffiti","call insert_HotSearch('"+name+"')")
    if rows==None:
        response_data["ans"]="empty"
        return HttpResponse(json.dumps(response_data, cls=db.JsonExtendEncoder), content_type="application/json")
    response_data["ans"]="success"
    response_data["data"]=rows
    return HttpResponse(json.dumps(response_data, ensure_ascii=False, cls=db.JsonExtendEncoder), content_type="application/json; charset=utf-8")
def userinfo(request):
    uid=request.GET['uid']
    opw=request.GET['opw']
    response_data={}
    if uid==None or opw!=PASSWORD:
        response_data["ans"]="error"
        return HttpResponse(json.dumps(response_data, cls=db.JsonExtendEncoder), content_type="application/json")
    rows=db.connect("iGraffiti","call select_UserInfo('"+str(uid)+"')",1)
    if rows==None:
        response_data["ans"]="empty"
        return HttpResponse(json.dumps(response_data, cls=db.JsonExtendEncoder), content_type="application/json")
    response_data["ans"]="success"
    response_data["data"]=rows[0]
    return HttpResponse(json.dumps(response_data, ensure_ascii=False, cls=db.JsonExtendEncoder), content_type="application/json; charset=utf-8")
def searchlist(request):
    opw=request.GET['opw']
    response_data={}
    if opw!=PASSWORD:
        response_data["ans"]="error"
        return HttpResponse(json.dumps(response_data, cls=db.JsonExtendEncoder), content_type="application/json")
    rows=db.connect("iGraffiti","call select_HotSearch('')",1)
    response_data["ans"]="success"
    response_data["data"]=rows
    return HttpResponse(json.dumps(response_data, ensure_ascii=False, cls=db.JsonExtendEncoder), content_type="application/json; charset=utf-8")
def createuser(request):
    un=request.GET['un']
    pw=request.GET['pw']
    info=request.GET['info']
    opw=request.GET['opw']
    response_data={}
    if un==None or pw==None or info==None or opw!=PASSWORD:
        response_data["ans"]="error"
        return HttpResponse(json.dumps(response_data, cls=db.JsonExtendEncoder), content_type="application/json")
    rows=db.connect("iGraffiti","select insert_User('"+un+"','"+pw+"','"+info+"')")
    row=rows[0]
    response_data["ans"]=row[row.keys()[0]]
    return HttpResponse(json.dumps(response_data, ensure_ascii=False, cls=db.JsonExtendEncoder), content_type="application/json; charset=utf-8")
def login(request):
    un=request.GET['un']
    pw=request.GET['pw']
    dt=request.GET['dt']
    opw=request.GET['opw']
    response_data={}
    if un==None or pw==None or opw!=PASSWORD:
        response_data["ans"]="error"
        return HttpResponse(json.dumps(response_data, cls=db.JsonExtendEncoder), content_type="application/json")
    rows=db.connect("iGraffiti","call select_User('"+un+"','"+pw+"','"+dt+"')",1)
    if len(rows)==0:
        response_data["ans"]="empty"
        return HttpResponse(json.dumps(response_data, cls=db.JsonExtendEncoder), content_type="application/json")
    db.connect("iGraffiti","call insert_UserToken('"+un+"','"+pw+"','"+dt+"')")
    response_data["ans"]="success"
    response_data["data"]=rows[0]
    return HttpResponse(json.dumps(response_data, ensure_ascii=False, cls=db.JsonExtendEncoder), content_type="application/json; charset=utf-8")
def addfavo(request):
    uid=request.GET['uid']
    wid=request.GET['wid']
    opw=request.GET['opw']
    response_data={}
    if uid==None or wid==None or opw!=PASSWORD:
        response_data["ans"]="error"
        return HttpResponse(json.dumps(response_data, cls=db.JsonExtendEncoder), content_type="application/json")
    rows=db.connect("iGraffiti","call insert_UserFavo('"+str(uid)+"','"+str(wid)+"')")
    response_data["ans"]="success"
    return HttpResponse(json.dumps(response_data, ensure_ascii=False, cls=db.JsonExtendEncoder), content_type="application/json; charset=utf-8")
def favolist(request):
    uid=request.GET['uid']
    opw=request.GET['opw']
    response_data={}
    if uid==None or opw!=PASSWORD:
        response_data["ans"]="error"
        return HttpResponse(json.dumps(response_data, cls=db.JsonExtendEncoder), content_type="application/json")
    rows=db.connect("iGraffiti","call select_UserFavo('"+str(uid)+"')",1)
    response_data["ans"]="success"
    response_data["data"]=rows
    return HttpResponse(json.dumps(response_data, ensure_ascii=False, cls=db.JsonExtendEncoder), content_type="application/json; charset=utf-8")
def removefavo(request):
    uid=request.GET['uid']
    wid=request.GET['wid']
    opw=request.GET['opw']
    response_data={}
    if uid==None or wid==None or opw!=PASSWORD:
        response_data["ans"]="error"
        return HttpResponse(json.dumps(response_data, cls=db.JsonExtendEncoder), content_type="application/json")
    db.connect("iGraffiti","call delete_UserFavo('"+str(uid)+"','"+str(wid)+"')")
    response_data["ans"]="success"
    return HttpResponse(json.dumps(response_data, ensure_ascii=False, cls=db.JsonExtendEncoder), content_type="application/json; charset=utf-8")
def walllist(request):
    uid=request.GET['uid']
    opw=request.GET['opw']
    response_data={}
    if uid==None or opw!=PASSWORD:
        response_data["ans"]="error"
        return HttpResponse(json.dumps(response_data, cls=db.JsonExtendEncoder), content_type="application/json")
    rows=db.connect("iGraffiti","call select_UserWall('"+str(uid)+"')",1)
    response_data["ans"]="success"
    response_data["data"]=rows
    return HttpResponse(json.dumps(response_data, ensure_ascii=False, cls=db.JsonExtendEncoder), content_type="application/json; charset=utf-8")
def uui(request):
    uid=request.GET['uid']
    info=request.GET['info']
    opw=request.GET['opw']
    response_data={}
    if uid==None or info==None or opw!=PASSWORD:
        response_data["ans"]="error"
        return HttpResponse(json.dumps(response_data, cls=db.JsonExtendEncoder), content_type="application/json")
    db.connect("iGraffiti","call update_UserInfo('"+str(uid)+"','"+info+"')")
    response_data["ans"]="success"
    return HttpResponse(json.dumps(response_data, ensure_ascii=False, cls=db.JsonExtendEncoder), content_type="application/json; charset=utf-8")
def addnoti(request):
    uid=request.GET['uid']
    wid=request.GET['wid']
    opw=request.GET['opw']
    response_data={}
    if opw!=PASSWORD:
        response_data["ans"]="error"
        return HttpResponse(json.dumps(response_data, cls=db.JsonExtendEncoder), content_type="application/json")
    db.connect("iGraffiti","call insert_UserNoti('"+str(uid)+"','"+str(wid)+"')")
    response_data["ans"]="success"
    return HttpResponse(json.dumps(response_data, ensure_ascii=False, cls=db.JsonExtendEncoder), content_type="application/json; charset=utf-8")
def removenoti(request):
    uid=request.GET['uid']
    wid=request.GET['wid']
    opw=request.GET['opw']
    response_data={}
    if opw!=PASSWORD:
        response_data["ans"]="error"
        return HttpResponse(json.dumps(response_data, cls=db.JsonExtendEncoder), content_type="application/json")
    db.connect("iGraffiti","call delete_UserNoti('"+str(uid)+"','"+str(wid)+"')")
    response_data["ans"]="success"
    return HttpResponse(json.dumps(response_data, ensure_ascii=False, cls=db.JsonExtendEncoder), content_type="application/json; charset=utf-8")
def notilist(request):
    uid=request.GET['uid']
    opw=request.GET['opw']
    response_data={}
    if opw!=PASSWORD:
        response_data["ans"]="error"
        return HttpResponse(json.dumps(response_data, cls=db.JsonExtendEncoder), content_type="application/json")
    rows=db.connect("iGraffiti","call select_UserNoti('"+str(uid)+"')",1)
    response_data["ans"]="success"
    response_data["data"]=rows
    return HttpResponse(json.dumps(response_data, ensure_ascii=False, cls=db.JsonExtendEncoder), content_type="application/json; charset=utf-8")
# Create your views here.
