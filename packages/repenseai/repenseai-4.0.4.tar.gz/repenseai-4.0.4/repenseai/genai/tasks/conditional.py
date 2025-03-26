from repenseai.genai.tasks.base import BaseTask

# Defining a Workflow step that will execute a task based on a condition.
# This will be helpful when chaining branching execution paths.
# A BooleanConditionalTask can encapsulate another BooleanConditionalTask inside a condition.
# this means we can create a Workflow such as:
# run user intention;
# if user intention is recommendation:
#     run recommendation ids
#     if recommendation ids are empty:
#         run a chat message suggesting another path
#     otherwise:
#         run a speak message recommending the items
# otherwise:
#     if the user intention is interacting with the cart:
#         if the user wants to add to the cart:
# (etc etc)
# This class is a simpler version of a possible conditional with more than true/false options that we can implement later.


class DummyTask(BaseTask):
    def run(self, context: dict | None = None) -> dict:
        return context or {}  # returns empty dict if context is None


class BooleanConditionalTask(BaseTask):
    """
    A chatbot Workflow step that initializes with:

    - a condition to evaluate (i.e. len(json.loads(response)) > 0)
    - a task to execute if the condition is true
    - a task to execute if the condition is false

    It then interfaces using the same interface as a Task, with the .run method
        requiring a user_input and a context, and the context requiring the response
        from the previous step (which needs evaluation).
    """

    def __init__(self, condition, true_task, false_task):
        self.condition = condition
        self.true_task = true_task
        self.false_task = false_task

    def run(self, context: dict | None = None):

        if not context:
            context = {}
            
        if self.condition(context):
            return self.true_task.run(context)
        else:
            return self.false_task.run(context)


class ConditionalTask(BaseTask):
    """
    A chatbot Workflow step that initializes with:

    - a condition to evaluate
    - a dict with {value: task} pairs

    It then interfaces using the same interface as a Task, with the .run method
        requiring a user_input and a context, executing the task that matches the value
        from the condition.
    """

    def __init__(self, condition, tasks, default_task=None):
        self.condition = condition
        self.tasks = tasks
        self.default_task = default_task

    def run(self, context: dict | None = None):

        if not context:
            context = {}

        if self.condition(context) in self.tasks.keys():
            return self.tasks[self.condition(context)].run(context)
        else:
            return self.default_task.run(context)
