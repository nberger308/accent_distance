import os
import re
import numpy as np
import itertools

# citation: https://github.com/closetothe/levenshtein/blob/master/levenshtein.py

def get_phone_set(inpath):
    """
    Extracts a set of unique phones (symbols) from the input file.

    Parameters:
    inpath (str): Path to the input file containing phones.

    Returns:
    set: A set of unique phones extracted from the file.
    """
    phone_set = set()
    with open(inpath, 'r') as infile:
        for line in infile:
            phone = re.split(r'[ \t]', line, maxsplit=1)[0]
            phone_set.add(phone)
    return phone_set

def tokenize_by_phone_set(input_text, phone_pattern):
    """
    Tokenizes the input text based on a given phone set pattern.

    Parameters:
    input_text (str): The text to tokenize.
    phone_pattern (re.Pattern): A compiled regular expression pattern of phones.

    Returns:
    list: A list of tokens matching the phone set pattern.
    """
    return phone_pattern.findall(input_text)

def remove_duplicates_preserve_order(lst):
    """
    Removes duplicates from a list while preserving the original order.

    Parameters:
    lst (list): The input list with potential duplicates.

    Returns:
    tuple: A list of unique elements and their original indices.
    """
    seen = set()
    result = []
    indices = []

    for i, word in enumerate(lst):
        if word not in seen:
            seen.add(word)
            result.append(word)
            indices.append(i)

    return result, indices

def levenshtein(a, b, ratio=True, print_matrix=False):
    """
    Computes the Levenshtein distance between two sequences.

    Parameters:
    a (str): First sequence (e.g., string or tokenized list).
    b (str): Second sequence.
    ratio (bool): Whether to return the ratio similarity (default) or the distance.
    print_matrix (bool): If True, prints the Levenshtein matrix.

    Returns:
    float: Levenshtein similarity ratio or distance.
    """
    n, m = len(a), len(b)
    lev = np.zeros((n+1, m+1))

    if n == 0 and m == 0:
        return 1.0 if ratio else 0
    if n == 0:
        return m if not ratio else 0.0
    if m == 0:
        return n if not ratio else 0.0

    for i in range(n+1):
        lev[i, 0] = i
    for j in range(m+1):
        lev[0, j] = j

    for i in range(1, n+1):
        for j in range(1, m+1):
            insertion = lev[i-1, j] + 1
            deletion = lev[i, j-1] + 1
            substitution = lev[i-1, j-1] + (1 if a[i-1] != b[j-1] else 0)
            lev[i, j] = min(insertion, deletion, substitution)

    if print_matrix:
        print(lev)

    return (n + m - lev[n, m]) / (n + m) if ratio else lev[n, m]
    

def compare_text_files(file_a, file_b):
    """
    Compares two text files, tokenizes their content based on a phone set, and calculates their average Levenshtein similarity.

    Parameters:
    file_a (str): Path to the first file.
    file_b (str): Path to the second file.

    Returns:
    float: The average Levenshtein similarity between the tokenized content of the two files.
    """
    with open(file_a, 'r') as fa, open(file_b, 'r') as fb:
        accent1 = fa.read().replace("_BB", "_B")
        accent2 = fb.read().replace("_BB", "_B")

        acc1_words = re.split(r'\+|_B', '_B'.join(accent1.splitlines()))
        acc2_words = re.split(r'\+|_B', '_B'.join(accent2.splitlines()))

        acc1_unique, indices = remove_duplicates_preserve_order(acc1_words)
        acc2_unique, _ = remove_duplicates_preserve_order(acc2_words)

        acc1_tokenized = [tokenize_by_phone_set(word, phone_pattern) for word in acc1_unique]
        acc2_tokenized = [tokenize_by_phone_set(acc2_words[i], phone_pattern) for i in indices]

        print(f"acc1 number of words: {len(acc1_words)}")
        print(f"acc2 number of words: {len(acc2_words)}")
        print(f"acc1 length after tokenization: {len(acc1_tokenized)}")
        print(f"acc2 length after tokenization: {len(acc2_tokenized)}")

        with open('acc1_out.txt', 'w') as out1, open('acc2_out.txt', 'w') as out2:
            for word in acc1_tokenized:
                out1.write(''.join(word) + '\n')
            for word in acc2_tokenized:
                out2.write(''.join(word) + '\n')

        running_averages = sum(levenshtein(w1, w2) for w1, w2 in zip(acc1_tokenized, acc2_tokenized))
        return running_averages / len(acc1_tokenized)

# Load phone set and compile regex pattern
phone_set = get_phone_set('/path/to/tgt.vocab') # replace path
phone_set_sorted = sorted(phone_set, key=len, reverse=True)
phone_pattern = re.compile(r'|'.join(re.escape(phone) for phone in phone_set_sorted))

# Compare files in the directory
directory =  '/path/to/directory' # replace path
candidate_files = [os.path.join(directory, f) for f in os.listdir(directory) if 'SYLLS' in f]
file_pairs = itertools.combinations(candidate_files, 2)

with open('difference_scores.txt', 'w') as diff_file:
    for file1, file2 in file_pairs:
        print(f"Comparing {os.path.basename(file1)} vs {os.path.basename(file2)}")
        diff = compare_text_files(file1, file2)
        diff_file.write(f"{os.path.basename(file1)} vs {os.path.basename(file2)}: {diff}\n")
