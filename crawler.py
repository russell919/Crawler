# pip install requests
# pip install lxml
# pip install xlwt
# 相关第三方库已安装

# Python 还有一个可以用来做 HTML 解析的库——Beautiful soup。它和 Requests 一样，也是第三方库。
# 这里选用的是 lxml模块的etree类 ，使用 Xpath 语言检索信息

# 导入相关库
import requests
from lxml import etree
import xlwt


movie_info_list = []


# 获取网页资源，返回 html 文本
def get_page_source(start_url, header):
    response = requests.get(url=start_url, headers=header)
    if response.status_code == 200:
        response.encoding = response.apparent_encoding
        page_data = response.text
        return page_data
    else:
        return "未连接到页面"


# 提取网页电影信息（数据定位）
def page_content(page_data):
    etree_data = etree.HTML(page_data)
    # <div class="article"> 在第250行， 对应的</div> 找不到
    selector = etree_data.xpath('//*[@class="article"]/ol/li/div/div[2]')
    # print(selector)
    for item in selector:

        # 电影名称
        movie_names = item.xpath('./div/a/span[1]/text()')
        # print(movie_names)

        # 电影类型、电影演职人员保存在同一个<p>标签内，这里使用 split() 函数分割提取信息
        # Python strip() 方法用于移除字符串头尾指定的字符（默认为空格或换行符）或字符序列。
        # 注意：该方法只能删除开头或是结尾的字符，不能删除中间部分的字符。
        movie_info = item.xpath('./div[2]/p[1]/text()')
        movie_people = movie_info[0].strip().replace("\xa0\xa0\xa0", "\t").split("\t")
        movie_infos = movie_info[1].strip().replace('\xa0', '').split('/')
        movie_dates, movie_areas, movie_type = movie_infos[0], movie_infos[1], movie_infos[2]
        # movie_starring = movie_info.split('主演：')

        # 电影评分
        movie_scores = item.xpath('./div[2]/div/span[2]/text()')
        # print(movie_scores)

        # 电影排名
        # 直接在 excel 表里有序排列即可

        # 电影评论人数
        movie_numbers = item.xpath('./div[2]/div/span[4]/text()')
        # print(movie_numbers)

        # 对电影的描述语
        # quotes = item.xpath('./div[2]/p[2]/span/text()')
        # print(quotes)

        # 将每一行获取到的信息添加到一个电影的列表中
        one_movie_info_list = [movie_names, movie_people, movie_dates, movie_areas, movie_type, movie_scores, movie_numbers]
        # 将一个电影的列表添加到大的列表中
        movie_info_list.append(one_movie_info_list)


# 编写主函数
# 函数调用
if __name__ == '__main__':
    for page in range(0, 10):
        url = 'https://movie.douban.com/top250?start={}&filter='.format(str(page*25))
        # page += 25，也可以做到
        # 定义请求头（这里的请求头直接使用网上可行的请求头，而不是本计算机的请求头）
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}
        t = get_page_source(start_url=url, header=headers)
        page_content(t)

        # 数据存储
        # 创建工作簿
        book = xlwt.Workbook(encoding='utf-8')
        # 创建表单
        sheet = book.add_sheet('豆瓣 Top250 电影数据')
        # 填写表头
        head = ['排名', '电影名称', '演职人员', '年份', '地区', '类型', '评分', '评论人数']
        # 写入表头
        for h in range(len(head)):
            sheet.write(0, h, head[h])
        # 排名
        for index in range(1, 251):
            sheet.write(index, 0, index)
            # 写入相对应的数据
        j = 1
        for data in movie_info_list:
            # 从索引为第1行开始写
            k = 1
            for d in data:
                sheet.write(j, k, d)
                k += 1
            j += 1
        # 退出工作簿并保存
        book.save('豆瓣Top250电影数据.xls')
