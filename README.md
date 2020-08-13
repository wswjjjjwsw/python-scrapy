# python-scrapy
this is final homework for python  
淘宝和京东两个文件夹分别为爬虫的代码  
其中，京东是按照标准的scrapy的方式进行的爬虫  
淘宝因为有防爬虫机制，最终是使用模拟用户操作来进行的爬虫  
爬虫的结果分别存储在淘宝京东各自文件夹中，淘宝的文件只上传了其中一小部分  
  
  
  
爬虫的结果进行了可视化分析，总共完成了三个任务，任务输出的结果图在 **__python大作业.pdf__** 中,任务题目如下：
## **任务 1:**
分别爬取京东和淘宝，在手机频道中，找出累积销量(所有商家销售同一型号手机的销 量之和)最高的 20 款手机。
说明:
1) 销量:京东以评论数为准，淘宝以付款人数为准。
2) 基础版本:一款手机只看最低配置和最低价格，例如iPhone11只按照64G的价格来计 算。高级版本:一款手机有多个型号，不同的配置算不同的型号，例如 iPhone 11 64G 算是一种型号，128G 算另一种型号。按照自己的能力选做基础版本或者是高级版本， 高级版本有加分。
结果展示:
按照销量，以直方图的形式展示手机型号及其销量，按照销量倒排序。图中的手机型号 请尽量简化，能够区分即可。
一个 figure 中有 2 个子图，2 个子图分别展示京东和淘宝中，手机价格直方图。
  

## **任务 2:**
用你爬取下来的数据制作散点图，横轴为手机价格，纵轴为该价格对应的商家个数。
结果展示:
一个 figure 中有 2 个子图，2 个子图分别展示京东和淘宝中，手机价格的分布情况。
  


## **任务 3:**
找出在两个平台上都有售卖的 5 款手机(找销量较大的)，由于两个平台上都有不同的 卖家都销售这些手机，价格也不同，需要将这些卖家销售这款手机的价格，做出箱型图，比 较不同平台上的价格情况。
结果展示:
一个 figure 中有 5 个子图，每个子图里面有两个平台上售卖的同一型号手机的 2 个价 格箱型图。
