#!/usr/bin/env python3
import sys
import os
import math

def read_terms(index_dir):
    file_path = os.path.join(index_dir, 'sorted_terms.txt')
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            terms = f.read().split()
        return terms
    else:
        print(f"Error: File not found - {file_path}")
        sys.exit(1)

def read_documents(index_dir):
    file_path = os.path.join(index_dir, 'sorted_documents.txt')
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            documents = f.read().split()
        return documents
    else:
        print(f"Error: File not found - {file_path}")
        sys.exit(1)

def read_matrix(index_dir):
    file_path = os.path.join(index_dir, 'td_matrix.txt')
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            matrix = [list(map(int, line.split())) for line in f]
        return matrix
    else:
        print(f"Error: File not found - {file_path}")
        sys.exit(1)

def preprocess_query(query):
    # Converted the query to lowercase
    query = query.lower()

    # Tokenized the query and created a dictionary to store term frequencies
    query_terms = [term.strip() for term in query.split()]
    term_frequencies = {term: query_terms.count(term) for term in query_terms if term != '1'}

    return term_frequencies

def compute_similarity(query_vector, document_vector):
    # Computed the dot product of query_vector and document_vector
    dot_product = sum(query_vector[i] * document_vector[i] for i in range(len(query_vector)))

    # Computed the Euclidean lengths of the query and document vectors
    query_length = math.sqrt(sum(freq**2 for freq in query_vector))
    doc_length = math.sqrt(sum(freq**2 for freq in document_vector))

    # Avoided division by zero, returned 0.0 in such cases
    if query_length == 0 or doc_length == 0:
        return 0.0
    # Returned the rounded cosine similarity in float point format
    return round(dot_product / (query_length * doc_length), 4)

if __name__ == "__main__":
    # Checked for the correct number of command-line arguments
    if len(sys.argv) != 2:
        print("Usage: ./search.py <index_directory>")
        sys.exit(1)

    # Read the index directory from the command-line arguments
    index_directory = sys.argv[1]

    # Read the terms, documents and matrix from the index directory
    index_terms = read_terms(index_directory)
    index_documents = read_documents(index_directory)
    index_matrix = read_matrix(index_directory)

    # Read the query from systems standard inpuit
    query_lines = []
    for line in sys.stdin:
        query_lines.append(line.strip())
    query = " ".join(query_lines)

    # Initialized the query vector with zeros
    query_vector = [0] * len(index_terms)

    # Preprocessed the query and created the query vector
    query_term_frequencies = preprocess_query(query)
    for term, frequency in query_term_frequencies.items():
        # Checked if the term was in the index terms
        if term in index_terms:
            term_index = index_terms.index(term)
            query_vector[term_index] += frequency

    # Transposed the matrix, computed similarities and stored pairs: similarity, document name
    similarity_pairs = []
    matrix_transpose = [[] for _ in index_documents]

    for row in index_matrix:
        # Ensured the dimensions matched
        if len(row) == len(index_documents):
            for col_index in range(len(index_documents)):
                matrix_transpose[col_index].append(row[col_index])

    for document_index, document_vector in enumerate(matrix_transpose):
        # Computed the similarity between the query and each document
        similarity = compute_similarity(query_vector, document_vector)
        similarity_pairs.append((similarity, index_documents[document_index]))

    # Sorted pairs in descending order of components: similarity and document name
    similarity_pairs.sort(key=lambda x: (x[0], x[1]), reverse=True)

    # Print line to compare with expected output
    for similarity, document in similarity_pairs:
        print(f"{similarity:.5f} {document}")
