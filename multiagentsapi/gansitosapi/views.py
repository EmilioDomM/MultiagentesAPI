from django.http import JsonResponse
from django.shortcuts import render
from mesa import Agent, Model
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid

class VehicleAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        x, y = self.pos
        # Check if the next position is within bounds
        if y + 1 < self.model.grid.height:
            self.model.grid.move_agent(self, (x, y + 1))

class VehicleModel(Model):
    def __init__(self):
        super().__init__()
        self.grid = MultiGrid(11, 11, torus=False)
        self.schedule = SimultaneousActivation(self)

        # Create agent
        agent = VehicleAgent(1, self)
        self.grid.place_agent(agent, (5, 0))
        self.schedule.add(agent)

    def step(self):
        self.schedule.step()

# Create the model globally so it's persistent across requests
model = VehicleModel()

def move_agent(request):
    # Perform 10 steps of the simulation
    for _ in range(10):
        model.step()

    # Get the final position of the agent
    agent_position = [agent.pos for agent in model.schedule.agents][0]
    
    # Return the position as a JSON response
    return JsonResponse({"final_position": agent_position})
