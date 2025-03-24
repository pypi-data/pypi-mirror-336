from sparkplug_core.permissions import (
    ActionPermission,
    IsAuthenticated,
    IsCreator,
)


class Image(
    ActionPermission,
):
    # user permissions
    create_perms = IsAuthenticated

    # object permissions
    read_perms = IsAuthenticated
    write_perms = IsCreator
