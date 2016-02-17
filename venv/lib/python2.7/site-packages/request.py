#!/usr/bin/env python
from dict import *
from get import *
from post import *
from public import *

REQUEST = dict()
REQUEST.update(GET)
REQUEST.update(POST)

public(REQUEST)

if __name__=="__main__":
	pass
