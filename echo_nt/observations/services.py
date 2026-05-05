from django.db import transaction
from .models import Observation


@transaction.atomic
def create_observation(user, form):
    observation = form.save(commit=False)
    observation.author = user
    observation.save()
    form.save_m2m()
    return observation

from django.core.exceptions import PermissionDenied


def get_user_observations(user):
    return Observation.objects.filter(author=user)


@transaction.atomic
def verify_observation(observation, user):
    observation.is_verified = True
    observation.verified_by = user
    observation.save()
    return observation


@transaction.atomic
def delete_observation(observation, user):
    if observation.author != user:
        raise PermissionDenied("Not allowed")

    observation.delete()