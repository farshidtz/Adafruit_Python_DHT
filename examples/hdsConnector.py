#!/usr/bin/python
# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import sys
import Adafruit_DHT
import httplib
import time
import json


sensor = 11
pin = 4

while True:
	# Try to grab a sensor reading.  Use the read_retry method which will retry up
	# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

	# Un-comment the line below to convert the temperature to Fahrenheit.
	# temperature = temperature * 9/5.0 + 32

	# Note that sometimes you won't get a reading and
	# the results will be null (because Linux can't
	# guarantee the timing of calls to read the sensor).  
	# If this happens try again!
	if humidity is not None and temperature is not None:
		print 'Temp={0:0.1f}C Humidity={1:0.1f}%'.format(temperature, humidity)
		
		conn = httplib.HTTPConnection("localhost", 8090)
		HEADERS = {"Content-Type": "application/senml+json"}
		# Post temperature
		senml = {"n": "http://farshidpi.duckdns.org:8090/sensor/temperature", "u": "C", "v": temperature}
		senmlArr = {"e": [senml]}
		BODY = json.dumps(senmlArr)
		conn.request("POST", "/data/65c575f9-d8f7-4144-936f-af068267e00d", BODY, HEADERS)
		response = conn.getresponse()
		print response.status, response.reason, response.read()
		# Post Humidity
		senml = {"n": "http://farshidpi.duckdns.org:8090/sensor/humidity", "u": "%", "v": humidity}
		senmlArr = {"e": [senml]}
		BODY = json.dumps(senmlArr)
		conn.request("POST", "/data/7260392b-451e-4aed-a6e3-8f03b43a692c", BODY, HEADERS)
		response = conn.getresponse()
		print response.status, response.reason, response.read()

	else:
		print 'Failed to get reading. Try again!'
	
	time.sleep(5)
