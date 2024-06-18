from typing import List, Dict, Optional
from pydantic import BaseModel

class PricePercentChanges(BaseModel):
    last_5m: str
    last_15m: str
    last_30m: str
    last_1h: str
    last_6h: str
    last_24h: str

class TokenValueDataItem(BaseModel):
    fdv_in_usd: Optional[float]
    market_cap_in_usd: Optional[float]

class AggregatedNetworkMetrics(BaseModel):
    total_swap_volume_usd_24h: str
    total_swap_volume_usd_48h_24h: str
    total_swap_count_24h: int
    total_swap_volume_percent_change_24h: str

class RelationshipDataItem(BaseModel):
    id: str
    type: str

class Relationships(BaseModel):
    dex: RelationshipDataItem
    tokens: List[RelationshipDataItem]
    pool_metric: RelationshipDataItem

class Attributes(BaseModel):
    address: str
    name: str
    from_volume_in_usd: str
    to_volume_in_usd: str
    api_address: str
    swap_count_24h: int
    price_percent_change: str
    price_percent_changes: PricePercentChanges
    pool_fee: Optional[float] = None
    base_token_id: str
    token_value_data: Dict[str, TokenValueDataItem]
    price_in_usd: str
    reserve_in_usd: str
    aggregated_network_metrics: AggregatedNetworkMetrics
    pool_created_at: str

class Pool(BaseModel):
    id: str
    type: str
    attributes: Attributes
    relationships: Relationships

class OHLCV(BaseModel):
    timestamp: int
    open: float
    high: float
    low: float
    close: float
    volume: float

class Attributes(BaseModel):
    ohlcv_list: List[List[OHLCV]]

class TokenInfo(BaseModel):
    address: str
    name: str
    symbol: str
    coingecko_coin_id: str

class Data(BaseModel):
    id: str
    type: str
    attributes: Attributes

class Meta(BaseModel):
    base: TokenInfo
    quote: TokenInfo

class ResponseModel(BaseModel):
    data: Data
    meta: Meta
