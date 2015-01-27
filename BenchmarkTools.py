import sys
import random
import gc
import json
import importlib
import timeit
import os

from pympler.asizeof import asizeof

if os.name == 'posix':
	import time
elif os.name == 'nt':
	import win32process
	import win32api

def random_substring(s, slen):
	index = random.randint(0, len(s) - slen - 1)
	return s[index : index + slen], index

# A benchmark task will be a single build of the data structure
# Followed by n lookups of m strings (default n=1000, m=1000)
class BenchmarkTaskInfo:
	
	@staticmethod
	def class_for_name(module_name, class_name):
		# load the module, will raise ImportError if module cannot be loaded
		m = importlib.import_module(module_name)
		# get the class, will raise AttributeError if class cannot be found
		c = getattr(m, class_name)
		return c

	@staticmethod
	def from_dict(d):
		corpus_filepath = d["corpus_filepath"]
		cl = d["test_class"]
		test_class = BenchmarkTaskInfo.class_for_name(cl[0], cl[1])
		text_len = d["text_len"]
		search_len = d["search_len"]
		num_searches = d["num_searches"]
		lookups_per_query = d["lookups_per_query"]
		return BenchmarkTaskInfo(corpus_filepath, test_class, text_len, search_len, num_searches, lookups_per_query)
		
	def __init__(self, corpus_filepath, test_class, text_len, search_len, num_searches=1000, lookups_per_query=1000, skip_queries=False, report_progress=False, do_output=None):
		self.corpus_filepath = corpus_filepath
		self.test_class = test_class
		self.text_len = text_len
		self.search_len = search_len
		self.num_searches = num_searches
		self.lookups_per_query = lookups_per_query
		self.skip_queries = skip_queries
		self.report_progress = report_progress
		self.do_output = do_output
		
	def get_text(self):
		with open(self.corpus_filepath) as corpus_file:
			corpus = corpus_file.read()
			if ("chinese" in self.corpus_filepath) or ("english" in self.corpus_filepath):
				text, text_index = random_substring(unicode(corpus, 'utf-8', 'replace'), self.text_len)
			else:
				text, text_index = random_substring(corpus, self.text_len)
		return text, text_index
	
	def get_searches(self, text):
		search = []
		search_indexes = []
		for c in range(0, self.num_searches):
			s, i = random_substring(text, self.search_len)
			search.append(s)
			search_indexes.append(i)
		return search, search_indexes

	def to_dict(self):
		d = {}
		d["corpus_filepath"] = self.corpus_filepath
		d["test_class"] = [self.test_class.__module__, self.test_class.__name__]
		d["text_len"] = self.text_len
		d["search_len"] = self.search_len
		d["num_searches"] = self.num_searches
		d["lookups_per_query"] = self.lookups_per_query
		return d

	def __hash__(self):
		return hash((self.test_class.__module__ + "." + self.test_class.__name__, self.text_len, self.search_len, self.num_searches, self.lookups_per_query))

	def __eq__(self, other):
		return (self.test_class.__module__ + "." + self.test_class.__name__, self.text_len, self.search_len, self.num_searches, self.lookups_per_query) == (other.test_class.__module__ + "." + other.test_class.__name__, other.text_len, other.search_len, other.num_searches, other.lookups_per_query)

def get_time():
	if os.name == 'posix':
		return time.clock()
	elif os.name == 'nt':
		return win32process.GetThreadTimes(win32api.GetCurrentThread())

def compute_time_diff(start, end):
	if os.name == 'posix':
		return {
			"KernelTime": 0,
			"UserTime": end - start
		}
	elif os.name == 'nt':
		return { 
			"KernelTime": (end["KernelTime"] - start["KernelTime"]) / 10000000.0,
			"UserTime": (end["UserTime"] - start["UserTime"]) / 10000000.0
		}
		
def run_benchmark(task_info):

	if task_info.report_progress:
		print "Running benchmark on", task_info.test_class, "TextLen:", task_info.text_len, "SearchLen:", task_info.search_len

	ret = {"info": task_info.to_dict()}
	text = ''
	
	# Get the appropriate corpus, and generate the text we are searching through
	text, text_index = task_info.get_text()	
	ret["text_len"] = len(text)
	ret["text_size"] = asizeof(text)
		
	# Generate search strings
	search, search_indexes = task_info.get_searches(text)    
	ret["avg_search_len"] = sum([len(s) for s in search]) / task_info.num_searches
	ret["avg_search_size"] = sum([asizeof(s) for s in search]) / task_info.num_searches
	
	# GC before testing
	gc.collect()
		
	# Build data structure
	#text = unicode(text, "utf-8", "replace")
	struct = task_info.test_class(text) #force_unicode=True if (("chinese" in task_info.corpus_filepath) or ("english" in task_info.corpus_filepath)) else False)
	
	# Check for UTF-8
	#if struct.supports_unicode():
	#	if ("chinese" in task_info.corpus_filepath) or ("english" in task_info.corpus_filepath):
	#		text = unicode(text, "utf-8", "replace")
	#		struct = task_info.test_class(text)
	#else:
	#	if ("chinese" in task_info.corpus_filepath) or ("english" in task_info.corpus_filepath):
	#		raise ValueError("This index type does not support unicode!")
	
	
	start_build = get_time()
	start_build_ti = timeit.default_timer()
	struct.build()
	end_build = get_time()
	end_build_ti = timeit.default_timer()
	
	ret["build_time"] = compute_time_diff(start_build, end_build)
	ret["build_time_ti"] = end_build_ti - start_build_ti
	ret["size"] = asizeof(struct)
	
	if task_info.skip_queries:
		return ret
	
	# Quick check to see if the index works:
	for i in range(0, len(search)):
		tofind = search[i]
		ans = struct.search(tofind)		
		assert len(ans) > 0
		for ind in ans:
			try:
				#assert tofind == unicode(text, 'utf-8')[ind : ind + len(tofind)]
				
				#if isinstance(tofind, unicode):
				#	assert tofind == unicode(text, 'utf-8', 'replace')[ind : ind + len(tofind)]
				#else:
				assert tofind == text[ind : ind + len(tofind)]
			except AssertionError as e:
				e.__tofind__ = tofind
				e.__text__ = text
				e.__struct__ = struct
				raise e
	
	# Query the structure
	start_search = get_time()
	start_search_ti = timeit.default_timer()
	for search_string in search:
		for i in range(0, task_info.lookups_per_query):
			struct.search(search_string)
	end_search = get_time()
	end_search_ti = timeit.default_timer()
	
	ret["search_time"] = compute_time_diff(start_search, end_search)
	ret["search_time_ti"] = end_search_ti - start_search_ti
	
	if task_info.do_output != None:
		with open(task_info.do_output, mode='a+') as output:
			output.write(json.dumps(ret) + '\n')
	
	return ret
		