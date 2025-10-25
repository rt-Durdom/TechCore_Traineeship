import asyncio
import aiofiles
import json

student = [
    {'name': 'Иванов', 'avg_grade':  3.4, 'year': 2021},
    {'name': 'Петров', 'avg_grade': 4.5, 'year': 2021},
    {'name': 'Сидоров', 'avg_grade':  3.9, 'year': 2021},
    {'name': 'Васильев', 'avg_grade': 4.9, 'year': 2021}
]


async def serialize_json(student):
    async with aiofiles.open(
        'module_3/data_json/config.json',
        'w', encoding='utf-8'
    ) as f:
        await f.write(json.dumps(student, ensure_ascii=False))


async def deserialize_json():
    async with aiofiles.open(
        'module_3/data_json/config.json',
        'r', encoding='utf-8'
    ) as file_json:
        text = await file_json.read()
        return json.loads(text)


if __name__ == '__main__':
    asyncio.run(serialize_json(student))
    print(asyncio.run(deserialize_json()))
