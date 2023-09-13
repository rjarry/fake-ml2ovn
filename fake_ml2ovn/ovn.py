# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2023 Robin Jarry

import itertools
import sys

from .mock import MockFinder


def connect(nb_endpoint: str, sb_endpoint: str) -> "OVNClient":
    _isolate_ml2_code(nb_endpoint, sb_endpoint)

    from neutron.plugins.ml2.drivers.ovn.agent import neutron_agent
    from neutron.plugins.ml2.drivers.ovn.mech_driver import mech_driver
    from neutron.plugins.ml2.drivers.ovn.mech_driver.ovsdb import (
        impl_idl_ovn,
        ovn_client,
    )
    from neutron_lib.worker import BaseWorker

    driver = mech_driver.OVNMechanismDriver()
    driver.initialize()
    neutron_agent.AgentCache(driver)

    nb_idl = impl_idl_ovn.OvsdbNbOvnIdl.from_worker(BaseWorker, driver)
    sb_idl = impl_idl_ovn.OvsdbSbOvnIdl.from_worker(BaseWorker, driver)

    return ovn_client.OVNClient(nb_idl, sb_idl)


def _isolate_ml2_code(nb_endpoint: str, sb_endpoint: str):
    # We want to use only the ML2 driver plugin in isolation of everything else.
    # Importing the following modules and any of their children causes errors
    # because they require valid database connection settings.
    # We couldn't care less about neutron database objects. Mock these imports so
    # that dummy modules/objects are returned and everyone is happy.
    finder = MockFinder(
        ["neutron_lib.db", "neutron.db", "neutron.objects", "oslo_policy"]
    )
    sys.meta_path.insert(0, finder)

    from neutron import opts as neutron_opts
    from neutron.conf.plugins.ml2.drivers.ovn import ovn_conf
    from oslo_config import cfg

    # We don't have any neutron.conf file. We only want to use the default settings
    # with some exceptions. Patch the oslo_config object so that we can return
    # whatever we want without issues.
    options = {}
    for group, opts in itertools.chain(
        neutron_opts.list_opts(),
        neutron_opts.list_ml2_conf_opts(),
        neutron_opts.list_ovs_opts(),
        ovn_conf.list_opts(),
    ):
        if group == "DEFAULT":
            options.setdefault(None, []).extend(opts)
        else:
            options.setdefault(group, []).extend(opts)

    def get_config(name, group=None, namespace=None):
        if group is None and name.lower() in options:
            return (
                cfg.ConfigOpts.GroupAttr(
                    cfg.CONF,
                    cfg.CONF._get_group(name, True),  # pylint: disable=protected-access
                ),
                None,
            )
        if group is not None:
            group = group.name.lower()
        for o in options.get(group, []):
            if o.name != name:
                continue
            loc = cfg.LocationInfo(cfg.Locations.opt_default, "")
            if o.name == "ovn_nb_connection":
                return (nb_endpoint, loc)
            if o.name == "ovn_sb_connection":
                return (sb_endpoint, loc)
            if o.name == "max_header_size":
                return (38, loc)
            return (o.default, loc)
        raise cfg.NoSuchOptError(name, group)

    cfg.CONF._do_get = get_config  # pylint: disable=protected-access
    cfg.CONF.find_file = lambda _: "/tmp"
