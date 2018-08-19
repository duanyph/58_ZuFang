import requests,bs4,csv,re,codecs,threading,time
with open("数据.csv","wb+") as a:
    a.write(codecs.BOM_UTF8)
open("响应错误日志.log","w").close()
open("页面解析错误日志.log","w").close()
ShuJv=open("数据.csv","a",encoding="utf-8",newline='')
XieRu=csv.writer(ShuJv,dialect="excel")
XieRu.writerow(["类型及标题","发布日期","租金","厅室及大小","位置及交通","信息来源","链接"])
GeShiHua="\S+"
def TiQu(XiangYing):
    XiangYing.encoding="utf-8"
    # print(XiangYing.status_code)
    # print(open("响应.html","w+",encoding="utf-8").write(XiangYing.text))
    bs41=bs4.BeautifulSoup(XiangYing.text,"html.parser")
    try:
        html_ul=bs41.find("ul",class_="listUl")
    except:
        print("页面解析错误！略过！")
        with open("页面解析错误日志.log","a") as a:
            a.write(str(bs41)+"\n")
    html_li_Ji=html_ul.find_all("li")[:-1]
    # print(html_li_Ji)
    for html_li in html_li_Ji:
        BiaoTi=html_li.find("h2").get_text()
        LianJie="http:"+html_li.find("h2").find("a")["href"]
        FaBu=html_li.find("div",class_="sendTime").get_text()
        ZuJin=html_li.find("div",class_="money").get_text()
        TingShi=html_li.find("p",class_="room").get_text()
        WeiZhi=html_li.find("p",class_="add").get_text()
        try:
            LaiYuan=html_li.find("div",class_="jjr").get_text()
        except:
            try:
                LaiYuan=html_li.find("p",class_="gongyu").get_text()
            except:
                LaiYuan=html_li.find("p",class_="geren").get_text()
        YuanSu=[]
        for a in [BiaoTi,FaBu,ZuJin,TingShi,WeiZhi,LaiYuan,LianJie]:
            a=re.findall(GeShiHua,a)
            c=""
            for b in a:
                c+=b
            # c=c.encode("utf-8").decode("gbk")
            YuanSu.append(c)
        print("写出数据：",YuanSu[0])
        XieRu.writerow(YuanSu)
        ShuJv.flush()
for YeShu in range(70):
    QiShi_url="http://cd.58.com/chuzu/pn"+str(YeShu)
    QIngQIuTou={"Host": "cd.58.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        # "Accept-Encoding": "gzip, deflate",
        "Referer": "http://cd.58.com/chuzu/",
        # "Cookie": "f=n; userid360_xml=35ACE45FC8B3A4E7EE8BFE40FBD99480; time_create=1535744396928; 58home=cd; f=n; id58=c5/njVtiDFFuTvjfBVv+Ag==; city=cd; 58tj_uuid=86d42cd4-c781-462c-9510-aad4e1fd97b1; new_session=0; new_uv=1; utm_source=; spm=; init_refer=https%253A%252F%252Fwww.baidu.com%252Flink%253Furl%253DBDrzkW_BMYOB9bKOXBFIsbC4kmNaH-vMFv3e5SgWBjS%2526wd%253D%2526eqid%253D84e6b2e100001f29000000035b620c4f; commontopbar_ipcity=cd%7C%E6%88%90%E9%83%BD%7C0; commontopbar_myfeet_tooltip=end; xxzl_deviceid=PRzgOlNzThX55jv5Xlg7jhgtcY72jqRudo6m%2BuRjv6QKq6uUG99tbku73gSVRuKC; als=0; wmda_uuid=27c0427d56f0c094fd7fb35a45aa3c4d; wmda_new_uuid=1; wmda_session_id_2385390625025=1533152389993-d0e96a78-af61-a3d0; wmda_visited_projects=%3B2385390625025; xzfzqtoken=EXvUEAWn4kgBRlx29EqdFdWHYVjiXQXbNDDVYlbfs5kklpcq2bVpJGtdlafFA%2BPnin35brBb%2F%2FeSODvMgkQULA%3D%3D",
        "Connection": "keep-alive",
        # "Upgrade-Insecure-Requests": "1",
        # "Cache-Control": "max-age=0"
        }
    try:
        XiangYing=requests.get(QiShi_url,QIngQIuTou)
    except:
        try:
            print("响应超时，重试！")
            XiangYing=requests.get(QiShi_url,QIngQIuTou)
        except:
            print("重试失败，略过！")
            with open("响应错误日志.log","a") as a:
                a.write(QiShi_url+"\n")
            continue
    threading.Thread(target=TiQu,args=(XiangYing,)).start()
    time.sleep(1)
if threading.activeCount()==0:
    ShuJv.close()