<p align="center">
  <a href="https://github.com/XpressAI/xircuits/tree/master/xai_components#xircuits-component-library-list">Component Libraries</a> •
  <a href="https://github.com/XpressAI/xircuits/tree/master/project-templates#xircuits-project-templates-list">Project Templates</a>
  <br>
  <a href="https://xircuits.io/">Docs</a> •
  <a href="https://xircuits.io/docs/Installation">Install</a> •
  <a href="https://xircuits.io/docs/category/tutorials">Tutorials</a> •
  <a href="https://xircuits.io/docs/category/developer-guide">Developer Guides</a> •
  <a href="https://github.com/XpressAI/xircuits/blob/master/CONTRIBUTING.md">Contribute</a> •
  <a href="https://www.xpress.ai/blog/">Blog</a> •
  <a href="https://discord.com/invite/vgEg2ZtxCw">Discord</a>
</p>

<p align="center"><i>Xircuits Component Library for Google Tasks! Seamlessly manage task lists and tasks within Xircuits.</i></p>

---

## Xircuits Component Library for Google Tasks

This library enables seamless integration with Google Tasks in Xircuits workflows. You can authenticate, manage task lists, and perform operations on tasks with ease.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Main Xircuits Components](#main-xircuits-components)
- [Installation](#installation)


## Prerequisites

Before you begin, you will need the following:

1. Python 3.9+.
2. Xircuits.
3. Google Tasks API credentials (Service Account JSON Key File)   

## Main Xircuits Components

### GoogleTasksAuth Component:  
Authenticates with Google Tasks API and provides a client object.  

<img src="https://github.com/user-attachments/assets/0c7eabf3-7c6c-4fb8-bdef-6dca3027219e" alt="Image" width="200" height="100" />


### TasklistInsert Component:  
Creates a new task list.

<img src="https://github.com/user-attachments/assets/1bc2577d-5c7f-4af4-8673-76fa6d5d4855" alt="Image" width="200" height="150" />


### TasklistGet Component:  
Retrieves a specific task list.

### TasklistDelete Component:  
Deletes a task list.

### TasklistList Component:  
Lists all task lists.

### TasklistUpdate Component:  
Updates a task list.

### TasklistPatch Component:  
Partially updates a task list.

### TaskInsert Component:  
Creates a new task in a specified task list.

### TaskGet Component:  
Retrieves a specific task.

### TaskDelete Component:  
Deletes a task from a task list.

### TaskList Component:  
Lists tasks within a specified task list.

### TaskClear Component:  
Clears completed tasks from a task list.

### TaskPatch Component:  
Partially updates a task.


## Installation

To use this component library, ensure that you have an existing [Xircuits setup](https://xircuits.io/docs/main/Installation). You can then install the Google Tasks library using the [component library interface](https://xircuits.io/docs/component-library/installation#installation-using-the-xircuits-library-interface), or through the CLI using:

```
xircuits install google-tasks
```

You can also install it manually by cloning the repository:

```
# base Xircuits directory

git clone https://github.com/XpressAI/xai-google-tasks xai_components/xai_google_tasks
pip install -r xai_components/xai_google_tasks/requirements.txt
```

