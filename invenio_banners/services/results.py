# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 CERN.
#
# Invenio-Banners is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Service results."""
from invenio_records_resources.services.records.results import RecordItem, RecordList


class BannerItem(RecordItem):
    """Single banner result."""

    def __init__(
        self,
        service,
        identity,
        banner,
        links_tpl=None,
        errors=None,
        schema=None,
    ):
        """Constructor."""
        super().__init__(service, identity, banner, errors, links_tpl, schema)

    @property
    def data(self):
        """Property to get the banner."""
        if self._data:
            return self._data

        self._data = self._schema.dump(
            self._obj,
            context={
                "identity": self._identity,
                "record": self._record,
            },
        )

        if self._links_tpl:
            self._data["links"] = self.links

        return self._data


class BannerList(RecordList):
    """List of banner results."""

    def __init__(
        self,
        service,
        identity,
        banners,
        params=None,
        links_tpl=None,
        links_item_tpl=None,
        schema=None,
    ):
        """Constructor."""
        super().__init__(
            service, identity, banners, params, links_tpl, links_item_tpl, schema
        )

    @property
    def hits(self):
        """Iterator over the hits."""
        for record in self._results:
            # Project the record
            projection = self._schema.dump(
                record,
                context=dict(
                    identity=self._identity,
                    record=record,
                ),
            )

            if self._links_item_tpl:
                projection["links"] = self._links_item_tpl.expand(
                    self._identity, record
                )

            yield projection

    @property
    def total(self):
        """Get total number of banners."""
        return len(self._results)