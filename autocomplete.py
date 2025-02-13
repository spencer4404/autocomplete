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

    def __str__(self):
        return f"{self.letter}"

class Autocomplete():
    def __init__(self, parent=None, document=""):
        self.root = Node()
        self.suggest = self.suggest_bfs #Default, change this to `suggest_dfs/ucs/bfs` based on which one you wish to use.
        self.queue = deque()
        # for checking purposes
        self.all_words = []

    # build the tree
    def build_tree(self, document):
        for word in document.split():
            node = self.root
            for char in word:
                #TODO for students
                # If the node for the letter does not exist under the root, create it
                if char not in list(node.children.keys()):
                    node.children[char] = Node(char)
                # jump down to new node
                node = node.children[char]
            # mark last node as the end of the word
            node.is_word = True

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

    #TODO for students!!!
    def suggest_bfs(self, prefix):
        # base case
        bfs_suggestions = []
        # traverse to the correct starting node
        start_node = self.root
        for i in prefix:
            # traverse to the correct part of the word tree
            if i in start_node.children:
                start_node = start_node.children[i]
            # avoid bogus words (assure we have a good starting node)
            else:
                return []
        # enqueue the first node
        self.queue.append((start_node, prefix))
        # run until queue is empty
        while self.queue:
            # unpack the tuple
            node, current_prefix = self.queue.popleft()
            # enqueue at all the node children while updating the prefix
            for child in node.children.values():
                new_prefix = current_prefix + child.letter
                self.queue.append((child, new_prefix))
                # spit out the suggestions
                if child.is_word:
                    bfs_suggestions.append(new_prefix)
        return bfs_suggestions


    #TODO for students!!!
    def suggest_dfs(self, prefix):
        # base case
        node = list(prefix)[-1] # top node
        root = self.root.children[node] # top node becomes root
        
        return []


    #TODO for students!!!
    def suggest_ucs(self, prefix):
        pass


a = Autocomplete()
words = "lit liter no cap bet fam fire tbh fr extra salty shook lowkey highkey vibe check sus simp ghosting salty snatched outfit cancelled shook tea is sis bruh bestie receipts facts curve basic extra totally  af simping cancelled glowed up mood flex clout drip fire iconic slay queen woke fam goals snatched tea no  savage shook lowkey highkey cap vibe check sus simp salty snatched cancelled shook tea sis bruh bestie receipts facts curve basic extra af glowed up mood flex clout drip iconic slay queen woke fam goals snatched tea savage periodt no cap finna turnt snatched tea savage shook lowkey vibe check sus simp salty snatched cancelled shook sis bruh bestie receipts facts curve basic extra af simping cancelled glowed up mood flex clout drip iconic slay queen woke goals tea savage lit no cap bet fam fire tbh fr extra salty shook lowkey vibe check sus simp ghosting salty snatched cancelled shook tea sis bruh bestie receipts facts curve basic extra af simping cancelled glowed up mood flex clout drip iconic slay queen woke fam goals snatched tea savage snatched receipts vibe check salty ghosting mood clout glow up facts sus fam basic slay there though that the their through thee thou thought thag"
a.build_tree(words)
a.print_tree()
print(" ".join(sorted(a.all_words)))
print(" ".join(sorted(set(words.split()))))
print(a.check_tree(a.all_words, set(words.split())))