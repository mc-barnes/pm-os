"""Simple CRUD application — no safety-critical logic."""
from dataclasses import dataclass


@dataclass
class Todo:
    id: int
    title: str
    completed: bool = False


class TodoList:
    """In-memory todo list manager."""

    def __init__(self):
        self.todos: list[Todo] = []
        self.next_id = 1

    def add(self, title: str) -> Todo:
        todo = Todo(id=self.next_id, title=title)
        self.todos.append(todo)
        self.next_id += 1
        return todo

    def complete(self, todo_id: int) -> bool:
        for todo in self.todos:
            if todo.id == todo_id:
                todo.completed = True
                return True
        return False

    def remove(self, todo_id: int) -> bool:
        self.todos = [t for t in self.todos if t.id != todo_id]
        return True

    def list_all(self) -> list[Todo]:
        return self.todos


if __name__ == "__main__":
    tl = TodoList()
    tl.add("Buy groceries")
    tl.add("Write documentation")
    tl.complete(1)
    print(tl.list_all())
