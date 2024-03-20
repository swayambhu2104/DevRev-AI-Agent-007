import re
from environment import *

# Create a list of tools
tools = [
    Tool.from_function(
        func=works_list,
        name='works_list',
        description='Returns a list of work items matching the request.',
        args_schema=works_list_input
    ),
    Tool.from_function(
        func=summarize_objects,
        name='summarize_objects',
        description='Summarizes a list of objects.',
        args_schema=summarize_objects_input
    ),
    Tool.from_function(
        func=prioritize_objects,
        name='prioritize_objects',
        description='Returns a list of objects sorted by priority.',
        args_schema=prioritize_objects_input
    ),
    Tool.from_function(
        func=add_work_items_to_sprint,
        name='add_work_items_to_sprint',
        description='Adds the given work items to the sprint.',
        args_schema=add_work_items_to_sprint_input
    ),
    Tool.from_function(
        func=get_sprint_id,
        name='get_sprint_id',
        description='Returns the ID of the current sprint.'
    ),
    Tool.from_function(
        func=get_similar_work_items,
        name='get_similar_work_items',
        description='Returns a list of work items that are similar to the given work item.',
        args_schema=get_similar_work_items_input
    ),
    Tool.from_function(
        func=search_object_by_name,
        name='search_object_by_name',
        description='Given a search string, returns the ID of a matching object in the system of record.',
        args_schema=search_object_by_name_input
    ),
    Tool.from_function(
        func=create_actionable_tasks_from_text,
        name='create_actionable_tasks_from_text',
        description='Given a text, extracts actionable insights, and creates tasks for them.',
        args_schema=create_actionable_tasks_from_text_input
    ),
    Tool.from_function(
        func=who_am_i,
        name='who_am_i',
        description='Returns the ID of the current user.'
    ),
]

chat_model = ChatOpenAI(temperature=0)
prompt = prompt.partial(
    tools=render_text_description_and_args(tools),
    tool_names=", ".join([t.name for t in tools]),
)
chat_model_with_stop = chat_model.bind(stop=["\nObservation"])
agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_log_to_str(x["intermediate_steps"]),
    }
    | prompt
    | chat_model_with_stop
    | ReActJsonSingleInputOutputParser()
)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, return_intermediate_steps=True, handle_parsing_errors=True)

def ReAct_function(query):
    response = agent_executor.invoke(
        {
            "input": query
        }
    )