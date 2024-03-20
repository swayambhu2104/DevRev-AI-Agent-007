import sys
sys.path.append(sys.path[0] + '/..')

from functions import devrev_functions
from example_pddl import problem, pddl_solution

def prompt_creater(query):
    prompt = 'You are an AI assistant designed to help developers in their day to day tasks by automating their requests using tools available to them.\n\n'

    prompt += 'The actions defined in this domain are:\n\n'

    actions = ''

    for i in devrev_functions:
        actions += 'The ' + i['name'] + ' action: '+  i['description']
        if not i['parameters']['properties']:
            actions += ' It has no parameters. \n'
        else:
            actions += ' It has the following parameters: \n'
            for j in i['parameters']['properties'].items():
                actions += '\t' + j[0] + ': ' + j[1]['description'] + '\n'
        actions += '\n'

    prompt += actions
    prompt += problem + pddl_solution 
    prompt += 'Now I have a new planning problem and its description is:\n\n'
    prompt += query + '\n\n'
    prompt += 'Provide me with the problem PDDL file that describes the new planning problem directly without further explanations? Only return the PDDL file. Do not return anything else.'
    return prompt

# print(prompt_creater('yes'))