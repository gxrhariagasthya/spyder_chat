import json
import aiomysql
import os
from db_config import DB_CONFIG

async def process_and_insert(filename: str):
    with open(filename, "r") as f:
        data = json.load(f)

    docs = data.get("results", [])

    conn = await aiomysql.connect(**DB_CONFIG)
    async with conn.cursor() as cur:
        await cur.execute("""
            CREATE TABLE IF NOT EXISTS executive_orders (
                id INT PRIMARY KEY AUTO_INCREMENT,
                title TEXT,
                summary TEXT,
                url TEXT,
                publication_date DATE,
                document_type VARCHAR(255)
            );
        """)
        for doc in docs:
            await cur.execute("""
                INSERT INTO executive_orders (title, summary, url, publication_date, document_type)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                doc.get("title", ""),
                doc.get("abstract", ""),
                doc.get("html_url", ""),
                doc.get("publication_date", ""),
                doc.get("document_type", "")
            ))
    await conn.commit()
    conn.close()
    print(f"[✓] Inserted data from {filename}")

# asyncio.run(process_and_insert("data/raw/2025-01-01.json"))
