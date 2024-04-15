# Store and retrieve connected user credentials

user_id = None
user_authenticated = False
instances = None
expiry_date = None

def set_expiry_date(
    expiry: str
) -> None:
    global expiry_date
    expiry_date = expiry

def set_instances(
    num_instances: int
) -> None:
    global instances
    instances = num_instances

def set_user_id(
    id: int
) -> None:
    global user_id
    user_id = id

def set_user_authenticated(
    authenticated: bool
) -> None:
    global user_authenticated
    user_authenticated = authenticated

def get_expiry() -> str:
    return expiry_date

def get_instances() -> int:
    return instances

def get_id() -> int:
    return user_id

def is_authenticated() -> bool:
    return user_authenticated