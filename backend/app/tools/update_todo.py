def update_todo(task):

    with open("project_todo.md", "a") as f:
        f.write(f"\n[ ] {task}")

    return {"status": "task_added"}