# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
#
# Invenio-Jobs is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio administration Runs view module."""

from invenio_administration.views.base import AdminResourceListView
from invenio_i18n import lazy_gettext as _


class RunsListView(AdminResourceListView):
    """Configuration for System Runs sets list view."""

    api_endpoint = "/runs"
    name = "Runs"
    search_request_headers = {"Accept": "application/vnd.inveniordm.v1+json"}
    title = "Runs"
    category = "System"
    resource_config = "jobs_resource"
    icon = "signal"
    extension_name = "invenio-rdm-records"
    display_search = False
    display_delete = False
    display_edit = False
    display_create = False
    actions = None
