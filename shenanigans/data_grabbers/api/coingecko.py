from loguru import logger
import asyncio
from api.base import Interface
from request_models.coingecko.terminal.coingecko import Pool

class Main(Interface):
    def __init__(self, capacity: int = 30, fill_rate: float = 1/60):
        super().__init__('https://pro-api.coingecko.com/api/v3/', (capacity, fill_rate))
        self.headers['x-cg-pro-api-key'] = 'PLACE API KEY HERE'

class Terminal(Interface):
    def __init__(self, capacity: int = 30, fill_rate: float = 1/60):
        super().__init__('https://app.geckoterminal.com/api/p1', (capacity, fill_rate))

    #TODO: The API Endpoint here (and really all endpoints) have a hard page cap of 10, which is so weird because obviously the universe of coins on the SOL
    # chain is HEAPS bigger than this. I can see on the front end that there is another endpoint that provides a structured JSON response that is very similar to this endpoints schema
    # but doesnt have this weird lookback maximum. Perhaps we should be using this instead... just be careful of rate limits maybe?
    async def refresh_universe(self):
        """Refresh data by paginating through all available pages in batches of 3."""
        i = 1
        data = []
        more_pages = True
        headers = {**self.headers, 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}
        common_params = {'include': 'dex,dex.network,dex.network.network_metric,tokens', 'include_network_metrics': 'true'}

        while more_pages:
            fetch_tasks = [self.request('solana/pools', 'GET', headers=headers, params={**common_params, 'page': i + j}) for j in range(3)]
            results = await asyncio.gather(*fetch_tasks)

            more_pages = False
            validated_results = [self.validate_response(r, Pool) for r in results['data']]

            for vr in validated_results:
                if not vr: continue
                if vr.data:
                    logger.debug(f"...found data for page#{i}")
                    data.extend(vr.data)
                    i += 1
                    more_pages = True
                else:
                    logger.debug(f"No more data found at page #{i}, stopping pagination...")
                    break

        return data

    #TODO: work out the logic for fetching OHLCV data for a token...
    async def get_ohlcv(self):
        pass