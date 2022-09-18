import random
import math
import time
from ete3 import Tree
import re
import os


class evolutionary_vector_architecture:
    def __init__(self, eva_seq, gentime=4, system_end=False):
        self.system_end = system_end
        self.eva_seq = eva_seq
        self.gentime = gentime

    def deletion(self, branch, mutation_site):
        branch =  list(branch)
        branch.pop(mutation_site)
        new_seq = ''.join(branch)

        return new_seq

    def insertion(self, branch, mutation_site):

        insertion_dict = {
            1 : 'A',
            2 : 'T',
            3 : 'C',
            4 : 'G',
        }

        nucleotide_index = random.randrange(1,5)
        nucleotide = insertion_dict[nucleotide_index]
        branch = list(branch)
        branch.insert(mutation_site, nucleotide)
        new_seq = ''.join(branch)

        return new_seq

    def transition(self, branch, mutation_site):

        transition_dict = {
            'A' : 'G',
            'G' : 'A',
            'C' : 'T',
            'T' : 'C',
        }

        branch = list(branch)
        old_nucleotide = branch[mutation_site]
        new_nucleotide = transition_dict[old_nucleotide]
        branch[mutation_site] = new_nucleotide
        new_seq = ''.join(branch)

        return new_seq

    def transversion(self, branch, mutation_site):

        chance = random.randrange(1,3)
        branch = list(branch)
        old_nucleotide = branch[mutation_site]
        if old_nucleotide == 'A' and chance == 1:
            new_nucleotide = 'T'
        elif old_nucleotide == 'A' and chance == 2:
            new_nucleotide = 'C'
        elif old_nucleotide == 'T' and chance == 1:
            new_nucleotide = 'G'
        elif old_nucleotide == 'T' and chance == 2:
            new_nucleotide = 'A'
        elif old_nucleotide == 'G' and chance == 1:
            new_nucleotide = 'T'
        elif old_nucleotide == 'G' and chance == 2:
            new_nucleotide = 'C'
        elif old_nucleotide == 'C' and chance == 1:
            new_nucleotide = 'G'
        elif old_nucleotide == 'C' and chance == 2:
            new_nucleotide = 'A'
        branch[mutation_site] = new_nucleotide
        new_seq = ''.join(branch)

        return new_seq

    def find_orf(self, branch):
        start_codon = 'AUG'
        stop_codons = ['UAA', 'UAG', 'UGA']

    def mutate(self, branch):
        if '\x1b' or 'X' not in branch:
            for number_of_mutations in range(int(len(branch) * 0.5)):
                mutation_site = int(random.randrange(len(branch)))

                mutation_dict = {
                    1 : self.transition(branch, mutation_site),
                    2 : self.transition(branch, mutation_site),
                    3 : self.transition(branch, mutation_site),
                    4 : self.transition(branch, mutation_site),
                    5 : self.transition(branch, mutation_site),
                    6 : self.transition(branch, mutation_site),
                    7 : self.transversion(branch, mutation_site),
                    8 : self.transversion(branch, mutation_site),
                    9 : self.insertion(branch, mutation_site),
                    10 : self.deletion(branch, mutation_site)
                }

                num = int(random.randrange(1,11))
                branch = mutation_dict[num]
        
            return branch
        else:
            return branch

    def tree_maker(self, babies, gen, tree, gene_pool, fission):
        start = 0
        end = 2
        node_list = []
        for start in range(0, len(babies), 2):
            node = str(babies[start:end]).replace('[', '(*').replace(']', ')').replace("'", "").replace(", ", ", *")
            end = end + 2
            node_list.append(node)
        tree = list(tree)
        node_index = 0
        for i in range(len(tree)):
            if tree[i] == '*':
                tree[i] = node_list[node_index]
                node_index += 1

        tree = ''.join(tree)

        tree, bad_seq, gene_pool, end_point = self.natural_selection(tree, gene_pool, fission)
        working_tree = f'{tree};'.replace('*', '')
        while re.search(r'\(\*?X\w*?, \*?X\w*?\)X', working_tree):
            to_replace = re.findall(r'\(\*?X\w*?, \*?X\w*?\)X', working_tree)
            working_tree = working_tree.replace(to_replace[0], 'X')
            #working_tree = working_tree.replace('XX', 'X')
        t = Tree(working_tree, format=1)
        growth = 2**gen
        end = end + growth + growth
        start = start + growth
        
        aesthetic_tree = t.get_ascii(show_internal=True)
        return tree, aesthetic_tree, gene_pool, bad_seq, end_point

    def natural_selection(self, tree, gene_pool, fission):
        fresh_leaves = re.findall(r'\*\w*', tree)
        if len(fresh_leaves) >= 4:
            gene_pool[len(gene_pool) - fission:] = fresh_leaves
            random_leaf = str(fresh_leaves[random.randrange(len(fresh_leaves))]).replace('*', '')
            while random_leaf == 'X':
                random_leaf = str(fresh_leaves[random.randrange(len(fresh_leaves))]).replace('*', '')
            bad_seq_size = int(len(random_leaf) * 0.45)
            start = random.randrange(len(random_leaf)-bad_seq_size)
            bad_seq = random_leaf[start:start+bad_seq_size]

            replace_dict = {}
            for leaf in fresh_leaves:
                if bad_seq in leaf:
                    #replace_dict[leaf] = ('\x1b[9m'.join(leaf) + '\x1b[0m').replace('*', '')
                    replace_dict[leaf] = '*X'
                else:
                    replace_dict[leaf] = leaf

            to_replace = list()
            for key in replace_dict:
                if key in tree:
                    to_replace.append(key)
            for replacement in to_replace:
                tree = tree.replace(replacement, replace_dict[replacement])
                gene_pool = [replace_dict[replacement] if item == replacement else item for item in gene_pool]
            #gene_pool.remove('X')
            gene_pool = [gene.replace('*', '') if '*' in gene else gene for gene in gene_pool]
        else:
            bad_seq = 'Nenhuma'

        clean = tree.replace('*', '')
        end_point = list(set(re.findall(r'\(\w*, \w*\)', clean)))
        return tree, bad_seq, gene_pool, end_point


    def life(self):
        fission = 1
        gene_pool = [self.eva_seq]
        start_time = time.time()
        seconds = self.gentime
        generation = 0
        absolute_time = 0
        index = 0
        tree = f'*{self.eva_seq}'
        working_tree = f'{tree};'.replace('*', '')
        t = Tree(working_tree, format=1)
        print(t)

        #while absolute_time <= self.max_evolution_time:
        try:

            while self.system_end == False:
                current_time = time.time()
                elapsed_time = current_time - start_time

                if elapsed_time >= seconds:
                    absolute_time = absolute_time + elapsed_time
                    generation += 1
                    gen = 0
                    while gen < generation:
                        seq = gene_pool[index]               
                        bipartitioned = tuple([seq]*2)

                        branch1, branch2 = bipartitioned
                        #branch1 = self.mutate(branch1)
                        branch2 = self.mutate(branch2)
                        gene_pool.append(branch1)
                        gene_pool.append(branch2)
                        fission += 1
                        index += 1
                        gen = int(math.log2(fission))

                    start_time = time.time()
                    babies = gene_pool[len(gene_pool) - fission:]
                    tree, aesthetic_tree, gene_pool, bad_seq, end_point = self.tree_maker(babies, gen, tree, gene_pool, fission)
                    os.system('clear')
                    print(f'Sequência deletéria: {bad_seq}')
                    print(aesthetic_tree)
                    if (len(end_point) == 1 and end_point[0] == '(X, X)'):
                        self.system_end = True


        except KeyboardInterrupt:
            pass

                #print(f'Geração {gen}:\n{babies} - (2**{gen}={len(babies)} indivíduos)')

        
        return gene_pool, generation
    
