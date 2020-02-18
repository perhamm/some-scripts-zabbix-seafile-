#!/usr/bin/env python3.6
# coding: utf-8

import sys
import requests
import os
import base64
import smtplib
import sys
import base64
import datetime
import time


max_count = 600
#max_count = 20
#timeformat = 	'%Y-%m-%d'
#timeformat = 	'%Y-%m-%d %H'
timeformat = 	'%Y-%m-%d'
tmp_file_sms = '/usr/lib/zabbix/alertscripts/sms.runlogdate.txt'



def file_read(filename):
    with open(filename, "r") as fd:
        text = fd.readlines()
    return text


def file_append(filename, text):
    with open(filename, "a") as fd:
        fd.write(str(text))
    return True


	
	
def spam_check(sms_body):
	
	dt = datetime.datetime.now()
	value = datetime.datetime.fromtimestamp(time.mktime(dt.timetuple()))

	data = file_read(tmp_file_sms)

	try:
		tail = data[-max_count]
		tail_end = data[-1]
	except Exception:
		tail = ''
		tail_end = ''



	time1 = value.strftime(timeformat)

	if tail.find('time') == 0:
		time2 = tail.split(';')[1]	
	else:
		time2 = ''
	
	

	
	
	
	
	if time1==time2:

		file_append(tmp_file_sms,"time;{0};{1};{2};{3}\n".format(value.strftime(timeformat),value.strftime('%Y-%m-%d %H-%M-%S'),sms_body,'АХТУНГ!!! Превышен порог') )
		if "АХТУНГ!!!" not in tail_end:
			rezult = 3
		else:
			rezult = 0
	else:

		file_append(tmp_file_sms,"time;{0};{1};{2}\n".format(value.strftime(timeformat),value.strftime('%Y-%m-%d %H-%M-%S'),sms_body) )
		rezult = 1
	return rezult



class sms(object):
	def __init__(self):
		super(sms, self).__init__()
		sms.url = "http://....../m2m/m2m_api.asmx/SendMessage?login=................."
		sms.mainurl = "...."
		sms.bkpurl1 = "http://...../sendsms.cgi?utf8"
		sms.url1 = "..."
		sms.bkpurl2 = "http://.../sendsms.cgi?utf8"
		sms.url2 = "fsdfsdfs"
		sms.bkpurl3 = "http://1..../sendsms.cgi?utf8"
		sms.url3 = "fsdfsdfsd"
		sms.message = ''
		sms.number = ''
		
	def send(self):
			
		url_append = "&msid={0}&message={1}&naming=TN_Diascan".format(self.number, self.message)

		url = self.url + url_append
		
		#print(url)	
		try:
			response = os.system("ping -c 1 -W 1 " + sms.mainurl)
			if response == 0:
				res = requests.get(url,verify=False, timeout=3)
				res_code = res.status_code
				#print(res_code)
				if res.status_code != 200:
					raise Exception("Main url not 200!")
				#print(res.text)
			else:
				raise Exception("Main url unreachable!")
		except:
			self.message = self.message.replace("%20", " ")
			#params = (('utf8', ''),)
			params = ''
			data = "[+{0}] {1}".format(self.number, self.message).encode('utf-8')
			#print(data)
			try:
				response = os.system("ping -c 1 -W 1 " + sms.url1)
				if response == 0:
					res = requests.post(self.bkpurl1, params=params, data=data, auth=('smsnetping', 'fsdfsdf!'),verify=False,  timeout=3)
					#print(res.status_code)
					if res.status_code  != 200:
						raise Exception("url1 not 200!")
					#print(res.text)
					if "ok" not in res.text:
						raise Exception("url1 not ok!")
				else:
					raise Exception("url1 unreachable!")
			except:
				try:
					response = os.system("ping -c 1 -W 1 " + sms.url2)
					if response == 0:
						res = requests.post(self.bkpurl2, params=params, data=data, auth=('smsnetping', 'fsdfsd!'),verify=False,  timeout=3)
						#print(res.status_code)
						if res.status_code != 200:
							raise Exception("url2 not 200!")
						#print(res.text)
						if "ok" not in res.text:
							raise Exception("url2 not ok!")
					else:
						raise Exception("url2 unreachable!")
				except:
					try:
						response = os.system("ping -c 1 -W 1 " + sms.url3)
						if response == 0:
							res = requests.post(self.bkpurl3, params=params, data=data, auth=('smsnetping', 'fsdfs!'),verify=False, timeout=3)
							#print(res.status_code)
							if res.status_code  != 200 :
								raise Exception("url3 not 200!")
							#print(res.text)
							if "ok" not in res.text:
								raise Exception("url3 not ok!")
						else:
							raise Exception("url3 unreachable!")
					except:
						raise Exception("All urls unreachable or not ok or not 200! Fuck!")


def main():
	
	smska = sms()
	smska.number = sys.argv[1]
	
	mesg = (sys.argv[2]+" "+''.join(string for string in sys.argv[3])).replace(" ", "%20")

	smska.message = mesg



	spm_chk = spam_check("|||"+smska.number+"|||"+smska.message+"|||")
	if (spm_chk == 1):
		smska.send()
	else:
		if (spm_chk == 3):
			smska.number = 'fsdfsdfsdfsdfs'
			print (smska.number)
			smska.message = 'sms limit reachable'.replace(" ", "%20")
			print (smska.message)
			smska.send()
			raise Exception("Spam!!! Fuck!!!Send it to admin...")
		else:
			raise Exception("Spam!!! Fuck!!!")
	

if __name__ == "__main__":
	main()
