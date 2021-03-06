import pytest

from debian_cloud_images.cli.upload_gce import UploadGceCommand


class TestCommand:
    @pytest.fixture
    def auth_file(self, tmp_path):
        p = tmp_path / 'auth.json'
        with p.open(mode='w') as f:
            f.write('{}')
        return p.as_posix()

    @pytest.fixture
    def config_files(self, tmp_path):
        p = tmp_path / 'config'
        with p.open(mode='w') as f:
            f.write('')
        return [p.as_posix()]

    @pytest.fixture
    def mock_env(self, monkeypatch):
        monkeypatch.delenv('GOOGLE_APPLICATION_CREDENTIALS', raising=False)
        return monkeypatch

    @pytest.fixture
    def mock_uploader(self, monkeypatch):
        from unittest.mock import MagicMock
        from debian_cloud_images.cli import upload_gce
        ret = MagicMock()
        monkeypatch.setattr(upload_gce, 'ImageUploaderGce', ret)
        return ret

    def test___init__(self, auth_file, config_files, mock_env, mock_uploader):
        UploadGceCommand(
            config={
                'gce.project': 'project',
                'gce.bucket': 'bucket',
                'gce.credentials_file': auth_file,
            },
            config_files=config_files,
            output='output',
        )

        mock_uploader.assert_called_once_with(
            auth={},
            bucket='bucket',
            output='output',
            project='project',
        )

    def test___init___auth_env(self, auth_file, config_files, mock_env, mock_uploader):
        mock_env.setenv('GOOGLE_APPLICATION_CREDENTIALS', auth_file)

        UploadGceCommand(
            config={
                'gce.project': 'project',
                'gce.bucket': 'bucket',
            },
            config_files=config_files,
            output='output',
        )

        mock_uploader.assert_called_once_with(
            auth={},
            bucket='bucket',
            output='output',
            project='project',
        )
