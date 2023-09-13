# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2023 Robin Jarry

from .base import NeutronResource, OVNClient, ResourceAction


class Network(NeutronResource):
    def actions(self) -> list[ResourceAction]:
        from neutronclient.neutron.v2_0 import network

        return [
            ResourceAction("add", network.CreateNetwork, self.add),
            ResourceAction("set", network.UpdateNetwork, self.update),
            ResourceAction("del", network.DeleteNetwork, self.delete),
        ]

    def add(self, client: OVNClient, body: dict):
        raise Exception(body)

    def update(self, client: OVNClient, body: dict):
        pass

    def delete(self, client: OVNClient, body: dict):
        pass
