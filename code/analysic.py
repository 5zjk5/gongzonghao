#!/usr/bin/env python
# coding: utf-8

# # 导入数据

# In[84]:


import pandas as pd 
import numpy as np


article = pd.read_excel('../data/article.xlsx',encoding='utf8')
reprint = pd.read_excel('../data/reprint.xlsx',encoding='utf8')


# In[85]:


article.head()


# In[86]:


reprint.head()


# # 探索性描述分析

# ##  发表文章总数

# In[87]:


eassy_num = article.shape[0]
eassy_num


# ## 原创，转载，广告文章数的占比

# In[88]:


# 三种类型的文章数
original_num = article[article['是否原创'] == '是'].shape[0]
reprint_num = article[article['是否广告'] == '是'].shape[0]
advertising_num = article[article['是否转载'] == '是'].shape[0]


# 占比圆环图
from pyecharts import options as opts
from pyecharts.charts import Pie
from pyecharts.globals import ThemeType


v = ['原创','广告','转载']
c = (
    Pie(init_opts=opts.InitOpts(theme=ThemeType.VINTAGE,chart_id=1))
    .add(
        "",
        [list(z) for z in zip(v, [original_num,reprint_num,advertising_num])],
        radius=["40%", "75%"],
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="转载，广告，原创占比"),
        legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%"),
    )
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
)
c.render('../output/转载，广告，原创占比.html')
c.render_notebook()


# ## 文章标题用词状况

# In[89]:


# 分词
import jieba

title_word = article['文章']
title_word = ' '.join(title_word)
word = jieba.lcut(title_word)


# 词云生成
from stylecloud import gen_stylecloud


gen_stylecloud(text=' '.join(word), collocations=False,
               palette='tableau.Tableau_20',
               font_path=r'‪C:\Windows\Fonts\msyh.ttc',
               icon_name='fas fa-file-alt',
               size=400,output_name='../output/标题词云.png')


# ## 文章发送成功人数的走势

# In[90]:


send_peo = article[['群发时间','发送成功人数']]

# 取年，月
send_peo['群发时间'] = send_peo['群发时间'].astype(str)
send_peo['群发时间'] = send_peo['群发时间'].str[:7]

# 以年月分组计算这个年月中最大的数，即为当月用户数
send_peo = send_peo.groupby('群发时间').max().reset_index()


# 绘制折线图
import pyecharts.options as opts
from pyecharts.charts import Line


x_data = send_peo['群发时间']
y_data = send_peo['发送成功人数']


c = (
    Line(init_opts=opts.InitOpts(theme=ThemeType.VINTAGE,chart_id=2))
    .add_xaxis(xaxis_data=x_data)
    .add_yaxis(
        series_name="用户数",
        y_axis=y_data,
        symbol="emptyCircle",
        is_symbol_show=True,
        label_opts=opts.LabelOpts(is_show=False),
        areastyle_opts=opts.AreaStyleOpts(opacity=1, color="#bcf580"),
    )
    .set_global_opts(
        tooltip_opts=opts.TooltipOpts(is_show=True),
        title_opts=opts.TitleOpts(title="用户走势"),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=True),
        ),
        xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
    )
)
c.render("../output/用户走势.html")
c.render_notebook()


# ## 阅读数区间划分

# In[92]:


# 区间切分，并统计每个区间数量
read_num = pd.DataFrame(article['阅读数'].astype(int))
read_num = pd.cut(read_num['阅读数'],bins=[0,150,300,450,600,1000])
read_num = pd.DataFrame(read_num.value_counts())


# 绘制直方图
from pyecharts import options as opts
from pyecharts.charts import Bar 


x = ['(0, 150]','(150, 300]','(300, 450]','(450, 600]','(600, 1000]']
y = [7,26,23,6,3]

c = (
    Bar(init_opts=opts.InitOpts(theme=ThemeType.VINTAGE,chart_id=3))
    .add_xaxis(x)
    .add_yaxis("数量", y, category_gap=0)
    .set_global_opts(title_opts=opts.TitleOpts(title="阅读数区间分布"))
)
c.render('../output/阅读数区间分布.html')
c.render_notebook()


# ## 看一看，点赞，赞赏金额分布

# In[94]:


look_support_money = article[['看一看','点赞','赞赏']]


# 箱型图绘制
from pyecharts import options as opts
from pyecharts.charts import Boxplot


v1 = [
    list(look_support_money['看一看']),
    list(look_support_money['点赞']),
    list(look_support_money['赞赏'])
]

c = Boxplot(init_opts=opts.InitOpts(theme=ThemeType.VINTAGE,chart_id=4))
c.add_xaxis(["看一看", "点赞",'赞赏'])
c.add_yaxis("", c.prepare_data(v1))
c.set_global_opts(title_opts=opts.TitleOpts(title="看一看,点赞,赞赏分布"))
c.render("../output/看一看,点赞,赞赏.html")
c.render_notebook()


# ## 文章类型占比

# In[95]:


kind = article['文章类型'].value_counts()


# 绘制玫瑰图
from pyecharts import options as opts
from pyecharts.charts import Pie


v = ['爬虫', '其他', '数据分析', '爬虫+数据分析', 'Python 脚本程序', '可视化', '爬虫+可视化']
c = (
    Pie(init_opts=opts.InitOpts(theme=ThemeType.VINTAGE,chart_id=5))
    .add(
        "",
        [list(z) for z in zip(v, [19, 14, 9, 7, 6, 5, 4])],
        radius=["30%", "75%"],
        center=["50%", "50%"],
        rosetype="radius",
        label_opts=opts.LabelOpts(is_show=True),
    )
    .set_global_opts(title_opts=opts.TitleOpts(title="文章类型占比"))
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
)
c.render('../output/文章类型占比.html')
c.render_notebook()


# ## 阅读数，看一看，点赞，赞赏，被转载数是否有相关性

# In[130]:


# 计算相关性，把相关性矩阵转换为列表
corrs = article[['阅读数','看一看','点赞','赞赏','被转载']].corr()
l = len(corrs.index)
corrs = np.array(corrs)
corrs = corrs.tolist()

# 把相关性取值对应为列表，并保留 2 位小数
value = []
for i in range(l):
    for j in range(l):
        value.append([i,j,round(corrs[i][j],2)])


# 绘制相关热力图
from pyecharts import options as opts
from pyecharts.charts import HeatMap


c = (
    HeatMap(init_opts=opts.InitOpts(theme=ThemeType.VINTAGE,chart_id=6))
    .add_xaxis(['阅读数','看一看','点赞','赞赏','被转载'])
    .add_yaxis(
        "",
        ['阅读数','看一看','点赞','赞赏','被转载'],
        value,
        label_opts=opts.LabelOpts(is_show=True, position="inside"),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="阅读数，看一看，点赞，赞赏，被转载相关性热力图",
                                pos_left='center'),
        visualmap_opts=opts.VisualMapOpts(is_show=False,min_=-1,
                                              max_=1),
    )
)
c.render('../output/阅读数，看一看，点赞，赞赏，被转载相关性热力图.html')
c.render_notebook()


# # 下钻分析

# ## 哪种类型文章阅读量高

# In[96]:


kind = article.groupby('文章类型')['阅读数'].sum().reset_index()
kind = kind.sort_values(by='阅读数')


from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.faker import Faker

c = (
    Bar(init_opts=opts.InitOpts(theme=ThemeType.VINTAGE,chart_id=7))
    .add_xaxis(list(kind['文章类型']))
    .add_yaxis("阅读数", list(kind['阅读数']))
    .reversal_axis()
    .set_series_opts(label_opts=opts.LabelOpts(position="right"))
    .set_global_opts(title_opts=opts.TitleOpts(title="文章类型阅读量排名"))
)
c.render('../output/文章类型阅读量排名.html')
c.render_notebook()


# ## 是否推送到其他群聊对阅读数的影响

# In[97]:


send_other = list(article[article['是否推送到其他群聊'] == '是']['阅读数'])
not_send_other = list(article[article['是否推送到其他群聊'] != '是']['阅读数'])


# 绘制对比箱型图
from pyecharts import options as opts
from pyecharts.charts import Boxplot

v1 = [
    send_other,
    not_send_other,
]
c = Boxplot(init_opts=opts.InitOpts(theme=ThemeType.VINTAGE,chart_id=8))
c.add_xaxis(["是", "否"])
c.add_yaxis("阅读数分布", c.prepare_data(v1))
c.set_global_opts(title_opts=opts.TitleOpts(title="是否推送到其他群聊对阅读数影响"))
c.render("../output/是否推送到其他群聊对阅读数的影响.html")
c.render_notebook()


# ## 被转载的都有哪些，是什么类型的

# In[98]:


be_reprint = article[article['被转载'] != 0]


# 绘制被转载文章名，被转载数从多到少的排行条形图
eassy_read = be_reprint[['文章','被转载']].sort_values(by='被转载')


from pyecharts import options as opts
from pyecharts.charts import Bar


c = (
    Bar(init_opts=opts.InitOpts(theme=ThemeType.VINTAGE,chart_id=9,
                               width='3000px',height='400px'))
    .add_xaxis(list(eassy_read['文章']))
    .add_yaxis("被转载数", list(eassy_read['被转载']))
    .reversal_axis()
    .set_series_opts(label_opts=opts.LabelOpts(position="right"))
    .set_global_opts(title_opts=opts.TitleOpts(title="被转载文章排行"))
)
c.render('../output/被转载文章排行.html')
c.render_notebook()


# ## 被转载的阅读数与原文的阅读数对比

# In[99]:


# 别转载的原文阅读量与转载文章阅读量
ori_read = list(article[article['被转载'] != 0]['阅读数'])
reprint_read = list(list(reprint['阅读量']))


# 绘制对比箱型图
from pyecharts import options as opts
from pyecharts.charts import Boxplot


v1 = [
    ori_read,
    reprint_read,
]
c = Boxplot(init_opts=opts.InitOpts(theme=ThemeType.VINTAGE,chart_id=10))
c.add_xaxis(["原文", "被转载"])
c.add_yaxis("阅读数分布", c.prepare_data(v1))
c.set_global_opts(title_opts=opts.TitleOpts(title="被转载的阅读数与原文的阅读数分布"))
c.render("../output/被转载的阅读数与原文的阅读数分布.html")
c.render_notebook()


# ## 哪一个公众号转载次数最多，累计阅读量

# In[100]:


reprint_author = reprint.groupby('转载公众号')['文章'].count().reset_index()
reprint_author = reprint_author.sort_values(by='文章')


# 绘制转载次数排行条形图
from pyecharts import options as opts
from pyecharts.charts import Bar


c = (
    Bar(init_opts=opts.InitOpts(theme=ThemeType.VINTAGE,chart_id=11,
                               width='1000px',height='400px'))
    .add_xaxis(list(reprint_author['转载公众号']))
    .add_yaxis("转载数", list(reprint_author['文章']))
    .reversal_axis()
    .set_series_opts(label_opts=opts.LabelOpts(position="right"))
    .set_global_opts(title_opts=opts.TitleOpts(title="转载公众号状况"))
)
c.render('../output/转载公众号状况.html')
c.render_notebook()


# ## 阅读数高的(400,+无穷]文章类型

# In[103]:


trait = article
trait['阅读数'] = trait['阅读数'].astype(int)
trait = trait[trait['阅读数'] >= 400]['文章类型'].value_counts()


# 绘制饼图
from pyecharts import options as opts
from pyecharts.charts import Pie


c = (
    Pie(init_opts=opts.InitOpts(theme=ThemeType.VINTAGE,chart_id=12))
    .add("", [list(z) for z in zip(['爬虫+数据分析', '爬虫', '其他', '可视化', 'Python 脚本程序', '爬虫+可视化'],
                                   [4, 4, 2, 2, 2, 1])])
    .set_global_opts(title_opts=opts.TitleOpts(title="阅读数较高文章类型"))
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
)
c.render('../output/阅读数较高文章类型.html')
c.render_notebook()


# In[ ]:




