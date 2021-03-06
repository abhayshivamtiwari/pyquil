##############################################################################
# Copyright 2016-2019 Rigetti Computing
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
##############################################################################
import warnings
from collections import namedtuple

import networkx as nx

QubitSpecs = namedtuple("_QubitSpecs", ["id", "fRO", "f1QRB", "f1QRB_std_err",
                                        "f1Q_simultaneous_RB", "f1Q_simultaneous_RB_std_err", "T1",
                                        "T2", "fActiveReset"])
EdgeSpecs = namedtuple("_QubitQubitSpecs", ["targets", "fBellState", "fCZ", "fCZ_std_err",
                                            "fCPHASE"])
_Specs = namedtuple("_Specs", ["qubits_specs", "edges_specs"])


class Specs(_Specs):
    """
    Basic specifications for the device, such as gate fidelities and coherence times.

    :ivar List[QubitSpecs] qubits_specs: The specs associated with individual qubits.
    :ivar List[EdgesSpecs] edges_specs: The specs associated with edges, or qubit-qubit pairs.
    """

    def f1QRBs(self):
        """
        Get a dictionary of single-qubit randomized benchmarking fidelities (for individual gate
        operation, normalized to unity) from the specs, keyed by qubit index.

        :return: A dictionary of 1Q RB fidelities, normalized to unity.
        :rtype: Dict[int, float]
        """
        return {qs.id: qs.f1QRB for qs in self.qubits_specs}

    def f1QRB_std_errs(self):
        """
        Get a dictionary of the standard errors of single-qubit randomized
        benchmarking fidelities (for individual gate operation, normalized to unity)
        from the specs, keyed by qubit index.

        :return: A dictionary of 1Q RB fidelity standard errors, normalized to unity.
        :rtype: Dict[int, float]
        """
        return {qs.id: qs.f1QRB_std_err for qs in self.qubits_specs}

    def f1Q_simultaneous_RBs(self):
        """
        Get a dictionary of single-qubit randomized benchmarking fidelities (for simultaneous gate
        operation across the chip, normalized to unity) from the specs, keyed by qubit index.

        :return: A dictionary of simultaneous 1Q RB fidelities, normalized to unity.
        :rtype: Dict[int, float]
        """
        return {qs.id: qs.f1Q_simultaneous_RB for qs in self.qubits_specs}

    def f1Q_simultaneous_RB_std_errs(self):
        """
        Get a dictionary of the standard errors of single-qubit randomized
        benchmarking fidelities (for simultaneous gate operation across the chip, normalized to
        unity) from the specs, keyed by qubit index.

        :return: A dictionary of simultaneous 1Q RB fidelity standard errors, normalized to unity.
        :rtype: Dict[int, float]
        """
        return {qs.id: qs.f1Q_simultaneous_RB_std_err for qs in self.qubits_specs}

    def fROs(self):
        """
        Get a dictionary of single-qubit readout fidelities (normalized to unity)
        from the specs, keyed by qubit index.

        :return: A dictionary of RO fidelities, normalized to unity.
        :rtype: Dict[int, float]
        """
        return {qs.id: qs.fRO for qs in self.qubits_specs}

    def fActiveResets(self):
        """
        Get a dictionary of single-qubit active reset fidelities (normalized to unity) from the
        specs, keyed by qubit index.

        :return: A dictionary of reset fidelities, normalized to unity.
        """
        return {qs.id: qs.fActiveReset for qs in self.qubits_specs}

    def T1s(self):
        """
        Get a dictionary of T1s (in seconds) from the specs, keyed by qubit index.

        :return: A dictionary of T1s, in seconds.
        :rtype: Dict[int, float]
        """
        return {qs.id: qs.T1 for qs in self.qubits_specs}

    def T2s(self):
        """
        Get a dictionary of T2s (in seconds) from the specs, keyed by qubit index.

        :return: A dictionary of T2s, in seconds.
        :rtype: Dict[int, float]
        """
        return {qs.id: qs.T2 for qs in self.qubits_specs}

    def fBellStates(self):
        """
        Get a dictionary of two-qubit Bell state fidelities (normalized to unity)
        from the specs, keyed by targets (qubit-qubit pairs).

        :return: A dictionary of Bell state fidelities, normalized to unity.
        :rtype: Dict[tuple(int, int), float]
        """
        warnings.warn(DeprecationWarning("fBellState device specs have been deprecated, and will "
                                         "be removed in release v2.13 (targeted for October 2019)"))
        return {tuple(es.targets): es.fBellState for es in self.edges_specs}

    def fCZs(self):
        """
        Get a dictionary of CZ fidelities (normalized to unity) from the specs,
        keyed by targets (qubit-qubit pairs).

        :return: A dictionary of CZ fidelities, normalized to unity.
        :rtype: Dict[tuple(int, int), float]
        """
        return {tuple(es.targets): es.fCZ for es in self.edges_specs}

    def fCZ_std_errs(self):
        """
        Get a dictionary of the standard errors of the CZ fidelities from the specs,
        keyed by targets (qubit-qubit pairs).

        :return: A dictionary of CZ fidelities, normalized to unity.
        :rtype: Dict[tuple(int, int), float]
        """
        return {tuple(es.targets): es.fCZ_std_err for es in self.edges_specs}

    def fCPHASEs(self):
        """
        Get a dictionary of CPHASE fidelities (normalized to unity) from the specs,
        keyed by targets (qubit-qubit pairs).

        :return: A dictionary of CPHASE fidelities, normalized to unity.
        :rtype: Dict[tuple(int, int), float]
        """
        warnings.warn(DeprecationWarning("fCPHASE device specs have been deprecated, and will "
                                         "be removed in release v2.13 (targeted for October 2019)"))
        return {tuple(es.targets): es.fCPHASE for es in self.edges_specs}

    def to_dict(self):
        """
        Create a JSON-serializable representation of the device Specs.

        The dictionary representation is of the form::

            {
                '1Q': {
                    "0": {
                        "f1QRB": 0.99,
                        "f1QRB_std_err": 0.02,
                        "T1": 20e-6,
                        ...
                    },
                    "1": {
                        "f1QRB": 0.989,
                        "f1QRB_std_err": 0.015,
                        "T1": 19e-6,
                        ...
                    },
                    ...
                },
                '2Q': {
                    "1-4": {
                        "fBellState": 0.93,
                        "fCZ": 0.92,
                        "fCZ_std_err": 0.03,
                        "fCPHASE": 0.91
                    },
                    "1-5": {
                        "fBellState": 0.9,
                        "fCZ": 0.89,
                        "fCZ_std_err": 0.05,
                        "fCPHASE": 0.88
                    },
                    ...
                },
                ...
            }

        :return: A dctionary representation of self.
        :rtype: Dict[str, Any]
        """
        return {
            '1Q': {
                "{}".format(qs.id): {
                    'f1QRB': qs.f1QRB,
                    'f1QRB_std_err': qs.f1QRB_std_err,
                    'f1Q_simultaneous_RB': qs.f1Q_simultaneous_RB,
                    'f1Q_simultaneous_RB_std_err': qs.f1Q_simultaneous_RB_std_err,
                    'fRO': qs.fRO,
                    'T1': qs.T1,
                    'T2': qs.T2,
                    'fActiveReset': qs.fActiveReset
                } for qs in self.qubits_specs
            },
            '2Q': {
                "{}-{}".format(*es.targets): {
                    'fBellState': es.fBellState,
                    'fCZ': es.fCZ,
                    'fCZ_std_err': es.fCZ_std_err,
                    'fCPHASE': es.fCPHASE
                } for es in self.edges_specs
            }
        }

    @staticmethod
    def from_dict(d):
        """
        Re-create the Specs from a dictionary representation.

        :param Dict[str, Any] d: The dictionary representation.
        :return: The restored Specs.
        :rtype: Specs
        """
        return Specs(
            qubits_specs=sorted([QubitSpecs(id=int(q),
                                            fRO=qspecs.get('fRO'),
                                            f1QRB=qspecs.get('f1QRB'),
                                            f1QRB_std_err=qspecs.get('f1QRB_std_err'),
                                            f1Q_simultaneous_RB=qspecs.get('f1Q_simultaneous_RB'),
                                            f1Q_simultaneous_RB_std_err=qspecs.get(
                                                'f1Q_simultaneous_RB_std_err'),
                                            T1=qspecs.get('T1'),
                                            T2=qspecs.get('T2'),
                                            fActiveReset=qspecs.get('fActiveReset'))
                                 for q, qspecs in d["1Q"].items()],
                                key=lambda qubit_specs: qubit_specs.id),
            edges_specs=sorted([EdgeSpecs(targets=[int(q) for q in e.split('-')],
                                          fBellState=especs.get('fBellState'),
                                          fCZ=especs.get('fCZ'),
                                          fCZ_std_err=especs.get('fCZ_std_err'),
                                          fCPHASE=especs.get('fCPHASE'))
                                for e, especs in d["2Q"].items()],
                               key=lambda edge_specs: edge_specs.targets)
        )


def specs_from_graph(graph: nx.Graph):
    """
    Generate a Specs object from a NetworkX graph with placeholder values for the actual specs.

    :param graph: The graph
    """
    qspecs = [QubitSpecs(id=q, fRO=0.90, f1QRB=0.99, f1QRB_std_err=0.01,
                         f1Q_simultaneous_RB=0.99, f1Q_simultaneous_RB_std_err=0.02, T1=30e-6,
                         T2=30e-6, fActiveReset=0.99)
              for q in graph.nodes]
    especs = [EdgeSpecs(targets=(q1, q2), fBellState=0.90, fCZ=0.90, fCZ_std_err=0.05, fCPHASE=0.80)
              for q1, q2 in graph.edges]
    return Specs(qspecs, especs)
