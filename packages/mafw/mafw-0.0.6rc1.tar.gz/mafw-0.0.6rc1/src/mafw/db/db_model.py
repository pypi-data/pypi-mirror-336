"""
The module provides functionality to MAFw to interface to a DB.
"""

import warnings
from typing import Any, Iterable, cast

import peewee
from peewee import DatabaseProxy, ModelInsert

# noinspection PyUnresolvedReferences
from playhouse.signals import Model

from mafw.db.trigger import Trigger
from mafw.mafw_errors import MAFwException

database_proxy = DatabaseProxy()
"""This is a placeholder for the real database object that will be known only at run time"""


class MAFwBaseModelDoesNotExist(MAFwException):
    """Raised when the base model class is not existing."""


class MAFwBaseModel(Model):
    """The base model for the MAFw library.

    Every model class (table) that the user wants to interface must inherit from this base.
    """

    @classmethod
    def triggers(cls) -> list[Trigger]:
        """
        Returns an iterable of :class:`~mafw.db.trigger.Trigger` objects to create upon table creation.

        The user must overload this returning all the triggers that must be created along with this class.
        """
        return []

    # noinspection PyUnresolvedReferences
    @classmethod
    def create_table(cls, safe: bool = True, **options: Any) -> None:
        """
        Create the table in the underlying DB and all the related trigger as well.

        If the creation of a trigger fails, then the whole table dropped, and the original exception is re-raised.

        .. warning::

            Trigger creation has been extensively tested with :link:`SQLite`, but not with the other database implementation.
            Please report any malfunction.

        :param safe: Flag to add an IF NOT EXISTS to the creation statement. Defaults to True.
        :type safe: bool, Optional
        :param options: Additional options passed to the super method.
        """
        super().create_table(safe, **options)
        if len(cls.triggers()):
            if isinstance(cls._meta.database, DatabaseProxy):  # type: ignore[attr-defined]  # peewee problem with _meta
                # the real database is the object connected to the proxy.
                if not isinstance(
                    cls._meta.database.obj,  # type: ignore[attr-defined]  # peewee problem with _meta
                    peewee.SqliteDatabase,
                ):
                    warnings.warn(
                        'Trigger generation within a model has been tested only Sqlite databases, '
                        'please report any malfunction.'
                    )
            else:
                if not isinstance(
                    cls._meta.database,  # type: ignore[attr-defined]  # peewee problem with _meta
                    peewee.SqliteDatabase,
                ):
                    warnings.warn(
                        'Trigger generation within a model has been tested only Sqlite databases, please report any '
                        'malfunction.'
                    )
        for trigger in cls.triggers():
            try:
                cls._meta.database.execute_sql(trigger.create())  # type: ignore[attr-defined]
            except:
                cls._meta.database.drop_tables([cls], safe=safe)  # type: ignore[attr-defined]
                for el in cls.triggers():
                    cls._meta.database.execute_sql(el.drop(True))  # type: ignore[attr-defined]
                raise

    @classmethod
    def std_upsert(cls, __data: dict[str, Any] | None = None, **mapping: Any) -> ModelInsert:
        """
        Perform a so-called standard upsert.

        An upsert statement is not part of the standard SQL and different databases have different ways to implement it.
        This method will work for modern versions of :link:`sqlite` and :link:`postgreSQL`.
        Here is a `detailed explanation for SQLite <https://www.sqlite.org/lang_upsert.html>`_.

        An upsert is a statement in which we try to insert some data in a table where there are some constraints.
        If one constraint is failing, then instead of inserting a new row, we will try to update the existing row
        causing the constraint violation.

        A standard upsert, in the naming convention of MAFw, is setting the conflict cause to the primary key with all
        other fields being updated. In other words, the database will try to insert the data provided in the table, but
        if the primary key already exists, then all other fields will be updated.

        This method is equivalent to the following:

        .. code-block:: python

            class Sample(MAFwBaseModel):
                sample_id = AutoField(
                    primary_key=True,
                    help_text='The sample id primary key',
                )
                sample_name = TextField(help_text='The sample name')


            (
                Sample.insert(sample_id=1, sample_name='my_sample')
                .on_conflict(
                    preserve=[Sample.sample_name]
                )  # use the value we would have inserted
                .execute()
            )

        :param __data: A dictionary containing the key/value pair for the insert. The key is the column name.
            Defaults to None
        :type __data: dict, Optional
        :param mapping: Keyword arguments representing the value to be inserted.
        """
        if cls._meta.composite_key:  # type: ignore[attr-defined]
            conflict_target = [
                cls._meta.fields[n]  # type: ignore[attr-defined]
                for n in cls._meta.primary_key.field_names  # type: ignore[attr-defined]
            ]
        else:
            conflict_target = [cls._meta.primary_key]  # type: ignore[attr-defined]  # peewee problem with _meta

        conflict_target_names = [f.name for f in conflict_target]
        preserve = [
            f
            for n, f in cls._meta.fields.items()  # type: ignore[attr-defined]
            if n not in conflict_target_names
        ]
        return cast(
            ModelInsert, cls.insert(__data, **mapping).on_conflict(conflict_target=conflict_target, preserve=preserve)
        )

    @classmethod
    def std_upsert_many(cls, rows: Iterable[Any], fields: list[str] | None = None) -> ModelInsert:
        """
        Perform a standard upsert with many rows.

        .. seealso::

            Read the :meth:`std_upsert` documentation for an explanation of this method.

        :param rows: A list with the rows to be inserted. Each item can be a dictionary or a tuple of values. If a
            tuple is provided, then the `fields` must be provided.
        :type rows: Iterable
        :param fields: A list of field names. Defaults to None.
        :type fields: list[str], Optional
        """
        if cls._meta.composite_key:  # type: ignore[attr-defined]  # peewee problem with meta
            conflict_target = [
                cls._meta.fields[n]  # type: ignore[attr-defined]  # peewee problem with meta
                for n in cls._meta.primary_key.field_names  # type: ignore[attr-defined]
            ]
        else:
            conflict_target = [cls._meta.primary_key]  # type: ignore[attr-defined]  # peewee problem with meta

        conflict_target_names = [f.name for f in conflict_target]
        preserve = [
            f
            for n, f in cls._meta.fields.items()  # type: ignore[attr-defined]  # peewee problem with meta
            if n not in conflict_target_names
        ]
        return cast(
            ModelInsert,
            (
                cls.insert_many(rows, fields).on_conflict(
                    conflict_target=conflict_target,
                    preserve=preserve,
                )
            ),
        )

    class Meta:
        """The metadata container for the Model class"""

        database = database_proxy
        """The reference database. A proxy is used as a placeholder that will be automatically replaced by the real 
        instance of the database at runtime."""

        legacy_table_names = False
        """
        Set the default table name as the snake case of the Model camel case name.
        
        So for example, a model named ThisIsMyTable will corresponds to a database table named this_is_my_table.
        """
