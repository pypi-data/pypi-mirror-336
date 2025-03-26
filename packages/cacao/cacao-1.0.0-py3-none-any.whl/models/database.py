"""Mock database for testing."""
from typing import Dict, List, Optional

class User:
    """Mock user model."""
    def __init__(self, user_id: int, username: str, email: str = None):
        self.id = user_id
        self.username = username
        self.email = email

    def to_dict(self) -> Dict:
        """Convert user to dictionary."""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }

class MockDatabase:
    """Mock database implementation."""
    def __init__(self):
        self.users: Dict[int, User] = {}
        self.next_id = 1

        # Add some test data
        self.create_user({"username": "johndoe", "email": "john@example.com"})
        self.create_user({"username": "janedoe", "email": "jane@example.com"})

    def create_user(self, data: Dict) -> User:
        """Create a new user."""
        if not data.get("username"):
            raise ValueError("Username is required")

        user = User(
            user_id=self.next_id,
            username=data["username"],
            email=data.get("email")
        )
        self.users[user.id] = user
        self.next_id += 1
        return user

    def get_user(self, user_id: int) -> Optional[User]:
        """Get a user by ID."""
        return self.users.get(user_id)

    def update_user_email(self, user_id: int, email: str) -> User:
        """Update a user's email."""
        user = self.get_user(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        user.email = email
        return user

    def delete_user(self, user_id: int) -> None:
        """Delete a user."""
        if user_id not in self.users:
            raise ValueError(f"User {user_id} not found")
        del self.users[user_id]

    def list_users(self) -> List[User]:
        """List all users."""
        return list(self.users.values())
