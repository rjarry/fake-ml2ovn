#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2023 Robin Jarry

"""
Simulate neutron commands to OVN northbound objects.
"""

import argparse
import sys

from . import ip, mock, network, ovn, port, router, sg


def main():
    finder = mock.MockFinder(["cliff.display", "cliff.show"])
    sys.meta_path.insert(0, finder)

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-n",
        "--nb-ovsdb-endpoint",
        default="tcp:127.0.0.1:6641",
        help="""
        The OVN northbound ovsdb socket endpoint.
        """,
    )
    parser.add_argument(
        "-s",
        "--sb-ovsdb-endpoint",
        default="tcp:127.0.0.1:6642",
        help="""
        The OVN southbound ovsdb socket endpoint.
        """,
    )
    sub = parser.add_subparsers(metavar="SUB_COMMAND", description=None)
    resources = [
        network.Network(sub),
        port.Port(sub),
        router.Router(sub),
        ip.Subnet(sub),
        ip.FloatingIp(sub),
        sg.SecurityGroup(sub),
    ]
    args = parser.parse_args()

    client = ovn.connect(args.nb_ovsdb_endpoint, args.sb_ovsdb_endpoint)

    args.callback(client, args)

    del resources  # make linters happy


if __name__ == "__main__":
    main()
