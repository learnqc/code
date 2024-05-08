# Building Quantum Software: A Developer's Guide



[<img src="/assets/images/Gonciulea-MEAP-HI.png">](https://www.manning.com/books/building-quantum-software)


[Building Quantum Software: A Developer's Guide](https://www.manning.com/books/building-quantum-software) will teach you the foundations of quantum computing, how to implement quantum computations, and when to take advantage of the benefits of quantum computing.

This repository ([https://github.com/learnqc/code](https://github.com/learnqc/code)) is the official companion to Building Quantum Software: A Developer's Guide. It includes the code for creating and running a quantum simulator, as well as a natural language assistant to help run quantum computations, exercises to accompany the book content, and a complete, standalone quantum simulator.

The code uses minimal dependencies to facilitate learning and ensure the longevity of its functionality. The notebooks for each chapter build incrementally on previous chapters, and only use code dependencies within each chapter module. 

Hume, our standalone quantum simulator, is the result of piecing together the code throughout the entire book.

# Resources
The book and its repository can help you at different levels:

* Read the book content and the inline code to learn the concepts behind quantum computing.
* Read or run the Jupyter notebooks in each chapter to interact with the code.
* Complete the exercises in each chapter to gain intuition and experience in problem-solving in quantum.
* Implement new experiments in notebooks, unit tests, or more complex applications to use your knowledge to create your own work in quantum.

In addition to the book, there are two more resources available for users:

* A series of mini applications based on specific topics in the book. These applications feature a simple UI that allows you to experiment with different concepts.
* An AI assistant that responds to written and spoken commands to run and visualize quantum computations.  
    
<!-- 
[TODO: mental model image]
-->

## Table of Contents

| Chapter                                                           | Code                                                                                                                                                                                                                          |
|-------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1. The Advantages and Challenges of Programming Quantum Computers | --                                                                                                                                                                                                                            |
| 2. A first look at quantum computations: the knapsack problem     | [ch02](https://github.com/learnqc/code/tree/main/src/ch02) / [notebook](https://github.com/learnqc/code/blob/main/src/ch02/ch02.ipynb)                                                                                        |
| 3. Single-qubit state and gates                                   | [ch03](https://github.com/learnqc/code/tree/main/src/ch03) / [notebook](https://github.com/learnqc/code/blob/main/src/ch03/ch03.ipynb) / [exercises](https://github.com/learnqc/code/blob/main/src/ch03/ch03_exercises.ipynb) |
| 4. Quantum state and circuits: beyond one qubit                   | [ch04](https://github.com/learnqc/code/tree/main/src/ch04) / [notebook](https://github.com/learnqc/code/blob/main/src/ch04/ch04.ipynb) / [exercises](https://github.com/learnqc/code/blob/main/src/ch04/ch04_exercises.ipynb) |
| 5. Selecting outcomes with quantum oracles                   | [ch05](https://github.com/learnqc/code/tree/main/src/ch05) / [notebook](https://github.com/learnqc/code/blob/main/src/ch05/ch05.ipynb) / [exercises](https://github.com/learnqc/code/blob/main/src/ch05/ch05_exercises.ipynb) |
## Getting Started
Below you'll find the structure of the repository and instructions for how to get started with using the code.

### Overview of contents and structure
<pre>
├── README.md
├── src                            # notebooks are designed to run from the src directory
│   ├── chXX
│   │   ├── chXX.ipynb             # notebook with chapter code that can be used for experimentation
│   │   ├── chXX_exercises.ipynb   # notebook with chapter exercises and solutions
│   │   └── x.py                   # the source code introduced in each chapter
│   ├── hume                       # the complete quantum simulator implemented over the course of the book
│   ├── ibmq                       # real quantum hardware experiments using IBMQ Quantum Platform Open Plan
│   ├── ...
</pre>

### Setting up the code
#### Clone repository
Start by cloning the repository:
```bash
 git clone https://github.com/learnqc/code
```

#### Runing the notebooks with Docker

Navigate to the project root directory:

```bash
cd code
```

Build the image for the Jupyter Notebook server:

```bash
docker-compose build
```

Start the Jupyter Notebook server:

```bash
docker-compose up
```

After running this command, the Jupyter Notebook server should be accessible at `http://localhost:8888` in your browser, Jupyter token is `token`

#### Using GitHub Code Spaces or Dev Containers VSCode pluging

This setup can also be used with GitHub Code Spaces. All the necessary configuration is provided in the devcontainer.json file. Just open this repository in a new code space, and the environment will be ready to go.

#### Code Setup

1. Next, **create a virtual environment** where you can run the code.
```bash
python -m venv bqs-env
```

2. **Activate the new environment.**
```bash
source bqs-env/bin/activate
```

3. **Install the dependencies** for the repository in the virtual environment.
```bash
pip install -r requirements.txt
```

# Notebooks
The notebooks included in the repository contain the code for each chapter as well as accompanying exercises.
You can read through the notebooks to learn how to code for different tasks, or you can edit them and experiment
with how changing the code impacts the different computations being run. All exercise notebooks include answers and explanations
to help you continue to build your intuition with the material.

# Hume
Hume is a standalone quantum simulator constructed in a couple of hundred lines of code. It can be translated directly to Qiskit and most of its syntax matches Qiskit, and  (which can then be run on a real quantum computer). Because Hume allows the use of classical methods, running it can be more efficient than a purely gate-based simulator. For a high-performance version of Hume implemented in Rust, check out [this repository](https://github.com/QuState/spinoza)!

Tests can be run with `pytest` from the `src` directory. For example:
```bash
python -m pytest hume --no-header  -qs
```
Or a more specific test file:
```bash
python -m pytest hume/tests/test_unitary.py --no-header  -qs
```
Or a more specific test:
```bash
python -m pytest hume/tests/test_util_qiskit.py::test_same_as_qiskit --no-header --no-summary -qs
```

<!-- 
# UI
## Setup for UI experiments
### macOS

1. Install dependencies
```bash
brew install poppler

pip install -r requirements-ui.txt
```
-->

<!--  
# Assistant
TODO: get from book_assistant
-->




