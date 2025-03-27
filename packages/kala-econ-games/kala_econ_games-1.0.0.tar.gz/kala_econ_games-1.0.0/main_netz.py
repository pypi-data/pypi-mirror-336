import os

os.environ["DEBUG"] = "True"

from kala import (
    GamePlan,
    play_game,
    get_summed_score,
    get_saver_agents,
    get_gini_coefficient,
    init_savers_gamestate_from_netz,
    shocks,
)


network_name = "dolphins"
game = init_savers_gamestate_from_netz(network_name, savers_share=0.5, memory_length=4)
agents = game.agents

shocks = {
    4: [shocks.RemovePlayer(agents[2])],
    6: [shocks.SwapRandomEdge()],
}


game_plan = GamePlan(10, shocks=shocks)

for time, state in play_game(game, game_plan):
    savers = get_saver_agents(state)
    num_savers = len(savers)
    total_score = get_summed_score(state.agents)
    saver_score = get_summed_score(savers)
    gini = get_gini_coefficient(state.agents)

    print(f"Time {time}: num_agents={len(state.agents)}; num_savers={num_savers}")
    print(f"\tTotal:  {round(total_score, 2)}")
    print(f"\tSavers: {round(saver_score, 2)}")
    print(f"\tGini:   {round(gini, 3)}")
