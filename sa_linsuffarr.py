
__impl_name__ = "Suffix Array 2"
__impl_author__ = "Julien Gosme <Julien.Gosme@unicaen.fr>"
__impl_url__ = "http://www.gosme.org/Linsuffarr.html"
__imp_desc__ = "performs the linear construction of the suffix array "
__impl_type__ = "Suffix Array"

from index_interface import IndexTest
import impl_linsuffarr_kark_sanders as lsa


class SuffixArrayTest(IndexTest):
	
	# 
	def __init__(self, corpus_str, defer_build=True, force_unicode=False):
		if not corpus_str[-1] == '$':
			corpus_str += '$'

		self.force_unicode = force_unicode
		self.corpus_str = corpus_str if (not self.force_unicode) or isinstance(corpus_str, unicode) else unicode(corpus_str, 'utf-8', 'replace')

		if not defer_build:
			self.build()
		else:
			self.sa = None

	#
	def build(self):
		self.sa = lsa.SuffixArray(self.corpus_str.encode('utf-8'), unit=lsa.UNIT_CHARACTER)
	
	# return: list int of offsets in original string where substring can be found
	def search(self, search_string):
		if not self.sa:
			raise ValueError
		else:
			return self.sa.find(search_string.encode('utf-8'))

	def supports_unicode(self):
		return True

if __name__ == "__main__":
	sat = SuffixArrayTest("fizz buzz bazz")
	sat.build()
	indices = sat.search("zz")
	trunc_len = 50

	for i in indices:
		print "index: {0}\t-\t{1}...".format(i, sat.corpus_str[i:i+trunc_len])