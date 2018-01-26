#!/usr/bin/python
# -*- coding: utf-8 -*-

import paho.mqtt.publish as publish

host = "iot.eclipse.org"
topic = "$SYS/broker/version"
payload = "hello mqtt"

print "topic: %s, message: %s" % (topic, payload)

publish.single(topic, payload, hostname=host)

