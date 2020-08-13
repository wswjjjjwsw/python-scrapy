import scrapy

import json

from jingdong.items import JingdongItem


class JdSpider(scrapy.Spider):
    name = 'jingdong'
    allowed_domains = ['jd.com']
    key_word = "手机"
    page = 1
    url = 'https://search.jd.com/Search?keyword=%s&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%s&page=%d&psort=3&click=0'
    next_url = 'https://search.jd.com/s_new.php?keyword=%s&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&page=%d&scrolling=y' \
               '&log_id=1578145467.33631&tpl=3_M&show_items=%s'
    comment_url = 'https://club.jd.com/comment/productCommentSummaries.action?referenceIds=%s'

    def start_requests(self):
        yield scrapy.Request(self.url % (self.key_word, self.key_word, self.page), callback=self.parse)

    def parse(self, response):
        pids = []
        for li in response.xpath('//*[@id="J_goodsList"]/ul/li/div'):
            item = JingdongItem()
            price = li.xpath('div[3]/strong/i/text()').extract()
            store = li.xpath('div[7]/span/a/text()').extract()
            url = li.xpath('div[@class="p-name p-name-type-2"]/a/@href').extract()

            pid = li.xpath('@data-pid').extract()
            pids.append(''.join(pid))

            item['pid'] = ''.join(pid)
            # item['title'] = ''.join(title)
            item['price'] = ''.join(price)
            item['store'] = ''.join(store)
            item['url'] = ''.join(url)

            if item['url'].startswith('//'):
                item['url'] = 'https:' + item['url']
            elif not item['url'].startswith('https:'):
                item['info'] = None
                yield item
                continue

            yield scrapy.Request(self.comment_url % ''.join(pid), callback=self.comment_parse, meta={"item": item})

        headers = {'referer': response.url}
        yield scrapy.Request(self.next_url % (self.key_word, self.page, ','.join(pids)),
                             callback=self.next_parse, headers=headers)

    def next_parse(self, response):
        for li in response.xpath('//li[@class="gl-item"]'):
            item = JingdongItem()
            # title = li.xpath('div/div/a/em/text()').extract()
            price = li.xpath('div/div/strong/i/text()').extract()
            store = li.xpath('div/div/span/a/text()').extract()
            url = li.xpath('div/div[@class="p-name p-name-type-2"]/a/@href').extract()

            pid = li.xpath('@data-pid').extract()

            item['pid'] = ''.join(pid)
            item['price'] = ''.join(price)
            item['store'] = ''.join(store)
            item['url'] = ''.join(url)

            if item['url'].startswith('//'):
                item['url'] = 'https:' + item['url']
            elif not item['url'].startswith('https:'):
                item['info'] = None
                yield item
                continue

            yield scrapy.Request(self.comment_url % ''.join(pid), callback=self.comment_parse, meta={"item": item})

        if self.page < 200:
            self.page += 2
            yield scrapy.Request(self.url % (self.key_word, self.key_word, self.page), callback=self.parse)

    def comment_parse(self, response):
        item = response.meta['item']
        data = json.loads(response.text).get('CommentsCount')
        comment_num = data[0]['CommentCount']
        item['purchase'] = comment_num
        yield scrapy.Request(item['url'], callback=self.info_parse, meta={"item": item})

    def info_parse(self, response):
        item = response.meta['item']
        lis = response.xpath('//*[@id="detail"]/div[2]/div[1]/div[1]/ul[3]/li')
        info = {}
        for li in lis:
            info[''.join(li.xpath('./text()').extract()).split('：')[0]] = ''.join(li.xpath('./text()').extract()).split('：')[1]
        try:
            item['model'] = info['商品名称']
            if item['purchase']:
                yield item
        except:
            pass
