from xai_components.base import InArg, OutArg, Component, xai_component
from typing import Optional, Dict, Any
import os
from googleapiclient.discovery import build
from google.oauth2 import service_account
from .auth_utils import get_credentials

def get_google_tasks_service():
    """Get Google Tasks service from context or create new one."""
    ctx = {}  # TODO: Get actual context from component
    if 'gtasks' in ctx:
        return ctx['gtasks']
    
    creds = get_credentials(['https://www.googleapis.com/auth/tasks'])
    service = build('tasks', 'v1', credentials=creds)
    ctx['gtasks'] = service
    return service

# Tasklists Components
@xai_component
class TasklistInsert(Component):
    """Creates a new task list and adds it to the authenticated user's task lists."""
    
    body: InArg[Dict[str, Any]]  # The request body for creating a task list
    x__xgafv: InArg[Optional[str]]  # Optional error format
    tasklist: OutArg[Dict[str, Any]]  # The created task list

    def execute(self, ctx) -> None:
        service = get_google_tasks_service()
        result = service.tasklists().insert(body=self.body.value, x__xgafv=self.x__xgafv.value).execute()
        self.tasklist.value = result


@xai_component
class TasklistGet(Component):
    """Returns the authenticated user's specified task list."""
    
    tasklist_id: InArg[str]  # Task list identifier
    x__xgafv: InArg[Optional[str]]  # Optional error format
    tasklist: OutArg[Dict[str, Any]]  # The requested task list

    def execute(self, ctx) -> None:
        service = get_google_tasks_service()
        result = service.tasklists().get(tasklist=self.tasklist_id.value, x__xgafv=self.x__xgafv.value).execute()
        self.tasklist.value = result


@xai_component
class TasklistDelete(Component):
    """Deletes the authenticated user's specified task list."""
    
    tasklist_id: InArg[str]  # Task list identifier
    x__xgafv: InArg[Optional[str]]  # Optional error format

    def execute(self, ctx) -> None:
        service = get_google_tasks_service()
        service.tasklists().delete(tasklist=self.tasklist_id.value, x__xgafv=self.x__xgafv.value).execute()


@xai_component
class TasklistList(Component):
    """Returns all the authenticated user's task lists."""
    
    maxResults: InArg[Optional[int]]  # Maximum number of task lists returned
    pageToken: InArg[Optional[str]]  # Token specifying the result page to return
    x__xgafv: InArg[Optional[str]]  # Optional error format
    tasklists: OutArg[Dict[str, Any]]  # The list of task lists

    def execute(self, ctx) -> None:
        service = get_google_tasks_service()
        result = service.tasklists().list(maxResults=self.maxResults.value, pageToken=self.pageToken.value, x__xgafv=self.x__xgafv.value).execute()
        self.tasklists.value = result


@xai_component
class TasklistUpdate(Component):
    """Updates the authenticated user's specified task list."""
    
    tasklist_id: InArg[str]  # Task list identifier
    body: InArg[Dict[str, Any]]  # The request body for updating a task list
    x__xgafv: InArg[Optional[str]]  # Optional error format
    tasklist: OutArg[Dict[str, Any]]  # The updated task list

    def execute(self, ctx) -> None:
        service = get_google_tasks_service()
        result = service.tasklists().update(tasklist=self.tasklist_id.value, body=self.body.value, x__xgafv=self.x__xgafv.value).execute()
        self.tasklist.value = result


@xai_component
class TasklistPatch(Component):
    """Updates the authenticated user's specified task list with patch semantics."""
    
    tasklist_id: InArg[str]  # Task list identifier
    body: InArg[Dict[str, Any]]  # The request body for patching a task list
    x__xgafv: InArg[Optional[str]]  # Optional error format
    tasklist: OutArg[Dict[str, Any]]  # The patched task list

    def execute(self, ctx) -> None:
        service = get_google_tasks_service()
        result = service.tasklists().patch(tasklist=self.tasklist_id.value, body=self.body.value, x__xgafv=self.x__xgafv.value).execute()
        self.tasklist.value = result


# Tasks Components
@xai_component
class TaskInsert(Component):
    """Creates a new task on the specified task list."""
    
    tasklist_id: InArg[str]  # Task list identifier
    body: InArg[Dict[str, Any]]  # The request body for creating a task
    parent: InArg[Optional[str]]  # Optional parent task identifier
    previous: InArg[Optional[str]]  # Optional previous sibling task identifier
    x__xgafv: InArg[Optional[str]]  # Optional error format
    task: OutArg[Dict[str, Any]]  # The created task

    def execute(self, ctx) -> None:
        service = get_google_tasks_service()
        result = service.tasks().insert(
            tasklist=self.tasklist_id.value,
            body=self.body.value,
            parent=self.parent.value,
            previous=self.previous.value,
            x__xgafv=self.x__xgafv.value
        ).execute()
        self.task.value = result


@xai_component
class TaskGet(Component):
    """Returns the specified task."""
    
    tasklist_id: InArg[str]  # Task list identifier
    task_id: InArg[str]  # Task identifier
    x__xgafv: InArg[Optional[str]]  # Optional error format
    task: OutArg[Dict[str, Any]]  # The requested task

    def execute(self, ctx) -> None:
        service = get_google_tasks_service()
        result = service.tasks().get(
            tasklist=self.tasklist_id.value,
            task=self.task_id.value,
            x__xgafv=self.x__xgafv.value
        ).execute()
        self.task.value = result


@xai_component
class TaskDelete(Component):
    """Deletes the specified task from the task list."""
    
    tasklist_id: InArg[str]  # Task list identifier
    task_id: InArg[str]  # Task identifier
    x__xgafv: InArg[Optional[str]]  # Optional error format

    def execute(self, ctx) -> None:
        service = get_google_tasks_service()
        service.tasks().delete(
            tasklist=self.tasklist_id.value,
            task=self.task_id.value,
            x__xgafv=self.x__xgafv.value
        ).execute()


@xai_component
class TaskList(Component):
    """Returns all tasks in the specified task list."""
    
    tasklist_id: InArg[str]  # Task list identifier
    completedMax: InArg[Optional[str]]  # Optional upper bound for completion date
    completedMin: InArg[Optional[str]]  # Optional lower bound for completion date
    dueMax: InArg[Optional[str]]  # Optional upper bound for due date
    dueMin: InArg[Optional[str]]  # Optional lower bound for due date
    maxResults: InArg[Optional[int]]  # Optional maximum number of tasks returned
    pageToken: InArg[Optional[str]]  # Optional token specifying the result page
    showAssigned: InArg[Optional[bool]]  # Optional flag to show assigned tasks
    showCompleted: InArg[Optional[bool]]  # Optional flag to show completed tasks
    showDeleted: InArg[Optional[bool]]  # Optional flag to show deleted tasks
    showHidden: InArg[Optional[bool]]  # Optional flag to show hidden tasks
    updatedMin: InArg[Optional[str]]  # Optional lower bound for last modification time
    x__xgafv: InArg[Optional[str]]  # Optional error format
    tasks: OutArg[Dict[str, Any]]  # The list of tasks

    def execute(self, ctx) -> None:
        service = get_google_tasks_service()
        result = service.tasks().list(
            tasklist=self.tasklist_id.value,
            completedMax=self.completedMax.value,
            completedMin=self.completedMin.value,
            dueMax=self.dueMax.value,
            dueMin=self.dueMin.value,
            maxResults=self.maxResults.value,
            pageToken=self.pageToken.value,
            showAssigned=self.showAssigned.value,
            showCompleted=self.showCompleted.value,
            showDeleted=self.showDeleted.value,
            showHidden=self.showHidden.value,
            updatedMin=self.updatedMin.value,
            x__xgafv=self.x__xgafv.value
        ).execute()
        self.tasks.value = result


@xai_component
class TaskClear(Component):
    """Clears all completed tasks from the specified task list."""
    
    tasklist_id: InArg[str]  # Task list identifier
    x__xgafv: InArg[Optional[str]]  # Optional error format

    def execute(self, ctx) -> None:
        service = get_google_tasks_service()
        service.tasks().clear(
            tasklist=self.tasklist_id.value,
            x__xgafv=self.x__xgafv.value
        ).execute()


@xai_component
class TaskPatch(Component):
    """Updates the specified task with patch semantics."""
    
    tasklist_id: InArg[str]  # Task list identifier
    task_id: InArg[str]  # Task identifier
    body: InArg[Dict[str, Any]]  # The request body for patching a task
    x__xgafv: InArg[Optional[str]]  # Optional error format
    task: OutArg[Dict[str, Any]]  # The patched task

    def execute(self, ctx) -> None:
        service = get_google_tasks_service()
        result = service.tasks().patch(
            tasklist=self.tasklist_id.value,
            task=self.task_id.value,
            body=self.body.value,
            x__xgafv=self.x__xgafv.value
        ).execute()
        self.task.value = result


@xai_component
class GoogleTasksAuth(Component):
    """A component to authenticate with Google Tasks API and generate a client object.
    
    If a client doesn't exist in the context, it will create one using credentials
    from the GOOGLE_SERVICE_ACCOUNT_CREDENTIALS environment variable.

    ##### outPorts:
    - client: A Google Tasks API client object.
    """

    client: OutArg[any]

    def execute(self, ctx) -> None:
        # Check if client already exists in context
        if 'gtasks' in ctx:
            self.client.value = ctx['gtasks']
            return

        # Get credentials and create service
        creds = get_credentials(['https://www.googleapis.com/auth/tasks'])
        
        # Create the service
        service = build('tasks', 'v1', credentials=creds)

        self.client.value = service
        ctx.update({'gtasks': service})
