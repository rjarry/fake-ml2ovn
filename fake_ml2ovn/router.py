# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2023 Robin Jarry

from .base import NeutronResource, OVNClient, ResourceAction


class Router(NeutronResource):
    def actions(self) -> list[ResourceAction]:
        from neutronclient.neutron.v2_0 import router

        return [
            ResourceAction("add", router.CreateRouter, self.add),
            ResourceAction("set", router.UpdateRouter, self.update),
            ResourceAction("del", router.DeleteRouter, self.delete),
            ResourceAction("set-gw", router.SetGatewayRouter, self.set_gw),
            ResourceAction("del-gw", router.RemoveGatewayRouter, self.del_gw),
            ResourceAction("add-port", router.AddInterfaceRouter, self.add_port),
            ResourceAction("del-port", router.RemoveInterfaceRouter, self.del_port),
        ]

    def add(self, client: OVNClient, body: dict):
        pass

    def update(self, client: OVNClient, body: dict):
        pass

    def delete(self, client: OVNClient, body: dict):
        pass

    def set_gw(self, client: OVNClient, body: dict):
        pass

    def del_gw(self, client: OVNClient, body: dict):
        pass

    def add_port(self, client: OVNClient, body: dict):
        pass

    def del_port(self, client: OVNClient, body: dict):
        pass
