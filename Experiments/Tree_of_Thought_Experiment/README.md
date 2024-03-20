# Tree-of-Thought
This repository contains the code used to test the ToT (Tree of Thoughts) prompting technique as a potential solution for our problem statement

### Usage of this repository 
Please refer the documentation for detailed guidance on utilizing the functionalities provided by this repository. The documentation outlines instructions on how to effectively use the repository, including comprehensive information on its features and functionalities. 

### OpenAI Integration
To access OpenAI's API, integrate your OpenAI key in openai.txt file

## Using MonteCarlo Tot approach to solve a query
`pip install -r requirements.txt`


```
from MonteCarlo_TOT import MonteCarloToT
query = "Get the current user's ID, find all work items in the 'development' stage, owned by that user, and have 'p1' priority."
MonteCarloToT(query)
```

## Methodology
ToT maintains a tree of thoughts, where thoughts represent coherent language sequences that serve as intermediate steps toward solving a problem. This approach enables an LM to self evaluate the progress intermediate thoughts make towards solving a problem through a deliberate reasoning process. The LM's ability to generate and evaluate thoughts is then combined with search algorithms (e.g., breadth-first search and depth-first search) to enable systematic exploration of thoughts with lookahead and backtracking. It follows the following steps -


### 1. Thought decomposition 
Unlike CoT prompting, ToT explicitly decomposes a problem into intermediate steps or thoughts, which are combined together to form a solution to the underlying problem. Depending on the problem, this decomposition can take a variety of different forms, such as outputting a few words or a single line of an equation.


### 2. Thought generation  
Once we have decided what will constitute a thought, we need to determine how thoughts should be generated during ToT prompting. Two basic techniques for thought generation are proposed:
#### a) Sampling: generating several thoughts independently with the same prompt
#### b) Proposing: generating several thoughts sequentially with a “propose prompt
The sampling approach works best when the thought space is rich, as several independently-generated thoughts are unlikely to be duplicates. If the thought space is more constrained, then the proposing technique can be used to generate several thoughts while avoiding duplicates.


### 3. State evaluation  
Once we have defined our thoughts and chosen how they will be generated, we need to define a heuristic for evaluating the quality of certain chains of thought. Otherwise, there is no way to know whether we are making progress towards a final solution. Given several thoughts that have been generated, an LLM is used to reason about the quality of each thought. In particular, two different strategies are followed:
#### 1. Value: 
independently assign a scalar value (i.e., rating from 1-10) or classification (i.e., sure, likely, or impossible to reach a solution) to each state.
#### 2. Vote: 
compare different solutions and select the one that is most promising.

Although both approaches can work well, voting is best when a successful solution
to a problem is hard to directly value (e.g., creative writing tasks). In both cases,
the LLM can be prompted multiple times in a manner similar to self-consistency to
achieve more reliable evaluations of each state.

### Search algorithm 
The final component of ToT prompting is the search algorithm
that is used to explore the solution space.


## Analysis
Tree-of-Thought (ToT) Prompting is an innovative technique that builds upon the principles of the Tree-of-Thoughts framework and expands the capabilities of the well-known Chain-of-Thought prompting concept. Adopting this approach, empowers Large Language Models, such as ChatGPT, and Bard to demonstrate advanced reasoning abilities. The Tree-of-Thought Prompting technique enables these models to autonomously rectify errors and continuously accumulate knowledge, resulting in enhanced performance and improved decision-making. Tree of thought gives the best accuracy of all the methods and even solves queries which involves some additional logic like combining the outputs of various functions, like mathematical operations, iterations, conditional logic etc and solves the bonus task. 

The only downside is it makes a lot of requests and consumes high number of tokens, which made it unfeasible for our problem. 


## Sample Result
1. Search for objects related to ProductABC, retrieve work items related to the search results, and then add them to the current sprint.
```
[
  {
    "tool_name": "search_object_by_name",
    "arguments": [
      {
        "argument_name": "query",
        "argument_value": "ProductABC"
      }
    ]
  },
  {
    "tool_name": "works_list",
    "arguments": [
      {
        "argument_name": "applies_to_part",
        "argument_value": ["$$PREV[0]"]
      }
    ]
  },
  {
    "tool_name": "get_sprint_id",
    "arguments": []
  },
  {
    "tool_name": "add_work_items_to_sprint",
    "arguments": [
      {
        "argument_name": "work_ids",
        "argument_value": ["$$PREV[1]"]
      },
      {
        "argument_name": "sprint_id",
        "argument_value": "$$PREV[2]"
      }
    ]
  }
]
```

2. Retrieve all issue work items that need a response and are associated with the Rev organization REV-789
```
  [
    {
        "tool_name": "works_list",
        "arguments": [
            {
                "argument_name": "ticket.needs_response",
                "argument_value": true
            },
            {
                "argument_name": "ticket.rev_org",
                "argument_value": "REV-789"
            },
            {
                "argument_name": "type",
                "argument_value": "issue"
            }
        ]
    }
]
```


## Bibliography
[source-paper](https://arxiv.org/pdf/2305.10601.pdf)

[source-code](https://github.com/kyegomez/tree-of-thoughts)
