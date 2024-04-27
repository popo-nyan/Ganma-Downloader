import asyncio

import GanmaDownloader


async def main() -> None:
    client = GanmaDownloader.Client()
    await client.create_account()
    magazine_alias = "yamadalv999"
    magazine = await client.get_magazine_data(magazine_alias)
    # for magazine in magazine.stories:
    #     print(magazine.title, magazine.subtitle)
    magazine_data = await client.get_magazine_story_reader(magazine_alias, "279dabe0-3322-11e9-994b-06e4e79605e7")
    print(magazine_data)
    await client.download_story_image()


if __name__ == "__main__":
    asyncio.run(main())
