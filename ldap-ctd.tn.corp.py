#!/usr/bin/env python
# coding: utf-8



import ldap
import requests
import datetime
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import json
headers = {
    'Authorization': 'Token аывавваываываываываыва',
}
headers2 = {
    'Authorization': 'Token аывавваываываываываыва',
    'Accept': 'application/json; indent=4',
}


import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
try:
	connection = mysql.connector.connect(host='localhost',
							 database='ccnet_db',
							 user='seafile',
							 password='haikie8X')
	
except mysql.connector.Error as error :
	connection.rollback() #rollback if any exception occured
	print("Failed SQl {}".format(error))

l = ldap.initialize("ldaps://аывавваываываываываыва")
l.protocol_version = ldap.VERSION3	
l.simple_bind_s("CN=svc01-vdiconf,...", "аывавваываываываываыва")


baseDN = "....p"
baseDNSamara = "O....rp"
baseDNUfa = "OU=.....rp"
searchScope = ldap.SCOPE_SUBTREE
retrieveAttributes = ['userPrincipalName']

###################################
###### Общий фильтр (сюда добавлять новые группы в фильтр ОБЯЗАТЕЛЬНО!)
###################################
searchFilter = "(&(!(UserAccountControl:1.2.840.113556.1.4.803:=2))(|(memberOf=CN=)(memberOf=CN=)))"

try:

	results = l.search_s(baseDN, searchScope, searchFilter, retrieveAttributes)
	for result in results:
		upn = result[1]['userPrincipalName'][0].lower()
		#print(upn)

		#insert into `LDAPUsers` (`email`,`password`,`is_staff`,`is_active`,`extra_attrs`,`reference_id`) VALUES ('basharovvv@ctd.tn.corp','','0','0',NULL,NULL)
		sql_insert_query = """insert ignore into `LDAPUsers` (`email`,`password`,`is_staff`,`is_active`,`extra_attrs`,`reference_id`) VALUES ('{0}','','0','1',NULL,NULL)""".format(upn)
		cursor = connection.cursor()
		result  = cursor.execute(sql_insert_query)
		connection.commit()


	results = l.search_s(baseDNSamara, searchScope, searchFilter, retrieveAttributes)
	for result in results:
		upn = result[1]['userPrincipalName'][0].lower()
		#print(upn)
		sql_insert_query = """insert ignore into `LDAPUsers` (`email`,`password`,`is_staff`,`is_active`,`extra_attrs`,`reference_id`) VALUES ('{0}','','0','1',NULL,NULL)""".format(upn)
		cursor = connection.cursor()
		result  = cursor.execute(sql_insert_query)
		connection.commit()


	results = l.search_s(baseDNUfa, searchScope, searchFilter, retrieveAttributes)
	for result in results:
		upn = result[1]['userPrincipalName'][0].lower()
		#print(upn)
		sql_insert_query = """insert ignore into `LDAPUsers` (`email`,`password`,`is_staff`,`is_active`,`extra_attrs`,`reference_id`) VALUES ('{0}','','0','1',NULL,NULL)""".format(upn)
		cursor = connection.cursor()
		result  = cursor.execute(sql_insert_query)
		connection.commit()




except ldap.LDAPError, e:
	print e

	
	
##############################
##############################
# Функция добавления и очистки
##############################

def add_or_remove_member(searchFilter,id):
	try:

		results = l.search_s(baseDN, searchScope, searchFilter, retrieveAttributes)
		for result in results:
			upn = result[1]['userPrincipalName'][0].lower()
			#print(upn)
			data = {
				'email': upn
			}
			url = 'https://vds01-pisfile01.ctd.tn.corp/api/v2.1/admin/groups/{0}/members/'.format(id)
			response = requests.post(url, headers=headers, data=data, verify=False)
			if " is already a group member" not in response.content: 
				with open("/var/log/ldap-sync.log", "a") as logfile: logfile.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + '\n')
				print(response.content)
				with open("/var/log/ldap-sync.log", "a") as logfile: logfile.write(response.content + '\n')
				
		results = l.search_s(baseDNSamara, searchScope, searchFilter, retrieveAttributes)
		for result in results:
			upn = result[1]['userPrincipalName'][0].lower()
			#print(upn)
			data = {
				'email': upn
			}
			url = 'https://vds01-pisfile01.ctd.tn.corp/api/v2.1/admin/groups/{0}/members/'.format(id)
			response = requests.post(url, headers=headers, data=data, verify=False)
			if " is already a group member" not in response.content:
				with open("/var/log/ldap-sync.log", "a") as logfile: logfile.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + '\n')
				print(response.content)
				with open("/var/log/ldap-sync.log", "a") as logfile: logfile.write(response.content + '\n')

		results = l.search_s(baseDNUfa, searchScope, searchFilter, retrieveAttributes)
		for result in results:
			upn = result[1]['userPrincipalName'][0].lower()
			#print(upn)
			data = {
				'email': upn
			}
			url = 'https://vds01-pisfile01.ctd.tn.corp/api/v2.1/admin/groups/{0}/members/'.format(id)
			response = requests.post(url, headers=headers, data=data, verify=False)
			if " is already a group member" not in response.content:
				with open("/var/log/ldap-sync.log", "a") as logfile: logfile.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + '\n')
				print(response.content)
				with open("/var/log/ldap-sync.log", "a") as logfile: logfile.write(response.content + '\n')

		

	except ldap.LDAPError, e:
		print e
	
	try:

		url = 'https://vds01-pisfile01.ctd.tn.corp/api/v2.1/admin/groups/{0}/members/'.format(id)
		response = requests.get(url, headers=headers2, verify=False)

		for value in  json.loads(response.text)['members']:

			if value['email']!='admin@seafile.local':

				searchFilterUser = "(&(userPrincipalName={0}){1})".format(value['email'],searchFilter)
				results1 = l.search_s(baseDN, searchScope, searchFilterUser, retrieveAttributes)
				results2 = l.search_s(baseDNSamara, searchScope, searchFilterUser, retrieveAttributes)
				results3 = l.search_s(baseDNUfa, searchScope, searchFilterUser, retrieveAttributes)
				not_in_group = 1
				for result in results1:
					not_in_group = 0
				for result in results2:
					not_in_group = 0
				for result in results3:
					not_in_group = 0
				if not_in_group == 1:
					with open("/var/log/ldap-sync.log", "a") as logfile: logfile.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + '\n')
					print "==================== удаление"	
					with open("/var/log/ldap-sync.log", "a") as logfile: logfile.write("==================== удаление" + '\n')
					print value['email']
					with open("/var/log/ldap-sync.log", "a") as logfile: logfile.write(value['email'])
					url_user='https://vds01-pisfile01.ctd.tn.corp/api/v2.1/admin/groups/{0}/members/{1}/'.format(id,value['email'])
					response = requests.delete(url_user, headers=headers, verify=False)
					print(response.content)
					with open("/var/log/ldap-sync.log", "a") as logfile: logfile.write(response.content + '\n')
					print "===================="
					with open("/var/log/ldap-sync.log", "a") as logfile: logfile.write("====================" + '\n')
		
	except Exception:
		pass

	
###################################
####C.. -  id=1
###################################

#print "1"

searchFilter = "(&(!(UserAccountControl:1.2.840.113556.1.4.803:=2))(|(memberOf=CN=..)))"
id='1'

add_or_remove_member(searchFilter,id)



###################################
#### ..  id=6
###################################

#print "6"

searchFilter = "(&(!(UserAccountControl:1.2.840.113556.1.4.803:=2))(|(memberOf=CN=..)))"
id='6'

add_or_remove_member(searchFilter,id)
	

###################################
#### ...  -  id=7
###################################

#print "7"

searchFilter = "(&(!(UserAccountControl:1.2.840.113556.1.4.803:=2))(|(memberOf=CN=..)))"
id='7'

add_or_remove_member(searchFilter,id)
	
	
	
###################################
#### ...  -  id=9
###################################

#print "9"

searchFilter = "(&(!(UserAccountControl:1.2.840.113556.1.4.803:=2))(|(memberOf=CN=..)))"
id='9'

add_or_remove_member(searchFilter,id)
	
###################################
#### CN=GRP01-SFL33-777.1,OU=33-777,OU=seafile.ctd.tn.corp,OU=Группы доступа,OU=CTD,DC=ctd,DC=tn,DC=corp  -  id=8
###################################

#print "8"

searchFilter = "(&(!(UserAccountControl:1.2.840.113556.1.4.803:=2))(|(memberOf=CN=..)))"
id='8'

add_or_remove_member(searchFilter,id)
	
	
	
###################################
#### ...  -  id=11
###################################

#print "11"

searchFilter = "(&(!(UserAccountControl:1.2.840.113556.1.4.803:=2))(|(memberOf=CN=..)))"
id='11'

add_or_remove_member(searchFilter,id)	
	
	
	
###################################
#### .... -  id=12
###################################

#print "12"

searchFilter = "(&(!(UserAccountControl:1.2.840.113556.1.4.803:=2))(|(memberOf=CN=..)))"
id='12'

add_or_remove_member(searchFilter,id)	
	

###################################
#### ....  -  id=13
###################################

#print "13"

searchFilter = "(&(!(UserAccountControl:1.2.840.113556.1.4.803:=2))(|(memberOf=CN=..)))"
id='13'

add_or_remove_member(searchFilter,id)	
	
	
	
try:
	l.unbind_s()
	connection.close()
except mysql.connector.Error as error :
	connection.rollback() #rollback if any exception occured
	print("Failed SQL {}".format(error))
except ldap.LDAPError, e:
	print e
