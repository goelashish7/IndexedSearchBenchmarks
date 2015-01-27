__author__ = 'christopher'
import itertools
import numpy

def ceildiv(N, D):
	return -(-N // D)


def lcp(T, P, toff=0, start=0):
	end = min(len(T) - toff, len(P))

	for i in range(start, end):
		if T[i + toff] != P[i]:
			i -= 1
			break

	return i + 1


def simple_accelerant(corpus_str, sa, P, initL=0, initR=None):
	L = initL
	R = len(sa) - 1 if initR is None else initR

	l = lcp(corpus_str, P, toff=sa[L])
	r = lcp(corpus_str, P, toff=sa[R])

	while L != R:
		mlr = min(l, r)

		#M = ceildiv(R + L, 2)
		M = (R + L) // 2
		#m = lcp(corpus_str[sa[M]:], P, start=mlr)
		m = lcp(corpus_str, P, toff=sa[M], start=mlr)

		if m == len(P):
			return M
		elif P[m] > corpus_str[sa[M] + m]:
			L = M
			l = m
		else:
			R = M
			r = m

	return -1


def secondary_index(corpus_str, sa, size=11):
	# max prefix size supported by int mapping
	if size > 31:
		size = 31

	start = "A" * size
	start_int = kmer_to_int(start)
	end = "T" * size
	end_int = kmer_to_int(end)

	index_dict = {}
	for i in range(start_int, end_int):
		index_dict[i] = None

	for i in range(0, len(sa)):
		sa_i = sa[i]
		if sa_i > len(corpus_str) - size:
			continue

		key = kmer_to_int(corpus_str[sa_i:sa_i+size])
		if not key in index_dict:
			pass
		elif index_dict[key] is None:
			index_dict[key] = i

	return index_dict


def index_search(corpus_str, sa, P, meta_index, size=11):
	# max prefix size supported by int mapping
	if size > 31:
		size = 31

	index_key = P[0:size]
	index_int = kmer_to_int(index_key)

	start = 0
	end = len(sa) - 1

	if index_int in meta_index:
		start = meta_index[index_int]

	successor = index_int + 1
	if successor in meta_index:
		end = meta_index[successor]

	if not start:
		start = 0
	if not end:
		end = len(sa) - 1

	if end < start:
		print "start", index_key, sa[start], corpus_str[sa[start]:sa[start]+50]
		print "end", successor, sa[end], corpus_str[sa[end]:sa[end]+50]

	actual = simple_accelerant(corpus_str, sa, P, initL=start, initR=end)

	# print start, actual, end

	return actual

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


def kmer_to_int(kmer):
	translated = ""
	for c in kmer:
		translated += translation_table[c]

	return int(translated, base=4)


def int_to_kmer(num):
	intermediate = numpy.base_repr(num, base=4)

	kmer = ""
	for c in intermediate:
		kmer += translation_table[c]

	return kmer