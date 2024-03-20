from openai import OpenAI
import functions

def read_api_key_from_file(file_path='Recursion_of_thought_experiment/openai.txt'):
    with open(file_path, 'r') as file:
        api_key = file.read().strip()
    return api_key

def examples(file_path='Recursion_of_thought_experiment/example_queries.txt'):
    with open(file_path, 'r') as file:
      return file.read()

def rot(query):
 client = OpenAI(api_key=read_api_key_from_file())
 
 prompt=f"""You need to answer the given query by giving an output in JSON format of the tools, argument names, argument values which are needed to solve the query.If the query cannot be solved by the list of tools I provide then outout an empty list.
 The following is the list of tools,argument names,descriptions,examples etc. Understand the functionality of each tool and argument:
 {functions.devrev_functions}
 
 
 To reference the value of the ith tool in the chain, use $$PREV[i] as argument value. i =
 0, 1, .. j-1; j = current tool’s index in the array
 If the query could not be answered with the given set of tools, output an empty list instead.
 
   Sample queries and their outputs:
   {examples()}
 
 The output is in JSON format. This is my problem statement.""" 
 reasoning = """Example:Now if the query is "Retrieve work items associated with the Rev organisation 'REV-123' and owned by the user 'DEVU-789' , Summarize them and prioritize by severity.",
 then the steps u need to follow are the steps the model should follow in recursion of thought (RoT).You should output all these steps when a new query is given to you,along with the output.
 
 1.Divide the problem into subproblems:
 
 Subproblem 1: Retrieve work items associated with the Rev organisation 'REV-123'.
 Subproblem 2: Filter work items from Subproblem 1 to only include those owned by the user 'DEVU-789.'
 Subproblem 3: Summarize the work items obtained from Subproblem 2.
 Subproblem 4: Prioritize the summarized work items by severity.
 
 2.Generate GO and STOP tokens:
 GO
 ... Subproblem 1 ...
 ... Subproblem 2 ...
 ... Subproblem 3 ...
 ... Subproblem 4 ...
 STOP
 
 3.Solve each subproblem recursively:
 
 For Subproblem 1, use the "works_list" tool with the argument "ticket.rev_org" set to "REV-123."
 For Subproblem 2, use the "works_list" tool with the arguments "owned_by" set to "DEVU-789" and "objects" set to the output of Subproblem 1.
 Subproblem 3 does not require further division and can be solved directly using the "summarize_objects" tool with the argument "objects" set to the output of Subproblem 2.
 Subproblem 4 does not require further division and can be solved directly using the "prioritize_objects" tool with the argument "objects" set to the output of Subproblem 3.
 
 4.Use appropriate tools and combine the outputs of Subproblems 1, 2, 3, and 4.Replace the corresponding THINK tokens with the actual results obtained from each subproblem.
 The final answer is the prioritized list of work items associated with 'REV-123,' owned by 'DEVU-789,' and summarized.
 
 "[
     {
         ""tool_name"": ""works_list"",
         ""arguments"": [
             {
                 ""argument_name"": ""ticket.rev_org"",
                 ""argument_value"": ""REV-123""
             },
             {
                 ""argument_name"": ""owned_by"",
                 ""argument_value"": ""DEVU-789""
             }
         ]
     },
     {
         ""tool_name"": ""summarize_objects"",
         ""arguments"": [
             {
                 ""argument_name"": ""objects"",
                 ""argument_value"": ""$$PREV[0]""
             }
         ]
     },
     {
         ""tool_name"": ""prioritize_objects"",
         ""arguments"": [
             {
                 ""argument_name"": ""objects"",
                 ""argument_value"": ""$$PREV[1]""
             }
         ]
     }
 ]
 "
 
 
 
 
 Now follow the same approach,after looking at the example above and answer the query. Refer to the sample queries and the outputs I had given.
 Give the final output in json format. """
 add = f"{query}. I would like u to follow the steps through which the problem can be solved like the example above and reach the end output."
 tup = (prompt,reasoning,add)
 prompt_final = ' '.join(tup)
 
 
 completion = client.chat.completions.create(
     model="gpt-4",
     messages=[
         {
             "role": "user",
             "content": prompt_final,
         },
     ],
 )
 print(completion.choices[0].message.content)
