import asyncio
import aiohttp
from more_itertools import chunked

from models import init_db, SwapiPeopleHW, Session

MAX_CHUNK = 5

fields = {
    'birth_year': (0, ''),
    'eye_color': (0, ''),
    'gender': (0, ''),
    'hair_color': (0, ''),
    'height': (0, ''),
    'mass': (0, ''),
    'name': (0, ''),
    'skin_color': (0, ''),
    'films': (2, 'title'),
    'homeworld': (1, 'name'),
    'species': (2, 'name'),
    'starships': (2, 'name'),
    'vehicles': (2, 'name'),
}


async def get_complex_info_about_person(url, session, search_field):
    http_response = await session.get(f"{url}")
    json_data = await http_response.json()
    return json_data[search_field]


async def get_person(person_id, session):
    http_response = await session.get(f"https://swapi.py4e.com/api/people/{person_id}/")
    if http_response.status != 200:
        return 0

    json_data = await http_response.json()
    json_data_filter = {}
    json_data_filter['person_id'] = person_id
    for key, value in fields.items():
        type_id = value[0]
        search_field = value[1]
        if type_id == 0:
            json_data_filter[key] = json_data.get(key)
        if type_id == 1:
            json_data_filter[key] = await get_complex_info_about_person(json_data[key], session, search_field)
        if type_id == 2:
            # continue
            data = [await get_complex_info_about_person(json, session, search_field) for json in json_data.get(key)]
            json_data_filter[key] = ",".join(data)

    return json_data_filter


async def insert_records(records):
    records = [SwapiPeopleHW(**record) for record in records if record != 0]
    # print(records)
    async with Session() as session:
        session.add_all(records)
        await session.commit()


async def main():
    print('start main')
    await init_db()
    session = aiohttp.ClientSession()

    for people_id_chunk in chunked(range(1, 20), MAX_CHUNK):
        print(people_id_chunk)
        coros = [get_person(person_id, session) for person_id in people_id_chunk]
        result = await asyncio.gather(*coros)
        asyncio.create_task(insert_records(result))
        # print(result)
    # result = await asyncio.gather(coro_1, coro_2, coro_3, coro_4)
    # print(result)
    await session.close()
    all_tasks_set = asyncio.all_tasks() - {asyncio.current_task()}
    await asyncio.gather(*all_tasks_set)
    print('\n\nend main')
    # await asyncio.gather(*all_tasks_set)


asyncio.run(main())
