#%%
from eva import evolutionary_vector_architecture as eva
import random
import itertools as itools
import os
import sys

def args():
    get_gen = 4
    for idx, arg in enumerate(sys.argv):
        if arg in ('--gentime' or '-g'):
            get_gen = int(sys.argv[idx + 1])

    return get_gen

def eva_sequence_generator():
    seq_size = random.randrange(8, 11)
    all_possible = list(itools.product('ATCG', repeat=seq_size))
    all_possible = [''.join(x) for x in all_possible]
    seq_index_picker = random.randrange(len(all_possible)+1)
    eva_seq = all_possible[seq_index_picker]
    return eva_seq

def main():
    gentime = args()
    os.system('clear')
    eva_seq = eva_sequence_generator()
    eva_object = eva(eva_seq, gentime=gentime)
    pool, generations = eva_object.life()
    print(f'\n{generations - 1} gerações bem-sucedidas')

if __name__ == '__main__':
    main()
