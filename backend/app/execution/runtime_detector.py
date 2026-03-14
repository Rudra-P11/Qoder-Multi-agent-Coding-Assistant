import os


class RuntimeDetector:

    EXTENSION_RUNTIME = {
        ".py": ["python"],
        ".js": ["node"],
        ".ts": ["node"],
        ".cpp": ["g++"],
        ".c": ["gcc"],
        ".java": ["javac", "java"],
        ".go": ["go", "run"],
        ".rs": ["rustc"],
        ".rb": ["ruby"],
        ".php": ["php"]
    }

    def detect_runtime(self, file_path: str):

        _, ext = os.path.splitext(file_path)

        if ext in self.EXTENSION_RUNTIME:
            return self.EXTENSION_RUNTIME[ext]

        return None


runtime_detector = RuntimeDetector()