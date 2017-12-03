import urllib2
import sys 
import os
import datetime as DT
import sys
import pickle
import json
import pprint 
pp = pprint.PrettyPrinter(indent=4)

fileFolder = os.path.dirname(os.path.realpath(__file__))
dataFolder = os.path.join(fileFolder, "spotify-charts-data-hashmapData")

#print dataFolder
#sys.exit()

#us, gb=UK, ar = argentina, at=austria, au=australia, be=belgium, bo=bolivia, 
#br=brazil, ca=canada, ch=switz, cl=chile, 

#listOfCountries = ["ch", "cl", "co", "cr", "cz", "de", "dk"] 
#listOfCountries = ["ch", "cl", "co", "cr", "cz", "de", "dk", "ec", "es", "fi", "fr", "gr", "hk", "id", "ie", "is", "it", 
#"jp", "mx", "my", "nl", "no", "nz", "pe", "ph", "pt", "se", "sg", "th","tw", "global"]

listOfCountries = ['ar', 'at', 'au', 'be', 'bo', 'br',
'ca', 'ch', 'cl', 'co', 'cr', 'cz', 'de', 'dk', 'ec', 'es', 
'fi', 'fr', 'gb', 'global', 'gr', 
'hk', 'id', 'ie', 'is', 'it', 'jp', 
'mx', 'my', 'nl', 'no', 'nz', 'pe', 'ph', 'pt', 
'se', 'sg', 'th', 'tw', 'us']

print len(listOfCountries)

countryMap = {}

#sys.exit()
for country in listOfCountries:
	print country

	countryList = [None]*40

	countryFolder = os.path.join(dataFolder, country)

	if not os.path.exists(countryFolder):
		os.makedirs(countryFolder)

	weekStart = "2017-10-06"
	weekEnd = "2017-10-13"

	#only modify weekStart, weekEnd can take weekStart values

	weekCount = 0
	while(True):

		weekMap = {}
		weekString = weekStart+"--"+weekEnd
		url = "https://spotifycharts.com/regional/"+country+"/weekly/"+weekString+"/download"
		
		try:
			result = urllib2.urlopen(url).read()
			#print type(result)
			#print "Checking content"
			content = result.splitlines()
			#print len(content)

			#print content[:10]

			content = content[1:101]
			#print len(content)
			#print content[0]

			for elem in content:
				obj = {}

				splittedArr = elem.split(",")
				#print len(splittedArr)
				#if len(splittedArr)!=5:
				#	print splittedArr

				obj['position'] = splittedArr[0].rstrip()
				splittedArr.pop(0)

				obj['track_href'] = splittedArr[len(splittedArr)-1].rstrip()
				splittedArr.pop(len(splittedArr)-1)

				trackKeyArr = obj['track_href'].split('/')
				trackKey = trackKeyArr[len(trackKeyArr)-1].rstrip()
				#print trackKey

				obj['streams'] = splittedArr[len(splittedArr)-1].rstrip()
				splittedArr.pop(len(splittedArr)-1)

				if len(splittedArr)==2:
					obj['songName'] = splittedArr[0].rstrip()
					obj['artistName'] = splittedArr[1].rstrip()

				else:
					#print splittedArr

					songEndIdx = None
					for i in range(0, len(splittedArr)):
						val = splittedArr[i]
						if val[len(val)-1]=='\"':
							#print i
							songEndIdx = i

					if songEndIdx==None:
						songEndIdx = len(splittedArr-1)

					songSubset = splittedArr[0:songEndIdx]
					artistSubset = splittedArr[songEndIdx:]

					obj['songName'] = "".join(songSubset).rstrip()
					obj['artistName'] = "".join(artistSubset).rstrip()

				#print len(obj)
				if len(obj)!=5:
					print obj

				weekMap[trackKey] = obj

			#pp.pprint(content)

			print len(weekMap)
		
			#break


		except:
			#print "I am in this main block"
			#break
			#sys.exit()
			e1 = sys.exc_info()[0]
			print e1 
			print weekString

		if weekEnd == "2017-01-06":
			break


		weekEnd = weekStart
		year, month, date = weekStart.split("-")
		currentDate = DT.date(int(year), int(month), int(date))
		previousWeek = currentDate - DT.timedelta(days=7)
		weekStart = str(previousWeek)
		countryList[weekCount] = weekMap
		weekCount+=1

	print weekCount
	print len(countryList)
	countryList.reverse()

	countryMap[country] = countryList
	"""with open("combinedData.json", "w") as fp:
		json.dump(countryMap, fp, indent=4)"""

	#break

with open("combinedData.json", "w") as fp:
	json.dump(countryMap, fp, indent=4)
