import aiohttp
import aiofiles
import os
from datetime import date
import json
import asyncio
async def download_federal_data(start_date: str, end_date: str):
    url = f"https://www.federalregister.gov/api/v1/documents.json?per_page=100&order=newest&conditions[publication_date][gte]={start_date}&conditions[publication_date][lte]={end_date}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                os.makedirs("data/raw", exist_ok=True)
                async with aiofiles.open(f"data/raw/{start_date}.json", "w") as f:
                    await f.write(json.dumps(data, indent=2))
                print(f"[✓] Downloaded data for {start_date}")
            else:
                print(f"[!] Failed: {response.status}")

#asyncio.run(download_federal_data("2025-01-01", "2025-01-11"))
