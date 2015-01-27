import abc
class IndexTest(object):
	__metaclass__ = abc.ABCMeta
	
	@abc.abstractmethod
	def __init__(self, corpus_str, defer_build=True, force_unicode=False):
		"""
		There must exist a constructor which accepts the corpus string and optionally builds the string index. 
		"""
		raise NotImplementedError
	@abc.abstractmethod
	def build(self):
		"""
		There must exist a method which builds the string index from the corpus string, stored as a property.
		"""
		raise NotImplementedError
	@abc.abstractmethod
	def search(self, search_string):
		"""
		There must exist a method which searches the string index if built for a given search string, returning ValueError if the index has not yet been instantiated.
		"""		
		raise NotImplementedError
	@abc.abstractmethod
	def supports_unicode(self):
		"""
		Indicate whether the string indexing implementation supports Unicode strings, or ASCII only.
		"""
		raise NotImplementedError