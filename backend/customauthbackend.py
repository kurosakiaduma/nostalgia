from .models import Member
import logging

logger = logging.getLogger(__name__)

class EmailAuthBackend():
    def authenticate(self, request, username, password):
        try:
            user = Member.objects.get(email=username)
            success = user.check_password(password)
            if success:
                logger.debug(f"User {username} authenticated successfully")
                return user
            else:
                logger.debug(f"User {username} failed authentication")
        except Member.DoesNotExist:
            logger.debug(f"User {username} does not exist")
            pass
        return None

    def get_user(self, uuid):
        try:
            return Member.objects.get(pk=uuid)
        except:
            logger.debug(f"User with id {uuid} not found")
            return None