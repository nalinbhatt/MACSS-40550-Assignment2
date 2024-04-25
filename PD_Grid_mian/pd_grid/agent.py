import mesa
import csv

class PDAgent(mesa.Agent):
    """Agent member of the iterated, spatial prisoner's dilemma model."""

    def __init__(self, pos, model, starting_move=None, count=0):
        """
        Create a new Prisoner's Dilemma agent.

        Args:
            pos: (x, y) tuple of the agent's position.
            model: model instance
            starting_move: If provided, determines the agent's initial state:
                           C(ooperating) or D(efecting). Otherwise, random.
        """
        super().__init__(pos, model)
        self.pos = pos
        self.score = 0
        self.increment = 0
        self.count = count
        
        if starting_move:
            self.move = starting_move
        else:
            #self.random.seed(self.model.next_id())
            self.move = self.random.choice(["C", "D"])
        self.next_move = None
        
        with open('initial_move.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                #writer.writerow(['My Position', 'Best Neighbor Position', 'Best Neighbor Score'])
                writer.writerow([self.pos, self.move, self.score])
                #print(f"my pos: {self.pos}, best neighbor pos: {best_neighbor.pos}, best neighbor score: {best_neighbor.score}")
        
 
    @property
    def isCooroperating(self):
        return self.move == "C"

    def step(self):
        """Get the best neighbor's move, and change own move accordingly
        if better than own score."""

        neighbors = self.model.grid.get_neighbors(self.pos, True, include_center=True, radius = self.model.radius)
        #print(len(neighbors))
        best_neighbor = max(neighbors, key=lambda a: a.score)
        self.next_move = best_neighbor.move
        self.count+=1
        if self.count == 1:
            #print(f"my pos: {self.pos}, best neighbor pos: {best_neighbor.pos}, best neighbor score: {best_neighbor.score}")
            with open('output.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                #writer.writerow(['My Position', 'Best Neighbor Position', 'Best Neighbor Score'])
                writer.writerow([f"{self.pos}, neighbors:{len(neighbors)}, best: {best_neighbor.pos}, {best_neighbor.move}, {best_neighbor.score}"])
                #print(f"my pos: {self.pos}, best neighbor pos: {best_neighbor.pos}, best neighbor score: {best_neighbor.score}")
        

 
        if self.model.schedule_type != "Simultaneous":
            self.advance()

        
    def advance(self):
        self.move = self.next_move
        self.score += self.increment_score()
        self.increment = self.increment_score()


    def increment_score(self):
        neighbors = self.model.grid.get_neighbors(self.pos, True)
        if self.model.schedule_type == "Simultaneous":
            moves = [neighbor.next_move for neighbor in neighbors]
        else:
            moves = [neighbor.move for neighbor in neighbors]
        return sum(self.model.payoff[(self.move, move)] for move in moves)
