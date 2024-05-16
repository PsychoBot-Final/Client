user_id = None
user_authenticated = None
instances = None
expiry_date = None
connected = False
username = None

def set_username(username_: str) -> None:
    global username
    username = username_

def get_username() -> str:
    return username

def set_connection_status(flag: bool) -> None:
    global connected
    connected = flag

def get_connection_status() -> bool:
    return connected

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

def get_authenticated() -> bool:
    return user_authenticated