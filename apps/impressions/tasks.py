from __future__ import absolute_import
from adomattic.celery import app as capp

@capp.task
def scrapy_command(spider_dir ,referer_url, domain):
    commands.getstatusoutput(
    	'cd %s && scrapy crawl intentscraper -a urls=%s -a domain=%s &', (
    		spider_dir, referer_url, domain
    	)
    )
    return