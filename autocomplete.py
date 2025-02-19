from collections import deque
import heapq
import random
import string


class Node:
    #TODO
    def __init__(self, letter = ""):
        self.children = {}
        self.letter = letter
        self.is_word = False
        self.frequency = 0

    def __str__(self):
        return f"{self.letter}: at {hex(id(self))}"

class Autocomplete():
    def __init__(self, parent=None, document=""):
        self.root = Node()
        self.suggest = self.suggest_dfs #Default, change this to `suggest_dfs/ucs/bfs` based on which one you wish to use.
        self.queue = deque()
        # for checking purposes
        self.all_words = []

    # build the tree
    def build_tree(self, document):
        all_words = {}
        for word in document.split():
            all_nodes = []
            node = self.root

            for char in word:
                #TODO for students
                # If the node for the letter does not exist under the root, create it
                if char not in node.children:
                    node.children[char] = Node(char)
                # jump down to new node
                node = node.children[char]
                all_nodes.append(node)

            # mark last node as the end of the word
            node.is_word = True
            # track unique words
            for n in all_nodes:
                n.frequency += 1  # Increment the frequency for each node in the path of the word

            all_words[word] = all_nodes

    # recursive function to see the tree, basically a DFS
    def print_tree(self, node=None, prefix=""):
        # base case
        if node == None:
            node = self.root
        # end
        if node.is_word:
            print(f"Word: {prefix}")
            self.all_words.append(prefix) # for checking purposes
        # recursive call
        for char, child in node.children.items():
            self.print_tree(child, prefix + char)

    # checking
    def check_tree(self, tree_words = list, words = list):
        return sorted(tree_words) == sorted(words)

    def suggest_random(self, prefix):
        random_suffixes = [''.join(random.choice(string.ascii_lowercase) for _ in range(3)) for _ in range(5)]
        return [prefix + suffix for suffix in random_suffixes]
    
    def get_start_node(self, prefix):
        """Helper function, runs through the prefix to get to the right starting spot of the tree"""
        start_node = self.root
        for i in prefix:
            # traverse to the correct part of the word tree
            if i in start_node.children:
                start_node = start_node.children[i]
            # return nothing when there is no children
            else:
                return []
        return start_node

    #TODO for students!!!
    def suggest_bfs(self, prefix):
        """Get word suggestions using BFS"""
        bfs_suggestions = []
        start_node = self.get_start_node(prefix) # traverse to the correct starting node
        self.queue.append((start_node, prefix)) # enqueue the first node
        # Run BFS on the queue
        while self.queue:
            # unpack the tuple, taking FIFO order
            node, current_prefix = self.queue.popleft()
            if node: # only run the search when there is children
                # enqueue at all the node children while updating the prefix
                for child in node.children.values():
                    new_prefix = current_prefix + child.letter
                    self.queue.append((child, new_prefix))
                    if child.is_word: 
                        bfs_suggestions.append(new_prefix) # add the suggestions when the node completes a word
        return bfs_suggestions

    #TODO for students!!!
    def suggest_dfs(self, prefix):
        """Get suggestions using DFS"""
        dfs_suggestions = []
        start_node = self.get_start_node(prefix) # get the correct start node
        self.queue.append((start_node, prefix))

        # run DFS on the queue
        while self.queue:
            # unpack tuple, taking LIFO order
            node, current_prefix = self.queue.pop()

            if node: # only run the search when there is children
                # enqueue the children, have to flip it to match lifo order
                for child in reversed(list(node.children.values())):
                    new_prefix = current_prefix + child.letter
                    self.queue.append((child, new_prefix))
                    if child.is_word:
                        dfs_suggestions.append(new_prefix) # add the suggestions when the node completes a word

        return dfs_suggestions

    #TODO for students!!!
    def suggest_ucs(self, prefix):
        """Get word suggestions using UCS"""
        ucs_suggestions = []
        heap = []

        start_node = self.get_start_node(prefix) # traverse to the correct starting node
        cost = 0
        heapq.heappush(heap, (cost, prefix, start_node)) # add first node to the heap

        # Run UCS on the heap
        while heap:
            # unpack the tuple, taking taking the node with the least cost first
            cost, current_prefix, node = heapq.heappop(heap)
            if node.is_word:
                ucs_suggestions.append(current_prefix)

            if node: # only run the search when there is children
                # add all the children based on the cost
                for child in node.children.values():
                    new_prefix = current_prefix + child.letter
                    child_cost = cost + (1 / child.frequency)

                    heapq.heappush(heap, (child_cost, new_prefix, child))
                    # if child.is_word:
                    #     ucs_suggestions.append(new_prefix) # add the suggestions when the node completes a word

        return ucs_suggestions