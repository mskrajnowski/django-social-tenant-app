#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    argv = list(sys.argv)

    if not argv:
        print("You need to specify the app: 'main' or 'tenant'.")
        sys.exit(1)

    app = argv.pop(1)
    if app not in ('main', 'tenant'):
        print("Invalid app name, must be either 'main' or 'tenant'.")
        sys.exit(1)

    settings_module = "social_tenant.{}.local_settings".format(app)
    os.environ["DJANGO_SETTINGS_MODULE"] = settings_module

    from django.core.management import execute_from_command_line

    execute_from_command_line(argv)
