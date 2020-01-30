import hashlib
import pickle
import socket
import time
import sys
import os

PORT = 20205
RECV_SIZE = 10485761

class packet():
	def __init__(self, _identifier, _content):
		self.identifier = _identifier
		self.content = _content



