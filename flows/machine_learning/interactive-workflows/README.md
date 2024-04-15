# Interactive Workflow Demo with Prefect

This repository demonstrates the integration of Prefect with interactive workflows, aiming to provide a hands-on example for orchestrating complex data pipelines interactively. It showcases how to leverage Prefect's powerful scheduling, execution, and management capabilities to build efficient and scalable data workflows.

## Overview

Interactive Workflow Demo is designed to guide you through the process of setting up and running interactive data pipelines using Prefect. It covers the basics of Prefect's workflow orchestration capabilities, including the use of tasks, flows, parameters, and Prefect Cloud for monitoring and managing workflows.

## Features

- **Prefect Integration**: Learn how to integrate Prefect into Python-based workflows, ensuring smooth operation and scalability.
- **Interactive Workflows**: Dive into creating workflows that can dynamically adjust based on user input or external data.
- **Task Management**: Understand how to define, organize, and manage tasks within Prefect to create comprehensive data pipelines.
- **Visualization**: Explore how to use Prefect's UI for monitoring and visualizing workflow execution.

## Understanding the Workflow
The demo includes detailed comments explaining each step of the workflow and how it integrates with Prefect's features. Pay special attention to the use of blocks for reusable logic and artifacts for visualizing workflow outputs.

#### Fetching Data
Fetches raw user data from the "https://randomuser.me/api/" and logs the response. This is a retry-enabled task in case of request failures.

#### Cleaning Data
Processes the raw data to retain only specified user features, which can be customized at runtime.

#### User Input for Feature Selection
Interactively allows a user to select which features to keep from the fetched data, defaulting to removing several including 'name', 'email', etc.

#### Creating Artifacts
Optionally creates a table artifact from the cleaned data if the user approves.

#### Creating User Names
Processes a specified number of user entries from the fetched data, based on interactive user input on the number of users to generate.

#### Uploading to Snowflake
If the user approves, the cleaned data can be uploaded to a Snowflake database using provided Snowflake credentials.

## Getting Started

### Prerequisites

Before starting, ensure you have the following installed:
- Python 3.6+
- Prefect
- Any other dependencies listed in `requirements.txt`.

### Dependencies

- `requests`: For making HTTP requests to fetch data.
- `prefect`: For workflow management and logging.
- `pydantic`: For data validation.
- `marvin_extension`: Custom library for additional functions.
- `prefect_snowflake`: For Snowflake database interactions.

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

2. **Execute the Workflow**

  Run the main script to execute the interactive workflow
  
```bash
python interactive-workflows.py
```
3. **Follow the interactive prompts to navigate through the workflow.**

### Important Notes
- The script includes exception handling to manage approvals and data integrity.
- Ensure your API limits and Snowflake usage are in accordance with your operational policies and capacity.
For further details, refer to the script comments and Prefect documentation.

### Contributing
We welcome contributions to improve this demo! Please feel free to fork the repository, make your changes, and submit a pull request. Whether it's adding new features, fixing bugs, or improving the documentation, your contributions are highly appreciated.

### Acknowledgments
Thanks to the Prefect community for providing the tools and support to make this demo possible.
Join us in exploring the capabilities of Prefect with interactive workflows, and see how it can transform your data pipeline management and execution.

