#!/usr/bin/python
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import numpy as np
import time

host = "localhost"
topic = "pulse/ibi"
user, password = "pi", "pi"

client = mqtt.Client()
client.username_pw_set(user, password)
client.connect(host, 1883, 60)

for i in xrange(10):
    payload = int(np.random.random()*100)
    print "topic: %s, message: %d" % (topic, payload)
    client.publish(topic, "%d" % (payload))
    time.sleep(0.01)

