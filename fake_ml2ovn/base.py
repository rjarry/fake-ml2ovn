# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2023 Robin Jarry

import argparse
import dataclasses
import re
import typing


OVNClient = typing.ForwardRef(
    "neutron.plugins.ml2.drivers.ovn.mech_driver.ovsdb.ovn_client.OVNClient"
)


@dataclasses.dataclass
class ResourceAction:
    name: str
    cmd_class: "neutronclient.neutron.v2_0.NeutronCommand"
    callback: typing.Callable[[OVNClient, dict], None]


class NeutronResource:
    def __init__(self, sub_parsers):
        desc = f"Manage {self.name()}s"
        p = sub_parsers.add_parser(self.name(), help=desc, description=desc)
        sub = p.add_subparsers(metavar="SUB_COMMAND", description=None)

        for a in self.actions():
            cmd = a.cmd_class(None, None)
            parser = cmd.get_parser(f"{sub._prog_prefix} {a.name}")
            parser.set_defaults(callback=self._make_callback(cmd, a.callback))
            parser.formatter_class = argparse.ArgumentDefaultsHelpFormatter
            parser.epilog = None
            choice_action = sub._ChoicesPseudoAction(a.name, [], parser.description)
            sub._choices_actions.append(choice_action)
            sub._name_parser_map[a.name] = parser

    def _make_callback(self, cmd, callback):
        def inner(client, args):
            body = cmd.args2body(args)
            return callback(client, body)

        return inner

    def name(self):
        dashed = re.sub(r"([A-Z])", r"-\1", self.__class__.__name__)
        return dashed.strip("-").lower()

    def actions(self) -> list[ResourceAction]:
        raise NotImplementedError()
