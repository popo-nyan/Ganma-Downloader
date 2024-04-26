import asyncio

import GanmaDownloader


async def main() -> None:
    client = GanmaDownloader.Ganma()
    await client.create_account()
    magazine_alias = "yamadalv999"
    magazine = await client.get_magazine_data(magazine_alias)
    await client.get_magazine_story_reader(magazine_alias, "279dabe0-3322-11e9-994b-06e4e79605e7")


if __name__ == "__main__":
    asyncio.run(main())
