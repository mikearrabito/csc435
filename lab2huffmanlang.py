# Michael Arrabito - CSC 435 - Lab 2
# Huffman coding - Part 2 - English alphabet

import heapq
import math


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
Data from assignment:
A	0.0642	B	0.0127	C   0.0218
D	0.0317	E	0.1031	F	0.0208
G	0.0152	H	0.0467	I	0.0575
J	0.0008	K	0.0049	L	0.0321
M	0.0198	N	0.0574	O	0.0632
P	0.0152	Q	0.0008	R	0.0484
S	0.0514	T	0.0796	U	0.0228
V	0.0083	W	0.0175	X	0.0013
Y	0.0164	Z	0.0005	Space	0.1859
"""

symbols = {0.0642: "A",  0.0127: "B",  0.0218: "C",  0.0317: "D",
           0.1031: "E",  0.0208: "F",  0.0152: "G",  0.0467: "H", 0.0575: "I",
           0.0008: "J", 0.0049: "K", 0.0321: "L", 0.0198: "M",
           0.0574: "N", 0.0632: "O", 0.0152: "P", 0.0008: "Q", 0.0484: "R",
           0.0514: "S", 0.0796: "T", 0.0228: "U", 0.0083: "V",
           0.0175: "W", 0.0013: "X", 0.0164: "Y", 0.0005: "Z", 0.1859: " "
           }

"""
Recursive function to traverse our constructed tree and print the Huffman code,
when we make a call to go left we add a 0 to the string and 1 for right
Once we reach a leaf we are done and we print the character and code created
"""

codelengthcount = 0  # Running total of bits used for codes - to determine average
symbolcount = 0

def printhuffmancode(node, s):
    if(node.left is None) and (node.right is None):
        # We are at a leaf, time to print code and character
        if node.char == " ":
            print("Space" + " : " + s)
        else:
            print(node.char + " : " + s)

        global codelengthcount, symbolcount
        codelengthcount += len(s)
        symbolcount += 1
        return

    printhuffmancode(node.left, s + "0")
    printhuffmancode(node.right, s + "1")


def entropy(symbols):
    ent = 0
    for probability in symbols:
        ent -= probability * math.log(probability, 2)
    return ent


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
averagecodelength = codelengthcount / symbolcount
print("Average Code length: " + str(averagecodelength) + " bits")
print("Entropy: " + str(entropy(symbols)))