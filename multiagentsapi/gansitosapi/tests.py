import unittest
from models import VehicleModel, VehicleAgent

class TestVehicleAgent(unittest.TestCase):
    def test_calculate_best_route(self):
        model = VehicleModel(1, [(0, 0)], [(2, 2)])
        agent = model.schedule.agents[0]
        path = agent.calculateBestRoute()
        expected_path = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]
        self.assertEqual(path, expected_path)

    def test_agent_reaches_objective(self):
        model = VehicleModel(1, [(0, 0)], [(2, 2)])
        agent = model.schedule.agents[0]
        agent.calculateBestRoute()
        while agent.pos != agent.objective:
            agent.step()
        self.assertEqual(agent.pos, agent.objective)

if __name__ == '__main__':
    unittest.main()

