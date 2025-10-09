
import math
import ast

DSAs = []

# dsa = {'id', 'name', 'categories', 'types', 'description', 'test'}

array = {
    'id': 'array',
    'name': 'Array',
    'categories': ['Static', 'Linear Data Structures'],
    'types': ['Normal', 'Queues', 'Stack'],
    'description': 'An array is a collection of elements stored in contiguous memory, accessible by index.',
    'content': [
        ["Definition: ", "An array is a data structure that holds a fixed number of elements of the same data type, stored in contiguous memory locations."],
        ["Access Time Complexity: ", "Accessing an element by index is O(1), making arrays efficient for retrieval."],
        ["Insertion and Deletion Time Complexity: ", "Inserting or deleting elements in the middle or at the start has a time complexity of O(n) due to shifting elements."],
        ["Contiguous Memory: ", "All elements of an array are stored in contiguous memory locations, which improves cache performance."],
        ["Fixed Size: ", "The size of an array is fixed at the time of creation and cannot be changed dynamically."],
        ["Indexing: ", "Elements in an array are indexed starting from 0, which allows for random access."],
        ["Data Type: ", "An array can only store elements of the same data type, which ensures consistency in operations."],
        ["Multidimensional Arrays: ", "An array can have multiple dimensions, like 2D or 3D arrays, used for representing matrices or grids."],
        ["Static vs. Dynamic Arrays: ", "Static arrays have a fixed size, while dynamic arrays (like Python lists) can grow or shrink at runtime."],
        ["Memory Allocation: ", "Arrays are stored in contiguous memory locations, which requires knowing the size at allocation."],
        ["Traversing: ", "Traversing an array involves visiting each element in a linear fashion, typically O(n)."],
        ["Searching: ", "Linear search has O(n) time complexity, while binary search on sorted arrays has O(log n)."],
        ["Sorting: ", "Arrays can be sorted using algorithms like QuickSort, MergeSort, or BubbleSort, depending on the use case."]
        ],
    'file': 'array_vis'
}

linked_list = {
    'id': 'linked_list',
    'name': 'Linked List',
    'categories': ['Dynamic', 'Linear Data Structures'],
    'types': ['Queue'],
    'description': 'A linked list is a linear data structure where elements are stored as nodes connected by pointers.',
    'content': [
        ["Linked List:", "A linked list is a linear collection of elements (nodes), where each node points to the next one."],
        ["Types:", "Types include singly linked lists (each node points to the next) and doubly linked lists (each node points to both the next and previous node)."],
        ["Operations:", "Common operations include insertion, deletion, and traversal, typically in O(n) time."],
        ["Dynamic Size:", "Unlike arrays, linked lists can grow or shrink in size dynamically."],
        ["Memory:", "Nodes are typically scattered in memory rather than stored in contiguous locations."],
        ["Head and Tail:", "In a singly linked list, the first node is referred to as the head, and the last node points to null, known as the tail."],
        ["Doubly Linked List:", "In a doubly linked list, each node has two pointers: one pointing to the next node and one to the previous node."],
        ["Circular Linked List:", "In a circular linked list, the last node points back to the first node, creating a circular structure."],
        ["Linked List vs Array:", "Unlike arrays, linked lists are more efficient for insertions and deletions as elements are not contiguous in memory."]
        ],
    'file': 'linkedlist_vis'
}

queue = {
    'id': 'queue',
    'name': 'Queue',
    'categories': ['Static', 'Dynamic', 'Queue', 'Linear Data Structures'],
    'types': ['Static', 'Dynamic', 'Priority', 'Circular'],
    'description': 'A queue is a data structure that follows the FIFO (First In, First Out) principle.',
    'content': [
        ["Queue:", "A queue is a linear data structure that follows the FIFO (First In, First Out) principle."],
        ["Problem:", "A static non-circular queue is memory inefficient, since it cannot be used again when the front pointer reaches the end."],
        ["Operations:", "Primary operations are enqueue (add item) and dequeue (remove item), both generally occurring at opposite ends."],
        ["Applications:", "Queues are commonly used in scheduling, buffers, and handling requests in a system."],
        ["Types:", "Types of queues include simple queues, circular queues, and priority queues."],
        ["Efficiency:", "Both enqueue and dequeue operations are typically O(1)."],
        ["Circular Queue:", "In a circular queue, after the last element, the next element is the first element, helping utilize the array more efficiently."],
        ["Priority Queue:", "A priority queue stores elements in order of priority, rather than insertion order, with the highest priority element dequeued first."],
        ["Queue vs Stack:", "Queues use FIFO while stacks use LIFO (Last In, First Out) for element processing."],
        ["Queue Use Cases:", "Queues are widely used in scenarios such as task scheduling and handling of asynchronous data like in networking and CPU process management."]
        ],
    'file': 'array_vis'
}

stack = {
    'id': 'stack',
    'name': 'Stack',
    'categories': ['Static', 'Dynamic', 'Linear Data Structures'],
    'types': ['Static', 'Dynamic'],
    'description': 'A stack is a data structure that follows the LIFO (Last In, First Out) principle.',
    'content': [
        ["Stack:", "A stack is a linear data structure that follows the LIFO (Last In, First Out) principle."],
        ["Push and Pop:", "Elements are added using push and removed using pop operations. Both occur at the same end (the top)."],
        ["Applications:", "Stacks are used in function call management, undo operations, and parsing expressions."],
        ["Memory Usage:", "Stacks usually have constant space usage for each element in the stack."],
        ["Efficiency:", "Both push and pop operations are typically O(1)."],
        ["Applications in Recursion:", "Stacks are crucial in recursion, as they hold the function calls and local variables until the function completes."],
        ["Balanced Parentheses:", "Stacks are often used to solve problems like balanced parentheses or checking for valid mathematical expressions."],
        ["Overflow and Underflow:", "Stack overflow occurs when the stack exceeds its limit, and underflow happens when you attempt to pop an element from an empty stack."],
        ["Memory Consideration:", "Since stacks use a dynamic memory allocation, managing the size carefully is crucial for performance."]
        ],
    'file': 'array_vis'
}

graph = {
    'id': 'graph',
    'name': 'Graph',
    'categories': ['Non-Linear Data Structures', 'DFS', 'BFS', 'Dijkstra’s'],
    'types': ['Normal'],
    'description': 'A graph is a collection of nodes connected by edges, representing relationships. Graph traversal algorithms explore all nodes in a graph in a specified order.',
    'content': [
        ["Graph:", "A graph is a collection of nodes (vertices) and edges (connections between nodes)."],
        ["Types of Graphs:", "Graphs can be directed (edges have a direction) or undirected, and can be weighted (edges have weights) or unweighted."],
        ["Applications:", "Graphs are used in representing networks, social media relationships, and computer networks."],
        ["Traversal Algorithms:", "Common traversal algorithms include Depth-First Search (DFS) and Breadth-First Search (BFS)."],
        ["Adjacency List vs Adjacency Matrix:", "Adjacency lists are memory efficient for sparse graphs, while adjacency matrices are used for dense graphs."],
        ["Shortest Path:", "Algorithms like Dijkstra’s and Bellman-Ford are used to find the shortest path between nodes in a weighted graph."],
        ["Graph Representation:", "Graphs can be represented in several ways, including adjacency matrices, adjacency lists, or edge lists, each having its pros and cons."],
        ["Cycle Detection:", "Graph algorithms are also used for detecting cycles in directed and undirected graphs, a key operation in many applications."],
        ["Degrees of Nodes:", "The degree of a node is the number of edges the node connects to."]
        ],
    'file': 'graph_vis'
}

tree = {
    'id': 'tree',
    'name': 'Tree',
    'categories': ['Non-Linear Data Structures', 'Pre-order', 'In-order', 'Post-order'],
    'types': ['Normal', 'Binary'],
    'description': 'A tree is a hierarchical data structure with nodes connected by edges, without cycles. Tree traversal algorithms visit all nodes in a tree in a specified order.',
    'content': [
        ["Tree:", "A tree is a hierarchical data structure with a root node and subtrees."],
        ["Binary Tree:", "A binary tree is a tree where each node has at most two children."],
        ["Binary Search Tree (BST):", "A binary search tree is a binary tree with the left child less than the parent node and the right child greater."],
        ["Balanced Tree:", "A balanced tree ensures that the height difference between subtrees of any node is minimal, helping improve search times."],
        ["Applications:", "Trees are used in database indexing, file systems, and decision-making algorithms."],
        ["Traversal Techniques:", "Common tree traversal techniques include pre-order, in-order, and post-order traversals."],
        ["Height and Depth:", "The height of a tree is the longest path from the root to a leaf node, while the depth of a node is the number of edges from the root to the node."],
        ],
    'file': 'graph_vis'
}

sorting = {
    'id': 'sorting',
    'name': 'Sorting',
    'categories': ['Sorting and Searching Algorithms'],
    'types': ['Bubble', 'Insertion', 'Merge'],
    'description': 'A sorting algorithm arranges elements in a specified order, such as ascending or descending.',
    'content': [
        ["Sorting:", "Sorting is the process of arranging elements in a particular order, typically ascending or descending."],
        ["Bubble Sort:", "A simple sorting algorithm where each element is compared with the next, and swapped if necessary, with an average time complexity of O(n^2)."],
        ["Merge Sort:", "A divide-and-conquer sorting algorithm with time complexity O(n log n), which splits the array into smaller parts and merges them in order."],
        ["Quick Sort:", "Another divide-and-conquer algorithm that partitions the array and recursively sorts subarrays, with an average time complexity of O(n log n)."],
        ["Insertion Sort:", "A simple algorithm where elements are picked one by one and inserted into their correct position within the sorted part of the array."],
        ["Time Complexity:", "Common time complexities for sorting algorithms include O(n^2) for bubble sort and O(n log n) for merge and quicksort."],
        ["Stability:", "A stable sorting algorithm preserves the relative order of records with equal keys, while an unstable sort does not."],
        ["Space Complexity:", "Merge sort has O(n) auxiliary space complexity, while algorithms like quicksort are considered in-place with O(log n) space complexity."]
        ],
    'file': 'sorting_vis'
}

searching = {
    'id': 'searching',
    'name': 'Searching',
    'categories': ['Sorting and Searching Algorithms'],
    'types': ['Linear', 'Binary'],
    'description': 'A searching algorithm finds a specific element within a data structure.',
    'content': [
        ["Definition:", "Searching is the process of finding a specific element within a data structure."],
        ["Linear Search:", "A simple algorithm that checks each element in a sequence one by one. The time complexity is O(n), where n is the number of elements. It works on both sorted and unsorted data but can be inefficient for large datasets."],
        ["Binary Search:", "A more efficient searching method that requires the data to be sorted. It divides the data in half with each comparison, reducing the search space significantly. The time complexity is O(log n), making it much faster than linear search on large sorted datasets."],
        ["Jump Search:", "This algorithm involves dividing the data into smaller blocks and performing a linear search within the block where the element might be. Its time complexity is O(√n)."],
        ["Comparisons:", "Binary search is faster for larger data sets but requires the data to be sorted. Linear search can be faster for smaller data sets."],
        ["Exponential Search:", "This is used for sorted data and involves two stages: finding a range where the element might be, followed by a binary search within that range. It works well when the data is infinite or unbounded."],
        ["Interpolation Search:", "A variation of binary search that estimates the position of the element based on the value being searched. It performs better when the values are uniformly distributed but has a worst-case complexity of O(n)."]
        ],
    'file': 'array_vis'
}

DSAs.append(array)
DSAs.append(queue)
DSAs.append(stack)
DSAs.append(graph)
DSAs.append(tree)
DSAs.append(sorting)
DSAs.append(searching)
DSAs.append(linked_list)

empty_list=[""]*500

#################'making the database with the hash'################

def makeDatabase():
    database=open("DSA Types Database.txt", "w", encoding="utf-8")
    
# the name of the dsa is the key
    def makingHash(element):
        key = element["name"]
    
        # hash function
    
        val = 1
        count = 1
        flip = True
    
        for letter in key:
            if flip == True:
                val *= (ord(letter)/1.5)
            else:
                val += (ord(letter)*2)
            flip = not flip
            count *= 2
    
        remainder = val % 3
        val = math.sqrt(val)
        val = round(val/count)
        val = str(val)
        
        hash_val = ""
    
    
        for i in val:
            hash_val += i
        hash_val = round(int(hash_val) * remainder)
    
        while empty_list[hash_val] != "":
            hash_val += 1
        
        return hash_val

    for dsa in DSAs:
        empty_list[makingHash(dsa)] = dsa
        print(makingHash(dsa))
    
    for i in empty_list:
        database.write(str(i) + "\n")
    
    database.close()


makeDatabase()




#########################################################################

database=open("DSA Types Database.txt", "r", encoding="utf-8")
database_list = database.readlines()

# the name acts as the key
# [:-1] is needed for the '\n' for the end of each line
def hashRetrieve(key):
    # hash function
    
    val = 1
    count = 1
    flip = True
    
    for letter in key:
        if flip == True:
            val *= (ord(letter)/1.5)
        else:
            val += (ord(letter)*2)
        flip = not flip
        count *= 2
    
    remainder = val % 3
    val = math.sqrt(val)
    val = round(val/count)
    val = str(val)
    
    hash_val = ""
    
    
    for i in val:
        hash_val += i
    hash_val = round(int(hash_val) * remainder)
        
    while ast.literal_eval(database_list[hash_val][:-1])["name"] != key:
        hash_val += 1
        
    return ast.literal_eval(database_list[hash_val][:-1])

#print(hashRetrieve("Stack")['name'])
#print(array['name'])
