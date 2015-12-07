from urllib2 import urlopen

appkey='6fvg96su2e3y6gbjfcrw7554'
url_neighborhood='http://api.trulia.com/webservices.php?library=LocationInfo&function=getNeighborhoodsInCity&city=Chicago&state=IL&apikey='+appkey
website_neighborhood = urlopen(url_neighborhood)

import xml.etree.ElementTree as ET
tree_neighborhood=ET.parse(website_neighborhood) 
# 获取xml 树的根
root_neighborhood=tree_neighborhood.getroot()

neighborhood_list= [{'neighborhood':i.find('./name').text, 'id':i.find('./id').text} for i in root_neighborhood.findall('./response/LocationInfo/neighborhood')]

import pandas as pd
neighborhood= pd.DataFrame(neighborhood_list, columns=['neighborhood','id'])

data=pd.DataFrame(columns=['neighborhood','date','type','number','price'])

for i in range(neighborhood.shape[0]):
	neighborhoodID=neighborhood.iloc[i,1]
	neighborhood_stat_url='http://api.trulia.com/webservices.php?library=TruliaStats&function=getNeighborhoodStats&neighborhoodId='+neighborhoodID+'&startDate=2014-08-20&endDate=2015-08-20&apikey='+appkey
	website_neighborhood_stat = urlopen(neighborhood_stat_url)
## http://api.trulia.com/webservices.php?library=TruliaStats&function=getNeighborhoodStats&neighborhoodId=2878&startDate=2015-02-10&endDate=2015-08-10&apikey=6fvg96su2e3y6gbjfcrw7554
	tree_neighborhood_stat=ET.parse(website_neighborhood_stat) 
	tree_neighborhood_stat.write('getNeighborhoodStats_'+neighborhood.iloc[i,0]+'.xml')
	root_neighborhood_stat=tree_neighborhood_stat.getroot()
	for j in root_neighborhood_stat.findall('./response/TruliaStats/listingStats/listingStat'):
		for k in j.findall('./listingPrice/subcategory'):
			each_price_list_over_time=[{'neighborhood': neighborhood.iloc[i,0] ,'date':j.find('./weekEndingDate').text, 'type': k.find('./type').text, 'number':k.find('./numberOfProperties').text, 'price': k.find('./averageListingPrice').text}]
			each_price_df_over_time=pd.DataFrame(each_price_list_over_time, columns=['neighborhood','date','type','number','price'])
			data=data.append(each_price_df_over_time)
	print i
data.to_csv('trulia_pricedata_1y.csv',sep=',')
