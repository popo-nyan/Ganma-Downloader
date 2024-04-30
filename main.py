import asyncio

import GanmaDownloader


async def main() -> None:
    client = GanmaDownloader.Client()
    await client.create_account()
    search_keyword = str(input("Enter your search keyword: "))
    search_data = await client.search_magazine(search_keyword)
    magazine = await client.get_magazine_data(search_data[0].magazine_id)
    if magazine is not None:
        for magazine in magazine.stories:
            magazine_data = await client.get_magazine_story_reader(search_data[0].magazine_id, magazine.storyId)
            for count in range(1, magazine_data.story_contents.page_images.page_count):
                await client.download_story_image(base_url=magazine_data.story_contents.page_images.page_image_base_url,
                                                  image_sign=magazine_data.story_contents.page_images.page_image_sign,
                                                  page_count=count,
                                                  alias=search_data[0].title,
                                                  title=magazine_data.story_contents.story_info.title,
                                                  subtitle=magazine_data.story_contents.story_info.subtitle)
                await asyncio.sleep(1)
            print(f"[INFO] Waiting to avoid overloading the server")
            await asyncio.sleep(5)
    else:
        print(f"[ERROR] {search_data[0].magazine_id} does not exist.")


if __name__ == "__main__":
    asyncio.run(main())
