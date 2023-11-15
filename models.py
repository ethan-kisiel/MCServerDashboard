from uuid import uuid4


class User:
    """
        is_authenticated
            This property should return True if the user is authenticated,
            i.e. they have provided valid credentials.
            (Only authenticated users will fulfill the criteria of login_required.)

        is_active
            This property should return True if this is an active user -
            in addition to being authenticated, they also have activated their
            account, not been suspended, or any condition your application has for rejecting an account.
            Inactive accounts may not log in (without being forced of course).

        is_anonymous
            This property should return True if this is an anonymous user.
            (Actual users should return False instead.)

    get_id()
    This method must return a str that uniquely identifies this user,
    and can be used to load the user from the user_loader callback.
    Note that this must be a str - if the ID is natively an int or some other type, you will need to convert it to str.
    """

    def __init__(self, is_admin: bool = False):
        self.__id = "admin" if is_admin else str(uuid4())
        self.is_authenticated = False

    # @property
    # def is_authenticated(self):
    #     return self.__is_authenticated

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return self.__id != "admin"

    def get_id(self):
        return self.__id
