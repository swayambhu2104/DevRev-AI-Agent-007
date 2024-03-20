# Dataset Generation

### The data generated includes two parts:
1) Query
2) JSON Schema

### Generation process:
1) A suitable prompt was created using the tools provided by Devrev.
2) The prompt was fed to ChatGPT (GPT-3.5).
3) The generated queries and JSON schemas were manually inspected for inaccuracies and rectified.
4) The validated queries and JSON schemas were added to the final dataset.

- **Bonus data**:
  
  > - Not every user query could be potentially solved by taking the composition of available
functions, and might need some additional logic around combining the outputs of those
functions, like mathematical operations, iterations, conditional logic etc.
  > - You would get bonus points if your solution can handle those cases/scenarios, rather than just being able to output the asked list of JSONs.
  1) To address these scenarios, the team developed tools capable of handling such cases.
  2) These tools were converted to a suitable prompt, and then fed to ChatGPT (GPT-3.5).
  3) The generated queries and JSON schemas were manually inspected for inaccuracies and rectified.
  4) The validated queries and JSON schemas were added to the final dataset.
