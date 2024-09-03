from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .models import VehicleModel 
import json

model = None

@csrf_exempt
def initialize_model(request):
    global model
    if request.method == 'POST':
        data = json.loads(request.body)
        numberOfAgents = data.get('numberOfAgents', 1)
        initial_positions = data.get('initialPositions', [])
        objectives = data.get('objectives', [])

        # checamos si alguna de estas no es del tipo int, si no lo es, checamos si es float y lo convertimos. de no ser float, 400
        if isinstance(numberOfAgents, float):
            numberOfAgents = int(numberOfAgents)
        elif not isinstance(numberOfAgents, int):
            return JsonResponse({'status': 'error', 'message': 'numberOfAgents must be an integer or float convertible to integer'}, status=400)

        try:
            initial_positions = [[int(coord) if isinstance(coord, (int, float)) else None for coord in pos] for pos in initial_positions]
            objectives = [[int(coord) if isinstance(coord, (int, float)) else None for coord in obj] for obj in objectives]
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Initial positions and objectives must be lists of integers or floats convertible to integers'}, status=400)

        # Ensure no None values were introduced during conversion
        if any(None in pos for pos in initial_positions) or any( None in obj for obj in objectives ):
            return JsonResponse({'status': 'error', 'message': 'Initial positions and objectives must be lists of integers or floats convertible to integers'}, status=400)

        # Check if the length of initial_positions and objectives matches numberOfAgents
        if len(initial_positions) != numberOfAgents or len(objectives) != numberOfAgents:
            return JsonResponse({'status': 'error', 'message': 'Initial positions and objectives must match the number of agents'}, status=400)

        model = VehicleModel(numberOfAgents, initial_positions, objectives)
        return JsonResponse({'status': 'success', 'message': f'Model initialized with {numberOfAgents} agents'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

def move_agent(request):
    global model
    if model is None:
        return JsonResponse({'status': 'error', 'message': 'Model not initialized'}, status=400)

    agent_steps = {agent.unique_id: [] for agent in model.schedule.agents}
    model.reboot_position()

    # max steps to avoid infinite loops
    MAX_STEPS = 1000 
    step = 0

    while step < MAX_STEPS:
        model.step()
        step += 1
        for agent in model.schedule.agents:
            agent_steps[agent.unique_id].append(agent.pos)
        
        all_reached = all(agent.pos == agent.objective for agent in model.schedule.agents)
        if all_reached:
            break

    if step >= MAX_STEPS:
        print("Max steps reached, some agents may not have reached their objectives.")
        agent_steps['status'] = 'incomplete'
    else:
        agent_steps['status'] = 'complete'

    return JsonResponse(agent_steps)

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


