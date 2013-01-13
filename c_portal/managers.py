from django.db import models
from django.db.models import Count

class MemberManager(models.Manager):
    """Manager for active members only"""
    def active(self):
        """Query for all members that have an active account
        
        Returns:
            object  - QuerySet() with all disabled accounts removed
        """
        return super(MemberManager, self).get_query_set().filter(
                active=True).order_by("nickname")


class ContentManager(models.Manager):
    """Manager for published content"""
    def published(self):
        """Query for all published content
        
        Returns:
            object  - QuerySet() with all unpublished content filtered out
        """
        return super(ContentManager, self).get_query_set().filter(
                published=True
                )

    def unpublished(self):
        return super(ContentManager, self).get_query_set().filter(
                published=False
                )
