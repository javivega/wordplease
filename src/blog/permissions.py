from rest_framework.permissions import BasePermission


class ArticlePermission(BasePermission):

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        """
        Define si el usuario puede realizar la acción sobre el objeto que quiere realizarlo
        :param request: HttpRequest
        :param view: UsersAPI/UserDetailAPI
        :param obj: User
        :return: True si puede, False si no puede
        """
        if request.method == "GET":
            return request.user.is_superuser or request.user == obj.owner or obj.post_published == "PUB"
        else:
            """permisos para put y delete ser el propietario o admin"""
            return request.user.is_superuser or request.user == obj.owner
