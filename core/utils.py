from uuid import uuid4
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from authentication.models import CustomUser


class ApiCustomResponse:
    def get_response(self, data=None, **kwargs):
        message = kwargs.get('message', 'Success')
        status_code = kwargs.get('status_code', status.HTTP_200_OK)

        response_data = {
            "status_code": status_code,
            "message": message,
            "data": data if data else dict()
        }
        return Response(data=response_data, status=status_code)
    

class CoreModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name=_("created"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated"))
    is_active = models.BooleanField(default=True, db_index=True)

    # objects = CoreManager()

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.pk)

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.pk}>"

    # def activate(self):
    #     if not self.is_active:
    #         self.is_active = True
    #         self.save(update_fields=["is_active", "updated_at"] if self.pk else None)

    # def deactivate(self):
    #     if self.is_active:
    #         self.is_active = False
    #         self.save(update_fields=["is_active", "updated_at"] if self.pk else None)


def get_user_object(pk):
    try:
        return CustomUser.objects.get(pk=pk)
    except CustomUser.DoesNotExist:
        raise Http404