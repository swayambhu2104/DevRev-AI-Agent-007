import re

def pddl_to_solution_function(pddl_code):
     solution = []

     encoded_tasks = pddl_code.split(':action')[1:]
     for encoded_task in encoded_tasks:
          tasks = encoded_task.split(':effect')[1:]
          decoded_task = {}
          for task in tasks:
               data = task.split('argument_of')[1].split()
               decoded_task['tool_name'] = data[0]
               data = [re.sub('[()"]', '', i) for i in data][1:]
               decoded_task['arguments'] = []
               for i in range(0, len(data) - 1, 2):
                    if data[i] == '': continue
                    argument = {}
                    argument['argument_name'] = data[i]
                    argument['argument_value'] = data[i + 1]
                    decoded_task['arguments'].append(argument)
               
          solution.append(decoded_task)
     return solution