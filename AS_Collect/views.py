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
        page = request.GET.get('page',default=0)
        size = request.GET.get('size',default=10)

        if request.GET.get('sort') is not None:
            s='-'+request.GET.get('sort')
        else:
            s='-score'
            query_set=Lin_Fanfiction_And_Section_Data.objects.all().order_by(s)
            tmp_set=query_set[page:page+size]
        return jsonResult(tmp_set)
    print('Updating...')
    #Spider.Update_Lin_fanfiction_and_Section()
    query_set=Lin_Fanfiction_And_Section_Data.objects.all().order_by('-score')
    tmp_set=query_set[page:page+size]
    return jsonResult(tmp_set)


#乃琳视频二创
def video(request):
    if request.method == 'GET':
        if request.GET.get('sort') is not None:
            s='-'+request.GET.get('sort')
        else:
            s='-score'
        return jsonResult(Lin_Video_Data.objects.all().order_by(s))
    print('Updating...')
    #Spider.Update_Lin_fanfiction_and_Section()
    return jsonResult(Lin_Video_Data.objects.all().order_by('-score'))


#豆瓣文章
def douban(request):
    data_dict={}
    search_data=request.GET.get('author',"")
    sort_data=request.GET.get('sort','-score')
    if search_data:
        data_dict['author__contains']=search_data

    if request.method == 'GET':
        if request.GET.get('sort') is not None:
            s='-'+request.GET.get('sort')
        else:
            s='-score'
        return jsonResult(DouBan_Article.objects.filter(**data_dict).order_by(s));
    return jsonResult(DouBan_Article.objects.all().order_by('-score'))


def jsonResult(data):#json化返回数据
    data = serializers.serialize('json', data)
    return HttpResponse(data)




