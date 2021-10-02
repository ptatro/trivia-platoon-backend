from rest_framework import permissions


class GamesCreatorOnlyCanChange(permissions.BasePermission):

    edit_methods = ("PUT", "PATCH", "DELETE")

    SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.creator == request.user:
            return True

        return False


class QuestionsCreatorOnlyCanChange(permissions.BasePermission):

    edit_methods = ("PUT", "PATCH", "DELETE")

    SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.game.creator == request.user:
            return True

        return False


class AnswersCreatorOnlyCanChange(permissions.BasePermission):

    edit_methods = ("PUT", "PATCH", "DELETE")

    SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.question.game.creator == request.user:
            return True

        return False


class ResultsCreatorOnlyCanChange(permissions.BasePermission):

    edit_methods = ("PUT", "PATCH", "DELETE")

    SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.player == request.user:
            return True

        return False
        