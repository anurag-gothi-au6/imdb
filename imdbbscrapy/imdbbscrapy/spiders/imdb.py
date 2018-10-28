import scrapy
from datetime import datetime
from time import strptime
#from scrapy.mail import MailSender

class series(scrapy.Spider):
		
	name = 'imdbseries'
	allowed_domains = ["imdb.com"]
	
	start_urls=['https://www.imdb.com/?ref_=nv_home']
	def  parse(self, response):
		#user_email=input("Email Address:")
		tvseries = input("Tv series:")
		if len(tvseries)==0:
			tvseries = input("Tv series:")
		#mailer= MailSender()
		#mailer.send(to = ["ianuraggothi@gmail.com"], subject = "subject data", body = tvseries)
		tv_series=tvseries.split(',')
		for nos in tv_series:
			request = scrapy.FormRequest.from_response(
			           response,
			           formname='imdbForm',
			           formdata={'q': nos},
			           callback=self.parse_serieslist
			       )
			yield request
	def parse_serieslist(self,response):
		link = response.css('td.result_text > a::attr(href)').extract_first()
		next_url = "https://www.imdb.com"+link
		yield scrapy.Request(next_url,self.parse_series)
	def parse_series(self,response):
		season_link = response.css('div.seasons-and-year-nav >div >a::attr(href)').extract_first()
		season_url = "https://www.imdb.com"+season_link
		yield scrapy.Request(season_url,self.parse_season)
	def parse_season(self,response):
		#i = 0
		series_name = response.css('div.parent>h3>a::text').extract_first().strip()
		
		currentDate=datetime.today().strftime('%Y-%m-%d')
		currentDate= datetime.strptime(currentDate, '%Y-%m-%d')
		
	
		for airdate in response.css('div.list_item'):
			
			episode = airdate.css('div.info > strong >a::text').extract_first()
			date = airdate.css('div.airdate::text').extract_first().strip()
 			

			if len(date)==4:
				print('Tv series name: '+series_name)
				airyear=airdate.css('div.airdate::text').extract_first().strip()
				print('Status: The next season begins in '+airyear)
				#i =1
				break

			
			elif len(date)==0:
				print('Tv series name: '+series_name)
				print('Next episode:'+episode)
				print('Status: The next episode will be air but the date is not confirmed ')
				#i=1
				break
			
			dat=date.split()[0]
			mon=date.split()[1].strip('.')
			year=date.split()[2]
			mon = strptime(mon,'%b').tm_mon
			fulldate = str(dat)+'/'+str(mon)+'/'+str(year)
			Fulldate = datetime.strptime(fulldate, '%d/%m/%Y')
			if Fulldate.date() > currentDate.date():
				print('Tv series name: '+series_name)
				print('Next episode:'+episode)
				print('Status: The next episode airs on '+fulldate)
				#i=1
				break
				

			lastdate = response.css('div.airdate::text')[-1].extract().strip()
			if len(lastdate)>4:
				dat1=lastdate.split()[0]
				mon1=lastdate.split()[1].strip('.')
				year1=lastdate.split()[2]
				mon1 = strptime(mon1,'%b').tm_mon
				fulldate1 = str(dat1)+'/'+str(mon1)+'/'+str(year1)
				Fulldate1 = datetime.strptime(fulldate1, '%d/%m/%Y')
				if Fulldate1.date()<currentDate.date():
					print('Tv series Name: '+series_name)
					print(' The show has finished streaming all its episodes.')
					#i=1
				break
			#if i == 0:

				#start_urls='https://www.imdb.com'
				#yield scrapy.Request(start_urls,self.another,dont_filter = True)
				
		
	#def another(self,response):
		#start_urls='https://www.imdb.com'
		#print("Do you want to find details of another Tv series ? ")
		#anotherseries = input('please enter yes or no:')
		#if anotherseries=='yes':
		#	yield scrapy.Request(start_urls,callback=self.parse,dont_filter = True )
		





