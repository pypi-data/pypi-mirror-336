"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2023
SEE COPYRIGHT NOTICE BELOW
"""

import typing as h

from babelwidget.type.dialog.generic import dialog_p
from babelwidget.type.dialog.message import message_dialog_p
from babelwidget.type.layout.scroll_container import scroll_container_p
from babelwidget.type.widget.button import button_p
from babelwidget.type.widget.dropdown_choice import dropdown_choice_p
from babelwidget.type.widget.image import image_p
from babelwidget.type.widget.label import label_p
from babelwidget.type.widget.menu import menu_p
from babelwidget.type.widget.radio_choice import radio_choice_p
from babelwidget.type.widget.text_box import text_box_p
from babelwidget.type.widget.text_line import text_line_p
from babelwidget.type.widget.text_list import text_list_p

base_h = h.TypeVar("base_h")
color_h = h.TypeVar("color_h")
constant_h = h.TypeVar("constant_h")
enum_h = h.TypeVar("enum_h")
layout_grid_h = h.TypeVar("layout_grid_h")
group_h = h.TypeVar("group_h")
layout_h_h = h.TypeVar("layout_h_h")
stack_h = h.TypeVar("stack_h")
tabs_h = h.TypeVar("tabs_h")
layout_v_h = h.TypeVar("layout_v_h")


class backend_p(h.Protocol):
    ALIGNED_CENTER: constant_h
    ALIGNED_HCENTER: constant_h
    ALIGNED_LEFT: constant_h
    ALIGNED_RIGHT: constant_h
    ALIGNED_TOP: constant_h
    BASE_PALETTE: constant_h
    DIALOG_ACCEPTATION: constant_h
    DIALOG_ACCEPT_OPEN: constant_h
    DIALOG_ACCEPT_SAVE: constant_h
    DIALOG_AUTO_OVERWRITE: constant_h
    DIALOG_MODE_ANY: constant_h
    DIALOG_MODE_EXISTING_FILE: constant_h
    DIALOG_MODE_FOLDER: constant_h
    FORMAT_RICH: constant_h
    LINE_NO_WRAP: constant_h
    SELECTABLE_TEXT: constant_h
    SIZE_EXPANDING: constant_h
    SIZE_FIXED: constant_h
    SIZE_MINIMUM: constant_h
    TAB_POSITION_EAST: constant_h
    WIDGET_TYPE: constant_h
    WORD_NO_WRAP: constant_h
    COLOR_e: enum_h
    KEY_e: enum_h

    base_t: base_h

    button_t: button_p
    dropdown_choice_t: dropdown_choice_p
    group_t: group_h
    image_t: image_p
    label_t: label_p
    menu_t: menu_p
    radio_choice_t: radio_choice_p
    scroll_container_t: scroll_container_p
    stack_t: stack_h
    tabs_t: tabs_h
    text_box_t: text_box_p
    text_line_t: text_line_p
    text_list_t: text_list_p

    layout_grid_t: layout_grid_h
    layout_h_t: layout_h_h
    layout_v_t: layout_v_h

    dialog_t: dialog_p
    message_dialog_t: message_dialog_p

    event_loop_t: h.Any
    event_loop: h.Any

    keyboard_shortcut_t: h.Any

    Color: h.Callable[[str], color_h]

    ShowMessage: h.Callable[..., None]
    ShowErrorMessage: h.Callable[..., None]

    AddMessageCanal: h.Callable[[h.Any, str, h.Callable], None]
    RemoveMessageCanal: h.Callable[[h.Any, str], None]


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
