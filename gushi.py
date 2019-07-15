import smtplib
from email.mime.text import MIMEText
from lxml import etree
import json,random,requests

def sendemail(url, headers):
    msg_from = '1953721516@qq.com'  # 发送方邮箱
    passwd = 'mcnuxeylpjfbcfbh'  # 填入发送方邮箱的授权码
    receivers = ['2396521241@qq.com']  # 收件人邮箱
    subject = '睡前小故事'  # 主题
    html = getHTMLText(url, headers)
    content = parsehtml2(html)  # 正文
    msg = MIMEText(content, "plain", 'utf-8')
    msg['Subject'] = subject
    msg['From'] = msg_from
    msg['To'] = ','.join(receivers)
    try:
        smtp = smtplib.SMTP()

        # s = smtplib.SMTP_SSL("smtp.qq.com",465)  # 邮件服务器及端口号
        smtp.connect("smtp.qq.com")
        smtp.login(msg_from, passwd)
        smtp.sendmail(msg_from, msg['To'].split(','), msg.as_string())
        print("发送成功")
    except:
        print("发送失败")
def parsehtml(urllist, html):
    url = 'http://www.tom61.com'
    tree = etree.HTML(html)
    #详情页href
    href = tree.xpath('//dd/a/@href')
    print('href===', href)
    for i in href:
        detail_url = url+i
        ##完整详情页列表：
        urllist.append(detail_url)
    print(urllist)
    #完整
    name_list = tree.xpath('//dd/a/@title')
    story_detail = {}
    for i, j in zip(name_list,urllist):
        story_detail[i]=j

    data = json.dumps(story_detail,ensure_ascii=False)
    with open('shuiqiangushi.json', 'w', encoding='utf-8')as fp:
        fp.write(data)
    return name_list

def parsehtml2(html):
    tree = etree.HTML(html)
    p_list = tree.xpath('//div[@class="t_news_txt"]/p/text()')
    return "\n".join(p_list)

def getHTMLText(url, headers):
    try:
        r = requests.get(url, headers=headers, timeout=30,verify= False)
        #如果发送了一个错误请求(一个 4XX 客户端错误，或者 5XX 服务器错误响应)，
        # 我们可以通过 Response.raise_for_status() 来抛出异常：
        r.raise_for_status()
        # 使用apparent_encoding可以获得页面中真实编码
        # r.encoding = r.apparent_encoding
        print(r.content.decode('utf-8'))
        return (r.content.decode('utf-8'))
    except:
        return ("爬取失败")

def main():
    # ua = UserAgent()
    # user = ua.random
    # print(user)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    }
    # url = 'http://www.tom61.com/ertongwenxue/shuiqiangushi/index.html'

    for i in range(1, 11):
        if i == 1:
            url = 'http://www.tom61.com/ertongwenxue/shuiqiangushi/index.html'
        else:
            url = 'http://www.tom61.com/ertongwenxue/shuiqiangushi/index_' + str(i) + '.html'
        print("正在爬取第%s页的故事链接：" % (i))
        print(url + '\n')
        html = getHTMLText(url, headers)##访问列表页信息
        with open('首页.html', 'w', encoding='utf-8')as fp:
            fp.write(html)
        namelist = parsehtml(urllist, html)
    sendemail(random.choice(urllist), headers)
    # sendemail(url, headers)
    print("爬取链接完成")

urllist = []
if __name__ == '__main__':
    main()