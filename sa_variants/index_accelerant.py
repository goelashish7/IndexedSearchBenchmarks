__impl_name__ = "Suffix Array - SAIS"
__impl_author__ = "davehughes"
__impl_url__ = "https://github.com/davehughes/sais"
__impl_desc__ = "Python wrapper around Yuta Mori's implementation of SA-IS suffix array construction."
__impl_type__ = "Suffix Array"

from index_interface import IndexTest
from sais_master.sais import Sequence
import sa_utils
import secondary_index

"""
Need to build/load the DLL into LIBC then install package before using
"""

class SuffixArrayTest(IndexTest):
	
	def __init__(self, corpus_str, defer_build=True, force_unicode=False, depth=11):
		"""

		"""
		if not corpus_str[-1] == '$':
			corpus_str += '$'

		self.force_unicode = force_unicode
		self.corpus_str = corpus_str if not self.force_unicode else unicode(corpus_str, 'utf-8', 'replace')
		self.depth = depth

		if not defer_build:
			self.build()
		else:
			self.lcp = None
			self.meta_index = None
	
	def build(self):
		"""

		"""
		seq = Sequence(self.corpus_str)

		suffix_array = seq.suffix_array[0: len(self.corpus_str)]
		self.meta_index = secondary_index.SecondaryIndex(self.corpus_str, suffix_array)

		self.lcp = seq.lcp_array[1: len(self.corpus_str)]

	def search(self, search_string):
		"""
		return: collection (list) int of offsets in original string where substring can be found
		"""
		if not self.meta_index or not self.lcp:
			raise ValueError
		else:
			search_string = search_string if not self.force_unicode else unicode(search_string, 'utf-8', 'replace')
			sa_i = self.meta_index.index_search(search_string)
			return sa_utils.lcp_scan(self.lcp, self.meta_index.suffix_array, search_string, sa_i) if sa_i >= 0 else []

	def supports_unicode(self):
		return True


if __name__ == "__main__":
	sais = SuffixArrayTest("fizz buzz bazz")
	sais.build()
	indices = sais.search("zz")

	print indices
	for i in indices:
		print i, "\t-\t", sais.corpus_str[i:]

	# # 12 	-	zz
	# # 7 	-	zz bazz
	# # 2 	-	zz buzz bazz