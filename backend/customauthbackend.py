from .models import Member

class EmailAuthBackend():
    def authenticate(self, request, username, password):
        try:
            user = Member.objects.get(email=username)
            success = user.check_password(password)
            print(f'FROM AUTH BACKEND USER=>{user} SUCCESS=>{success} UNAME=>{username} PWD=>{password}')
            if success:
                return user
        except Member.DoesNotExist:
            pass
        return None

    def get_user(self, uuid):
        try:
            return Member.objects.get(uuid=uuid)
        except:
            return None