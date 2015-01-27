
def ceildiv(N, D):
	"""
	integer division, with ceiling rather than floor
	"""
	return -(-N // D)


def lcp(T, P, toff=0, start=0):
	"""
	given two strings T and P, determine the number of shared characters
	between T[start+toff:] and P[start:]
	"""
	end = min(len(T) - toff, len(P))

	for i in range(start, end):
		if T[i + toff] != P[i]:
			i -= 1
			break

	return i + 1


def simple_accelerant(corpus_str, sa, P, initL=0, initR=None):
	"""
	perform binary search on the suffix array sa to locate pattern P in corpus_str

	track and store LCP of left and right binary search bounds to minimize repeated comparisons
	"""
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


def binary_search(original_string, suffix_array, search_string):
	"""
	adapted: http://nbviewer.ipython.org/gist/BenLangmead/6765182
	author: Ben Langmead
	license: ???

	from class slides

	naive binary search of suffix_array for pattern search_string in original_string
	"""
	assert original_string[-1] == '$'  # t already has terminator

	if len(original_string) == 1:
		return [1]

	l, r = 0, len(original_string)  # invariant: sa[l] < p < sa[r]

	while True:
		c = (l + r) // 2
		# determine whether p < T[sa[c]:] by doing comparisons
		# starting from left-hand sides of p and T[sa[c]:]
		plt = True  # assume p < T[sa[c]:] until proven otherwise
		i = 0
		while i < len(search_string) and suffix_array[c]+i < len(original_string):
			if search_string[i] < original_string[suffix_array[c]+i]:
				break  # p < T[sa[c]:]
			elif search_string[i] > original_string[suffix_array[c]+i]:
				plt = False
				break  # p > T[sa[c]:]
			i += 1  # tied so far
		if plt:
			if c == l + 1:
				return c
			r = c
		else:
			if c == r - 1:
				return r
			l = c

	return -1


def lcp_binary_search(original_string, suffix_array, lcp, search_string):
	"""

	"""

	lcp_l, lcp_r = create_lcplr(lcp)
	return super_accelerant(original_string, suffix_array, search_string, lcp_l, lcp_r)


def super_accelerant(original_string, suffix_array, search_string, lcp_l, lcp_r):
	"""
	perform binary search on suffix_array to locate pattern search_string in original_string

	utilize precomputed LCPs for left and right binary search boundaries to eliminate redundant comparisons entirely
	"""
	assert original_string[-1] == '$'  # t already has terminator
	
	p = len(search_string)
	n = len(original_string)
	l, r = 0, n  # invariant: sa[l] < p < sa[r]
	i, lcpl, lcpr = 0, 0, 0
	
	while r - l > 1:
		c = (l + r) // 2
		
		if lcpr > lcpl:
			if lcpr < lcp_r[c-1]:
				r = c
				continue
			elif lcpr > lcp_r[c-1]:
				l = c
				continue
		elif lcpl > lcpr:
			if lcpl < lcp_l[c-1]:
				l = c
				continue
			elif lcpl > lcp_l[c-1]:
				r = c
				continue

		
		while i < p and suffix_array[c]+i < n:
			if search_string[i] == original_string[suffix_array[c]+i]:
				i += 1 
			elif search_string[i] < original_string[suffix_array[c]+i]:
				r = c
				lcpr = i
				break 
			else:
				l = c
				lcpl = i
				break

		if i == p:
			return c
				
	return -1


def create_lcp(first, second):
	"""
	calculate the least common prefix of two strings
	"""

	i = 0
	while i < len(first) and i < len(second) and first[i] == second[i]:
		i += 1
	return i


def create_lcplr(lcp1):
	"""
	adapted: http://nbviewer.ipython.org/gist/BenLangmead/6783863
	author: Ben Langmead
	license: ???

	from class slides

	recursively compute lcp l and r from original lcp array (lcp1)
	"""
	llcp, rlcp = [None] * len(lcp1), [None] * len(lcp1)
	lcp1 += [0]

	def precomputeLcpsHelper(l, r):
		if l == r-1: return lcp1[l]
		c = (l + r) // 2
		llcp[c-1] = precomputeLcpsHelper(l, c)
		rlcp[c-1] = precomputeLcpsHelper(c, r)
		return min(llcp[c-1], rlcp[c-1])

	precomputeLcpsHelper(0, len(lcp1))
	return llcp, rlcp


def naive_scan(suffix_array, original_string, search_str, sa_i):
	"""
	from a given index in the suffix array where a match is known to occur, and the length of the search string,
		search forwards and backwards for additional starting indices utilizing the LCP array.
	notice that if two suffixes share a prefix of length >= the length of the search string, if at least one of them
		matches the search string, then both match the search string.

	preconditions:
		original_string is the string the suffix array was constructed from
		suffix_array is the correct suffix array of the original string
		sa_i is the index of a proper match for the search_str in the suffix array
		search_str is a prefix of suffix_array[sa_i]
	return: collection (list) of indices which match the search string, assuming correct parameters
	"""
	indices = [suffix_array[sa_i]]

	sa_j = sa_i - 1
	while sa_j >= 0:
		j = suffix_array[sa_j]
		if original_string[j:j+len(search_str)] == search_str:
			indices.append(j)
			sa_j -= 1
		else:
			break

	sa_j = sa_i + 1
	while sa_j < len(suffix_array):
		j = suffix_array[sa_j]
		if original_string[j:j+len(search_str)] == search_str:
			indices.append(j)
			sa_j += 1
		else:
			break

	return indices


def lcp_scan(lcp, suffix_array, search_str, sa_i):
	"""
	from a given index in the suffix array where a match is known to occur, and the length of the search string,
		search forwards and backwards for additional starting indices utilizing the LCP array.
	notice that if two suffixes share a prefix of length >= the length of the search string, if at least one of them
		matches the search string, then both match the search string.

	preconditions:
		lcp contains the LCP array, where lcp[i] = the length of the matching prefix of sa[i] and sa[i+1]
		suffix_array is the correct suffix array of the original string
		sa_i is the index of a proper match for the search_str in the suffix array
		search_str is the same length as that matching string
	return: collection (list) of indices which match the search string, assuming correct parameters
	"""
	indices = [suffix_array[sa_i]]
	sa_j = sa_i - 1
	while sa_j > 0 and lcp[sa_j] >= len(search_str) :
		indices.append(suffix_array[sa_j])
		sa_j -= 1
	sa_j = sa_i
	while sa_j < len(lcp) and lcp[sa_j] >= len(search_str):
		indices.append(suffix_array[sa_j + 1])
		sa_j += 1
		
	return indices