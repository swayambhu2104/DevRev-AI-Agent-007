import os
from langchain import hub
from langchain.chat_models import ChatOpenAI
from typing import Sequence, List, Tuple, Optional, Any
from langchain.agents.agent import Agent, AgentOutputParser
from langchain.prompts.prompt import PromptTemplate
from langchain.prompts.base import BasePromptTemplate
from langchain.tools.base import BaseTool
from langchain.agents import Tool, initialize_agent, AgentExecutor, AgentType
from langchain.llms import OpenAI
from langchain.agents.react.output_parser import ReActOutputParser
from langchain_core.exceptions import OutputParserException
from langchain.tools.render import render_text_description, render_text_description_and_args
from langchain.agents.output_parsers import ReActJsonSingleInputOutputParser
from langchain.agents.format_scratchpad import format_log_to_str
from pydantic import BaseModel, Field

def read_api_key_from_file(file_path):
    with open(file_path, 'r') as file:
        api_key = file.read().strip()
    return api_key

openai_api_key = read_api_key_from_file('openai_key.txt')
os.environ['OPENAI_API_KEY'] = openai_api_key
prompt = hub.pull("hwchase17/react-json")

class Issue():
    def __init__(self, priority = [], rev_orgs = []):
        self.priority = priority
        self.rev_orgs = rev_orgs

        allowed_priorities = ['p0', 'p1', 'p2', 'p3']
        if type(priority) == str: 
            priority_condition = False
            for allowed_priority in allowed_priorities:
                if priority == allowed_priority:
                    priority_condition = True
            if not priority_condition:
                raise AssertionError('Wrong Priority given. It should be one of these values -> [\'p0\', \'p1\', \'p2\', \'p3\']')
        else:
            for p in priority:
                priority_condition = False
                for allowed_priority in allowed_priorities:
                    if p == allowed_priority:
                        priority_condition = True
                if not priority_condition:
                    raise AssertionError('Wrong Priority given. It should be one of these values -> [\'p0\', \'p1\', \'p2\', \'p3\']')

class Ticket():
    def __init__(self, needs_response = bool, rev_org = [], severity = [], source_channel = []):
        self.needs_response = needs_response
        self.rev_org = rev_org
        self.severity = severity
        self.source_channel = source_channel

        allowed_severities = ['blocker', 'high', 'low', 'medium']
        if type(severity) == str:
            severity_condition = False
            for allowed_severity in allowed_severities:
                if severity == allowed_severity:
                    severity_condition = True
            if not severity_condition:
                raise AssertionError('Wrong Severity given. It should be one of these values -> [\'blocker\', \'high\', \'low\', \'medium\']')
        else:
            for s in severity:
                severity_condition = False
                for allowed_severity in allowed_severities:
                    if s == allowed_severity:
                        severity_condition = True
                if not severity_condition:
                    raise AssertionError('Wrong Severity given. It should be one of these values -> [\'blocker\', \'high\', \'low\', \'medium\']')

class Stage():
    def __init__(self, name = []):
        self.name = name

issue = Issue()
stage = Stage()
ticket = Ticket()

def works_list(input):
    return 'works_list'

class works_list_input(BaseModel):
    applies_to_part: List[str] = Field(default=[])
    created_by: List[str] = Field(default=[])
    issue.priority: List[str] = Field(default=[])
    issue.rev_orgs: List[str] = Field(default=[])
    limit: int = Field(default=50)
    owned_by: List[str] = Field(default=[])
    stage.name: List[str] = Field(default=[])
    ticket.rev_org: List[str] = Field(default=[])
    ticket.severity: List[str] = Field(default=[])
    ticket.source_channel: List[str] = Field(default=[])
    type: List[str] = Field(pattern=r'issue|ticket|task', default=[])

def summarize_objects(input):
    print(input)
    print('summary of the objects')
    return ['summary of the objects']

class summarize_objects_input(BaseModel):
    objects: List[Any] = Field(default=[])

def prioritize_objects(input):
    return 'A list of prioritized objects'

class prioritize_objects_input(BaseModel):
    objects: List[Any] = Field(default=[])

def add_work_items_to_sprint(input):
    return 'work items to sprint has been added'

class add_work_items_to_sprint_input(BaseModel):
    work_ids: List[str] = Field(default=[])
    sprint_id: str = Field(default='')

def get_sprint_id():
    return 'sprint_id'

def get_similar_work_items(input):
    print('similiar_work_items')
    return 'similiar_work_items'

class get_similar_work_items_input(BaseModel):
    work_id: str = Field(default='')

def search_object_by_name(input):
    return 'searched objects'

class search_object_by_name_input(BaseModel):
    query: str = Field(default='')

def create_actionable_tasks_from_text(input):
    return 'list of actionable tasks'

class create_actionable_tasks_from_text_input(BaseModel):
    text: str = Field(default='')

def who_am_i():
    return 'who am I'