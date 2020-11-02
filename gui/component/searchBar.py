from PySide2.QtGui import QStandardItemModel, QStandardItem
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QLineEdit, QCompleter

class SearchBar(QLineEdit):
    def __init__(self, parent=None, placeholder="", completerContents=[]):
        super(SearchBar, self).__init__(parent)

        self.setPlaceholderText(placeholder)
        self.completer = QCompleter(self)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.setCompleter(self.completer)
        self.updateCompletionList(completerContents)
        
    def updateCompletionList(self, autocomplete_list):
        self.autocomplete_model = QStandardItemModel()
        for text in autocomplete_list:
            self.autocomplete_model.appendRow(QStandardItem(text))
        self.completer.setModel(self.autocomplete_model)