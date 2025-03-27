# -*- coding: utf-8 -*-

from orbit_orator.migrations import DatabaseMigrationRepository
from .base_command import BaseCommand


class InstallCommand(BaseCommand):
    """
    Install the migration repository.

    migrate:install
        {--d|database= : The database connection to use.}
    """

    def handle(self):
        """
        Execute the console command.
        """
        database = self.option("database")
        repository = DatabaseMigrationRepository(self.resolver, "migrations")

        repository.set_source(database)
        repository.create_repository()

        self.info("Migration table created successfully")
