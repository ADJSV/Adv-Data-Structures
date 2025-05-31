#Angel Salges HW3, Quadtree for 2D K-Nearest Neighbors
import random
import heapq
import matplotlib.pyplot as plt

# Quadtree
class KNNQuadtreeNode:
    def __init__(self, x, y, width, height, capacity=1):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.capacity = capacity
        self.points = []
        self.children = []

    def contains(self, px, py):
        return self.x <= px < self.x + self.width and self.y <= py < self.y + self.height

    def insert(self, px, py):
        if not self.contains(px, py):
            return False

        if len(self.points) < self.capacity and not self.children:
            self.points.append((px, py))
            return True

        if not self.children:
            self.subdivide()

        for child in self.children:
            if child.insert(px, py):
                return True
        return False

    def subdivide(self):
        hw, hh = self.width / 2, self.height / 2
        self.children = [
            KNNQuadtreeNode(self.x, self.y + hh, hw, hh),        # NW
            KNNQuadtreeNode(self.x + hw, self.y + hh, hw, hh),   # NE
            KNNQuadtreeNode(self.x, self.y, hw, hh),             # SW
            KNNQuadtreeNode(self.x + hw, self.y, hw, hh),        # SE
        ]
        for px, py in self.points:
            for child in self.children:
                if child.insert(px, py):
                    break
        self.points = []

    def knn_query(self, qx, qy, k):
        heap = []

        def recurse(node):
            if not node:
                return
            for px, py in node.points:
                if (px, py) == (qx, qy):
                    continue  # Skip itself
                dist = (qx - px)**2 + (qy - py)**2
                heapq.heappush(heap, (-dist, (px, py)))
                if len(heap) > k:
                    heapq.heappop(heap)
            for child in node.children:
                recurse(child)

        recurse(self)
        return [pt for _, pt in sorted(heap, reverse=True)]

# Data 
random.seed(42)
rand_points = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(50)] # Region of [0, 100] × [0, 100]).

# Insert
knn_root = KNNQuadtreeNode(0, 0, 100, 100)
for p in rand_points:
    knn_root.insert(*p)

# 5 random queries
query_pts = random.sample(rand_points, 5)
k = 3

# Main
results = []
for qx, qy in query_pts:
    qt_result = knn_root.knn_query(qx, qy, k)
    bf_result = sorted([p for p in rand_points if p != (qx, qy)],key=lambda p: (qx - p[0])**2 + (qy - p[1])**2)[:k]
    results.append({
        'query': (qx, qy),
        'quadtree': qt_result,
        'brute_force': bf_result,
        'match': set(qt_result) == set(bf_result)
    })

# Results
for res in results:
    print(f"\nQuery Point: {res['query']}")
    print("  Quadtree KNN:", res['quadtree'])
    print("  Brute-Force KNN:", res['brute_force'])
    print("  Match:", res['match'])

# Ploting 
fig, axs = plt.subplots(1, 5, figsize=(20, 4))
for ax, result in zip(axs, results):
    qx, qy = result['query']
    qt_neighbors = result['quadtree']

    ax.scatter(*zip(*rand_points), color='gray', alpha=0.5, label='All Points')
    ax.scatter(qx, qy, color='red', label='Query')
    ax.scatter(*zip(*qt_neighbors), color='blue', label='KNN')
    ax.set_title(f"Query @ ({qx:.1f}, {qy:.1f})")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_aspect('equal')
    ax.grid(True)

handles, labels = axs[0].get_legend_handles_labels()
fig.legend(handles, labels, loc='upper right')
plt.tight_layout()
plt.show()
