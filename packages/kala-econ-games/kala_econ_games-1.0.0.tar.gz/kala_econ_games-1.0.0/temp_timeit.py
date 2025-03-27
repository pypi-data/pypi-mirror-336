import itertools
import numpy as np
from pydantic import BaseModel

# from kala import (
#     DiscreteTwoByTwoGame,
#     FractionMemoryRule,
#     init_investor_graph,
#     NetzDatabase,
#     CooperationStrategy,
# )

from kala.models.game import DiscreteTwoByTwoGame
from kala.models.strategies import CooperationStrategy
from kala.models.memory_rules import FractionMemoryRule
from kala.utils.io import NetzDatabase
from kala.models.graphs import init_investor_graph


class Spec(BaseModel):
    """Spec for an experiment."""

    network_name: str
    subnetwork: str | None
    memory_length: int
    memory_frac: float
    savers_share: float
    differentials: tuple[float, float]  # efficient, inefficient
    num_rounds: int
    num_games: int


NET_DB = NetzDatabase()


class BaseExperiment:
    """
    Base class to run experiments.

    Methods
    -------
    multigame_summary()
    single_run_history()
    """

    spec: Spec
    num_players: int

    def __init__(self, spec: Spec):
        self.spec = spec
        self._nx_graph = NET_DB.read_netzschleuder_network(spec.network_name, spec.subnetwork)
        self.num_players = self._nx_graph.number_of_nodes()
        self._mem_rule = FractionMemoryRule(spec.memory_length, fraction=spec.memory_frac)

    def _init_game(self) -> DiscreteTwoByTwoGame:
        graph = init_investor_graph(
            self._nx_graph,
            savers_share=self.spec.savers_share,
            min_specialization=1 - self.spec.differentials[1],
            update_rule=self._mem_rule,
        )

        eff, ineff = self.spec.differentials
        coop = CooperationStrategy(
            stochastic=True,
            differential_efficient=eff,
            differential_inefficient=ineff,
        )

        return DiscreteTwoByTwoGame(graph, coop)

    def _single_game_summary(self) -> tuple[int, int]:
        savers = np.zeros(self.spec.num_rounds, dtype=int)
        game = self._init_game()

        for i in range(self.spec.num_rounds):
            n_savers = game.get_num_savers()
            savers[i] = n_savers

            if n_savers == self.num_players:
                return self.num_players, i

            if n_savers == 0:
                savers = savers[: i + 1]
                break

            game.play_round()

        return savers.min(), savers.argmin()

    def multigame_summary(self) -> np.ndarray:
        """
        Track the min of savers and the time when it is achieved across multiple games.

        """
        empty_iterables = [[]] * self.spec.num_games  # type: ignore
        out = list(itertools.starmap(self._single_game_summary, empty_iterables))

        return np.array(out)


if __name__ == "__main__":
    spec = Spec(
        network_name="student_cooperation",
        subnetwork=None,
        memory_length=10,
        memory_frac=0.5,
        savers_share=0.5,
        differentials=(0.1, 0.15),  # efficient, inefficient
        num_rounds=1000,  # ,0,
        num_games=12,  # 48,
    )
    exp = BaseExperiment(spec)
    res = exp.multigame_summary()
    # print("end")
