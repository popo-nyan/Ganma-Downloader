import asyncio

from GanmaDownloader.client import Ganma


async def main() -> None:
    client = Ganma()
    await client.create_account()
    magazine = await client.get_magazine_data("yamadalv999")
    for story in magazine.items:
        print(story)


if __name__ == "__main__":
    asyncio.run(main())
