import json
from BenchmarkTools import random_substring, BenchmarkTaskInfo, run_benchmark
from sa_variants.simple_accel import SuffixArrayTest as SAV1
from sa_variants.super_accel import SuffixArrayTest as SAV2
from multiprocessing import Pool

if __name__ == "__main__":
	
	K = 1000
	M = K * 1000
	G = M * 1000
	DataDir = "/cygdrive/c/Users/vtsue_000/Documents/IPython Notebooks/IndexedSearchBenchmarks/"
	corpuses = ["corpus_genomic.txt"]
	
	sizes = [64 * K, 128 * K, 256 * K, 512 * K, 1 * M, 2 * M, 4 * M, 8 * M, 16 * M, 32 * M, 64 * M]
	lens = [50, 100, 250, 500, 1000, 2500, 5000]
	
	# Simple Accel testing
	tasks = []
	for corpus in corpuses:
		for s in sizes:
			for l in lens:
				task = BenchmarkTaskInfo(DataDir + corpus, SAV1, s, l, report_progress=True, do_output="result.sa_simple_accel.txt")
				tasks.append(task)

	# Super Accel testing
	for corpus in corpuses:
		for s in sizes:
			for l in lens:
				task = BenchmarkTaskInfo(DataDir + corpus, SAV2, s, l, report_progress=True, do_output="result.sa_super_accel.txt")
				tasks.append(task)
				
	pool = Pool(6)
	results = pool.map(run_benchmark, tasks)
	pool.close()
	pool.join()