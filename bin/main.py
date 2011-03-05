#!/usr/bin/env python
# -*- coding: utf-8 -*-

if __name__ == "__main__":
	import os
	import sys

	sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))
	from imageuploader.main import main

	main()

