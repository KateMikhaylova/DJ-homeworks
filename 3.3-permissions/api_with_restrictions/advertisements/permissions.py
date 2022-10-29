from rest_framework.permissions import BasePermission


class IsOwnerOrAdmin(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        if request.user.is_staff:
            return True
        return request.user == obj.creator


class IsOwnerOrNotDraft(BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.status != 'DRAFT':
            return True
        return request.user == obj.creator
