"""
TODO:
search function implementation isn't quite right. fix it (integrate code from slides)
"""
from interface import BenchmarkInterface

import math
import tools_karkkainen_sanders as tks

class SuffixArray1(BenchmarkInterface):
	
	### Annotations ###
	__impl_name__ = ""
	__impl_author__ = ""
	__impl_desc__ = ""
	__impl_url__ = ""
	###################
	
	# 
	def __init__(self, corpus_str, defer_build=True):
		self.corpus_str = unicode(corpus_str, 'utf-8', 'replace')
		if not defer_build:
			self.build()
		else:
			self.sa = None
			self.lcp = None

	#
	def build(self):
		self.sa = tks.simple_kark_sort(self.corpus_str)
		self.lcp = tks.LCP(self.corpus_str, self.sa)
		#? self.sa = self.sa[0 : len(self.corpus_str) ]
	
	# return: list int of offsets in original string where substring can be found
	def search(self, search_string):
		search_string = unicode(search_string)
		if not self.sa or not self.lcp:
			raise ValueError
		else:
			search_string = unicode(search_string)
			return self.binary_search_sa(search_string)
	
	def binary_search_sa(self, search_str):
		low = 0
		high = len(self.corpus_str)
		
		while low != high:
			mid = int(math.ceil( (low + high) / 2 ) )
			suffix_i = self.sa[mid]
			# match
			if search_str == self.corpus_str[suffix_i:suffix_i+len(search_str)]:
				return self.scan(search_str, mid, low, high)
			# in lower half
			elif search_str < self.corpus_str[suffix_i:]:
				high = mid
			# in upper half
			else:
				low = mid
		
		return -1
	
	def scan(self, search_str, i, low, high):
		start = i
		end = i
		
		while start > low:
			suffix_i = self.sa[start - 1]
			if search_str != self.corpus_str[suffix_i:suffix_i+len(search_str)]:
				break
			else:
				start -= 1
		
		while end < high:
			suffix_i = self.sa[start + 1]
			if search_str != self.corpus_str[suffix_i:suffix_i+len(search_str)]:
				break
			else:
				end += 1
		
		return self.sa[start : end]

