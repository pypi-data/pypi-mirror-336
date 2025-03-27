import os
import networkx as nx

os.environ["DEBUG"] = "1"

from kala import CooperationStrategy, DiscreteTwoByTwoGame, init_investor_graph
from kala.models.shocks import AddRandomEdge, RemoveRandomEdge, SwapRandomEdge


g = nx.Graph()
g.add_edges_from([(0, 1), (0, 2), (1, 2), (2, 3), (3, 4), (3, 5), (4, 5)])
G = init_investor_graph(g, savers_share=0.5, rng=0)


coop = CooperationStrategy(
    stochastic=True, differential_efficient=0.5, differential_inefficient=0.05, rng=0
)

game = DiscreteTwoByTwoGame(G, coop)


game.play_round()
shock = SwapRandomEdge(rng=0)
shock.apply(game)
shock.apply(game)

AddRandomEdge(rng=0).apply(game)

# print(g)
# print(game.graph)
# # game.play_round()


# new_G = SimpleGraph(g, nodes=agents)
# new_game = DiscreteTwoByTwoGame(new_G, coop)
# print(new_game.graph)
# game.play_round()


# if __name__ == "__main__":
#     pass
