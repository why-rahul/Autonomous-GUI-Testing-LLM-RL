def analyze_failure(step, error):

    if "no such element" in error.lower():
        return {
            "action": step["action"],
            "target": "//input",
            "value": step.get("value", "")
        }

    if "timeout" in error.lower():
        return {
            "action": "wait",
            "target": "",
            "value": 2
        }

    return None