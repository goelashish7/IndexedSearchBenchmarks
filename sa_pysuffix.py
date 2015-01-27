
__impl_name__ = "Suffix Array 1"
__impl_author__ = "rbrix..., fchapl..., cyril.ba... @gmail.com"
__impl_url__ = "https://code.google.com/p/pysuffix/"
__imp_desc__ = "a python implementation for efficient augmented suffix array construction (Karkkainen Sanders)."
__impl_type__ = "Suffix Array"

from index_interface import IndexTest
import sa_utils

import impl_pysuffix_kark_sanders as tks


class SuffixArrayTest(IndexTest):
	
	# 
	def __init__(self, corpus_str, defer_build=True, force_unicode=False):
		if not corpus_str[-1] == '$':
			corpus_str += '$'

		self.force_unicode = force_unicode
		self.corpus_str = corpus_str if not self.force_unicode else unicode(corpus_str, 'utf-8', 'replace')

		if not defer_build:
			self.build()
		else:
			self.sa = None

	#
	def build(self):
		self.sa = tks.simple_kark_sort(self.corpus_str)
		self.sa = self.sa[0: len(self.corpus_str)]
	
	# return: list int of offsets in original string where substring can be found
	def search(self, search_string):
		search_string = unicode(search_string)
		if not self.sa:
			raise ValueError
		else:
			search_string = search_string if not self.force_unicode else unicode(search_string, 'utf-8', 'replace')

			sa_i = sa_utils.binary_search(self.corpus_str, self.sa, search_string)
			return sa_utils.naive_scan(self.sa, self.corpus_str, search_string, sa_i) if sa_i >= 0 else []

	def supports_unicode(self):
		return True


if __name__ == "__main__":
	sat = SuffixArrayTest("fizz buzz bazz")
	sat.build()
	indices = sat.search("zz")
	trunc_len = 50

	for i in indices:
		print "index: {0}\t-\t{1}...".format(i, sat.corpus_str[i:i+trunc_len])