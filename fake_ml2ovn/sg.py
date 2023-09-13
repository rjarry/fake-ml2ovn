# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2023 Robin Jarry

from .base import NeutronResource, OVNClient, ResourceAction


class SecurityGroup(NeutronResource):
    def actions(self) -> list[ResourceAction]:
        from neutronclient.neutron.v2_0 import securitygroup

        return [
            ResourceAction("add", securitygroup.CreateSecurityGroup, self.add),
            ResourceAction("del", securitygroup.DeleteSecurityGroup, self.delete),
            ResourceAction(
                "add-rule", securitygroup.CreateSecurityGroupRule, self.add_rule
            ),
            ResourceAction(
                "del-rule", securitygroup.DeleteSecurityGroupRule, self.del_rule
            ),
        ]

    def add(self, client: OVNClient, body: dict):
        pass

    def delete(self, client: OVNClient, body: dict):
        pass

    def add_rule(self, client: OVNClient, body: dict):
        pass

    def del_rule(self, client: OVNClient, body: dict):
        pass
