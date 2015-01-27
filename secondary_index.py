
import sys
import numpy
import sa_utils


class SecondaryIndex:
	"""

	"""

	def __init__(self, corpus_str, suffix_array, size=None):
		global max_size
		if size is None:
			binary_search_steps = numpy.log2(len(suffix_array))
			to_reduce = binary_search_steps - 6.0
			size = int(numpy.ceil(to_reduce / 2.0))

		self.depth = min(size, max_size)
		print "index depth", self.depth
		self.suffix_array = suffix_array
		self.corpus_str = corpus_str
		self.index_dict = self.build_index()
		self.lower_bound = None
		self.upper_bound = None

	def build_index(self):
		start = "A" * self.depth
		self.lower_bound = self.kmer_to_int(start)
		end = "T" * self.depth
		self.upper_bound = self.kmer_to_int(end)

		index_dict = {}

		for i in range(0, len(self.suffix_array)):
			sa_i = self.suffix_array[i]
			if sa_i > len(self.corpus_str) - self.depth:
				continue

			key = self.kmer_to_int(self.corpus_str[sa_i:sa_i+self.depth])
			if not key in index_dict:
				index_dict[key] = i

		return index_dict

	def index_search(self, pattern):
		padding = self.depth - len(pattern)
		if padding > 0:
			start_key = pattern + ("A" * padding)
			start_int = self.kmer_to_int(start_key) - 1

			end_key = pattern + ("T" * padding)
			end_int = self.kmer_to_int(end_key) + 1
		else:
			start_key = pattern[0:self.depth]
			start_int = self.kmer_to_int(start_key)

			end_int = start_int + 1

		while not start_int in self.index_dict and start_int >= self.lower_bound:
			start_int -= 1
		start = self.index_dict[start_int] if start_int in self.index_dict else 0

		while not end_int in self.index_dict and end_int <= self.upper_bound:
			end_int += 1
		end = self.index_dict[end_int] if end_int in self.index_dict else len(self.suffix_array) - 1

		return sa_utils.simple_accelerant(self.corpus_str, self.suffix_array, pattern, initL=start, initR=end)

	translation_table = {
		"A": "0",
		"0": "A",
		"C": "1",
		"1": "C",
		"G": "2",
		"2": "G",
		"T": "3",
		"3": "T",
		"$": ""
		}

	@staticmethod
	def kmer_to_int(kmer):
		translated = ""
		for c in kmer:
			translated += SecondaryIndex.translation_table[c]

		return int(translated, base=4)

	@staticmethod
	def int_to_kmer(num):
		intermediate = numpy.base_repr(num, base=4)

		kmer = ""
		for c in intermediate:
			kmer += SecondaryIndex.translation_table[c]

		return kmer

max_kmer = SecondaryIndex.int_to_kmer(sys.maxint)
max_size = len(max_kmer) - 1