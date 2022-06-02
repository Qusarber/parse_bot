from bs4 import BeautifulSoup as beautifulsoup
from fake_useragent import UserAgent
import aiohttp
import aiofiles
from aiocsv import AsyncWriter


async def parse_data(category="", search_field="", lowest_price=0, highest_price=10000000):
    data = []

    for page in range(10):
        headers = {
            'User-Agent': UserAgent().random
        }
        url = f'https://www.olx.ua/d/{category}/q-{search_field}/?currency=UAH&search%5Bfilter_float_price:from%5D={lowest_price}&search%5Bfilter_float_price:to%5D={highest_price}&page={page}'
        async with aiohttp.ClientSession() as session:
            
            response = await session.get(url=url, headers=headers)
            soup = beautifulsoup(await response.text(), 'lxml')
            
            offers = soup.find_all('div', class_='offer-wrapper')
            print(offers)
            for offer in offers:
                name = offer.find('h3', class_='lheight22 margintop5').get_text(strip=True)
                price = offer.find('p', class_='price').get_text(strip=True)
                link = offer.find('a', class_='marginright5').get('href')  

                if lowest_price <= price <= highest_price:
                    data.append(
                        [name, price, link]
                    )
        
    async with aiofiles.open(f'{search_field}-{category}.csv', 'a') as file:
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
                
    return f'{search_field}-{category}.csv'
