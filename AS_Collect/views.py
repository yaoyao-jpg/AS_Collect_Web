from AS_Collect.models import Lin_Fanfiction_And_Section_Data,Lin_Video_Data,DouBan_Article
from django.shortcuts import render, redirect

#主页面
def main_page(request):
    return redirect('/douban/')


#乃琳文章二创
def news(request):
    if request.method == 'GET':
        if request.GET.get('sort') is not None:
            s='-'+request.GET.get('sort')
        else:
            s='-score'
        return render(request, 'news.html', {'res':
            Lin_Fanfiction_And_Section_Data.objects.all().order_by(s)})
    print('Updating...')
    #Spider.Update_Lin_fanfiction_and_Section()
    return render(request, 'news.html', {'res':
            Lin_Fanfiction_And_Section_Data.objects.all().order_by('-score')})


#乃琳视频二创
def video(request):
    if request.method == 'GET':
        if request.GET.get('sort') is not None:
            s='-'+request.GET.get('sort')
        else:
            s='-score'
        return render(request, 'video.html', {'res':
            Lin_Video_Data.objects.all().order_by(s)})
    print('Updating...')
    #Spider.Update_Lin_fanfiction_and_Section()
    return render(request, 'video.html', {'res':
            Lin_Video_Data.objects.all().order_by('-score')})


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
        return render(request,'douban.html', {'res':
            DouBan_Article.objects.filter(**data_dict).order_by(s),'search_data':search_data})
    return render(request, 'douban.html', {'res':DouBan_Article.objects.all().order_by('-score')})






