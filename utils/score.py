from AS_Collect.models import DouBan_Article

#修改豆瓣文章自定义评分
def make_Douban_score():
    for obj in DouBan_Article.objects.all():
        obj.score=round((obj.collect*2+obj.like)/500,2)
        obj.save()





























