__impl_name__ = "FM-Index 1"
__impl_author__ = "egonelbre"
__impl_url__ = "https://github.com/egonelbre/fm-index"
__impl_desc__ = "Educational implementations of Burrows-Wheeler Tranformation and Ferragina-Manzini index."
__impl_type__ = "FM-Index"

"""
Using FM-Index implementation defined in https://github.com/egonelbre/fm-index
"""

from index_interface import IndexTest
from fm_index_master.src import fmindex


class FMIndexTest(IndexTest):
	
	def __init__(self, corpus_str, defer_build=True, force_unicode=False):
		"""

		"""
		if not corpus_str[-1] == '$':
			corpus_str += '$'

		self.force_unicode = force_unicode
		self.corpus_str = corpus_str if not self.force_unicode else unicode(corpus_str, 'utf-8', 'replace')

		if not defer_build:
			self.build()
		else:
			self.idx = None
	
	def build(self):
		"""

		"""
		self.idx = fmindex.index(self.corpus_str)

	def search(self, search_string):
		"""
		return: collection (list) int of offsets in original string where substring can be found
		"""
		if not self.idx:
			raise ValueError
		else:
			search_string = search_string if not self.force_unicode else unicode(search_string, 'utf-8', 'replace')
			return self.idx.search(search_string)

	def supports_unicode(self):
		return True


fmt = FMIndexTest("fizz buzz bazz")
fmt.build()
indices = fmt.search("zz")
for i in indices:
	print i, "\t-\t", fmt.corpus_str[i:]

# # 12 	-	zz
# # 7 	-	zz bazz
# # 2 	-	zz buzz bazz