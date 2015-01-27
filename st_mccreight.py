__impl_name__ = "Suffix Tree McCreight"
__impl_author__ = "Che-Liang Chiou"
__impl_url__ = "http://wizardry-and-studies.blogspot.com/2005/12/mccreights-algorithm-of-building.html"
__impl_desc__ = "McCreight's Algorithm of Building Suffix Tree"
__impl_type__ = "Suffix Tree"


from index_interface import IndexTest
import impl_st_mccreight as stm


class STMcCreightTest(IndexTest):
	
	def __init__(self, corpus_str, defer_build=True, force_unicode=False):
		"""

		"""
		if not corpus_str[-1] == '$':
			corpus_str += '$'
			
		self.force_unicode = force_unicode
		self.corpus_str = corpus_str
		#self.corpus_str = corpus_str if type(corpus_str) is unicode else unicode(corpus_str, 'utf-8', 'replace')
		
		if not defer_build:
			self.build()
		else:
			self.idx = None
	
	def build(self):
		"""

		"""
		self.struct = stm.buildTree(self.corpus_str)

	def search(self, search_string):
		"""
		return: collection (list) int of offsets in original string where substring can be found
		"""
		#try:
		search_string = search_string
		#except:
		#	print search_string
		#	raise ValueError()
		return stm.searchTree(self.struct, search_string)
		
	def supports_unicode(self):
		return True

fmt = STMcCreightTest("fizz buzz bazz")
fmt.build()
indices = fmt.search("zz")
print indices
for i in indices:
	print i, "\t-\t", fmt.corpus_str[i:]

# 12 	-	zz
# 7 	-	zz bazz
# 2 	-	zz buzz bazz