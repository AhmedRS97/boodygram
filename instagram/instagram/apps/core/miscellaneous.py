from django.shortcuts import _get_queryset
import uuid
from os.path import join


# custom function that substitute get_list_or_404 cuz i don't want 404.
def filter_or_none(klass, *args, **kwargs):
    queryset = _get_queryset(klass)
    try:
        obj_list = list(queryset.filter(*args, **kwargs))
    except AttributeError:
        klass__name = klass.__name__ if isinstance(klass, type) else klass.__class__.__name__
        raise ValueError(
            "First argument to get_list_or_404() must be a Model, Manager, or "
            "QuerySet, not '%s'." % klass__name
        )
    except DoesNotExist:
        return None
    if not obj_list:
        obj_list = None
    return obj_list


def get_or_none(klass, *args, **kwargs):
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except AttributeError:
        klass__name = klass.__name__ if isinstance(klass, type) else klass.__class__.__name__
        raise ValueError(
            "First argument to get_object_or_404() must be a Model, Manager, "
            "or QuerySet, not '%s'." % klass__name
        )
    except queryset.model.DoesNotExist:
        return None


def get_file_path(file_dir):
    """
    This function is useful for join the file name to the desired directory name.
    :param file_dir: string contains the desired directory to save the file into.
    :return: Anonymous function that takes model instance and filename from django.
    """
    # extension = filename.split('.')[-1]
    # filename = "%s.%s" % (uuid.uuid4(), ext)
    # return join(file_dir, filename)
    return lambda instance, filename: (
            join(file_dir, "%s.%s" % (uuid.uuid4(), filename.split('.')[-1]))
    )
