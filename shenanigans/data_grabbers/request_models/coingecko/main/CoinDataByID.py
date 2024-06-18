from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Dict, Union, Any

class MarketDataPrice(BaseModel):
    aed: Optional[float] = None
    ars: Optional[float] = None
    aud: Optional[float] = None
    bch: Optional[float] = None
    usd: Optional[float] = None
    sats: Optional[float] = None


class MarketDataDates(BaseModel):
    aed: str
    ars: str
    aud: str
    bch: str
    usd: str
    sats: str

class MarketData(BaseModel):
    current_price: MarketDataPrice
    total_value_locked: Optional[Any]
    mcap_to_tvl_ratio: Optional[Any]
    fdv_to_tvl_ratio: Optional[Any]
    roi: Optional[Any]
    ath: MarketDataPrice
    ath_change_percentage: MarketDataPrice
    ath_date: MarketDataDates
    atl: MarketDataPrice
    atl_change_percentage: MarketDataPrice
    atl_date: MarketDataDates
    market_cap: MarketDataPrice
    market_cap_rank: int | None
    fully_diluted_valuation: MarketDataPrice
    market_cap_fdv_ratio: float | None
    total_volume: MarketDataPrice
    high_24h: MarketDataPrice
    low_24h: MarketDataPrice
    price_change_24h: float
    price_change_percentage_24h: float
    price_change_percentage_7d_in_currency: MarketDataPrice
    price_change_percentage_14d_in_currency: MarketDataPrice
    price_change_percentage_30d_in_currency: MarketDataPrice
    price_change_percentage_60d_in_currency: MarketDataPrice
    price_change_percentage_200d_in_currency: Dict | MarketDataPrice
    # Add other fields similar to above pattern

class Localization(BaseModel):
    en: str
    de: str
    es: str
    fr: str
    it: str
    # Add other languages as per your JSON structure

class Links(BaseModel):
    homepage: List[str]
    whitepaper: str | None
    blockchain_site: List[str]
    official_forum_url: List[str]
    chat_url: List[str]
    announcement_url: List[str]
    twitter_screen_name: str
    facebook_username: str
    bitcointalk_thread_identifier: Optional[Any]
    telegram_channel_identifier: str
    subreddit_url: str | None
    repos_url: Dict[str, List[str]]

class Image(BaseModel):
    thumb: str
    small: str
    large: str

class CodeAdditionsDeletions(BaseModel):
    additions: int | None
    deletions: int | None

class DeveloperData(BaseModel):
    forks: int
    stars: int
    subscribers: int
    total_issues: int
    closed_issues: int
    pull_requests_merged: int
    pull_request_contributors: int
    code_additions_deletions_4_weeks: CodeAdditionsDeletions
    commit_count_4_weeks: int
    last_4_weeks_commit_activity_series: List

class CommunityData(BaseModel):
    facebook_likes: Optional[Any]
    twitter_followers: int
    reddit_average_posts_48h: float
    reddit_average_comments_48h: float
    reddit_subscribers: int
    reddit_accounts_active_48h: int
    telegram_channel_user_count: Optional[Any]

class TickerMarket(BaseModel):
    name: str
    identifier: str
    has_trading_incentive: bool

class ConvertedLast(BaseModel):
    btc: float
    eth: float
    usd: float

class ConvertedVolume(BaseModel):
    btc: float
    eth: float
    usd: float

class Ticker(BaseModel):
    base: str
    target: str
    market: TickerMarket
    last: float
    volume: float
    converted_last: ConvertedLast
    converted_volume: ConvertedVolume
    trust_score: str | None
    bid_ask_spread_percentage: float | None
    timestamp: str
    last_traded_at: str
    last_fetch_at: str
    is_anomaly: bool
    is_stale: bool
    trade_url: Optional[HttpUrl]
    token_info_url: Optional[Any]
    coin_id: str
    target_coin_id: Optional[str] = None  # Confirmed as optional to handle missing cases

class Validator(BaseModel):
    id: str
    symbol: str
    name: str
    web_slug: str
    asset_platform_id: Optional[Any]
    platforms: Dict[str, str]
    detail_platforms: Dict[str, Dict[str, Optional[str | int | float]]]
    block_time_in_minutes: int
    hashing_algorithm: str | None
    categories: List[str]
    preview_listing: bool
    public_notice: Optional[Any]
    additional_notices: List
    localization: Localization
    description: Localization
    links: Links
    image: Image
    country_origin: str
    genesis_date: str | None
    sentiment_votes_up_percentage: float | None
    sentiment_votes_down_percentage: float | None
    watchlist_portfolio_users: int
    market_cap_rank: int | None
    market_data: MarketData
    community_data: CommunityData
    developer_data: DeveloperData
    status_updates: List
    last_updated: str
    tickers: List[Ticker]
