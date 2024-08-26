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
        self.agent = VehicleAgent(1, self)
        self.grid.place_agent(self.agent, (5, 0))
        self.schedule.add(self.agent)

    def step(self):
        self.schedule.step()
        
    def reboot_position(self):
        self.grid.place_agent(self.agent, (5, 0))
        

# Create the model globally so it's persistent across requests
model = VehicleModel()

def move_agent(request):
    agent_positions = {}
    model.reboot_position()

    # Perform 10 steps
    for step in range(10):
        model.step()
        # Get the position of each agent
        positions = [agent.pos for agent in model.schedule.agents]
        # Store the positions with the step number as the key
        agent_positions[f"Step {step + 1}"] = positions

    # Return the positions as a JSON response
    return JsonResponse(agent_positions)