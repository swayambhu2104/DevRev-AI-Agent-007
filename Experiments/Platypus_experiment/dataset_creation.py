import datasets
import pandas as pd
import json

input =  '''You are an AI assistant designed to help developers in their day to day tasks by automating their requests using tools available to them.

The actions defined in this domain are:

The works_list action: Returns a list of work items matching the request. It has the following parameters: 
	applies_to_part: Filters for work belonging to any of the provided parts.
	created_by: Filters for work created by any of these users.
	issue.priority: Filters for issues with any of the provided priorities. Allowed values: p0, p1, p2, p3.
	issue.rev_orgs: Filters for issues with any of the provided Rev organizations.
	limit: The maximum number of works to return. The default is '50'.
	owned_by: Filters for work owned by any of these users.
	stage.name: Filters for records in the provided stage(s) by name.
	ticket.needs_response: Filters for tickets that need a response.
	ticket.rev_org: Filters for tickets associated with any of the provided Rev organizations.
	ticket.severity: Filters for tickets with any of the provided severities. Allowed values: blocker, high, low, medium.
	ticket.source_channel: Filters for tickets with any of the provided source channels.
	type: Filters for work of the provided types. Allowed values: issue, ticket, task.


The summarize_objects action: Summarizes a list of objects. The logic of how to summarize a particular object type is an internal implementation detail. It has the following parameters: 
	objects: List of objects to summarize.


The prioritize_objects action: Returns a list of objects sorted by priority. The logic of what constitutes priority for a given object is an internal implementation detail. It has the following parameters: 
	objects: A list of objects to be prioritized.


The add_work_items_to_sprint action: Adds the given work items to the sprint. It has the following parameters: 
	work_ids: A list of work item IDs to be added to the sprint.
	sprint_id: The ID of the sprint to which the work items should be added.


The get_sprint_id action: Returns the ID of the current sprint. It has no parameters. 

The get_similar_work_items action: Returns a list of work items that are similar to the given work item. It has the following parameters: 
	work_id: The ID of the work item for which you want to find similar items.


The search_object_by_name action: Given a search string, returns the ID of a matching object in the system of record. If multiple matches are found, it returns the one where the confidence is highest. It has the following parameters: 
	query: The search string, could be for example customer’s name, part name, user name.


The create_actionable_tasks_from_text action: Given a text, extracts actionable insights, and creates tasks for them, which are kind of a work item. It has the following parameters: 
	text: The text from which the actionable insights need to be created.


The who_am_i action: Returns the ID of the current user. It has no parameters. 
'''

dataset_csv = pd.read_csv('../data/Dataset.csv')

dataset_csv.rename(columns={'Query':'instruction', 'Output':'output'}, inplace=True)
dataset_csv['input'] = input
dataset_csv['data_source'] = ''
dataset_csv.to_json(path_or_buf='dataset_train.json', indent=4, orient='records')
dataset_csv.to_csv('dataset_train.csv', index=False)

