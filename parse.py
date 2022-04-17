import datetime
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent
import aiohttp
import aiofiles
import asyncio
from aiocsv import AsyncWriter


async def parse_data(search_field="", lowest_price=0, highest_price=1000000):
    cur_time = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')
    
    for page in range(5):
        headers = {
            'User-Agent': UserAgent().random
        }
        url = f'https://www.olx.ua/elektronika/noutbuki-i-aksesuary/q-{search_field}/?search%5Bfilter_float_price%3Afrom%5D={lowest_price}&search%5Bfilter_float_price%3Ato%5D={highest_price}&page={page}'
        async with aiohttp.ClientSession() as session:
            
            response = await session.get(url=url, headers=headers)
            soup = BS(await response.text(), 'lxml')
            
            offers = soup.find_all('div', class_='offer-wrapper')
            data = []
            for offer in offers:
                name = offer.find('h3', class_='lheight22 margintop5').get_text(strip=True)
                price = offer.find('p', class_='price').get_text(strip=True)
                link = offer.find('a', class_='marginright5').get('href')  
                # print(name + ', ' + price)
                # print(link)
                data.append(
                    [name, price, link]
                )
        
        async with aiofiles.open(f'{search_field}-{lowest_price}-{highest_price}.csv', 'a') as file:
            writer = AsyncWriter(file)
            
            await writer.writerow(
                [
                    'Назва',
                    'Ціна',
                    'Посилання'
                ]
            )
            await writer.writerows(
                data
            )
                
    return f'{search_field}-{lowest_price}-{highest_price}.csv'




async def main():
    await parse_data(search_field="", lowest_price=0, highest_price=1000000)
    
    
if __name__ == '__main__':
    asyncio.run(main())