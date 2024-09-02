from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .models import VehicleModel  # Import VehicleModel from models.py
import json

# Create the model globally so it's persistent across requests
model = None

@csrf_exempt
def initialize_model(request):
    global model
    if request.method == 'POST':
        data = json.loads(request.body)
        numberOfAgents = data.get('numberOfAgents', 1)
        initial_positions = data.get('initialPositions', [])
        objectives = data.get('objectives', [])

        if len(initial_positions) != numberOfAgents or len(objectives) != numberOfAgents:
            return JsonResponse({'status': 'error', 'message': 'Initial positions and objectives must match the number of agents'}, status=400)

        model = VehicleModel(numberOfAgents, initial_positions, objectives)
        return JsonResponse({'status': 'success', 'message': f'Model initialized with {numberOfAgents} agents'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

def move_agent(request):
    global model
    if model is None:
        return JsonResponse({'status': 'error', 'message': 'Model not initialized'}, status=400)

    agent_positions = {}
    model.reboot_position()

    # max steps para evitar loops gigantes
    MAX_STEPS = 1000 
    step = 0

    while step < MAX_STEPS:
        model.step()
        step += 1
        positions = [agent.pos for agent in model.schedule.agents]
        agent_positions[f"Step {step}"] = positions
        
        all_reached = all(agent.pos == agent.objective for agent in model.schedule.agents)
        if all_reached:
            break

    if step >= MAX_STEPS:
        print("Max steps reached, some agents may not have reached their objectives.")
        agent_positions['status'] = 'incomplete'
    else:
        agent_positions['status'] = 'complete'

    return JsonResponse(agent_positions)


def delete_agent(request, agent_id):
    global model
    if model is None:
        return JsonResponse({'status': 'error', 'message': 'Model not initialized'}, status=400)

    model.remove_agent(agent_id)
    return JsonResponse({'status': 'success', 'message': f'Agent {agent_id} removed'})

def delete_all_agents(request):
    global model
    if model is None:
        return JsonResponse({'status': 'error', 'message': 'Model not initialized'}, status=400)

    model.remove_all_agents()
    return JsonResponse({'status': 'success', 'message': 'All agents removed'})

def root_page(request):
    return


