# myfunsearch

## FunSearch

FunSearch stands for Function Search. It is an evolutionary method that uses an LLM to discover new mathematical algorithms.

<img width="749" height="491" alt="image" src="https://github.com/user-attachments/assets/1b00d26c-bf0a-43a5-baf7-e63d87adaf9c" />

The Creator (LLM): We give the LLM a skeleton of Python code. Its job is to write the "body" of the function. It generates creative, sometimes crazy, code solutions.


The Judge (Evaluator): We take that code and actually run it to see if it works.
If the code fails or is wrong: Trash it.
If the code works well: Save it to a database.
