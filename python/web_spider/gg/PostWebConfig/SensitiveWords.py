#! /usr/bin/python
# -*- coding: utf-8 -*-

import requests
import re
import json
    
def filter(value):
    value=value.replace('武汉肺炎','新冠肺炎')
    value=value.replace('武肺','新冠肺炎')
    value=value.replace('习近平','习近平主席')
    return(value)
