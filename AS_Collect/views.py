from AS_Collect.models import Lin_Fanfiction_And_Section_Data,Lin_Video_Data,DouBan_Article
from django.shortcuts import render, redirect
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import json
from django.core import serializers

#主页面
def main_page(request):
    return redirect('/douban/')


#乃琳文章二创
def news(request):
    if request.method == 'GET':
        page = int(request.GET.get('page',default=0))
        size = int(request.GET.get('size',default=10))
        s='-'+request.GET.get('sort',default='score')
        key=request.GET.get('key',default='')#筛选字段名，如author等
        value=request.GET.get('value',default='')#筛选字段值
    data_dict={}
    if key:
        data_dict[key+'__contains']=value
    print('Updating...')
    #Spider.Update_Lin_fanfiction_and_Section()
    query_set=Lin_Fanfiction_And_Section_Data.objects.filter(**data_dict).order_by(s)
    tmp_set=query_set[page:page+size]
    return jsonResult(tmp_set)


#乃琳视频二创
def video(request):
    if request.method == 'GET':
        page = int(request.GET.get('page',default=0))
        size = int(request.GET.get('size',default=10))
        s='-'+request.GET.get('sort',default='score')
        key=request.GET.get('key',default='')
        value=request.GET.get('value',default='')
    data_dict={}
    if key:
        data_dict[key+'__contains']=value
    print('Updating...')
    #Spider.Update_Lin_fanfiction_and_Section()
    query_set=Lin_Video_Data.objects.filter(**data_dict).order_by(s)
    tmp_set=query_set[page:page+size]
    return jsonResult(tmp_set)


#豆瓣文章
def douban(request):
    if request.method == 'GET':
        page = int(request.GET.get('page',default=0))
        size = int(request.GET.get('size',default=10))
        s='-'+request.GET.get('sort',default='score')
        key=request.GET.get('key',default='')
        value=request.GET.get('value',default='')
    data_dict={}
    if key:
        data_dict[key+'__contains']=value

    query_set=DouBan_Article.objects.filter(**data_dict).order_by(s)
    tmp_set=query_set[page:page+size]
    return jsonResult(tmp_set)


def jsonResult(data):#json化返回数据
    data = serializers.serialize('json', data)
    return HttpResponse(data)




