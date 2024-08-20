from mesa import Agent, Model
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid

class VehicleAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    # Al momento, el agente se mueve solamente en la dirección Y positiva, en donde se encuentra el objetivo final
    def step(self):
        x, y = self.pos
        print(f"Posición Actual: {self.pos}")
        self.model.grid.move_agent(self, (x, y + 1))



class VehicleModel(Model):
    def __init__(self):

        super().__init__()

        self.grid = MultiGrid(11, 11, torus=False)
        self.schedule = SimultaneousActivation(self)

        # Create agents
        agent = VehicleAgent(1, self)
        print("Se coloca al agente en la posición inicial (5,0)")
        self.grid.place_agent(agent, (5, 0))
        self.schedule.add(agent)

    def step(self):
        self.schedule.step()


print("Inicializando sistema y colocando al agente en la posición inicial..")
model = VehicleModel()
print("Se desplazará al agente hacia el final de la calle a la posición (5, 10)")
for i in range(10):
    model.step()

agent_position = [agent.pos for agent in model.schedule.agents][0]
print(f"Posición final del agente: {agent_position}")