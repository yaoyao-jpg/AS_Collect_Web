from AS_Collect.models import DouBan_Article


#对豆瓣文章去重，后续可以考虑加入文章更新提示
def distinct():
    while True:
        dit={}
        for obj in DouBan_Article.objects.all():
            a=DouBan_Article.objects.filter(url=obj.url).all()
            if len(a)>1:
                for i in a:
                    if not dit.__contains__(i.url):
                        dit[i.url]=set()
                        dit[i.url].add(i.id)
                    else:
                        dit[i.url].add(i.id)
        if len(dit)==0:
            return
        for tit,id_list in dit.items():
            print(tit,id_list)
            for i in id_list:
                DouBan_Article.objects.filter(id=i).delete()
                break








