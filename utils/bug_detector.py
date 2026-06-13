class BugDetector:

    def detect(self, message):

        if not message:
            return None

        msg = message.lower()

        # 🔴 Element issues
        if "no such element" in msg:
            return "Element Not Found Bug"

        # 🔴 Login failure
        if "login failed" in msg:
            return "Login Failure Bug"

        # 🔴 Logout failure
        if "logout failed" in msg:
            return "Logout Failure Bug"

        # 🔴 URL/navigation issue
        if "url" in msg and "not" in msg:
            return "Navigation Bug"

        # 🔴 Timeout / wait issue
        if "timeout" in msg:
            return "Timeout Bug"

        # 🔴 Invalid credentials behavior
        if "invalid" in msg:
            return "Invalid Credential Handling Bug"

        # 🔴 Selenium error fallback
        if "exception" in msg or "error" in msg:
            return "General Selenium Bug"

        return None