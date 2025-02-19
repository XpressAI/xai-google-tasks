from xai_components.base import InArg, InCompArg, OutArg, Component, xai_component
from typing import Optional, Any
import os   
import base64
import json
from googleapiclient.discovery import build
from google.oauth2 import service_account

def get_credentials(scopes, json_path=None):
    """Get credentials from file or environment variable.
    
    Args:
        scopes: List of Google API scopes needed
        json_path: Optional path to service account JSON file
        
    Returns:
        Google OAuth credentials object
    """
    if json_path:
        if not os.path.exists(json_path):
            raise FileNotFoundError(f"Credentials file not found: {json_path}")
        return service_account.Credentials.from_service_account_file(
            json_path,
            scopes=scopes
        )
    
    # Fall back to environment variable
    creds_b64 = os.getenv('GOOGLE_SERVICE_ACCOUNT_CREDENTIALS')
    if not creds_b64:
        raise EnvironmentError("No credentials file provided and GOOGLE_SERVICE_ACCOUNT_CREDENTIALS environment variable not set")
    
    # Decode base64 credentials
    creds_json = base64.b64decode(creds_b64).decode('utf-8')
    creds_dict = json.loads(creds_json)
    
    # Create credentials object
    return service_account.Credentials.from_service_account_info(
        creds_dict,
        scopes=scopes
    )


def get_google_tasks_service(ctx=None, client=None):
    """Get Google Tasks service from provided client, context, or create new one."""
    if client:
        return client
        
    if ctx and 'gtasks' in ctx:
        return ctx['gtasks']
    
    creds = get_credentials(['https://www.googleapis.com/auth/tasks'])
    service = build('tasks', 'v1', credentials=creds)
    if ctx:
        ctx['gtasks'] = service
    return service

@xai_component
class GoogleTasksAuth(Component):
    """A component to authenticate with Google Tasks API and generate a client object.
    
    If a client doesn't exist in the context, it will create one using credentials
    from either:
    1. The provided JSON key file path
    2. The GOOGLE_SERVICE_ACCOUNT_CREDENTIALS environment variable (base64 encoded)

    ##### inPorts:
    - json_path: Optional path to service account JSON key file

    ##### outPorts:
    - client: A Google Tasks API client object
    """

    json_path: InArg[Optional[str]]  # Optional path to service account JSON file
    client: OutArg[any]

    def execute(self, ctx) -> None:
        # Check if client already exists in context
        if 'gtasks' in ctx:
            self.client.value = ctx['gtasks']
            return

        # Get credentials and create service
        creds = get_credentials(['https://www.googleapis.com/auth/tasks'], self.json_path.value if self.json_path else None)
        
        # Create the service
        service = build('tasks', 'v1', credentials=creds)

        self.client.value = service
        ctx.update({'gtasks': service})


# Tasklists Components
@xai_component
class TasklistInsert(Component):
    """Creates a new task list and adds it to the authenticated user's task lists."""
    
    client: InArg[any]  # Google Tasks client from GoogleTasksAuth
    body: InCompArg[dict]  # The request body for creating a task list
    tasklist: OutArg[dict]  # The created task list

    def execute(self, ctx) -> None:
        service = get_google_tasks_service(ctx, self.client.value if self.client else None)
        result = service.tasklists().insert(body=self.body.value).execute()
        self.tasklist.value = result


@xai_component
class TasklistGet(Component):
    """Returns the authenticated user's specified task list."""
    
    tasklist_id: InCompArg[str]  # Task list identifier
    tasklist: OutArg[dict]  # The requested task list

    def execute(self, ctx) -> None:
        service = get_google_tasks_service()
        result = service.tasklists().get(tasklist=self.tasklist_id.value).execute()
        self.tasklist.value = result


@xai_component
class TasklistDelete(Component):
    """Deletes the authenticated user's specified task list."""
    
    tasklist_id: InArg[str]  # Task list identifier

    def execute(self, ctx) -> None:
        service = get_google_tasks_service()
        service.tasklists().delete(tasklist=self.tasklist_id.value).execute()


@xai_component
class TasklistList(Component):
    """Returns all the authenticated user's task lists."""
    
    maxResults: InArg[Optional[int]]  # Maximum number of task lists returned
    pageToken: InArg[Optional[str]]  # Token specifying the result page to return
    tasklists: OutArg[dict]  # The list of task lists

    def execute(self, ctx) -> None:
        service = get_google_tasks_service()
        result = service.tasklists().list(maxResults=self.maxResults.value, pageToken=self.pageToken.value).execute()
        self.tasklists.value = result


@xai_component
class TasklistUpdate(Component):
    """Updates the authenticated user's specified task list."""
    
    tasklist_id: InArg[str]  # Task list identifier
    body: InArg[dict]  # The request body for updating a task list
    tasklist: OutArg[dict]  # The updated task list

    def execute(self, ctx) -> None:
        service = get_google_tasks_service()
        result = service.tasklists().update(tasklist=self.tasklist_id.value, body=self.body.value).execute()
        self.tasklist.value = result


@xai_component
class TasklistPatch(Component):
    """Updates the authenticated user's specified task list with patch semantics."""
    
    tasklist_id: InArg[str]  # Task list identifier
    body: InArg[dict]  # The request body for patching a task list
    tasklist: OutArg[dict]  # The patched task list

    def execute(self, ctx) -> None:
        service = get_google_tasks_service()
        result = service.tasklists().patch(tasklist=self.tasklist_id.value, body=self.body.value).execute()
        self.tasklist.value = result


# Tasks Components
@xai_component
class TaskInsert(Component):
    """Creates a new task on the specified task list."""
    
    tasklist_id: InArg[str]  # Task list identifier
    body: InArg[dict]  # The request body for creating a task
    parent: InArg[Optional[str]]  # Optional parent task identifier
    previous: InArg[Optional[str]]  # Optional previous sibling task identifier
    task: OutArg[dict]  # The created task

    def execute(self, ctx) -> None:
        service = get_google_tasks_service()
        result = service.tasks().insert(
            tasklist=self.tasklist_id.value,
            body=self.body.value,
            parent=self.parent.value,
            previous=self.previous.value
        ).execute()
        self.task.value = result


@xai_component
class TaskGet(Component):
    """Returns the specified task."""
    
    tasklist_id: InArg[str]  # Task list identifier
    task_id: InCompArg[str]  # Task identifier
    task: OutArg[dict]  # The requested task

    def execute(self, ctx) -> None:
        service = get_google_tasks_service()
        result = service.tasks().get(
            tasklist=self.tasklist_id.value,
            task=self.task_id.value
        ).execute()
        self.task.value = result


@xai_component
class TaskDelete(Component):
    """Deletes the specified task from the task list."""
    
    tasklist_id: InArg[str]  # Task list identifier
    task_id: InArg[str]  # Task identifier

    def execute(self, ctx) -> None:
        service = get_google_tasks_service()
        service.tasks().delete(
            tasklist=self.tasklist_id.value,
            task=self.task_id.value
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
    tasks: OutArg[dict]  # The list of tasks

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
            updatedMin=self.updatedMin.value
        ).execute()
        self.tasks.value = result


@xai_component
class TaskClear(Component):
    """Clears all completed tasks from the specified task list."""
    
    tasklist_id: InArg[str]  # Task list identifier

    def execute(self, ctx) -> None:
        service = get_google_tasks_service()
        service.tasks().clear(
            tasklist=self.tasklist_id.value
        ).execute()


@xai_component
class TaskPatch(Component):
    """Updates the specified task with patch semantics."""
    
    tasklist_id: InArg[str]  # Task list identifier
    task_id: InArg[str]  # Task identifier
    body: InArg[dict]  # The request body for patching a task
    task: OutArg[dict]  # The patched task

    def execute(self, ctx) -> None:
        service = get_google_tasks_service()
        result = service.tasks().patch(
            tasklist=self.tasklist_id.value,
            task=self.task_id.value,
            body=self.body.value
        ).execute()
        self.task.value = result


