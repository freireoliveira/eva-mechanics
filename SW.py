# -*- coding: utf-8 -*-

# Importing Python packages
from enum import IntEnum
import numpy as np
import re

# Assigning the constants for the scores
class Score(IntEnum):
    MATCH = 1
    MISMATCH = -1
    GAP = -1

# Assigning the constant values for the traceback
class Trace(IntEnum):
    STOP = 0
    LEFT = 1 
    UP = 2
    DIAGONAL = 3

# Implementing the Smith Waterman local alignment
def smith_waterman(seq1, seq2):
    # Generating the empty matrices for storing scores and tracing
    row = len(seq1) + 1
    col = len(seq2) + 1
    matrix = np.zeros(shape=(row, col), dtype=np.int)  
    tracing_matrix = np.zeros(shape=(row, col), dtype=np.int)  
    
    # Initialising the variables to find the highest scoring cell
    max_score = -1
    max_index = (-1, -1)
    
    # Calculating the scores for all cells in the matrix
    for i in range(1, row):
        for j in range(1, col):
            # Calculating the diagonal score (match score)
            match_value = Score.MATCH if seq1[i - 1] == seq2[j - 1] else Score.MISMATCH
            diagonal_score = matrix[i - 1, j - 1] + match_value
            
            # Calculating the vertical gap score
            vertical_score = matrix[i - 1, j] + Score.GAP
            
            # Calculating the horizontal gap score
            horizontal_score = matrix[i, j - 1] + Score.GAP
            
            # Taking the highest score 
            matrix[i, j] = max(0, diagonal_score, vertical_score, horizontal_score)
            
            # Tracking where the cell's value is coming from    
            if matrix[i, j] == 0: 
                tracing_matrix[i, j] = Trace.STOP
                
            elif matrix[i, j] == horizontal_score: 
                tracing_matrix[i, j] = Trace.LEFT
                
            elif matrix[i, j] == vertical_score: 
                tracing_matrix[i, j] = Trace.UP
                
            elif matrix[i, j] == diagonal_score: 
                tracing_matrix[i, j] = Trace.DIAGONAL 
                
            # Tracking the cell with the maximum score
            if matrix[i, j] >= max_score:
                max_index = (i,j)
                max_score = matrix[i, j]
    
    # Initialising the variables for tracing
    aligned_seq1 = ""
    aligned_seq2 = ""   
    current_aligned_seq1 = ""   
    current_aligned_seq2 = ""  
    (max_i, max_j) = max_index
    
    # Tracing and computing the pathway with the local alignment
    while tracing_matrix[max_i, max_j] != Trace.STOP:
        if tracing_matrix[max_i, max_j] == Trace.DIAGONAL:
            current_aligned_seq1 = seq1[max_i - 1]
            current_aligned_seq2 = seq2[max_j - 1]
            max_i = max_i - 1
            max_j = max_j - 1
            
        elif tracing_matrix[max_i, max_j] == Trace.UP:
            current_aligned_seq1 = seq1[max_i - 1]
            current_aligned_seq2 = '-'
            max_i = max_i - 1    
            
        elif tracing_matrix[max_i, max_j] == Trace.LEFT:
            current_aligned_seq1 = '-'
            current_aligned_seq2 = seq2[max_j - 1]
            max_j = max_j - 1
            
        aligned_seq1 = aligned_seq1 + current_aligned_seq1
        aligned_seq2 = aligned_seq2 + current_aligned_seq2
    
    # Reversing the order of the sequences
    aligned_seq1 = aligned_seq1[::-1]
    aligned_seq2 = aligned_seq2[::-1]

    gen_seq1 = list(aligned_seq1)
    gen_seq2 = list(aligned_seq2)
    gen_seq1 = ['\w' if item == '-' else item for item in gen_seq1]
    for i in range(len(gen_seq1)):
        if gen_seq1[i] != gen_seq2[i]:
            gen_seq1[i] =  '\w'
    gen_seq1 = ''.join(gen_seq1)

    match = re.search(f'{gen_seq1}', seq2)
    span = match.span()

    intermediate = list(aligned_seq2)
    for i in range(len(intermediate)):
        if aligned_seq1[i] != intermediate[i]:
            intermediate[i] = '*'
    intermediate = ''.join(intermediate)

    exception = range(span[0], span[1])
    changes_seq = []
    while i <= len(seq2):
        if i not in range(span[0], span[1]):
            changes_seq.append('*')
            i += 1
        else:
            changes_seq.append(intermediate)
            i = i + len(intermediate)
        #aligned_seq2 = f'{aligned_seq2}-'

    changes_seq = ''.join(changes_seq)

    return changes_seq