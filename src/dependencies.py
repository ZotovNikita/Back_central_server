from src.utils.admin_checker import AdminChecker
from src.services.auth import get_current_user


AUTHORIZED = get_current_user
ADMIN_ONLY = AdminChecker()
