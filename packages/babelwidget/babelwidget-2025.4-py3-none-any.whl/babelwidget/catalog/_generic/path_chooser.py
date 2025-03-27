"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2023
SEE COPYRIGHT NOTICE BELOW
"""

import typing as h
from pathlib import Path as path_t

from babelwidget.type.backend.main import backend_t
from babelwidget.type.dialog.generic import dialog_p
from babelwidget.type.widget.button import button_p
from babelwidget.type.widget.dropdown_choice import dropdown_choice_p
from babelwidget.type.widget.label import label_p
from babelwidget.type.widget.radio_choice import radio_choice_p
from babelwidget.type.widget.text_line import text_line_p
from babelwidget.type.widget.text_list import text_list_p

_WHY = {"input": "Reading/Input", "output": "Writing/Output"}
_WHAT = {
    "document": "a Document",
    "folder": "a Folder",
    "any": "a Document or a Folder",
}

_N_COLUMNS = 6
_N_COLUMNS_OVER_3 = _N_COLUMNS // 3


class path_chooser_t:
    purpose: h.Literal["input", "output"]
    kind: h.Literal["any", "document", "folder"]

    accepts_documents: bool
    accepts_folders: bool

    folder: path_t | None
    parents: tuple[path_t, ...] | None
    nodes: list[path_t] | None
    documents: list[path_t] | None
    folders: list[path_t] | None
    others: list[path_t] | None

    should_show_hidden: bool

    backend: backend_t
    library_wgt: dialog_p
    parents_wgt: dropdown_choice_p
    goto_parent_wgt: button_p
    nodes_wgt: text_list_p
    hidden_label: label_p
    hidden_true: radio_choice_p
    hidden_false: radio_choice_p
    extensions_wgt: dropdown_choice_p
    custom: text_line_p | None
    create: button_p | None
    cancel: button_p
    enter: button_p
    select: button_p

    selected_node: path_t | None

    _programmatically_caused: bool


    @classmethod
    def New(
        cls,
        purpose: h.Literal["input", "output"],
        kind: h.Literal["any", "document", "folder"],
        backend: backend_t,
        /,
        *,
        folder: str | path_t = path_t.home(),
        message: str | None = None,
    ) -> h.Self:
        """"""
        output = cls()

        output.purpose = purpose
        output.kind = kind

        output.accepts_documents = kind in ("document", "any")
        output.accepts_folders = kind in ("folder", "any")

        output.folder = None
        output.parents = None
        output.nodes = None
        output.documents = None
        output.folders = None
        output.others = None

        output.should_show_hidden = False

        output.selected_node = None
        output._programmatically_caused = False

        output.backend = backend
        output.library_wgt = backend.dialog_t()

        if message is None:
            message = ""
        else:
            message += ": "
        title_wgt = backend.label_t(
            f"<h3>{message}Select {_WHAT[kind]} for {_WHY[purpose]}</h3>"
        )

        parents_wgt = backend.dropdown_choice_t()
        goto_parent_wgt = backend.button_t("Up")

        nodes_wgt = backend.text_list_t()

        hidden_label = backend.label_t("Show Hidden")
        hidden_true = backend.radio_choice_t("True")
        hidden_false = backend.radio_choice_t("False")
        if output.accepts_documents:
            extensions_wgt = backend.dropdown_choice_t()
        else:
            extensions_wgt = None

        if purpose == "output":
            custom = backend.text_line_t()
            create = backend.button_t("Create Folder")
        else:
            custom = create = None

        cancel = backend.button_t("Cancel")
        enter = backend.button_t("Enter Folder")
        select = backend.button_t("Select")

        output.parents_wgt = parents_wgt
        output.goto_parent_wgt = goto_parent_wgt
        output.nodes_wgt = nodes_wgt
        output.hidden_label = hidden_label
        output.hidden_true = hidden_true
        output.hidden_false = hidden_false
        output.extensions_wgt = extensions_wgt
        output.custom = custom
        output.create = create
        output.cancel = cancel
        output.enter = enter
        output.select = select

        hidden_true.setChecked(False)
        hidden_false.setChecked(True)
        if create is not None:
            create.setEnabled(False)
        enter.setEnabled(False)
        select.setEnabled(output.accepts_folders)

        # cancel.setStyleSheet('QPushButton {background-color: red;}')
        # enter.setStyleSheet('QPushButton {background-color: blue;}')
        # select.setStyleSheet('QPushButton {background-color: green;}')

        output.SetFolder(path_t(folder))

        parents_wgt.currentIndexChanged.connect(output._OnFolderUpChangeRequest)
        goto_parent_wgt.clicked.connect(lambda: output._OnFolderUpChangeRequest(1))
        nodes_wgt.currentRowChanged.connect(output._OnNewNodeSelection)
        nodes_wgt.itemDoubleClicked.connect(output._OnNodeDoubleClicked)
        if custom is not None:
            custom.textChanged.connect(output._OnCustomChanged)
            create.clicked.connect(output._OnFolderCreationRequest)
        hidden_true.released.connect(output._OnHiddenChangeRequest)
        hidden_false.released.connect(output._OnHiddenChangeRequest)
        if extensions_wgt is not None:
            extensions_wgt.currentIndexChanged.connect(
                output._OnExtensionFilteringRequest
            )
        cancel.clicked.connect(output.library_wgt.close)
        enter.clicked.connect(output._OnFolderDownChangeRequest)
        select.clicked.connect(output._OnNodeSelection)

        # For some reason, clearSelection leaves a dimmed selection instead of
        # "removing" it completely. Using setCurrentRow(-1) instead.
        shortcut = backend.keyboard_shortcut_t(backend.KEY_e.Deselect, output.library_wgt)
        shortcut.activated.connect(lambda: output.nodes_wgt.setCurrentRow(-1))

        layout = backend.layout_grid_t()
        layout.addWidget(title_wgt, 0, 0, 1, _N_COLUMNS)
        layout.addWidget(parents_wgt, 1, 0, 1, _N_COLUMNS - 1)
        layout.addWidget(goto_parent_wgt, 1, _N_COLUMNS - 1)
        layout.addWidget(nodes_wgt, 2, 0, 1, _N_COLUMNS)
        layout.addWidget(hidden_label, 3, 0)
        layout.addWidget(hidden_true, 3, 1)
        layout.addWidget(hidden_false, 3, 2)
        if extensions_wgt is not None:
            layout.addWidget(extensions_wgt, 3, 3, 1, 3)
        if custom is None:
            next_row = 4
        else:
            layout.addWidget(custom, 4, 0, 1, _N_COLUMNS - 1)
            layout.addWidget(create, 4, _N_COLUMNS - 1)
            next_row = 5
        layout.addWidget(cancel, next_row, 0, 1, _N_COLUMNS_OVER_3)
        layout.addWidget(enter, next_row, _N_COLUMNS_OVER_3, 1, _N_COLUMNS_OVER_3)
        layout.addWidget(select, next_row, 2 * _N_COLUMNS_OVER_3, 1, _N_COLUMNS_OVER_3)
        output.library_wgt.setLayout(layout)

        return output

    def NewSelected(self) -> path_t | None:
        """"""
        self.library_wgt.exec()
        return self.selected_node

    def SetFolder(self, folder: path_t, /) -> None:
        """"""
        nodes = tuple(folder.glob("*"))
        documents = sorted(filter(path_t.is_file, nodes))
        folders = sorted(filter(_NodeIsFolderLike, nodes))
        others = sorted(set(nodes).difference(documents + folders))

        self.folder = folder
        self.parents = (folder,) + tuple(folder.parents)

        self.documents = documents
        self.folders = folders
        self.others = others

        self.parents_wgt.clear()
        self.parents_wgt.addItems(map(str, self.parents))

        self._UpdateNodes()

        if self.extensions_wgt is not None:
            # /!\\ Currently, the extension of hidden documents are discarded.
            extensions = ("*",) + tuple(
                set(
                    filter(
                        lambda _: _.__len__() > 0,
                        (
                            _.suffix
                            for _ in documents
                            if not str(_.name).startswith(".")
                        ),
                    )
                )
            )
            self.extensions_wgt.clear()
            self.extensions_wgt.addItems(extensions)

    def _UpdateNodes(self) -> None:
        """"""
        MatchHiddenStatus = lambda _: self.should_show_hidden or not str(
            _.name
        ).startswith(".")
        if self.extensions_wgt is None:
            valid_extension = "*"
        else:
            valid_extension = self.extensions_wgt.currentText()
        documents = sorted(
            filter(
                lambda _: MatchHiddenStatus(_) and (valid_extension in ("*", _.suffix)),
                self.documents,
            )
        )
        folders = sorted(filter(MatchHiddenStatus, self.folders))
        others = sorted(filter(MatchHiddenStatus, self.others))

        documents_postfixes = ("",) * documents.__len__()
        folders_postfixes = ("/",) * folders.__len__()
        others_postfixes = ("?",) * others.__len__()

        documents_validity_s = (self.accepts_documents,) * documents.__len__()
        folders_validity_s = (self.accepts_folders,) * folders.__len__()
        others_validity_s = (False,) * others.__len__()
        if self.accepts_folders:
            nodes = folders + documents + others
            postfixes = folders_postfixes + documents_postfixes + others_postfixes
            validity_s = folders_validity_s + documents_validity_s + others_validity_s
        else:
            nodes = documents + folders + others
            postfixes = documents_postfixes + folders_postfixes + others_postfixes
            validity_s = documents_validity_s + folders_validity_s + others_validity_s

        self.nodes = nodes
        self.nodes_wgt.clear()
        self.nodes_wgt.addItems(f"{_.name}{__}" for _, __ in zip(nodes, postfixes))

        for row, valid in enumerate(validity_s):
            if not valid:
                self.nodes_wgt.item(row).setForeground(self.backend.COLOR_e.Gray)

    def _OnFolderUpChangeRequest(self, index: int, /) -> None:
        """"""
        if self._programmatically_caused:
            return

        self._programmatically_caused = True
        self.SetFolder(self.parents[index])
        self._programmatically_caused = False

    def _OnFolderDownChangeRequest(self) -> None:
        """"""
        if self._programmatically_caused:
            return

        self._programmatically_caused = True
        self.SetFolder(self.nodes[self.nodes_wgt.currentRow()])
        self._programmatically_caused = False

    def _OnNewNodeSelection(self, row: int, /) -> None:
        """"""
        if row < 0:
            self.enter.setEnabled(False)
            self.select.setEnabled(self.accepts_folders)
        else:
            node = self.nodes[row]
            node_is_folder = _NodeIsFolderLike(node)
            self.enter.setEnabled(node_is_folder)
            self.select.setEnabled(
                (self.accepts_documents and node.is_file())
                or (self.accepts_folders and node_is_folder)
            )

    def _OnNodeDoubleClicked(self, _, /) -> None:
        """
        Hint of _ is, for Qt6 for example, PyQt6.QtWidgets.QListWidgetItem.
        """
        if self._programmatically_caused:
            return

        node = self.nodes[self.nodes_wgt.currentRow()]
        if node.is_file():
            if self.accepts_documents:
                if self.purpose == "input":
                    if _NodeIsEmpty(node):
                        confirmed = self._ConfirmedAnswer(
                            f"{node} is empty.", "Do you want to open/use it anyway?"
                        )
                    else:
                        confirmed = True
                else:
                    confirmed = self._ConfirmedAnswer(
                        f"{node} exists.", "Do you want to override it?"
                    )
                if confirmed:
                    self.selected_node = node
                    self.library_wgt.close()
            elif self.custom is not None:
                self.custom.setText(node.name)
        elif _NodeIsFolderLike(node):
            self._programmatically_caused = True
            self.SetFolder(node)
            self._programmatically_caused = False

    def _OnHiddenChangeRequest(self) -> None:
        """"""
        self.should_show_hidden = self.hidden_true.isChecked()
        self.hidden_false.setChecked(not self.should_show_hidden)

        self._programmatically_caused = True
        self._UpdateNodes()
        self._programmatically_caused = False

    def _OnExtensionFilteringRequest(self) -> None:
        """"""
        if self._programmatically_caused:
            return

        self._programmatically_caused = True
        self._UpdateNodes()
        self._programmatically_caused = False

    def _OnCustomChanged(self, content: str, /) -> None:
        """"""
        self.create.setEnabled(not (self.folder / content).exists())

    def _OnFolderCreationRequest(self) -> None:
        """"""
        folder = self.folder / self.custom.Text()
        try:
            folder.mkdir()
        except Exception as exception:
            self.backend.ShowErrorMessage(f"Folder {folder} could not be created:\n{exception}")
        else:
            self._programmatically_caused = True
            self.SetFolder(folder)
            self._programmatically_caused = False

    def _OnNodeSelection(self) -> None:
        """"""
        if self.custom is None:
            custom = ""
        else:
            custom = self.custom.Text()
        if custom.__len__() > 0:
            node = self.folder / custom
        elif (row := self.nodes_wgt.currentRow()) >= 0:
            node = self.nodes[row]
        else:
            node = self.folder

        confirmed = False
        if self.purpose == "input":
            if self.accepts_documents and node.is_file():
                if _NodeIsEmpty(node):
                    confirmed = self._ConfirmedAnswer(
                        f"{node} is empty.", "Do you want to open/use it anyway?"
                    )
                else:
                    confirmed = True
            elif self.accepts_folders and _NodeIsFolderLike(node):
                if _NodeIsEmpty(node):
                    confirmed = self._ConfirmedAnswer(
                        f"{node} is empty.", "Do you want to use it as input anyway?"
                    )
                else:
                    confirmed = True
        else:
            if self.accepts_documents and node.is_file():
                confirmed = self._ConfirmedAnswer(
                    f"{node} exists.", "Do you want to override it?"
                )
            elif self.accepts_folders and _NodeIsFolderLike(node):
                if _NodeIsEmpty(node):
                    confirmed = True
                else:
                    confirmed = self._ConfirmedAnswer(
                        f"{node} is not empty.",
                        "Do you want to use it as output anyway?",
                    )

        if confirmed:
            self.selected_node = node
            self.library_wgt.close()


    def _ConfirmedAnswer(self, message: str, question: str, /) -> bool:
        """"""
        message_dialog_t = self.backend.message_dialog_t
        dialog = message_dialog_t()

        dialog.setText(message)
        dialog.setInformativeText(question)
        dialog.setStandardButtons(
            message_dialog_t.StandardButton.Yes | message_dialog_t.StandardButton.No
        )
        dialog.setDefaultButton(message_dialog_t.StandardButton.No)

        answer = dialog.exec()

        return answer == message_dialog_t.StandardButton.Yes


def _NodeIsFolderLike(node: path_t, /) -> bool:
    """"""
    return node.is_dir() or node.is_junction() or node.is_mount()


def _NodeIsEmpty(node: path_t, /) -> bool:
    """"""
    if node.is_file():
        return node.stat().st_size == 0

    return tuple(node.glob("*")).__len__() == 0


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
