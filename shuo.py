#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import qqlib
import urllib
import os
channel = 18
QQnum=""
QQpass=""
weiboUm=""
weiboPass=""
def histoday():
	content = urllib.request.urlopen('https://aoaoao.me/api/today.php').read()
	return (content.decode('utf-8'))
def old_text(temperature):
	file_r = open('/home/pi/shuo/log.txt')
	data_old = file_r.read()
	file_r.close( )
	log_text = str(temperature)
	file_object = open('log.txt','w')
	file_object.write(log_text)
	file_object.close()
	if(temperature>int(data_old)):
		return "今天的温度相比昨日此时高了"+str(temperature-int(data_old))+"℃"
	elif(temperature == int(data_old)):
		return "今天的温度与昨日此时持平哦"
	else:
		return "今天的温度相比昨日此时低了"+str(int(data_old)-temperature)+"℃"
def getdata(channel):
	data = []
	j = 0
	while GPIO.input(channel) == GPIO.LOW:
		continue
	while GPIO.input(channel) == GPIO.HIGH:
		continue
	while j < 40:
		k = 0
		while GPIO.input(channel) == GPIO.LOW:
			continue
		while GPIO.input(channel) == GPIO.HIGH:
		    k += 1
		    if k > 100:
		    	break
		if k < 8:
		    data.append(0)
		else:
		    data.append(1)
		j += 1
	return (data)
check = 0
tmp = 1
while (check !=tmp):
	GPIO.setmode(GPIO.BCM)

	time.sleep(1)

	GPIO.setup(channel, GPIO.OUT)
	GPIO.output(channel, GPIO.LOW)
	time.sleep(0.02)
	GPIO.output(channel, GPIO.HIGH)
	GPIO.setup(channel, GPIO.IN)
	data = getdata(channel)
	print (data)
	tmp = 1
	check = 0
	humidity_bit = data[0:8]
	humidity_point_bit = data[8:16]
	temperature_bit = data[16:24]
	temperature_point_bit = data[24:32]
	check_bit = data[32:40]

	humidity = 0
	humidity_point = 0
	temperature = 0
	temperature_point = 0

	for i in range(8):
		humidity += humidity_bit[i] * 2 ** (7-i)
		humidity_point += humidity_point_bit[i] * 2 ** (7-i)
		temperature += temperature_bit[i] * 2 ** (7-i)
		temperature_point += temperature_point_bit[i] * 2 ** (7-i)
		check += check_bit[i] * 2 ** (7-i)

	tmp = humidity + humidity_point + temperature + temperature_point
	GPIO.cleanup()
	time.sleep(1)
s="【温度自动播报】当前室内温度为："+str(temperature)+"℃ （来自DHT11传感器）  相对空气湿度："+str(humidity)+"% ,"+old_text(temperature)+"\n【历史上的今天】\n"+histoday()+"\n(本消息由我家树莓派自动发送)"
file_object1 = open('/home/pi/shuo/t.txt','w')
file_object1.write(s)
file_object1.close()
qq = qqlib.QQ(QQnum, QQpass)
qq.feed(s)
os.system("python weibo/weibo.py "+weiboUm+" "+weiboPass)
print(s)
