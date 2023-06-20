from .models import Member

class EmailAuthBackend():
    def authenticate(self, request, username, password):
        try:
            user = Member.objects.get(email=username)
            success = user.check_password(password)
            if success:
                return user
        except Member.DoesNotExist:
            pass
        return None

    def get_user(self, uuid):
        try:
            return Member.objects.get(pk=uuid)
        except:
            return None