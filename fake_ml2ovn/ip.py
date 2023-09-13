# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2023 Robin Jarry

from .base import NeutronResource, OVNClient, ResourceAction


class FloatingIp(NeutronResource):
    def actions(self) -> list[ResourceAction]:
        from neutronclient.neutron.v2_0 import floatingip

        return [
            ResourceAction("add", floatingip.CreateFloatingIP, self.add),
            ResourceAction("del", floatingip.DeleteFloatingIP, self.delete),
            ResourceAction("bind", floatingip.AssociateFloatingIP, self.bind),
            ResourceAction("unbind", floatingip.DisassociateFloatingIP, self.unbind),
        ]

    def add(self, client: OVNClient, body: dict):
        pass

    def delete(self, client: OVNClient, body: dict):
        pass

    def bind(self, client: OVNClient, body: dict):
        pass

    def unbind(self, client: OVNClient, body: dict):
        pass


class Subnet(NeutronResource):
    def actions(self) -> list[ResourceAction]:
        from neutronclient.neutron.v2_0 import subnet

        return [
            ResourceAction("add", subnet.CreateSubnet, self.add),
            ResourceAction("update", subnet.UpdateSubnet, self.update),
            ResourceAction("del", subnet.DeleteSubnet, self.delete),
        ]

    def add(self, client: OVNClient, body: dict):
        pass

    def update(self, client: OVNClient, body: dict):
        pass

    def delete(self, client: OVNClient, body: dict):
        pass
