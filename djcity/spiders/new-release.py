# -*- coding: utf-8 -*-
import scrapy
from ..items import Track
from datetime import datetime
from urllib.parse import urljoin


class NewReleaseSpider(scrapy.Spider):
    name = 'new-release'
    allowed_domains = ['www.djcity.com']
    start_urls = ['http://www.djcity.com/digital/record-pool.aspx']

    def parse(self, response):
        times = response.xpath('//div[contains(@class, "day_time")]/text()').extract()
        for i, elem in enumerate(response.xpath('//ul[@class="record_pool_listing"]')):
            artists = elem.xpath('descendant::div[@class="player_txt"]/text()').extract()
            names = elem.xpath('descendant::div[@class="player_txt"]/h2/a/text()').extract()
            urls = elem.xpath('descendant::div[@class="player_txt"]/h2/a/@href').extract()
            for artist, name, url in zip(artists, names, urls):
                track = Track()
                track['name'] = name
                track['artist'] = artist
                track['url'] = urljoin(self.start_urls[0].strip(), url.strip())
                track['publish'] = self.parse_publish(times[i])
                yield track

    @staticmethod
    def parse_publish(publish_str):
        return datetime.strptime(publish_str, '%A, %B %d, %Y')
