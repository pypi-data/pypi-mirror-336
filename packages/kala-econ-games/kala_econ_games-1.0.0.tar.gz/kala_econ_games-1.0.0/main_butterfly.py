import os
import networkx as nx

os.environ["DEBUG"] = "True"

from kala.models.agents import init_saver_agent
from kala.models.graphs import AgentPlacementNetX, get_neighbours
from kala.models.shocks import RemovePlayer, SwapRandomEdge
from kala.models.game import GameState, GamePlan, play_game, get_summed_score
from kala.models.strategies import MatchingStrategy, SaverCooperationPayoffStrategy



def print_neigh(agent):
    print(f"\nNode {str(agent.uuid)[:8]}")
    for n in get_neighbours(a, g, placements):
        print(f"-> {str(n.uuid)[:8]}")


# Below is working
# rule = kala.models.memory.SaverFlipAfterFractionLost(frac=0)
# a = kala.models.agents.init_saver_agent(True, memory_length=2, update_rule=rule)
# print(a.properties.is_saver, a.score)
# a.update(payoff=1, lost_match=True, time=0)
# print(a.properties.is_saver, a.score)
# a.update(payoff=1, lost_match=False, time=1)
# print(a.properties.is_saver, a.score)

is_saver = [True] * 3 + [False] * 3
agents = [init_saver_agent(s, memory_length=2) for s in is_saver]
extra_agent = init_saver_agent(True, memory_length=2)


g = nx.Graph()
g.add_edges_from([(0, 1), (0, 2), (1, 2), (2, 3), (3, 4), (3, 5), (4, 5)])

# Below is working
# placements = AgentPlacementNetX()
# for i, a in enumerate(agents):
#     print(f"Adding {str(a.uuid)[:8]}")
#     placements.add_agent(a, i)


placements = AgentPlacementNetX.init_bijection(agents, g)
print("Initialised graph")
for i, a in enumerate(agents):
    print(f"Node{i}: {str(a.uuid)[:8]}")


# a = agents[2]
# assert placements.get_position(a) == 2, "get_position failed"
# print_neigh(agents[2])

# i = 1
# node = placements.get_agent(i)
# print(f"\nClearing Node{i}: {str(node.uuid)[:8]}")
# placements.clear_node(i)

# print_neigh(a)

game = GameState(g, agents, placements, SaverCooperationPayoffStrategy(), MatchingStrategy())
shock = RemovePlayer(agents[2])

# Below is working
# shock.apply(game)

# neighs = get_neighbours(agents[2], g, placements) # NB: this changed because the shock also modified agents
# for n in neighs:
#     print(f"neigh: {str(n.uuid)[:8]}")


shocks = {
    4: [shock],
    6: [SwapRandomEdge()],   
}


game_plan = GamePlan(10, shocks=shocks)

for time, state in play_game(game, game_plan):
    assert state.graph.number_of_nodes() == 6
    assert state.graph.number_of_edges() == 7

    print(f"Time {time}: num_agents={len(state.agents)}")
    print(f"\tScore: {round(get_summed_score(state), 2)}")
    print(f"\tSavers: {round(get_summed_score(state, filt=is_saver), 2)}")
