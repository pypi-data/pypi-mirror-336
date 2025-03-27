"""
Module provides a Trigger class and related tools to create triggers in the database via the ORM.
"""

from enum import StrEnum
from typing import Any, Self

import peewee
from peewee import Model

from mafw.mafw_errors import MissingSQLStatement


def and_(*conditions: str) -> str:
    """
    Concatenates conditions with logical AND.

    :param conditions: The condition to join.
    :type conditions: str
    :return: The and-concatenated string of conditions
    :rtype: str
    """
    conditions_l = [f'({c})' for c in conditions]
    return ' AND '.join(conditions_l)


def or_(*conditions: str) -> str:
    """
    Concatenates conditions with logical OR.

    :param conditions: The condition to join.
    :type conditions: str
    :return: The or-concatenated string of conditions.
    :rtype: str
    """
    conditions_l = [f'({c})' for c in conditions]
    return ' OR '.join(conditions_l)


class TriggerWhen(StrEnum):
    """String enumerator for the trigger execution time (Before, After or Instead Of)"""

    Before = 'BEFORE'
    After = 'AFTER'
    Instead = 'INSTEAD OF'


class TriggerAction(StrEnum):
    """String enumerator for the trigger action (Delete, Insert, Update)"""

    Delete = 'DELETE'
    Insert = 'INSERT'
    Update = 'UPDATE'


class Trigger:
    """Trigger template wrapper for use with peewee ORM."""

    def __init__(
        self,
        trigger_name: str,
        trigger_type: tuple[TriggerWhen, TriggerAction],
        source_table: type[Model] | Model | str,
        safe: bool = False,
        for_each_row: bool = False,
        update_columns: list[str] | None = None,
    ):
        """
        Constructor parameters:

        :param trigger_name: The name of this trigger. It needs to be unique!
        :type trigger_name: str
        :param trigger_type: A tuple with :class:`TriggerWhen` and :class:`TriggerAction` to specify on which action
            the trigger should be invoked and if before, after or instead of.
        :type trigger_type: tuple[TriggerWhen, TriggerAction]
        :param source_table: The table originating the trigger. It can be a model class, instance, or also the name of
            the table.
        :type source_table: type[Model] | Model | str
        :param safe: A boolean flag to define if in the trigger creation statement a 'IF NOT EXISTS' clause should be
            included. Defaults to False
        :type safe: bool, Optional
        :param for_each_row: A boolean flag to repeat the script content for each modified row in the table.
            Defaults to False.
        :type for_each_row: bool, Optional
        :param update_columns: A list of column names. When defining a trigger on a table update, it is possible to
            restrict the firing of the trigger to the cases when a subset of all columns have been updated. An column
            is updated also when the new value is equal to the old one. If you want to discriminate this case, use the
            :meth:`add_when` method. Defaults to None.
        :type update_columns: list[str], Optional
        """
        if update_columns is None:
            update_columns = []
        self._create = 'CREATE TRIGGER'
        self.trigger_name = trigger_name
        self.trigger_type = trigger_type
        self._trigger_when, self._trigger_op = self.trigger_type
        self._of_columns = (
            f'OF ({", ".join(update_columns)})' if self._trigger_op == TriggerAction.Update and update_columns else ''
        )
        if isinstance(source_table, (Model, type(Model))):
            # noinspection PyUnresolvedReferences
            self.target_table = source_table._meta.table_name  # type: ignore
        else:
            self.target_table = source_table
        self.if_not_exists = 'IF NOT EXISTS' if safe else ''
        self._for_each_row = 'FOR EACH ROW' if for_each_row else ''

        self._compiled_whens = ''
        self._compiled_sqls = ''
        self._when_list: list[str] = []
        self._sql_list: list[str] = []

    @property
    def trigger_action(self) -> TriggerAction:
        return self._trigger_op

    @trigger_action.setter
    def trigger_action(self, action: TriggerAction) -> None:
        self._trigger_op = action

    @property
    def trigger_when(self) -> TriggerWhen:
        return self._trigger_when

    @trigger_when.setter
    def trigger_when(self, when: TriggerWhen) -> None:
        self._trigger_when = when

    def __setattr__(self, key: Any, value: Any) -> None:
        if key == 'safe':
            self.if_not_exists = 'IF NOT EXISTS' if value else ''
        elif key == 'for_each_row':
            self._for_each_row = 'FOR EACH ROW' if value else ''
        else:
            super().__setattr__(key, value)

    def __getattr__(self, item: str) -> Any:
        if item == 'safe':
            return self.if_not_exists == 'IF NOT EXISTS'
        elif item == 'for_each_row':
            return self._for_each_row == 'FOR EACH ROW'
        else:
            return item

    def add_sql(self, sql: str | peewee.Query) -> Self:
        """
        Add an SQL statement to be executed by the trigger.

        The ``sql`` can be either a string containing the sql statement, or it can be any other peewee Query.

        For example:

        .. code-block:: python

            # assuming you have created a trigger ...

            sql = AnotherTable.insert(
                field1=some_value, field2=another_value
            )
            trigger.add_sql(sql)

        In this way the SQL code is generated with parametric placeholder if needed.

        :param sql: The SQL statement.
        :type sql: str | peewee.Query
        :return: self for easy chaining
        :rtype: Trigger
        """
        if not isinstance(sql, str):
            sql = str(sql)
        sql = sql.strip()
        sql = chr(9) + sql
        if not sql.endswith(';'):
            sql += ';'
        self._sql_list.append(sql)
        return self

    def add_when(self, *conditions: str) -> Self:
        """
        Add conditions to the `when` statements.

        Conditions are logically ANDed.
        To have mixed `OR` and `AND` logic, use the functions :func:`and_` and :func:`or_`.

        :param conditions: Conditions to be added with logical AND
        :type conditions: str
        :return: self for easy chaining
        :rtype: Trigger
        """
        conditions_l = [f'({c.strip()})' for c in conditions]
        self._when_list.append(f'({" AND ".join(conditions_l)})')
        return self

    def create(self) -> str:
        """
        Generates the SQL create statement.

        :return: The trigger creation statement.
        :raise MissingSQLStatement: if no SQL statements are provided.
        """
        if len(self._sql_list) == 0:
            raise MissingSQLStatement('No SQL statements provided')
        self._compiled_whens = f'WHEN {" AND ".join(self._when_list)}' if len(self._when_list) else ''
        self._compiled_sqls = f'{chr(10)}'.join(self._sql_list)
        return (
            f'{self._create} {self.if_not_exists} {self.trigger_name}{chr(10)}'
            f'{self._trigger_when} {self._trigger_op} {self._of_columns} ON {self.target_table}{chr(10)}'
            f'{self._for_each_row} {self._compiled_whens}{chr(10)}'
            f'BEGIN{chr(10)}'
            f'{self._compiled_sqls}'
            f'{chr(10)}END;{chr(10)}'
        )

    def drop(self, safe: bool = True) -> str:
        """
        Generates the SQL drop statement.

        :param safe: If True, add an IF EXIST. Defaults to True.
        :type safe: bool, Optional
        :return: The drop statement
        :rtype: str
        """
        return f'DROP TRIGGER {"IF EXISTS" if safe else ""} {self.trigger_name}'
