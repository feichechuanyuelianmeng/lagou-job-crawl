# lagou-job-crawl
爬取拉钩网关键字为python所有职位信息

爬取所有关键字时python的职位信息并保存为csv格式
说明：
1.关键字可以是任意的在相应函数中修改就可以
2.由于反爬虫需要添加middleware中间件，来添加随机请求头和代理
3.由于使用selenium不添加代理只能爬取十几页的信息，想要爬取所有的应该是三十页左右
4.你也可以通过参数来自定义起始页和第几个位置开始下载主要是为了防止由于网速等外界因素导致爬虫只能下载一部分，下次可以从上次结束的位置下载
5.具体信息说明如下：
职位详情页这里将它们分解为：

 1. 公司名称
 2. 公司主要应用领域
 3. 公司目前发展阶段
 4. 公司网址
 5. 公司规模
 6. 工作薪水
 7. 工作具体描述
 8. 工作具体名称
 9. 工作福利
 10.工作地点
 11.工作简要描述
 
 6.具体参数修改如下：
 必改参数：第4步的chromedriver存放地址，其他可不改，
 
 1）middlewares.py中Ip列表存放的是代理ip和端口
 2)settings.py
          DOWNLOADER_MIDDLEWARES = {
            'lagou.middlewares.UserAgentDownLoadMiddleware': 543,
            # 'lagou.middlewares.IpDownLoadMiddleware': 540,
            }
            
  上面两个中间件一个是随机请求头，一个是代理如果没有代理就像上面一样注释掉
  
  3）start.py一个是有日志命令行，一个是无日志输出的，看自己需要修改，默认无日志输出
  4）主爬虫程序init方法
        self.driver = webdriver.Chrome(executable_path=r"D:\programs\chrome_driver\chromedriver.exe")# 这是我的chromedriver存放路径改成自己的
        self.start_page = 4 # 从第几页开始爬取
        self.start_num = 10 # 从第几个开始爬取
 5）文件在当前文件夹下自动生成相应csv文件想要修改在pipelines.py中修改
