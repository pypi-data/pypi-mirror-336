import tempfile
from pathlib import Path
from unittest.mock import PropertyMock, patch

import pandas as pd
import pytest
from qtpy.QtCore import QModelIndex, Qt
from requests import HTTPError

from iblqt import core


class TestDataFrameTableModel:
    def test_dataframe_model(self, qtbot):
        # instantiation / setting of dataframe
        df = pd.DataFrame({'X': [0, 1, 2], 'Y': ['A', 'B', 'C']})
        model = core.ColoredDataFrameTableModel()
        assert model.dataFrame.empty
        model = core.ColoredDataFrameTableModel(dataFrame=df)
        assert model.dataFrame is not df
        assert model.dataFrame.equals(df)
        with qtbot.waitSignal(model.modelReset, timeout=100):
            model.dataFrame = df

        # header data
        assert model.headerData(-1, Qt.Orientation.Horizontal) is None
        assert model.headerData(1, Qt.Orientation.Horizontal) == 'Y'
        assert model.headerData(2, Qt.Orientation.Horizontal) is None
        assert model.headerData(-1, Qt.Orientation.Vertical) is None
        assert model.headerData(2, Qt.Orientation.Vertical) == 2
        assert model.headerData(3, Qt.Orientation.Vertical) is None
        assert model.headerData(0, 3) is None

        # index
        assert model.index(1, 0).row() == 1
        assert model.index(1, 0).column() == 0
        assert model.index(1, 0).isValid()
        assert not model.index(5, 5).isValid()
        assert model.index(5, 5) == QModelIndex()

        # writing data
        with qtbot.waitSignal(model.dataChanged, timeout=100):
            assert model.setData(model.index(0, 0), -1)
        assert model.dataFrame.iloc[0, 0] == -1
        assert not model.setData(model.index(5, 5), 9)
        assert not model.setData(model.index(0, 0), 9, 6)

        # reading data
        assert model.data(model.index(0, 1)) == 'A'
        assert model.data(model.index(5, 5)) is None
        assert model.data(model.index(0, 1), 6) is None

        # sorting
        with qtbot.waitSignal(model.layoutChanged, timeout=100):
            model.sort(1, Qt.SortOrder.DescendingOrder)
        assert model.data(model.index(0, 1)) == 'C'
        assert model.setData(model.index(0, 1), 'D')
        assert model.data(model.index(0, 1)) == 'D'
        assert model.headerData(0, Qt.Orientation.Vertical) == 2
        with qtbot.waitSignal(model.layoutChanged, timeout=100):
            model.sort(1, Qt.SortOrder.AscendingOrder)
        assert model.data(model.index(0, 1)) == 'A'
        assert model.data(model.index(2, 1)) == 'D'
        assert model.headerData(0, Qt.Orientation.Vertical) == 0

        # colormap
        with qtbot.waitSignal(model.colormapChanged, timeout=100):
            model.colormap = 'CET-L1'
        assert model.getColormap() == 'CET-L1'
        model.sort(1, Qt.SortOrder.AscendingOrder)
        assert (
            model.data(model.index(0, 0), Qt.ItemDataRole.BackgroundRole).redF() == 1.0
        )
        assert (
            model.data(model.index(2, 0), Qt.ItemDataRole.BackgroundRole).redF() == 0.0
        )
        assert (
            model.data(model.index(0, 0), Qt.ItemDataRole.ForegroundRole).redF() == 0.0
        )
        assert (
            model.data(model.index(2, 0), Qt.ItemDataRole.ForegroundRole).redF() == 1.0
        )

        # alpha
        with qtbot.waitSignal(model.alphaChanged, timeout=100):
            model.alpha = 128
        assert model.alpha == 128
        assert (
            model.data(model.index(0, 0), Qt.ItemDataRole.BackgroundRole).alpha() == 128
        )
        assert (
            model.data(model.index(2, 0), Qt.ItemDataRole.BackgroundRole).alpha() == 128
        )


class TestPathWatcher:
    @pytest.mark.xfail(
        reason='This fails with the GitHub Windows runner for some reason.'
    )
    def test_path_watcher(self, qtbot):
        parent = core.QObject()
        w = core.PathWatcher(parent=parent, paths=[])

        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            path1 = Path(temp_file.name)
            path2 = path1.parent

            assert w.addPath(path1) is True
            assert len(w.files()) == 1
            assert path1 in w.files()
            assert w.removePath(path1) is True
            assert path1 not in w.files()

            assert len(w.addPaths([path1, path2])) == 0
            assert w.addPaths(['not-a-path']) == [Path('not-a-path')]
            assert len(w.files()) == 1
            assert len(w.directories()) == 1
            assert path1 in w.files()
            assert path2 in w.directories()

            with qtbot.waitSignal(w.fileChanged) as blocker:
                with path1.open('a') as f:
                    f.write('Hello, World!')
            assert blocker.args[0] == path1

            assert w.removePath(path1) is True
            with qtbot.waitSignal(w.directoryChanged) as blocker:
                path1.unlink()
            assert blocker.args[0] == path2

            assert len(w.removePaths([path2])) == 0
            assert len(w.directories()) == 0
            assert path1 not in w.directories()


class TestQAlyx:
    @pytest.fixture
    def mock_alyx_client(self):
        """Mock the AlyxClient to avoid real network calls."""
        with patch('iblqt.core.AlyxClient', autospec=True) as MockAlyxClient:
            yield MockAlyxClient

    def test_login_success(self, qtbot, mock_alyx_client):
        """Test successful login."""
        mock_client = mock_alyx_client.return_value
        mock_client.user = 'test_user'
        type(mock_client).is_logged_in = PropertyMock(side_effect=[False, True])

        q_alyx = core.QAlyx(base_url='https://example.com')

        with (
            qtbot.waitSignal(q_alyx.loggedIn) as s1,
            qtbot.waitSignal(q_alyx.statusChanged) as s2,
        ):
            q_alyx.login(username='test_user', password='correct_password')
            assert s1.args[0] == 'test_user'
            assert s2.args[0] is True

    def test_login_failure(self, qtbot, mock_alyx_client):
        """Test successful login."""
        mock_client = mock_alyx_client.return_value
        mock_client.base_url = 'https://example.com'
        mock_client.user = 'test_user'
        mock_client.is_logged_in = False

        q_alyx = core.QAlyx(base_url='https://example.com')

        mock_client.authenticate.side_effect = UserWarning(
            'No password or cached token'
        )
        with qtbot.waitSignal(q_alyx.tokenMissing) as s1:
            q_alyx.login(username='test_user', password='some_password')
            assert s1.args[0] == 'test_user'

        mock_client.authenticate.side_effect = ConnectionError("Can't connect")
        with (
            qtbot.waitSignal(q_alyx.connectionFailed),
            patch('iblqt.core.QMessageBox.critical') as mock,
        ):
            q_alyx.login(username='test_user', password='some_password')
            mock.assert_called_once()

        mock_client.authenticate.side_effect = HTTPError(400, 'Blah')
        with qtbot.waitSignal(q_alyx.authenticationFailed) as s1:
            q_alyx.login(username='test_user', password='some_password')
            assert s1.args[0] == 'test_user'

        mock_client.authenticate.side_effect = HTTPError(401, 'Blah')
        with pytest.raises(HTTPError):
            q_alyx.login(username='test_user', password='some_password')

    def test_logout(self, qtbot, mock_alyx_client):
        """Test logout functionality."""
        mock_client = mock_alyx_client.return_value

        q_alyx = core.QAlyx(base_url='https://example.com')

        mock_client.is_logged_in = False
        with qtbot.assertNotEmitted(q_alyx.loggedOut):
            q_alyx.logout()

        mock_client.is_logged_in = True
        with (
            qtbot.waitSignal(q_alyx.statusChanged) as s1,
            qtbot.waitSignal(q_alyx.loggedOut),
        ):
            q_alyx.logout()
            assert s1.args[0] is False

    def test_rest(self, qtbot, mock_alyx_client):
        """Test rest functionality."""
        mock_client = mock_alyx_client.return_value

        q_alyx = core.QAlyx(base_url='https://example.com')
        q_alyx.rest('some_arg', some_kwarg=True)
        mock_client.rest.assert_called_once_with('some_arg', some_kwarg=True)

        mock_client.rest.side_effect = HTTPError(400, 'Blah')
        with patch('iblqt.core.QMessageBox.critical') as mock:
            q_alyx.rest('some_arg', some_kwarg=True)
            mock.assert_called_once()

        mock_client.rest.side_effect = HTTPError(401, 'Blah')
        with (
            qtbot.waitSignal(q_alyx.connectionFailed),
            patch('iblqt.core.QMessageBox.critical') as mock,
        ):
            q_alyx.rest('some_arg', some_kwarg=True)
            mock.assert_called_once()
