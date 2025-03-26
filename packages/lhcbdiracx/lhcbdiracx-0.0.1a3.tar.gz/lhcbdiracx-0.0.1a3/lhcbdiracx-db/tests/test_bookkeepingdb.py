from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from lhcbdiracx.db.sql.bookkeeping.db import BookkeepingDB

if TYPE_CHECKING:
    from typing import AsyncGenerator

# Each DB test class must defined a fixture looking like this one
# It allows to get an instance of an in memory DB,


@pytest.fixture
async def bookkeeping_db(tmp_path) -> AsyncGenerator[BookkeepingDB, None]:
    bookkeeping_db = BookkeepingDB("sqlite+aiosqlite:///:memory:")
    async with bookkeeping_db.engine_context():
        async with bookkeeping_db.engine.begin() as conn:
            await conn.run_sync(bookkeeping_db.metadata.create_all)
        yield bookkeeping_db


async def test_insert_and_summary(bookkeeping_db: BookkeepingDB):
    async with bookkeeping_db as bookkeeping_db:
        # First we check that the DB is empty
        result = await bookkeeping_db.hello()
        assert result == 0, result
