# Recursion-of-Thought:

This folder contains the code used to test the Recursion of Thought prompting technique as a potential solution for our problem statement.


#### OpenAI integration:

To access OpenAI's API, integrate your OpenAI key in openai.txt file


#### Tool and Argument Documentation:

The comprehensive list of essential tools and arguments is documented in the 'functions.py' file. To extend functionality, users have the flexibility to introduce new functions by editing this file.


## Methodology

Recursion of Thought is an approach in problem-solving that involves breaking down complex tasks into smaller subproblems and recursively solving them to derive the final solution. There are 4 parts in the methodology used: 

### 1. Problem Definition and Context:
The methodology begins with defining the problem or query that requires a solution. Each problem is formulated to include the main question (Q) and the expected answer sequence (A).


### 2. Special Tokens and Context Division:
RoT introduces special tokens, namely GO, STOP, and THINK, to guide the LLM in generating recursive intermediate steps. The GO and STOP tokens mark the start and end of a problem sequence, while THINK initiates a recursion procedure. These tokens facilitate the division of the problem into multiple contexts, allowing the model to handle problems exceeding the maximum context size.


### 3. Inference and Context Generation:
The LLM is tasked with inferring the probability of the next token given a sequence (p(xi+1 | X1:i)). The inference process involves generating contexts (X) based on the concatenation of the main question (Q), subproblems (Qsub,), and their corresponding answers (Asub,). The recursive context control allows the model to create multiple contexts by producing special tokens, effectively dividing the problem into manageable segments.


### 4. Recursive Problem-Solving:
During the inference process, the LLM solves multiple subproblems by generating sub-questions (Qsub,) and their respective answers (Asub,). The key innovation lies in the use of the THINK token, which triggers a recursive process, separating the sub-question into a new context. If the new context is a base case, the answer is produced directly; otherwise, the model recursively solves more subproblems.


## Local setup (Installing dependencies)

 `pip install -r requirements.txt`

## Solving the query using ``` rot ``` function

 Customize the query below to suit the reporting needs.
 ```
from Recursion_of_thought_experiment.Recursion_of_Thought import rot
query = "Retrieve work items associated with the Rev organization Rev-789 and tickets that need a response, and create a summary."
rot(query)
```

## Sample result:
```
1. Divide the problem into subproblems:

Subproblem 1: Retrieve work items associated with the Rev organisation 'Rev-789'.
Subproblem 2: Filter work items from Subproblem 1 to only include those that need a response.
Subproblem 3: Create a summary of the work items obtained from Subproblem 2.

2. Generate GO and STOP tokens:
GO
... Subproblem 1 ...
... Subproblem 2 ...
... Subproblem 3 ...
STOP

3. Solve each subproblem recursively:

For Subproblem 1, use the "works_list" tool with the argument "ticket.rev_org" set to "Rev-789."
For Subproblem 2, use the "works_list" tool with the argument "ticket.needs_response" set to true and "objects" set to the output of Subproblem 1.
Subproblem 3 does not require further division and can be solved directly using the "summarize_objects" tool with the argument "objects" set to the output of Subproblem 2.

4. Use appropriate tools and combine the outputs of Subproblems 1, 2, and 3. Replace the corresponding THINK tokens with the actual results obtained from each subproblem.

The final answer is the summarized list of work items associated with 'REV-789' that need a response.

json
[
  {
    "tool_name": "works_list",
    "arguments": [
      {
        "argument_name": "ticket.rev_org",
        "argument_value": "Rev-789"
      }
    ]
  },
  {
    "tool_name": "works_list",
    "arguments": [
      {
        "argument_name": "objects",
        "argument_value": "$$PREV[0]"
      },
      {
        "argument_name": "ticket.needs_response",
        "argument_value": "true"
      }
    ]
  },
  {
    "tool_name": "summarize_objects",
    "arguments": [
      {
        "argument_name": "objects",
        "argument_value": "$$PREV[1]"
      }
    ]
  }
]
```

## Analysis
The lengths of the Chain of Thought (CoT) can rapidly expand with the complexity of a problem, often surpassing the maximum context size. Recursion of Thought (RoT), can address this challenge. RoT introduces several special tokens that the models can output to trigger context-related operations.This allows the model to break down a problem into different contexts, offering a more versatile approach to handling complex tasks. RoT demonstrates a remarkable enhancement in LLMs' reasoning capabilities. By introducing special tokens and recursive context control, the technique enables models to break down complex problems into manageable segments. This results in improved accuracy in solving problems with reasoning steps extending beyond the traditional context limits.


However, the introduction of recursive processes and multiple contexts may incur computational overhead. While RoT demonstrates effectiveness in solving complex problems, it is crucial to consider the potential impact on computational resources, especially when dealing with large-scale reasoning tasks.

## Bibliography
[Source Paper](https://arxiv.org/abs/2306.06891)
