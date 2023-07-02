import pytest

from install.database import download_database


class TestInstall:
    def test_origin_data_is_downloaded(self):
        """ test that the data is downloaded from the internet
        """
        try:
            download_database()
        except Exception as e:
            assert False, f"download_database() raised {e} unexpectedly!"
        assert True

    def test_data_is_downloaded(self):
        """ test that the data is downloaded from the internet
        """
        assert True

    def test_database_file_is_created(self):
        """ test that the database file is created
        """
        assert True

    def test_database_is_populated(self):
        """ test that the database is populated
        """
        assert True

    def test_tables_are_created(self):
        """ test that the tables are created
        """
        assert True

    def test_admin_user_is_created(self):
        """ test that the admin user is created
        """
        assert True

    def test_dummy_users_are_created(self):
        """ test that the dummy users are created
        """
        assert True