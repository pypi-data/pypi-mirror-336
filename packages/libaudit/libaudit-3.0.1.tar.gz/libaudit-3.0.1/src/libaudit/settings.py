from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from typing import Tuple


"""Настройки по-умолчанию."""

HANDLER: str = 'libaudit.handlers.stdout'
"""Приложение содержащее реализацию обработчика изменений в наблюдаемых таблицах."""

CONTEXT_RESOLVER_CLS: str = 'libaudit.core.requests.DefaultAuditContextResolver'
"""Класс извлекающая контекст запроса."""

EXCLUDED_TABLES: 'Tuple[str, ...]' = ()
"""Таблицы, на которые не будут установлены триггеры."""
