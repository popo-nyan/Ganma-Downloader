import asyncio

import GanmaDownloader


async def main() -> None:
    client = GanmaDownloader.Ganma()
    await client.create_account()
    magazine_alias = "yamadalv999"
    magazine = await client.get_magazine_data(magazine_alias)
    for story in magazine.items:
        print(story)


if __name__ == "__main__":
    asyncio.run(main())
