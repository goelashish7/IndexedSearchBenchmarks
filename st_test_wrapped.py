
"""
requires suffix_tree Python module from:
http://www.dcs.bbk.ac.uk/~dell/code/suffix_tree_unicode.zip
http://researchonsearch.blogspot.com/2010/05/suffix-tree-implementation-with-unicode.html

extract and build/install with python setup.py install

authors: Thomas Mailund, Dell Zhang (added unicode support)
"""

from suffix_tree import SuffixTree
from index_interface import IndexTest

class SuffixTreeTest(IndexTest):
	def __init__(self, corpus_str, defer_build=True, force_unicode=False):
		if force_unicode:
			return ValueError("Wrapped Suffix Tree implementation does not support unicode")

		# This implementation handles the terminal symbol for us
		# remove, rather than append
		while corpus_str[-1] == '$':
			corpus_str = corpus_str[:-1]

		# this implementation not only supports unicode, but it REQUIRES it
		self.corpus_str = corpus_str

		if not defer_build:
			self.build()
		else:
			self.suffix_tree = None

	def build(self):
		self.suffix_tree = SuffixTree(self.corpus_str)

	"""
	def search(self, search_string):
		current_node = self.suffix_tree.root
		current_child = current_node.firstChild

		index = 0
		while not current_child is None:
			if index >= len(search_string):
				break

			cmplen = min(len(current_child.edgeLabel), len(search_string) - index)
			if search_string[index:index+cmplen] == current_child.edgeLabel[0:cmplen]:
				current_node = current_child
				current_child = current_node.firstChild
				index += cmplen
			# edge matches search string, follow and continue search
			else:
				current_child = current_child.next

		if len(current_node.pathLabel) >= len(search_string):
			indices = set()
			self.dfs(current_node, indices)
			return indices

		return set()
	"""

	def dfs(self, tree_node, indices):
		indices.add(tree_node.index)

		current_child = tree_node.firstChild
		while not current_child is None:
			self.dfs(current_child, indices)
			current_child = current_child.next

	def search(self, pattern):
		# loc = set()

		current_node = self.suffix_tree.root
		pattern_offset = 0

		pattern_len = len(pattern)

		while pattern_offset < pattern_len and current_node is not None:
			current_child = current_node.firstChild

			while current_child is not None:
				child_label_len = len(current_child.edgeLabel)
				if current_child.edgeLabel[0] == pattern[pattern_offset]:
					k = min(child_label_len, pattern_len - pattern_offset)

					if current_child.edgeLabel[:k] == pattern[pattern_offset:pattern_offset+k]:
						pattern_offset = pattern_offset + child_label_len
						current_node = current_child
					else:
						current_node = None
					break
				current_child = current_child.next
			else:
				current_node = None

		if current_node is None:
			return []
		else:
			# loc.add(len(self.corpus_str) - find_all(current_node, loc).path_len())
			return [current_node.index]

	def supports_unicode(self):
		return False

if __name__ == "__main__":
	text_len = int(2e3)
	st = SuffixTreeTest("banana")
	st.build()
	for i in st.search("ana"):
		print("{0}:\t{1}".format(i, st.corpus_str[i:]))