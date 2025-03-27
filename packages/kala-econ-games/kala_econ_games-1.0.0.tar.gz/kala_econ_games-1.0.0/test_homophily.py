import networkx as nx

from kala.models.agents import init_saver_agent
from kala.models.graphs import (
    AgentPlacementNetX,
    get_neighbours,
    get_neighbour_sample_with_homophily,
)


def print_neigh(agent):
    print(f"\nNode {str(agent.uuid)[:8]}")
    for n in get_neighbours(a, g, placements):
        print(f"-> {str(n.uuid)[:8]}")


HOMOPHILY = 1

is_saver = [True] * 3 + [False] * 3
agents = [init_saver_agent(s, memory_length=2, homophily=HOMOPHILY) for s in is_saver]


g = nx.Graph()
g.add_edges_from([(0, 1), (0, 2), (1, 2), (2, 3), (3, 4), (3, 5), (4, 5)])


placements = AgentPlacementNetX.init_bijection(agents, g)
print("Initialised graph")
for i, a in enumerate(agents):
    print(f"Node{i}: {str(a.uuid)[:8]}")


a = agents[2]
print_neigh(agents[2])

i = 1
node = placements.get_agent(i)
print(f"\nClearing Node{i}: {str(node.uuid)[:8]}")
placements.clear_node(i)

selected = get_neighbour_sample_with_homophily(a, g, placements, size=2)
for s in selected:
    print(f"\nSelected node with homophily: {str(s.uuid)[:8]}")
