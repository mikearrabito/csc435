# Michael Arrabito - CSC 435 - Lab 2
# Huffman coding

import heapq


class Node:
    def __init__(self, char, freq):
        self.left = None
        self.right = None
        self.char = char
        self.freq = freq

    def __eq__(self, other):
        return self.freq == other.freq

    def __lt__(self, other):
        return self.freq < other.freq

    def __gt__(self, other):
        return self.freq > other.freq


"""
Recursive function to traverse our constructed tree and print the Huffman code,
when we make a call to go left we add a 0 to the string and 1 for right
Once we reach a leaf we are done and we print the character and code created
"""
def printhuffmancode(node, s):
    if(node.left is None) and (node.right is None):
        # We are at a leaf, time to print code and character
        print(node.char + " : " + s)
        return
    printhuffmancode(node.left, s + "0")
    printhuffmancode(node.right, s + "1")


# Given data from assignment:
# alphabet X = {x1, x2, x3, x4, x5, x6, x7, x8, x9} with corresponding probabilities,
# P = {0.2, 0.15, 0.13, 0.12, 0.1, 0.09, 0.08, 0.07, 0.06}
symbols = {0.2: "x1",  0.15: "x2",  0.13: "x3",  0.12: "x4",
           0.1: "x5",  0.09: "x6",  0.08: "x7",  0.07: "x8", 0.06: "x9"}

"""
(Using this algorithm - https://www.geeksforgeeks.org/huffman-coding-greedy-algo-3/):
1. Create a leaf node for each unique character and build a min heap of all leaf nodes (Min Heap is used as a priority queue.
 The value of frequency field is used to compare two nodes in min heap. Initially, the least frequent character is at root)
2. Extract two nodes with the minimum frequency from the min heap.
3. Create a new internal node with a frequency equal to the sum of the two nodes frequencies. 
Make the first extracted node as its left child and the other extracted node as its right child. Add this node to the min heap.
4. Repeat steps#2 and #3 until the heap contains only one node. The remaining node is the root node and the tree is complete.
"""

nodes = list()
for sym in symbols:
    nodes.append(Node(symbols[sym], sym))

# Constructing min-heap
heapq.heapify(nodes)
# Now we have characters in heap with min frequency guaranteed to be seen first when popped

root = Node("root", 0)

while len(nodes) > 2:
    newnode = Node("n/a", 0)
    newnode.left = heapq.heappop(nodes)
    newnode.freq = newnode.left.freq
    newnode.right = heapq.heappop(nodes)
    newnode.freq += newnode.right.freq
    # Pushing internal node into min heap which has sum of 2 lower nodes
    heapq.heappush(nodes, newnode)

    if len(nodes) == 2:
        root.left = nodes[0]
        root.right = nodes[1]
        root.freq = root.left.freq + root.right.freq


# Now we have a constructed Huffman coding tree with "root" as the handle to the tree

printhuffmancode(root, "")