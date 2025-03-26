from repenseai.genai.tasks.base import BaseTask
from repenseai.utils import logs


class Workflow(BaseTask):

    def __init__(self, steps):
        self.steps = steps

    def run(self, context: dict | None = None):

        if not context:
            context = {}
            
        for step in self.steps:
            try:
                if isinstance(step[0], BaseTask):
                    if step[1] is None:
                        step[0].run(context)
                    else:
                        if chat_history := context.get("chat_history"):
                            step[0].history = chat_history
                        elif memory_dict := context.get("memory_dict"):
                            step[0].history = memory_dict.get("chat_history", [])
                            
                        context[step[1]] = step[0].run(context)
                else:
                    context[step[1]] = step[0](context)

            except Exception as e:
                logs.logger(f"step {step[1]} -> Erro: {e}")
            
        return context

