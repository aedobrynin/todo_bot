import asyncio

from aredis_om import Migrator, get_redis_connection

from models import user_data


async def main():
    await Migrator().run()
    test = user_data.UserData(
         user_id='test_user')
    await test.save()


if __name__ == "__main__":
    asyncio.run(main())
