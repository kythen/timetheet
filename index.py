#!/usr/bin/python
#coding:utf-8
import json, web,re,xlrd,copy
from web.contrib.template import render_jinja
from conf import deal_data

render = render_jinja('templates',encoding='utf-8')
urls = (
	'/','Index',
	'/about','About',
	'/detail.html','Detail_page',
	'/detail','Detail'
	)
app = web.application(urls,globals())
data = deal_data()

class Index:
	def GET(self):
		return render.index(locals())

class About:
	def GET(self):
		path = r'E:/table/' + web.input().fileName
		timeRange = json.loads(web.input().timeRange,encoding='utf-8')
		try:
			data.testXlrd(path)
		except:
			return json.dumps({'errCode':0});
		rtndata = {}
		data.classify()

		for key in data.disposal_data:
			rtndata[key] = data.timestamp_compare(data.disposal_data[key],timeRange)

		return json.dumps(rtndata, encoding='UTF-8', ensure_ascii=False)

class Detail_page:
	def GET(self):
		return render.detail(locals())

class Detail:
	def GET(self):
		param = web.input().job_number
		return json.dumps({'info':data.disposal_data[param],'job_number':data.disposal_data[param][0]['job_number'],'name':data.disposal_data[param][0]['name']},encoding='utf-8',ensure_ascii=False)

if __name__ == '__main__':
	app.run()
