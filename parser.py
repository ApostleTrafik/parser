from bs4 import BeautifulSoup
import requests
from openpyxl import Workbook
print('start')
wb = Workbook()
ws = wb.active
ws['A1'] = 'link'#
ws['B1'] = 'title_1'#
ws['C1'] = 'comment_1'#
ws['D1'] = 'date_comment_1'#
ws['E1'] = 'name_comment_1'#
ws['F1'] = 'product_id'#хз
ws['G1'] = 'date_comment_2'
ws['H1'] = 'name_comment_2'
ws['I1'] = 'comment_2'
title_1=[]
baza = {}
text_comments=[]
URL = 'https://www.woman.ru/health/forum/1/?sort=new' 
HEADERS = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 YaBrowser/20.7.1.68 Yowser/2.5 Safari/537.36'}
response = requests.get(URL,headers = HEADERS)
soup = BeautifulSoup(response.content,'lxml')
pages = int(soup.find('div',class_='pager__container').text.split('  ')[-2])
links = []
x = 0
i = 2
for x in range(pages):
	try:
		URL = 'http://www.woman.ru/health/forum/' + str(x) +'/?sort=new'
		HEADERS = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 YaBrowser/20.7.1.68 Yowser/2.5 Safari/537.36'}
		response = requests.get(URL,headers = HEADERS)
		soup = BeautifulSoup(response.content,'lxml')
		items = soup.findAll('li',class_='list-item')
		for item in items:
			links.append('http://www.woman.ru' + item.find('a',class_='list-item__link').get('href'))
		for link in links:
			URL = link
			response = requests.get(URL,headers = HEADERS)
			soup = BeautifulSoup(response.content,'lxml')
			answers_total = soup.findAll('div',class_='card card_answer')
			for answer_total in answers_total:
				###past1
				title_1 = soup.find('h1',class_='card__topic-title').text
				comment_1 = soup.find('div',class_='card card_topic-start').find('p').text
				name_comment_1 = soup.find('div',class_='card_topic-start').find(class_='user__name').text
				date_comment_1 = soup.find('div',class_='card_topic-start').find(class_='user__metadata').text.split('-')[1]
				###past2
				date_comment_2 = answer_total.find(class_='user__metadata').text.split('-')[1]
				name_comment_2 = answer_total.find(class_='user__name').text
				comment_2 = answer_total.find('div',class_='card__text').text
				###past1
				baza.update({'0' : link })
				baza.update({'1' : title_1})
				baza.update({'2' : comment_1})
				baza.update({'3': date_comment_1})
				baza.update({'4' : name_comment_1})
				baza.update({'5' : date_comment_2})
				baza.update({'6' : name_comment_2})
				baza.update({'7' : comment_2})
				###past1
				ws['A'+str(i)] = baza['0']
				ws['B'+str(i)] = baza['1']
				ws['C'+str(i)] = baza['2']
				ws['D'+str(i)] = baza['3']
				ws['E'+str(i)] = baza['4']
				###past2
				ws['G'+str(i)] = baza['5']
				ws['H'+str(i)] = baza['6']
				ws['I'+str(i)] = baza['7']
				i+=1
				x+=1
	except:
		continue
print('success')
wb.save("work.xlsx")







