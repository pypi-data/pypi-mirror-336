# -*- coding: utf-8 -*-

import os
from orbit_orator.migrations import MigrationCreator
from .base_command import BaseCommand


class MigrateMakeCommand(BaseCommand):
    """
    Create a new migration file.

    make:migration
        {name : The name of the migration.}
        {--t|table= : The table to create the migration for.}
        {--C|create : Whether the migration will create the table or not.}
        {--p|path= : The path to migrations files.}
    """

    needs_config = False

    def handle(self):
        """
        Execute the console command.
        """
        creator = MigrationCreator()

        name = self.argument('name')
        table = self.option('table')
        create = bool(self.option('create'))

        if not table and create:
            table = create

        path = creator.create(name, os.path.join(os.getcwd(), 'migrations'), table, create)

        self.line('<info>Created migration:</info> %s' % os.path.basename(path))

    def _write_migration(self, creator, name, table, create, path):
        """
        Write the migration file to disk.
        """
        file_ = os.path.basename(creator.create(name, path, table, create))

        return file_
