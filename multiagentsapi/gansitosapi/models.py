from mesa import Agent, Model
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid
import heapq

class VehicleAgent(Agent):
    def __init__(self, unique_id, model, initial_position, objective):
        super().__init__(unique_id, model)
        self.pos = tuple(initial_position) 
        self.objective = tuple(objective)
        self.path = self.calculateBestRoute() 
        self.path_index = 0

    def calculateBestRoute(self):
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        def get_neighbors(pos):
            neighbors = []
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (pos[0] + dx, pos[1] + dy)
                if 0 <= neighbor[0] < self.model.grid.width and 0 <= neighbor[1] < self.model.grid.height:
                    if self.model.grid.is_cell_empty(neighbor):
                        neighbors.append(neighbor)
            return neighbors

        start = self.pos
        goal = self.objective

        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: heuristic(start, goal)}
        closed_set = set()
        open_set_hash = set([start])

        while open_set:
            current = heapq.heappop(open_set)[1]
            open_set_hash.remove(current)

            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                path.reverse()
                self.path = path
                return path

            closed_set.add(current)

            for neighbor in get_neighbors(current):
                if neighbor in closed_set:
                    continue

                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    if neighbor not in open_set_hash:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))
                        open_set_hash.add(neighbor)

        return None  

    def step(self):
        if self.path_index < len(self.path):
            next_pos = self.path[self.path_index]
            self.model.grid.move_agent(self, next_pos)
            self.path_index += 1

    
class VehicleModel(Model):
    def __init__(self, n, initial_positions, objectives):
        super().__init__()
        self.grid = MultiGrid(11, 11, torus=False)
        self.schedule = SimultaneousActivation(self)
        self.n = n

        for i in range(self.n):
            initial_position = initial_positions[i]
            objective = objectives[i]
            agent = VehicleAgent(i + 1, self, tuple(initial_position), tuple(objective))
            self.grid.place_agent(agent, initial_position)
            self.schedule.add(agent)

    def step(self):
        self.schedule.step()
        
    def reboot_position(self):
        for agent in self.schedule.agents:
            self.grid.place_agent(agent, agent.pos)  

    def remove_all_agents(self):
        for agent in self.schedule.agents[:]:
            self.schedule.remove(agent)
            self.grid.remove_agent(agent)
