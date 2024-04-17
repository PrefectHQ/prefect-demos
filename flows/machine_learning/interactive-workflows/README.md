# Interactive Workflow Demo with Prefect

This repository demonstrates the integration of Prefect with interactive workflows, aiming to provide a hands-on example for orchestrating complex data pipelines interactively. It showcases how to leverage Prefect's powerful scheduling, execution, and management capabilities to build efficient and scalable data workflows.

## Overview

Interactive Workflow Demo is designed to guide you through the process of setting up and running interactive data pipelines using Prefect. It covers the basics of Prefect's workflow orchestration capabilities, including the use of tasks, flows, parameters, and Prefect Cloud for monitoring and managing workflows.

## Features

- **Prefect Integration**: Learn how to integrate Prefect into Python-based workflows, ensuring smooth operation and scalability.
- **Interactive Workflows**: Dive into creating workflows that can dynamically adjust based on user input or external data.
- **Task Management**: Understand how to define, organize, and manage tasks within Prefect to create comprehensive data pipelines.
- **Visualization**: Explore how to use Prefect's UI for monitoring and visualizing workflow execution.

## Getting Started

### Prerequisites

Before starting, ensure you have the following installed:
- Python 3.6+
- Prefect
- Marvin 
- Any other dependencies listed in `requirements.txt`.

### Installation

1. Clone this repository:
```bash
git clone https://github.com/Sahiler/interactive-workflow-demo.git
cd interactive-workflow-demo
```
2. Set up a virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
3. Install dependencies
```bash
pip install -r requirements.txt
```

### Running the Demo
1. **Start Prefect**

  Make sure Prefect is running and you are logged into Prefect Cloud or your local Prefect instance.

2. **Prefect & Marvin environment is set up**

Ensure your S3Bucket block is correctly set up to upload files to that specific region. Additionally, ensure you have the OpenAI api key correctly loaded into Marvin. Once you are authenticated to the correct workspace, you are good to go to run the workflow.

2. **Execute the Deployment script**

  Run the main script to execute the interactive workflow
  
```bash
python interactive-workflows.py
```
3. **Follow the interactive prompts to navigate through the workflow.**

### Understanding the Workflow
#### 1. deploy-interactive-workflow.py

- **Purpose**: Deploys an interactive workflow using Prefect to a managed execution environment.
- **Key Components**: Prefect flows, job variable configuration for Python packages.
- **Usage**: Run this script to deploy the workflow defined in the `interactive-workflow.py` script to an execution environment. Ensure you have Prefect and other dependencies installed.

#### 2. interactive-workflow.py

- **Purpose**: Defines an interactive data processing workflow that fetches data from an API, allows users to specify data cleaning preferences, and manages user approvals for further actions.
- **Key Components**: Prefect flows and tasks, user interaction for data processing, logging and error handling.
- **Dependencies**: Requires `marvin_extension` module, `requests` for API calls, and Prefect libraries for workflow management.
- **Usage**: Run this script in an environment where Prefect is set up and the `marvin_extension.py` is accessible.

#### 3. marvin_extension.py

- **Purpose**: Provides custom functionalities used by the interactive workflow, likely data processing or feature extraction methods tailored for specific needs.
- **Usage**: This script is imported and used in `interactive-workflow.py`. It should be present in the same directory or properly installed as a module.


### Contributing
We welcome contributions to improve this demo! Please feel free to fork the repository, make your changes, and submit a pull request. Whether it's adding new features, fixing bugs, or improving the documentation, your contributions are highly appreciated.

### Acknowledgments
Thanks to the Prefect community for providing the tools and support to make this demo possible.
Join us in exploring the capabilities of Prefect with interactive workflows, and see how it can transform your data pipeline management and execution.

