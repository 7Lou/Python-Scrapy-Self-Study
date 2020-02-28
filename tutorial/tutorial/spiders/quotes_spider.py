# -*- coding: utf-8 -*-
import scrapy


class QuotesSpiderSpider(scrapy.Spider):
    name = "quotes"

    '''#方法一 直接返回request对象
    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    '''
    #方法二 系统默认
    start_urls = [
        'http://quotes.toscrape.com/page/1/'
    ]

    def parse(self, response):
        '''#例子
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
        '''
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)#使用该urljoin()方法构建完整的绝对URL （因为链接可以是相对的）
            yield scrapy.Request(next_page, callback=self.parse)
        
        '''#response.follow直接支持相对URL-无需调用urljoin。
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
        '''

        '''您也可以将选择器传递给response.follow而不是字符串。该选择器应提取必要的属性：

        for href in response.css('li.next a::attr(href)'):
            yield response.follow(href, callback=self.parse)
        '''

        '''对于<a>元素，有一个快捷方式：response.follow自动使用其href属性。因此，代码可以进一步缩短：

        for a in response.css('li.next a'):
            yield response.follow(a, callback=self.parse)
        '''