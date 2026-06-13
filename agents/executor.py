class ExecutorAgent:

    def __init__(self, env):
        self.env = env

    def execute(self, step):
        try:
            action = step["action"]
            target = step["target"]
            value = step["value"]

            if action == "open_url":
                self.env.open_url()
                return 0, ""

            elif action == "type":
                self.env.type(target, value)
                return 0, ""

            elif action == "click":
                self.env.click(target)
                return 0, ""

            elif action == "verify":
                return self.env.verify(target)

            else:
                return -1, f"Unknown action: {action}"

        except Exception as e:
            return -1, str(e)