"""Graphical user interface components."""

from enum import IntEnum
from typing import Any

from qtpy.QtCore import (
    Property,
    QAbstractItemModel,
    QEvent,
    QModelIndex,
    QRect,
    Qt,
    Signal,
    Slot,
)
from qtpy.QtGui import QIcon, QMouseEvent, QPainter
from qtpy.QtWidgets import (
    QApplication,
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLayout,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QStyle,
    QStyledItemDelegate,
    QStyleOptionButton,
    QStyleOptionViewItem,
    QVBoxLayout,
    QWidget,
)

from iblqt import resources  # noqa: F401
from iblqt.core import QAlyx


class CheckBoxDelegate(QStyledItemDelegate):
    """
    A custom delegate for rendering checkboxes in a QTableView or similar widget.

    This delegate allows for the display and interaction with boolean data as checkboxes.
    """

    def paint(
        self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex
    ) -> None:
        """
        Paints the checkbox in the view.

        Parameters
        ----------
        painter : QPainter
            The painter used to draw the checkbox.
        option : QStyleOptionButton
            The style option containing the information needed for painting.
        index : QModelIndex
            The index of the item in the model.
        """
        super().paint(painter, option, index)
        control = QStyleOptionButton()
        control.rect = QRect(option.rect.topLeft(), QCheckBox().sizeHint())
        control.rect.moveCenter(option.rect.center())
        control.state = QStyle.State_On if index.data() is True else QStyle.State_Off
        QApplication.style().drawControl(
            QStyle.ControlElement.CE_CheckBox, control, painter
        )

    def displayText(self, value: Any, locale: Any) -> str:
        """
        Return an empty string to hide the text representation of the data.

        Parameters
        ----------
        value : Any
            The value to be displayed (not used).
        locale : Any
            The locale to be used (not used).

        Returns
        -------
        str
            An empty string.
        """
        return ''

    def editorEvent(
        self,
        event: QEvent,
        model: QAbstractItemModel,
        option: QStyleOptionViewItem,
        index: QModelIndex,
    ) -> bool:
        """
        Handle user interaction with the checkbox.

        Parameters
        ----------
        event : QEvent
            The event that occurred (e.g., mouse click).
        model : QAbstractItemModel
            The model associated with the view.
        option : QStyleOptionViewItem
            The style option containing the information needed for handling the event.
        index : QModelIndex
            The index of the item in the model.

        Returns
        -------
        bool
            True if the event was handled, False otherwise.
        """
        if isinstance(event, QMouseEvent) and event.type() == QEvent.MouseButtonRelease:
            checkbox_rect = QRect(option.rect.topLeft(), QCheckBox().sizeHint())
            checkbox_rect.moveCenter(option.rect.center())
            if checkbox_rect.contains(event.pos()):
                model.setData(index, not model.data(index))
                event.accept()
                return True
        return super().editorEvent(event, model, option, index)


class StatefulButton(QPushButton):
    """A QPushButton that maintains an active/inactive state."""

    clickedWhileActive = Signal()  # type: Signal
    """Emitted when the button is clicked while it is in the active state."""

    clickedWhileInactive = Signal()  # type: Signal
    """Emitted when the button is clicked while it is in the inactive state."""

    stateChanged = Signal(bool)  # type: Signal
    """Emitted when the button's state has changed. The signal carries the new state 
    (True for active, False for inactive)."""

    def __init__(
        self,
        textActive: str | None = None,
        textInactive: str | None = None,
        active: bool = False,
        parent: QWidget | None = None,
    ):
        """Initialize the StatefulButton with the specified active state.

        Parameters
        ----------
        textActive : str, optional
            The text shown on the button when in active state.
        textInactive : str, optional
            The text shown on the button when in inactive state.
        active : bool, optional
            Initial state of the button (default is False).
        parent : QWidget
            The parent widget.
        """
        self._isActive = active
        self._textActive = textActive or ''
        self._textInactive = textInactive or ''
        super().__init__(self._textActive if active else self._textInactive, parent)

        self.clicked.connect(self._onClick)
        self.stateChanged.connect(
            lambda active: self.setText(
                self._textActive if active else self._textInactive
            )
        )

    def getActive(self) -> bool:
        """Get the active state of the button.

        Returns
        -------
        bool
            True if the button is active, False otherwise.
        """
        return self._isActive

    @Slot(bool)
    def setActive(self, value: bool):
        """Set the active state of the button.

        Emits `stateChanged` if the state has changed.

        Parameters
        ----------
        value : bool
            The new active state of the button.
        """
        if self._isActive != value:
            self._isActive = value
            self.stateChanged.emit(self._isActive)

    active = Property(bool, fget=getActive, fset=setActive, notify=stateChanged)  # type: Property
    """The active state of the button."""

    def getTextActive(self) -> str:
        """Get the text shown on the button when in active state.

        Returns
        -------
        str
            The text shown during active state.
        """
        return self._textActive

    def setTextActive(self, text: str):
        """Set the text shown on the button when in active state.

        Parameters
        ----------
        text : str
            The text to be shown during active state.
        """
        self._textActive = text
        if self.active:
            self.setText(self._textActive)

    textActive = Property(str, fget=getTextActive, fset=setTextActive)
    """The text shown on the button during active state."""

    def getTextInactive(self) -> str:
        """Get the text shown on the button during inactive state.

        Returns
        -------
        str
            The text shown during inactive state.
        """
        return self._textInactive

    def setTextInactive(self, text: str):
        """Set the text shown on the button during inactive state.

        Parameters
        ----------
        text : str
            The text to be shown during inactive state.
        """
        self._textInactive = text
        if not self.active:
            self.setText(self._textInactive)

    textInactive = Property(str, fget=getTextInactive, fset=setTextInactive)
    """The text shown on the button during inactive state."""

    @Slot()
    def _onClick(self):
        """Handle the button click event.

        Emits `clickedWhileActive` if the button is active,
        otherwise emits `clickedWhileInactive`.
        """
        if self._isActive:
            self.clickedWhileActive.emit()
        else:
            self.clickedWhileInactive.emit()


class UseTokenCache(IntEnum):
    """Enumeration that defines the strategy for caching the login token."""

    NEVER = -1
    """Indicates that the login token should never be stored."""

    ASK = 0
    """Indicates that the user should be prompted whether to store the login token."""

    ALWAYS = 1
    """Indicates that the login token should always be stored."""


class AlyxUserEdit(QLineEdit):
    """A specialized :class:`QLineEdit` for logging in to Alyx.

    A one-line text editor for entering a username. The widget handles login
    actions, including displaying the login status. A :class:`AlyxLoginDialog`
    is triggered when no authentication token is available.
    """

    def __init__(
        self, alyx: QAlyx, parent: QWidget, cache: UseTokenCache = UseTokenCache.ASK
    ) -> None:
        """Initialize the widget.

        Parameters
        ----------
        alyx : QAlyx
            The alyx instance.
        parent : QWidget
            The parent widget.
        cache : UseTokenCache
            Strategy for handling the token cache. Defaults to UseTokenCache.ASK.
        """
        super().__init__(parent)
        self.alyx = alyx
        self._cache = cache
        self._checkIcon = QIcon(':/icon/check')

        self.setPlaceholderText('Username')
        self.returnPressed.connect(self.login)
        self.alyx.loggedIn.connect(self._onLoggedIn)
        self.alyx.loggedOut.connect(self._onLoggedOut)
        self.alyx.tokenMissing.connect(self._onTokenMissing)

    def login(self):
        """Attempt to log in to Alyx with the entered username.

        If the username field is empty, the login attempt is ignored.
        """
        if len(self.text()) == 0:
            return
        self.alyx.login(username=self.text())

    def _onLoggedIn(self, username: str):
        """Handle successful login by updating the UI.

        Parameters
        ----------
        username : str
            The username of the logged-in user.
        """
        self.addAction(self._checkIcon, self.ActionPosition.TrailingPosition)
        self.setText(username)
        self.setReadOnly(True)
        self.setStyleSheet('background-color: rgb(246, 245, 244);')

    def _onLoggedOut(self):
        """Handle logout by resetting the UI elements."""
        for action in self.actions():
            self.removeAction(action)
        self.setText('')
        self.setReadOnly(False)
        self.setStyleSheet('')

    def _onTokenMissing(self, username: str):
        """Prompt the user for password when the authentication token is missing.

        Parameters
        ----------
        username : str
            The username for which the token is missing.
        """
        AlyxLoginDialog(self.alyx, username, self, self._cache).exec_()


class AlyxLoginWidget(QWidget):
    """A widget used for managing the connection to Alyx.

    This widget contains an :class:`AlyxUserEdit` for entering a username and a
    :class:`StatefulButton` for logging in and out.
    """

    def __init__(
        self,
        alyx: QAlyx | str,
        parent: QWidget | None = None,
        cache: UseTokenCache = UseTokenCache.ASK,
    ) -> None:
        """Initialize the widget.

        Parameters
        ----------
        alyx : QAlyx | str
            The Alyx instance or the base URL for the Alyx API.
        parent : QWidget
            The parent widget.
        cache : UseTokenCache
            Strategy for handling the token cache. Defaults to UseTokenCache.ASK.
        """
        super().__init__(parent)

        if isinstance(alyx, QAlyx):
            self.alyx = alyx
        else:
            self.alyx = QAlyx(base_url=alyx, parent=self)

        # edit field for username
        self.userEdit = AlyxUserEdit(alyx=self.alyx, cache=cache, parent=self)
        self.userEdit.textChanged.connect(self._onTextChanged)

        # stateful button that is used for, both, logging in and logging out
        self.button = StatefulButton(
            textActive='Logout', textInactive='Login', parent=self
        )
        self.button.setEnabled(False)
        self.button.clickedWhileInactive.connect(self.userEdit.login)
        self.button.clickedWhileActive.connect(self.alyx.logout)
        self.alyx.statusChanged.connect(self.button.setActive)

        QHBoxLayout(self)
        self.layout().addWidget(self.userEdit)
        self.layout().addWidget(self.button)

    def _onTextChanged(self, username: str):
        """Only enable the login button when a username has been entered."""
        text_entered = len(username) > 0
        if self.button.isEnabled() ^ text_entered:
            self.button.setEnabled(text_entered)


class AlyxLoginDialog(QDialog):
    """A password dialog window used for authenticating with Alyx."""

    def __init__(
        self,
        alyx: QAlyx,
        username: str | None = None,
        parent: QWidget | None = None,
        cache: UseTokenCache = UseTokenCache.ASK,
    ) -> None:
        """Initialize the widget.

        Parameters
        ----------
        alyx : QAlyx
            The alyx instance.
        username : str
            The username.
        parent : QWidget
            The parent widget.
        cache : UseTokenCache
            Strategy for handling the token cache. Defaults to ASK.
        """
        super().__init__(parent)
        self.setWindowTitle('Login')

        self._alyx = alyx
        self._alyx.authenticationFailed.connect(self._onAuthentificationFailed)
        self._alyx.loggedIn.connect(self._onAuthentificationSucceeded)

        if cache == UseTokenCache.ALWAYS:
            self._cache = True
        else:
            self._cache = False

        form_widget = QWidget(self)
        self.userEdit = QLineEdit(username or '', form_widget)
        self.passEdit = QLineEdit(form_widget)
        self.userEdit.textChanged.connect(self._onTextChanged)
        self.passEdit.setFocus()
        self.passEdit.setEchoMode(QLineEdit.Password)
        self.passEdit.textChanged.connect(self._onTextChanged)
        form_layout = QFormLayout(form_widget)
        form_layout.addRow('Server', QLabel(self._alyx.client.base_url, form_widget))
        form_layout.addRow('Username', self.userEdit)
        form_layout.addRow('Password', self.passEdit)
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_widget.setLayout(form_layout)

        control_widget = QWidget(self)
        self.buttonBox = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, control_widget
        )
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        self.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.accept)
        self.buttonBox.button(QDialogButtonBox.Cancel).clicked.connect(self.reject)
        control_layout = QHBoxLayout(control_widget)
        if cache == UseTokenCache.ASK:
            check_cache = QCheckBox('Remember me', control_widget)
            check_cache.stateChanged.connect(self._setCache)
            control_layout.addWidget(check_cache)
        control_layout.addItem(
            QSpacerItem(20, 0, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        )
        control_layout.addWidget(self.buttonBox)
        control_layout.setContentsMargins(0, 0, 0, 0)
        control_widget.setLayout(control_layout)

        QVBoxLayout(self)
        self.layout().addWidget(form_widget)
        self.layout().addItem(
            QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)
        )
        self.layout().addWidget(control_widget)
        self.layout().setSizeConstraint(QLayout.SetFixedSize)

    def _setCache(self, do_cache: int) -> None:
        self._cache = do_cache == Qt.CheckState.Checked

    def accept(self):
        """Hide the dialog and set the result code to Accepted."""
        self._alyx.login(self.userEdit.text(), self.passEdit.text(), self._cache)

    def _onAuthentificationSucceeded(self, _: str) -> None:
        super().accept()

    def _onAuthentificationFailed(self, _: str):
        """Show :class:`QMessageBox` on authentication failure."""
        self.passEdit.setText('')
        QMessageBox.critical(
            self,
            'Login Failed',
            'Authentication has failed.\nPlease try again.',
        )

    def _onTextChanged(self):
        """Only enable the OK button when text has been entered in both fields."""
        ok_button = self.buttonBox.button(QDialogButtonBox.Ok)
        text_entered = all([len(x.text()) > 0 for x in (self.userEdit, self.passEdit)])
        if ok_button.isEnabled() ^ text_entered:
            ok_button.setEnabled(text_entered)
