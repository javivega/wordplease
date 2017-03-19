from rest_framework.permissions import BasePermission



class UserPermission(BasePermission):

    def has_permission(self, request, view):
        """Define si un usuario puede usar o no el endpoint que quiere utilizar
        """
        from users.api import UserDetailAPI
        if request.method == "POST":
            return True
        #si esta autenticado y quiere hace algo sobre el detalle o es superusuario y quiere hacer algo sobre el listado entonces devolvemos true
        if request.user.is_authenticated() and (request.user.is_superuser or isinstance(view, UserDetailAPI)):
                return True

        return False

    def has_object_permission(self, request, view, obj):
        """
        Define si el usuario puede realizar la acción sobre el objeto que quiere realizarlo
        :param request: HttpRequest
        :param view: UsersAPI/UserDetailAPI
        :param obj: User
        :return: True si puede, False si no puede
        """
        #si es admin o es el mismo le dejamos realizar la acción
        return request.user.is_superuser or request.user == obj


