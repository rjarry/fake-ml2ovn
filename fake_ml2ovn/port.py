# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2023 Robin Jarry

from .base import NeutronResource, OVNClient, ResourceAction


class Port(NeutronResource):
    def actions(self) -> list[ResourceAction]:
        from neutronclient.neutron.v2_0 import port

        return [
            ResourceAction("add", port.CreatePort, self.add),
            ResourceAction("set", port.UpdatePort, self.update),
            ResourceAction("del", port.DeletePort, self.delete),
        ]

    def add(self, client: OVNClient, body: dict):
        pass

    def update(self, client: OVNClient, body: dict):
        pass

    def delete(self, client: OVNClient, body: dict):
        pass
