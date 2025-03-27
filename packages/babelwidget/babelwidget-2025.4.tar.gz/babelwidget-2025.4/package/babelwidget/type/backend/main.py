"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2023
SEE COPYRIGHT NOTICE BELOW
"""

import dataclasses as d
import sys as s
import types as t

from babelwidget.constant.definition import CATALOG
from babelwidget.constant.path import BACKEND_PATH, GENERIC_PATH
from babelwidget.extension.python import STANDARD_MODULES
from babelwidget.task.building import NewWidgetClass
from babelwidget.task.importing import (
    ImportedBackendWidgetModule,
    ImportedElement,
    ImportedPluginModule,
)
from babelwidget.type.backend.protocol import backend_p


@d.dataclass(repr=False, eq=False)
class backend_t(backend_p):
    name: str

    should_instantiation_event_loop: d.InitVar[bool] = True

    def __post_init__(self, should_instantiation_event_loop) -> None:
        """"""
        path = BACKEND_PATH / self.name
        if not path.is_dir():
            raise ValueError(f"Invalid backend folder: {path}.")

        for path in (path, GENERIC_PATH):
            for node in path.rglob("*.py"):
                if (not node.is_file()) or node.name.startswith("_"):
                    continue

                module_plugin = ImportedPluginModule(node)
                content = dir(module_plugin)

                if CATALOG in content:
                    # File babelwidget.catalog.<SOME_BACKEND>.widget.py: Create widget
                    # classes and add them to the backend.
                    default_module = ImportedBackendWidgetModule(module_plugin)
                    for stripe, definition in getattr(module_plugin, CATALOG).items():
                        if isinstance(definition, str):
                            element = ImportedElement(definition, default_module)
                        else:
                            base = ImportedElement(definition[0], default_module)
                            element = NewWidgetClass(
                                stripe,
                                base,
                                attributes=definition[1],
                                methods=definition[2],
                                class_methods=definition[3],
                            )
                            assert issubclass(element, definition[4])
                        setattr(self, stripe, element)
                else:
                    # File babelwidget.catalog.<SOME_BACKEND>.<SOME_OTHER_FILE>: Add any
                    # non-module, non-private, non-standard element to the backend.
                    for name in content:
                        if name[0] == "_":
                            continue

                        element = getattr(module_plugin, name)
                        if not (
                            isinstance(element, t.ModuleType)
                            or (not hasattr(element, "__module__"))
                            or (element.__module__[0] == "_")
                            or (element.__module__ in STANDARD_MODULES)
                        ):
                            setattr(self, name, element)

        if should_instantiation_event_loop:
            self.event_loop = self.event_loop_t(s.argv)


"""
COPYRIGHT NOTICE

This software is governed by the CeCILL  license under French law and
abiding by the rules of distribution of free software.  You can  use,
modify and/ or redistribute the software under the terms of the CeCILL
license as circulated by CEA, CNRS and INRIA at the following URL
"http://www.cecill.info".

As a counterpart to the access to the source code and  rights to copy,
modify and redistribute granted by the license, users are provided only
with a limited warranty  and the software's author,  the holder of the
economic rights,  and the successive licensors  have only  limited
liability.

In this respect, the user's attention is drawn to the risks associated
with loading,  using,  modifying and/or developing or reproducing the
software by the user in light of its specific status of free software,
that may mean  that it is complicated to manipulate,  and  that  also
therefore means  that it is reserved for developers  and  experienced
professionals having in-depth computer knowledge. Users are therefore
encouraged to load and test the software's suitability as regards their
requirements in conditions enabling the security of their systems and/or
data to be ensured and,  more generally, to use and operate it in the
same conditions as regards security.

The fact that you are presently reading this means that you have had
knowledge of the CeCILL license and that you accept its terms.

SEE LICENCE NOTICE: file README-LICENCE-utf8.txt at project source root.

This software is being developed by Eric Debreuve, a CNRS employee and
member of team Morpheme.
Team Morpheme is a joint team between Inria, CNRS, and UniCA.
It is hosted by the Centre Inria d'Université Côte d'Azur, Laboratory
I3S, and Laboratory iBV.

CNRS: https://www.cnrs.fr/index.php/en
Inria: https://www.inria.fr/en/
UniCA: https://univ-cotedazur.eu/
Centre Inria d'Université Côte d'Azur: https://www.inria.fr/en/centre/sophia/
I3S: https://www.i3s.unice.fr/en/
iBV: http://ibv.unice.fr/
Team Morpheme: https://team.inria.fr/morpheme/
"""
