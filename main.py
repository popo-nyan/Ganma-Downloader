import asyncio

import GanmaDownloader


async def main() -> None:
    client = GanmaDownloader.Client()
    await client.create_account()
    magazine_alias = str(input("Magazine Alias: "))
    magazine = await client.get_magazine_data(magazine_alias)
    if magazine is not None:
        for magazine in magazine.stories:
            magazine_data = await client.get_magazine_story_reader(magazine_alias, magazine.storyId)
            if magazine_data is None:
                continue
            for count in range(1, magazine_data.story_contents.page_images.page_count):
                if magazine_data.story_contents.story_info.subtitle is None:
                    continue
                await client.download_story_image(base_url=magazine_data.story_contents.page_images.page_image_base_url,
                                                  image_sign=magazine_data.story_contents.page_images.page_image_sign,
                                                  page_count=count,
                                                  alias=magazine_alias,
                                                  title=magazine_data.story_contents.story_info.title,
                                                  subtitle=magazine_data.story_contents.story_info.subtitle)
                await asyncio.sleep(1)
            print(f"[INFO] Waiting to avoid overloading the server")
            await asyncio.sleep(5)
    else:
        print(f"[ERROR] {magazine_alias} does not exist.")


if __name__ == "__main__":
    asyncio.run(main())
