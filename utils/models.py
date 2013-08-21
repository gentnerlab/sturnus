from django.db import models

# Create your models here.

class NaiveHierarchyManager(models.Manager):
    def get_roots(self):
        return self.get_query_set().filter(parent__isnull=True)

class NaiveHierarchy(models.Model):
    parent = models.ForeignKey('self', null=True)

    tree = NaiveHierarchyManager()

    def get_children(self):
        return self._default_manager.filter(parent=self)

    def get_descendants(self):
        descs = set(self.get_children())
        for node in list(descs):
            descs.update(node.get_descendants())
        return descs

    class Meta:
        abstract = True