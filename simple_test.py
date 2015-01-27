import random
import time
import math
import sys

import st_test_wrapped
import sa_variants.naive as naive
import sa_variants.simple_accel as accel
import sa_variants.super_accel as super_accel
import sa_variants.index_accelerant as secondary


def random_string(len, chars=['A', 'C', 'G', 'T']):
	return "".join(random.choice(chars) for i in range(0, len))

if __name__ == "__main__":
	pattern_length = 5000
	num_searches = 10000

	text_lens = [int(64e3), int(128e3), int(256e3), int(1e6), int(4e6)]  # int(256e6)]
	texts = []

	for text_len in text_lens:
		texts.append(random_string(text_len))

	implementations = {	#"suffix array (naive)": naive.SuffixArrayTest,
						#"suffix array (simple accel)": accel.SuffixArrayTest,
						"suffix array (super accel)": super_accel.SuffixArrayTest,
						"suffix array (secondary index)": secondary.SuffixArrayTest}
	for text in texts:
		pattern_indices = [random.randint(0, len(text) - pattern_length) for i in range(0, num_searches)]
		patterns = [text[i:i+pattern_length] for i in pattern_indices]

		print "=== Running all tests for genomic string of length {0}".format(len(text))

		for name, implementation in implementations.iteritems():
			print "\n{0}".format(name)

			structure = implementation(text)

			start_time = time.clock()
			structure.build()
			end_time = time.clock()
			print "CPU time for {0} build: {1}".format(name, end_time - start_time)

			failed = []
			start_time = time.clock()
			for pattern_index, pattern in zip(pattern_indices, patterns):
				found = structure.search(pattern)

				if not pattern_index in found:
					failed.append(pattern_index)
			end_time = time.clock()
			print "CPU time for {0} search: {1}".format(name, end_time - start_time)
			if len(failed) > 0:
				print "{0} search failed: missing {1} patterns".format(name, len(failed))



