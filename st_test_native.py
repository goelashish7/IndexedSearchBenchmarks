__impl_name__ = "Suffix Tree Ukkonen"
__impl_author__ = "kvh <kvh - http://kenvanharen.com/>"
__impl_url__ = "https://github.com/kvh/Python-Suffix-Tree/blob/master/suffix_tree.py l"
__impl_desc__ = "Ukkonen's Algorithm of Building Suffix Tree"
__impl_type__ = "Suffix Tree"

from impl_suffix_tree import SuffixTree
from index_interface import IndexTest

class SuffixTreeTest(IndexTest):
	def __init__(self, corpus_str, defer_build=True, force_unicode=False):
		if not corpus_str[-1] == '$':
			corpus_str += '$'

		self.force_unicode = force_unicode
		self.corpus_str = corpus_str if not self.force_unicode else unicode(corpus_str, 'utf-8', 'replace')

		if not defer_build:
			self.build()
		else:
			self.suffix_tree = None

	def build(self):
		self.suffix_tree = SuffixTree(self.corpus_str)

	def search(self, search_string):
		search_string = search_string if not self.force_unicode else unicode(search_string, 'utf-8', 'replace')
		# problem, only returns single index. how to return all?
		return [self.suffix_tree.find_substring(search_string)]

	def supports_unicode(self):
		return True


if __name__ == "__main__":
	st = SuffixTreeTest("fizz buzz bazz")
	st.build()
	for i in st.search("zz"):
		print("{0}:\t{1}".format(i, st.corpus_str[i:]))