# -*- coding: utf-8 -*-

from orbit_orator.migrations import Migrator, DatabaseMigrationRepository
from .base_command import BaseCommand


class StatusCommand(BaseCommand):
    """
    Show the status of each migration.

    migrate:status
        {--d|database= : The database connection to use.}
        {--p|path= : The path of migrations files to be executed.}
    """

    def handle(self):
        """
        Execute the console command.
        """
        database = self.option('database')

        repository = DatabaseMigrationRepository(self.resolver, self.config.get('migrations.table', 'migrations'))

        if not repository.repository_exists():
            return self.error('No migrations found.')

        migrator = Migrator(repository, self.resolver)

        ran = migrator.get_repository().get_ran()

        migrations = []
        for migration in migrator.get_migrations_files(self._get_migration_path()):
            migrations.append({
                'migration': migration,
                'batch': migrator.get_repository().get_last_batch_number() if migration in ran else '',
                'ran': 'Yes' if migration in ran else 'No'
            })

        if not migrations:
            return self.error('No migrations found')

        self.render_status(migrations, database)

    def _prepare_database(self, migrator, database):
        migrator.set_connection(database)
