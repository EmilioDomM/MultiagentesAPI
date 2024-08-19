from mesa import Agent, Model
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid

class VehicleAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        x, y = self.pos

        print(f"Posición Actual: {self.pos}")

        if x < 5:
            self.model.grid.move_agent(self, (x + 1, y))



class VehicleModel(Model):
    def __init__(self):

        super().__init__()

        self.grid = MultiGrid(6, 6, torus=False)
        self.schedule = SimultaneousActivation(self)

        # Create agents
        agent = VehicleAgent(1, self)
        self.grid.place_agent(agent, (1, 3))
        self.schedule.add(agent)

    def step(self):
        self.schedule.step()

model = VehicleModel()
for i in range(4):  # Necesita 4 pasos para llegar a (5, 3)
    model.step()

agent_position = [agent.pos for agent in model.schedule.agents][0]
print(f"Posición final del agente: {agent_position}")