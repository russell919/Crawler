# pip install matplotlib
# pip install pandas
# pip install pyecharts
# pip install wordcloud

from matplotlib import pyplot as plt
import pandas as pd

from pyecharts import options as opts
from pyecharts.charts import Bar
# from pyecharts.faker import Faker

from collections import Counter


# 读取表格
df = pd.read_excel("豆瓣Top250电影数据.xls", index_col=False)
df.head()
# 数据预处理
# 上映年份格式不统一（有的电影年份后会带上地区信息）
year = []
for i in df["年份"]:
    i = i[0:4]
    year.append(i)
df["年份"] = year
df["年份"].value_counts()
x1 = list(df["年份"].value_counts().sort_index().index)
y1 = list(df["年份"].value_counts().sort_index().values)
y1 = [str(i) for i in y1]


# 上映年份分布
c1 = (
    Bar()
    .add_xaxis(x1)
    .add_yaxis("影片数量", y1)
    .set_global_opts(
        title_opts=opts.TitleOpts(title="豆瓣Top250电影年份分布"),
        datazoom_opts=opts.DataZoomOpts(),
    )
    # 最后的.render('.html')会创建一个html的文件，图表就在其中
    # 如果在jupyter下运行的代码，可以改为.render_notebook()
    .render("电影上映年份分布.html")
)


# 评分分布情况
# 生成表（图片形式）
plt.figure(figsize=(10, 6))
plt.hist(list(df["评分"]), bins=8, facecolor="blue", edgecolor="black", alpha=0.7)
plt.show()
# 生成表（储存在 .html)
a1 = list(df["评分"].value_counts().sort_index().index)
b1 = list(df["评分"].value_counts().sort_index().values)
b1 = [str(i) for i in b1]
d1 = (
    Bar()
    .add_xaxis(a1)
    .add_yaxis("影片数量", b1)
    .set_global_opts(
        title_opts=opts.TitleOpts(title="豆瓣Top250电影评分分布"),
        datazoom_opts=opts.DataZoomOpts(),
    )
    .render("电影评分分布.html")
)


# 排名与评分分布情况
plt.figure(figsize=(10, 5), dpi=100)
plt.scatter(df.index, df['评分'])
plt.show()

'''
# 评论人数TOP10
# 结果存在问题！！！
c2 = (
    Bar()
    .add_xaxis(df["电影名称"].to_list())
    .add_yaxis("评论数", df["评论人数"].to_list(), color=Faker.rand_color())
    .reversal_axis()
    .set_series_opts(label_opts=opts.LabelOpts(position="right"))
    .set_global_opts(title_opts=opts.TitleOpts(title="电影评论Top10"))
    .render("评论人数TOP10.html")
)
'''


# 电影类型图
colors = ' '.join([i for i in df['类型']]).strip().split()
c = dict(Counter(colors))
f = zip(c.keys(), c.values())
words = sorted(f)
# print(c)
# 其中有个错误值“1978(中国大陆)”，执行删除操作
d = c.pop('1978(中国大陆)')
my_df = pd.DataFrame(c, index=['数量']).T.sort_values(by='数量', ascending=False)
# 生成电影类型图
x2 = list(c.keys())
y2 = list(c.values())
c3 = (
    Bar()
    .add_xaxis(x2)
    .add_yaxis("影片数量", y2)
    .set_global_opts(
        title_opts=opts.TitleOpts(title="豆瓣Top250电影类型图"),
        datazoom_opts=opts.DataZoomOpts(),
    )
    .render("电影类型图.html")
)


# 绘制词云图
# import wordcloud
'''
c4 = (
    WordCloud()
    .add(
        "",
        words,
        word_size_range=[20, 100],
        textstyle_opts=opts.TextStyleOpts(font_family="cursive"),
    )
    .set_global_opts(title_opts=opts.TitleOpts(title="WordCloud-自定义文字样式"))
    .render("电影类型词云图.html")
)
'''


# 电影地区分布图
colors2 = ' '.join([i for i in df['地区']]).strip().split()
cc = dict(Counter(colors2))
ff = zip(cc.keys(), cc.values())
words2 = sorted(ff)
# print(cc)
# 生成电影类型图
x3 = list(cc.keys())
y3 = list(cc.values())
dq = (
    Bar()
    .add_xaxis(x3)
    .add_yaxis("影片数量", y3)
    .set_global_opts(
        title_opts=opts.TitleOpts(title="豆瓣Top250电影地区分布图"),
        datazoom_opts=opts.DataZoomOpts(),
    )
    .render("电影地区分布图.html")
)
