import asyncio

from alembic import context
from sqlalchemy import engine_from_config
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from bot.db import Base


def run_migrations_online():
    connectable = context.config.attributes.get("connection", None)

    if connectable is None:
        connectable = AsyncEngine(
            engine_from_config(
                context.config.get_section(context.config.config_ini_section),
                prefix="sqlalchemy.",
                future=True,
            )
        )

    # Note, we decide whether to run asynchronously based on the kind of engine we're dealing with.
    if isinstance(connectable, AsyncEngine):
        asyncio.run(run_async_migrations(connectable))
    else:
        do_run_migrations(connectable)


# Then use their setup for async connection/running of the migration
async def run_async_migrations(connectable):
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=Base.metadata)

    with context.begin_transaction():
        context.run_migrations()


# But the outer layer still allows sychronous execution also.
run_migrations_online()
