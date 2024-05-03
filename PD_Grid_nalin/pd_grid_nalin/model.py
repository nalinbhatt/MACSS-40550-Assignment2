import mesa

from .agent import PDAgent


class PdGrid(mesa.Model):
    """Model class for iterated, spatial prisoner's dilemma model."""

    schedule_types = {
        "Sequential": mesa.time.BaseScheduler,
        "Random": mesa.time.RandomActivation,
        "Simultaneous": mesa.time.SimultaneousActivation,
    }

    # This dictionary holds the payoff for this agent,
    # keyed on: (my_move, other_move)

    payoff = {("C", "C"): 1, ("C", "D"): 0, ("D", "C"): 1.1, ("D", "D"): 0}

    def __init__(
        self, width=50, height=50, schedule_type="Random", payoffs=None, seed=None, radius=1,
    ):
        """
        Create a new Spatial Prisoners' Dilemma Model.

        Args:
            width, height: Grid size. There will be one agent per grid cell.
            schedule_type: Can be "Sequential", "Random", or "Simultaneous".
                           Determines the agent activation regime.
            payoffs: (optional) Dictionary of (move, neighbor_move) payoffs.
        """
        super().__init__()
        self.grid = mesa.space.SingleGrid(width, height, torus=True)
        self.schedule_type = schedule_type
        self.schedule = self.schedule_types[self.schedule_type](self)
        self.radius = radius

        # Create agents
        for x in range(width):
            for y in range(height):
                agent = PDAgent((x, y), self)
                self.grid.place_agent(agent, (x, y))
                self.schedule.add(agent)

        self.datacollector = mesa.DataCollector(
            model_reporters = {
                "Cooperating_Agents": lambda m: len(
                    [a for a in m.schedule.agents if a.move == "C"]
                ),
                "total_pay_off": lambda m: sum([a.increment for a in m.schedule.agents]),
            },
            agent_reporters = {
                "pos": "pos", 
                "score": "score", 
                "increment": "increment",
                "count": "count", 
                "current_best_neighbor_move": "current_best_neighbor_move",
                "current_best_neighbor_pos": "current_best_neighbor_pos",
                "current_best_neighbor_score":"current_best_neighbor_score"
            }
        )

        # self.datacollector_agent = mesa.DataCollector(
        #     model_reporters={"happy": "happy", "Avg Similarity": "similarity", 
        #                     "seed": "_seed"},  # Model-level count of happy agents
        #     agent_reporters={"Number of Similar Neighbors": "similar", 
        #     "Agent type": "type"}
        # )

 
        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)

    def run(self, n):
        """Run the model for n steps."""
        for _ in range(n):
            self.step()
