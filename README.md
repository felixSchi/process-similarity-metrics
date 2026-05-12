# process-similarity-metrics

Python program to compute the M2T and T2T similarity between a business process model (bpmn-2.0) in .xml format and a textual process description in .txt format.

## How to run the code:

- First, run "pip install -r requirements.txt" in your console.

- To compute the m2t similarity of a bpmn model, run: "..." in your console.
  - Replace the path placeholders with the actual paths.
  - process decription: "data/text/process-description.txt"
  - bpmn models: "data/bpmn/[Model].xml" (Model = ["Claude", "GPT", "Llama"])
  - The code will now automatically perform the m2t similarity computations, compute all metrics and print the solutions in the console.

- To compute the t2t similarity of a bpmn model, run "..." in your console.
  - Replace the path placeholders with the actual paths.
  - process decription: "data/text/process-description.txt"
  - bpmn models: "data/bpmn/[Model].xml" (Model = ["Claude", "GPT", "Llama"])
  - The code will now automatically transform the model into a text, perform the t2t similarity computations, compute all metrics and print the solutions in the console.
