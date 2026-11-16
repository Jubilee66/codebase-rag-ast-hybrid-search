from data.sample_repository.services.user_service import register_user, get_user
from data.sample_repository.services.auth_service import authenticate

def run_demo():
    user = register_user("jane@example.com", "correct-horse")
    print("Registered:", user["email"])

    logged_in = authenticate("jane@example.com", "correct-horse")
    print("Authenticated:", logged_in)

    fetched = get_user("jane@example.com")
    print("Fetched:", fetched)

if __name__ == "__main__":
    run_demo()
