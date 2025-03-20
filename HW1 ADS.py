#Angel Salges HW1, Interval Tree
class IntervalNode:
    def __init__(self, low, high):
        self.low = low  #interval start
        self.high = high  #interval end
        self.max_high = high  #subtree max height
        self.left = None
        self.right = None

def insert(root, low, high):
    if root is None:
        return IntervalNode(low, high)
    if low < root.low:
        root.left = insert(root.left, low, high)
    else:
        root.right = insert(root.right, low, high)
    root.max_high = max(root.max_high, high)
    return root

def build_interval_tree(intervals):
    root = None
    for low, high in intervals:
        root = insert(root, low, high)
    return root

def is_overlap(interval, x):
    #Check x is on the interval
    return interval.low <= x <= interval.high

def query(root, x, result):
    #Find intervals that overlap with x 
    if root is None:
        return

    #If x is inside interval, add to result
    if is_overlap(root, x):
        result.append((root.low, root.high))

    #If left child's max_high > x, check left subtree
    if root.left and root.left.max_high >= x:
        query(root.left, x, result)

    #Always check the right subtree
    query(root.right, x, result)

def min_value_node(node):
    #Finds node with the smallest value in the tree
    current = node
    while current.left is not None:
        current = current.left
    return current

def delete(root, low, high):
    #Delete interval from the tree
    if root is None:
        return None

    if low < root.low:
        root.left = delete(root.left, low, high)
    elif low > root.low:
        root.right = delete(root.right, low, high)
    elif root.high == high:  
        if root.left is None:
            return root.right
        elif root.right is None:
            return root.left
        temp = min_value_node(root.right)
        root.low, root.high = temp.low, temp.high
        root.right = delete(root.right, temp.low, temp.high)

    #Update max_high after deletion
    root.max_high = root.high
    if root.left:
        root.max_high = max(root.max_high, root.left.max_high)
    if root.right:
        root.max_high = max(root.max_high, root.right.max_high)
    return root

##################################################################################################
#Main:
#Intervals
intervals = [(15, 20), (10, 30), (17, 19), (5, 20)]
root = build_interval_tree(intervals)

#Query overlapping interval
result = []
query(root, 17, result)
print("Overlapping intervals:", result)

#Insert Interval
root=insert(root, 5, 35)
result = []
query(root, 17, result)
print("Overlapping intervals after insertion:", result)

#Delete interval
root=delete(root, 10, 30)
result = []
query(root, 17, result)
print("Overlapping intervals after deletion:", result)