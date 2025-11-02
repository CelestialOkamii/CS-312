from pathlib import Path
import time
import alignment

def read_sequence(file: Path) -> str:
    return ''.join(file.read_text().splitlines())

align_times = {}
for N in [100, 1000, 5000, 10000, 15000, 20000, 25000, 30000]:
    seq1 = read_sequence(Path('test_files/bovine_coronavirus.txt'))[:N]
    seq2 = read_sequence(Path('test_files/murine_hepatitus.txt'))[:N]
    start = time.time()
    score, aseq1, aseq2 = alignment.align(seq1, seq2, banded_width=2)
    end = time.time()
    align_times[N] = end - start
    print(N)
print(align_times)