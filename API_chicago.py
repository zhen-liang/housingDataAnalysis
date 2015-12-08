
import sklearn
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
from urllib2 import urlopen
from json import load
from xml.dom import minidom
from urllib import quote
import pandas as pd
from pandas import read_csv
from pandas import DataFrame
import xml.etree.ElementTree as ET
from xml.etree import ElementTree as etree
import sys, os
ZWSID='X1-ZWz1eumplkmdcb_5upah'
# http://www.zillow.com/webservice/GetDemographics.htm?zws-id=X1-ZWz1eumplkmdcb_5upah&state=NY&city=NewYork&neighborhood=Upper%20West%20Side
# Owners vs. Renters
# Average Commute Time (Minutes)
# Census Summary-CommuteTime

url_neighborhood='http://www.zillow.com/webservice/GetRegionChildren.htm?zws-id=X1-ZWz1eumplkmdcb_5upah&state=IL&city=chicago&childtype=neighborhood'
# 打开网页
from urllib2 import urlopen # 从urllib2包中导入urlopen()函数
website_neighborhood = urlopen(url_neighborhood)
# 读取xml 树状结构
import xml.etree.ElementTree as ET # 导入xml.etree.ElementTree包，并重命名为简写ET
tree_neighborhood=ET.parse(website_neighborhood) #调用ET包中的parse()函数
# 获取xml 树的根
root_neighborhood=tree_neighborhood.getroot()
# 根据树的结构，以root_neighborhood为起点，查找每一个neighborhood的名字，保存在名为neighborhood的list里
neighborhood= [i.text for i in root_neighborhood.findall('./response/list/region/name')]
# neighborhood=[i.replace(" ",'%20') for i in neighborhood]
data=pd.DataFrame(columns=['medianSalePrice','medHouseIncome','avgCommuteTime','Renters_percent','url_OwnersvsRenters'])


# GetDemographics
for i in neighborhood:
	url='http://www.zillow.com/webservice/GetDemographics.htm?zws-id='+ZWSID+'&state=IL&city=chicago&neighborhood='+i.replace(" ",'%20')
	website = urlopen(url)
	tree=ET.parse(website)
	tree.write('GetDemographics'+i+'.xml')
	root=tree.getroot()
	if root.findall("./message/code")[0].text != '0':
		print i+' failed:'+root.findall("./message/text")[0].text
		continue
	# Home Value index
	#homeValueIndex=root.findall("./response/pages/page")[0].findall('./tables/table/data/attribute')[1][0][0].text
	#root.findall("./response/pages/page")[0].findall('./tables/table/data/attribute/values')[0].text
	
	# median sale price
	if root.findall("./response/pages/page")[0].findall('./tables/table/data/attribute')[10][0].text == 'Median Sale Price':
		medianSalePrice=root.findall("./response/pages/page")[0].findall('./tables/table/data/attribute')[10][1][0][0].text
	else:
		medianSalePrice=np.NaN

	regionID=root.find('./response/region/id').text
	# charts= [i[0].text for i in root.findall('./response/charts/chart')]
	# charts.index('Owners vs. Renters')
	# root.findall('./response/charts/chart')[5][1].text
	url_OwnersvsRenters='http://www.zillow.com/app?chartType=home_ownVsRent&graphType=barChart&regionId='+regionID+'&regionType=8&service=chart'
	# root.findall("./response/charts/[@name='Owners vs. Renters']")
	# Renters_percent=root.findall("./response/pages/page")[1].findall('./tables/table/data')[0][1][1][0][0].text
	try:
		Renters_percent=root.findall("./response/pages/page")[1].findall('./tables/table/data/attribute')[1].findall('./values/neighborhood/value')[0].text
	except:
		Renters_percent=np.NaN
	# another method
	# Renters_percent=root.findall("./response/pages/page")[1].findall('./tables/table')[1].findall('./data/attribute')[1][1].text

	# Median Household Income
	try:
		medHouseIncome=root.findall("./response/pages/page")[2].find('./tables/table/data/attribute/values/neighborhood/value').text
	except:
		medHouseIncome=np.NaN
	# Average Commute Time (Minutes)
	# root.findall("./response/pages/page")[2].findall('./tables/table/data')[0][6][0].text  = avg commute time
	try:
		avgCommuteTime=root.findall("./response/pages/page")[2].findall('./tables/table/data/attribute')[6].findall('./values/neighborhood/value')[0].text
	except:
		avgCommuteTime=np.NaN
	a={'neighborhood':i,'medianSalePrice':medianSalePrice, 'medHouseIncome':medHouseIncome,'avgCommuteTime':avgCommuteTime,'Renters_percent':Renters_percent,'url_OwnersvsRenters':url_OwnersvsRenters}
	c=DataFrame([a])
	data=data.append(c)
data.to_csv('data.csv',sep=',')
data2=data.dropna()
np.where(data2['medianSalePrice']=='0')
data3=data2[data2['medianSalePrice']!='0']
data3['medianSalePrice']=data3['medianSalePrice'].astype(int)
data3['neighborhood']=data3['neighborhood'].astype(str)
data3.loc[:,['Renters_percent','avgCommuteTime','medHouseIncome']]=data3.loc[:,['Renters_percent','avgCommuteTime','medHouseIncome']].astype(float)

data3.loc[:,['neighborhood','medianSalePrice','Renters_percent','avgCommuteTime','medHouseIncome']].to_csv('data2.csv',sep=',')
data3['neighborhood'].to_csv('chicago_neighborhood.csv',sep=',')

#regr = linear_model.LinearRegression()
#regr.fit(data3.loc[:,['Renters_percent','avgCommuteTime','medHouseIncome']], data3['medianSalePrice'])
#print('Coefficients: \n', regr.coef_)

############
#root.findall("./response/charts/chart/[@name='Owners vs. Renters']/url")
#root[1][0].text #check error message

# 初始化一个 DataFrame 类型的数据，名为data，列名依次是以下黄色部分
data=pd.DataFrame(columns=['medianSalePrice','medHouseIncome','avgCommuteTime','Renters_percent','url_OwnersvsRenters'])
# 建立一个循环，对每一个neighborhood提取相关的信息
for i in neighborhood:
	url='http://www.zillow.com/webservice/GetDemographics.htm?zws-id='+ZWSID+'&state=IL&city=chicago&neighborhood='+i.replace(" ",'%20')
	website = urlopen(url)
	tree=ET.parse(website)
	# 把读取到的xml文档存起来
	tree.write('GetDemographics'+i+'.xml')

	root=tree.getroot()
	# 寻找包含 Median Sale Price的节点，如果存在这个节点，则把相关数据保存为 medianSalePrice
	if root.findall("./response/pages/page")[0].findall('./tables/table/data/attribute')[10][0].text == 'Median Sale Price':
		medianSalePrice=root.findall("./response/pages/page")[0].findall('./tables/table/data/attribute')[10][1][0][0].text
	else:
		medianSalePrice=np.NaN
	
	# 将获取到的信息整合成一个 dictionary, dictionary数据结构的特征是 {key:value} （即{关键字：值} ）成对出现
	a={'neighborhood':i,'medianSalePrice':medianSalePrice, 'medHouseIncome':medHouseIncome,'avgCommuteTime':avgCommuteTime,'Renters_percent':Renters_percent,'url_OwnersvsRenters':url_OwnersvsRenters}
	c=DataFrame([a]) # 把a变为 DataFrame格式
	data=data.append(c) # 把c并入名为data的DataFrame的最后一行
# 循环结束后，把data保存为csv的格式
data.to_csv('data.csv',sep=',')
