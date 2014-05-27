#!/usr/bin/python
import httplib
import sys
import time
import ConfigParser
from xml.dom.minidom import parseString
from Tkinter import *
from PIL import Image, ImageTk

def updateTime(time, tz):
	tzh = tz / 3600
	tzhm = tzh * 3600
	if tzhm != tz:
		tzm = (tz - tzhm) / 60
	else:
		tzm = 0
	tzms = tzm * 60
	if tzhm + tzms != tz:
		tzs = tz - tzhm - tzms
	else:
		tzs = 0
	parts = time.split(':')
	hh = int(parts[0]) + tzh
	mm = int(parts[1]) + tzm
	ss = int(parts[2]) + tzs
	fixed = '{0:02d}:{1:02d}:{2:02d}'.format(hh, mm, ss)
	return fixed

def getUrl(path, idCity, apiId):
	server = 'openweathermap.org'
	args_a = '?id='
	args_b = '&units=imperial&mode=xml'
	api = '&APPID=' + apiId
	request = path + args_a + idCity + args_b + api
	conn = httplib.HTTPConnection(server)
	conn.request('GET', request)
	http_response = conn.getresponse()
	if http_response.status == 200:
		response = http_response.read()
	else:
		response = str(http_response.status) + ':  ' + http_response.reason
		print response
		sys.exit()
	conn.close()
	return response

def currentConditions(city_id, api_id):
	output = []
	pathCur = '/data/2.5/weather'
	httpResponse = getUrl(pathCur, city_id, api_id)
	dom = parseString(httpResponse)
	child = dom.childNodes[0].toxml()

	tagCloud = dom.getElementsByTagName('clouds')[0]
	cName = tagCloud.attributes["name"].value
	cNum = tagCloud.attributes["value"].value

	tagSumm = dom.getElementsByTagName('weather')[0]
	summary = tagSumm.attributes["value"].value
	icon = tagSumm.attributes["icon"].value
	output.append(cName + ' (' + cNum + ')'+ ', ' + summary)

	tagSun = dom.getElementsByTagName('sun')[0]
	sunRise = tagSun.attributes["rise"].value.split('T')[1]
	sunRise = updateTime(sunRise, -time.timezone)
	sunSet = tagSun.attributes["set"].value.split('T')[1]
	sunSet = updateTime(sunSet, -time.timezone)
	output.append('Sunrise: ' + str(sunRise) + " - Sunset: " + str(sunSet))

	tagTemp = dom.getElementsByTagName('temperature')[0]
	tMin = tagTemp.attributes["min"].value
	tMax = tagTemp.attributes["max"].value
	tCur = tagTemp.attributes["value"].value
	tUnit = tagTemp.attributes["unit"].value
	output.append('Temperature:  ' + tCur + ', ' + tMin + ' - ' + tMax + ' ' + tUnit)

	tagHum = dom.getElementsByTagName('humidity')[0]
	hCur = tagHum.attributes["value"].value
	hUnit = tagHum.attributes["unit"].value
	output.append('Humidity: ' + hCur + hUnit)

	tagPres = dom.getElementsByTagName('pressure')[0]
	pCur = tagPres.attributes["value"].value
	pUnit = tagPres.attributes["unit"].value
	output.append('Pressure: ' + pCur + pUnit)

	tagWind = dom.getElementsByTagName('wind')[0]
	tagWSpeed = dom.getElementsByTagName('speed')[0]
	tagWDir = dom.getElementsByTagName('direction')[0]
	wSpeed = tagWSpeed.attributes["value"].value
	wName = tagWSpeed.attributes["name"].value
	wDir = tagWDir.attributes["code"].value
	output.append('Wind: ' + wSpeed + wDir + ' (' + wName + ')')

	tagPrec = dom.getElementsByTagName('precipitation')[0]

	output.append('')
	return output, icon

def currentForecast(city_id, api_id):
	pathCast = '/data/2.5/forecast'
	table = []
	httpResponseCast = getUrl(pathCast, city_id, api_id)
	domCast = parseString(httpResponseCast)
	tagHour = domCast.getElementsByTagName('time')
	oldDay = ''
	dayTemps = ''
	hh = 0
	while hh < 24:
		dayTemps += ',' + str(hh) + ":00"
		hh += 3
	first = True
	for hour in tagHour:
		hTime = hour.attributes["from"].value
		timeParts = hTime.split('T')
		if timeParts[0] != oldDay:
			table.append(dayTemps)
			oldDay = timeParts[0]
			dayTemps = oldDay
			first = True
		hh = int(timeParts[1].split(':')[0]) / 3
		if first:
			while hh > 0:
				dayTemps += ','
				hh -= 1
		domHour = parseString(hour.toxml())
		tagHourTemp = hour.getElementsByTagName('temperature')[0]
		hTemp = tagHourTemp.attributes["value"].value
		tagHourSym = hour.getElementsByTagName('symbol')[0]
		hCode = tagHourSym.attributes["number"].value
		hPrec = ''
		listEl = hour.getElementsByTagName('precipitation')
		if len(listEl) > 0:
			tagHourPrecip = listEl[0]
			aPrec = tagHourPrecip.attributes.get("value", None)
			if aPrec != None:
				hPrec = '\n' + aPrec.value
		hSym = tagHourSym.attributes["var"].value
		dayTemps += ',%3.2f' % float(hTemp) + hPrec + ';' + str(hSym)
		first = False
	return table

def layoutData(win, path, icon, conditions, forecast):
	del widgets[:]
	lCurTitle = Label(win, text='Current Conditions')
	lCurrent = Label(win, text=out)
	lForecast = Label(win, text='Forecast')
	bOk = Button(win, text="OK", command=win.quit)
	bRef = Button(win, text='Refresh', command=refreshData)
	nameIcon = path + "/" + icon + ".gif"
	photo = PhotoImage(file=nameIcon)
	lWeather = Label(win, image=photo)
	lWeather.photo = photo
	widgets.append(lCurTitle)
	widgets.append(lCurrent)
	widgets.append(lForecast)
	widgets.append(bOk)
	widgets.append(bRef)
	widgets.append(lWeather)

	lCurTitle.grid(row=0, columnspan=9)
	lCurrent.grid(row=1, columnspan=9)
	lWeather.grid(row=2, columnspan=9)

	lForecast.grid(row=4, columnspan=9)
	nRow = 5
	for line in forecast:
		nCol = 0
		for col in line.split(','):
			tn = col.split(';')
			if len(tn) > 1:
				nameImg = path + "/" + tn[1] + ".gif"
				photo = PhotoImage(file=nameImg)
				cell = Label(win, text=tn[0], image=photo)
				cell.photo = photo
				cell.config(compound=CENTER, fg='Red')
			else:
				cell = Label(win, text=tn[0])
			cell.grid(row=nRow, column=nCol)
			widgets.append(cell)
			nCol += 1
		nRow += 1
	bOk.grid(row=nRow, columnspan=9)
	bRef.grid(row=nRow + 1, columnspan=9)
	return widgets

def refreshData():
	global widgets
	for w in widgets:
		w.grid_forget()
		w.destroy()
	conditions, icon = currentConditions(city_id)
	forecast = currentForecast(city_id)
	out = "\n".join(conditions)
	widgets = layoutData(root, path, icon, conditions, forecast)

config = ConfigParser.ConfigParser()
path = sys.path[0]
config.read(path + "/wx.cfg")
def_id = config.get("Identification", "city")
api_id = config.get("Identification", "user")
widgets = []
if len(sys.argv) > 1:
	city_id = sys.argv[1]
else:
	city_id = def_id

conditions, icon = currentConditions(city_id, api_id)
forecast = currentForecast(city_id, api_id)
out = "\n".join(conditions)

root = Tk()
root.title('Weather')
widgets = layoutData(root, path, icon, conditions, forecast)
root.mainloop()
root.destroy()

