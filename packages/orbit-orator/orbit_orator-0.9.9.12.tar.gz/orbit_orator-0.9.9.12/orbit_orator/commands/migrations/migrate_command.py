# -*- coding: utf-8 -*-

from orbit_orator.migrations import Migrator, DatabaseMigrationRepository
from .base_command import BaseCommand


class MigrateCommand(BaseCommand):
    """
    Run the database migrations.

    migrate
        {--d|database= : The database connection to use.}
        {--p|path= : The path of migrations files to be executed.}
        {--s|seed : Indicates if the seed task should be re-run.}
        {--seed-path= : The path of seeds files to be executed.
                        Defaults to <comment>./seeders</comment>.}
        {--P|pretend : Dump the SQL queries that would be run.}
        {--f|force : Force the operation to run.}
    """

    def handle(self):
        """
        Execute the console command.
        """
        if not self.confirm_to_proceed(
            "<question>Are you sure you want to proceed with the migration?</question> "
        ):
            return

        self._prepare_database()

        pretend = bool(self.option('pretend'))
        step = self.option('step')

        if step and not isinstance(step, bool):
            step = int(step)

        database = self.option('database')

        repository = DatabaseMigrationRepository(self.resolver, self.config.get('migrations.table', 'migrations'))

        migrator = Migrator(repository, self.resolver)

        if not self.option('pretend'):
            migrator.run(self._get_migration_path(), pretend)

            for note in migrator.get_notes():
                self.line(note)

            if step > 0:
                migrator.rollback(self._get_migration_path(), step)

                for note in migrator.get_notes():
                    self.line(note)

            if database:
                self.line('<info>Database %s was migrated.</info>' % database)
            else:
                self.line('<info>Database was migrated.</info>')

        # If the "seed" option has been given, we will rerun the database seed task
        # to repopulate the database.
        if self.option("seed"):
            options = [("--force", self.option("force"))]

            if database:
                options.append(("--database", database))

            if self.get_definition().has_option("config"):
                options.append(("--config", self.option("config")))

            if self.option("seed-path"):
                options.append(("--path", self.option("seed-path")))

            self.call("db:seed", options)

    def _prepare_database(self):
        """
        Prepare the migration database for running.
        """
        database = self.option('database')

        repository = DatabaseMigrationRepository(self.resolver, self.config.get('migrations.table', 'migrations'))

        if not repository.repository_exists():
            repository.create_repository()
