# Autonomous GUI Testing using LLM and Reinforcement Learning

## Overview

This project presents an autonomous GUI testing framework that combines Large Language Models (LLMs), Reinforcement Learning (DQN), Selenium automation, and OpenCV-based visual validation.

The system converts natural language testing requirements into executable UI test plans, interacts with web applications automatically, detects failures, performs visual verification, and continuously improves decision-making through reinforcement learning.

---

## Problem Statement

Traditional GUI testing relies on manually written test scripts and predefined workflows. Maintaining these scripts becomes difficult when web interfaces change frequently.

This project aims to automate the testing process by generating executable test plans from natural language instructions and allowing an RL agent to learn effective testing strategies through interaction with the environment.

---

## Workflow Architecture

Detailed workflow diagram:

[View Workflow Diagram](WorkFlow%20Diagram.pdf)

The workflow includes:

* User Input
* LLM Planner
* Test Plan Generation
* RL Agent (DQN)
* Selenium Environment
* Action Execution
* Screenshot Capture
* Bug Detection
* OpenCV Vision Validation
* Critic Agent
* RL Memory Update
* DQN Training
* Continuous Learning Loop

---

## Key Features

* Natural language test generation using LLM
* Autonomous GUI interaction using Selenium
* Deep Q-Network (DQN) based decision making
* Epsilon-greedy exploration and exploitation
* OpenCV-based visual validation
* Automated bug detection
* Critic agent for self-healing recovery
* Multi-agent architecture
* Continuous learning through experience replay

---

## Technology Stack

| Component              | Technology                   |
| ---------------------- | ---------------------------- |
| Programming Language   | Python                       |
| Browser Automation     | Selenium                     |
| Reinforcement Learning | PyTorch                      |
| Deep Learning Model    | Multi-Layer Perceptron (MLP) |
| Computer Vision        | OpenCV                       |
| LLM Integration        | Ollama                       |
| Data Format            | JSON                         |

---

## Project Structure

```text
llm_rl_gui_testing/
│
├── main.py
├── config.py
├── requirements.txt
│
├── llm/
│   ├── planner.py
│   ├── critic.py
│   └── ollama_client.py
│
├── rl/
│   ├── dqn_agent.py
│   ├── model.py
│   └── replay_buffer.py
│
├── env/
│   ├── selenium_env.py
│   └── state_extractor.py
│
├── utils/
│   ├── vision.py
│   ├── bug_detector.py
│   └── logger.py
│
├── agents/
├── dashboard/
├── tests/
└── outputs/
```

---

## Reinforcement Learning Setup

### State

Current testing state and execution progress.

### Actions

* Open URL
* Type Text
* Click Element
* Verify Result

### Reward Function

| Condition         | Reward |
| ----------------- | ------ |
| Success           | +1     |
| Failure           | -1     |
| Intermediate Step | 0      |

### Exploration Strategy

The RL agent follows an epsilon-greedy policy:

* Explore → Random Action Selection
* Exploit → Best Learned Action

---

## Installation

Clone the repository:

```bash
git clone https://github.com/why-rahul/Autonomous-GUI-Testing-LLM-RL.git
cd Autonomous-GUI-Testing-LLM-RL
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Run the Project

```bash
python main.py
```

---

## Sample Input

```text
Test login with valid and invalid credentials and logout
```

---

## Core Components

### LLM Planner

Generates executable UI test plans from natural language requirements.

### RL Agent (DQN)

Learns action-selection policies through rewards and environment interaction.

### Selenium Environment

Executes browser actions such as typing, clicking, navigation, and verification.

### OpenCV Vision Module

Performs screenshot comparison and visual validation.

### Critic Agent

Analyzes failures and suggests recovery actions for self-healing execution.

### Bug Detector

Identifies Selenium and UI-related execution failures.

---

## Future Enhancements

* Vision-Language Models (VLMs)
* Cross-browser testing
* Mobile application testing
* Distributed execution
* Advanced visual bug localization
* Automated report generation

---

## Author

Rahul Jana

M.Sc. Computer Science

Ramakrishna Mission Vivekananda Educational and Research Institute (RKMVERI)

---

## License

This project is developed for academic and research purposes.
