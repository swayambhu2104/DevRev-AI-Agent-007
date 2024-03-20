from model.openai_models import OpenAILanguageModel, OptimizedOpenAILanguageModel
from treeofthoughts import TreeofThoughts, MonteCarloTreeofThoughts, TreeofThoughtsBFS, TreeofThoughtsDFS, TreeofThoughtsBEST, TreeofThoughtsASearch
from model.abstract_language_model import AbstractLanguageModel
from model.huggingface_model import HuggingLanguageModel, HFPipelineModel
import re

def read_api_key_from_file(file_path='openai.txt'):
    with open(file_path, 'r') as file:
        api_key = file.read().strip()
    return api_key

def MonteCarloToT(query):
    # Setting up the API Key and Model:
    api_model = "gpt-4" # Specifies the OpenAI language model to be used (in this case, GPT-4).
    api_key = read_api_key_from_file() # Specifies the API key for accessing the OpenAI API.

    # Initializing the Language Model and MonteCarloTreeofThoughts:
    model = OpenAILanguageModel(api_key=api_key, api_model=api_model) # Creates an instance of the OpenAILanguageModel class using the specified API key and model.
    tree_of_thoughts = MonteCarloTreeofThoughts(model) # Creates an instance of the MonteCarloTreeofThoughts class, extending TreeofThoughts, with the language model.

    initial_prompt = """
    Query: """ + query + """
    Functions: name, description, parameters
              works_list,	Returns a list of work items matching the request.,	{{'type': 'object', 'properties': {{'applies_to_part': {{'title': 'applies_to_part', 'type': 'array of strings', 'description': 'Filters for work belonging to any of the provided parts.', 'example': ['FEAT-123', 'ENH-123', 'PROD-123', 'CAPL-123']}}, 'created_by': {{'title': 'created_by', 'type': 'array of strings', 'description': 'Filters for work created by any of these users.', 'example': ['DEVU-123']}}, 'issue.priority': {{'title': 'issue.priority', 'type': 'array of strings', 'description': 'Filters for issues with any of the provided priorities. Allowed values: p0, p1, p2, p3.', 'example': ['p0', 'p1']}}, 'issue.rev_orgs': {{'title': 'issue.rev_orgs', 'type': 'array of strings', 'description': 'Filters for issues with any of the provided Rev organizations.', 'example': ['REV-123']}}, 'limit': {{'title': 'limit', 'type': 'integer (int32)', 'description': 'The maximum number of works to return. The default is 50.', 'example': 50}}, 'owned_by': {{'title': 'owned_by', 'type': 'array of strings', 'description': 'Filters for work owned by any of these users.', 'example': ['DEVU-123']}}, 'stage.name': {{'title': 'stage.name', 'type': 'array of strings', 'description': 'Filters for records in the provided stage(s) by name.', 'example': ['Stage-A', 'Stage-B']}}, 'ticket.needs_response': {{'title': 'ticket.needs_response', 'type': 'boolean', 'description': 'Filters for tickets that need a response.', 'example': True}}, 'ticket.rev_org': {{'title': 'ticket.rev_org', 'type': 'array of strings', 'description': 'Filters for tickets associated with any of the provided Rev organizations.', 'example': ['REV-123']}}, 'ticket.severity': {{'title': 'ticket.severity', 'type': 'array of strings', 'description': 'Filters for tickets with any of the provided severities. Allowed values: blocker, high, low, medium.', 'example': ['high', 'medium']}}, 'ticket.source_channel': {{'title': 'ticket.source_channel', 'type': 'array of strings', 'description': 'Filters for tickets with any of the provided source channels.', 'example': ['Email', 'Chat']}}, 'type': {{'title': 'type', 'type': 'array of strings', 'description': 'Filters for work of the provided types. Allowed values: issue, ticket, task.', 'example': ['issue', 'task']}}}}, 'required': []}}
              summarize_objects,	Summarizes a list of objects. The logic of how to summarize a particular object type is an internal implementation detail.,	{{'type': 'object', 'properties': {{'objects': {{'title': 'objects', 'type': 'array of objects', 'description': 'List of objects to summarize.', 'example': [{'id': 1, 'name': 'Object-A'}, {'id': 2, 'name': 'Object-B'}]}}}}, 'required': []}}
              prioritize_objects,	Returns a list of objects sorted by priority. The logic of what constitutes priority for a given object is an internal implementation detail.,	{{'type': 'object', 'properties': {{'objects': {{'title': 'objects', 'type': 'array of objects', 'description': 'A list of objects to be prioritized.', 'example': [{'id': 1, 'priority': 'high'}, {'id': 2, 'priority': 'medium'}]}}}}, 'required': []}}
              add_work_items_to_sprint,	Adds the given work items to the sprint.,	{{'type': 'object', 'properties': {{'work_ids': {{'title': 'work_ids', 'type': 'array of strings', 'description': 'A list of work item IDs to be added to the sprint.', 'example': ['WI-001', 'WI-002']}}, 'sprint_id': {{'title': 'sprint_id', 'type': 'str', 'description': 'The ID of the sprint to which the work items should be added.', 'example': 'Sprint-001'}}}}, 'required': []}}
              get_sprint_id,	Returns the ID of the current sprint.,	{{'type': 'object', 'properties': {{}}}}
              get_similar_work_items,	Returns a list of work items that are similar to the given work item.,	{{'type': 'object', 'properties': {{'work_id': {{'title': 'work_id', 'type': 'string', 'description': 'The ID of the work item for which you want to find similar items.', 'example': 'WI-123'}}}}, 'required': []}}
              search_object_by_name,	Given a search string, returns the ID of a matching object in the system of record. If multiple matches are found, it returns the one where the confidence is highest.	{{'type': 'object', 'properties': {{'query': {{'title': 'query', 'type': 'string', 'description': 'The search string, could be for example customerâ€™s name, part name, user name.', 'example': 'John Doe'}}}}, 'required': []}}
              create_actionable_tasks_from_text,	Given a text, extracts actionable insights, and creates tasks for them, which are kind of a work item.,	{{'type': 'object', 'properties': {{'text': {{'title': 'text', 'type': 'string', 'description': 'The text from which the actionable insights need to be created.', 'example': 'Extract actionable insights from this text.'}}}}, 'required': []}}

        
    Input: Create an ouput JSON structure to solve the Query using Functions. Give the name to fucntion used as "tool_name" and name the parameters as "arguments" and inside "arguments" make keys as "argument_name" and "argument_value" and assign the respective parameter name and values. To reference the value of the ith tool in the chain, use $$PREV[i] as argument value. i =0, 1, .. j-1; j = current tools index in the array
    If the query could not be answered with the given set of tools, output an empty list instead.
    """
    solution = tree_of_thoughts.solve(initial_prompt=initial_prompt)

