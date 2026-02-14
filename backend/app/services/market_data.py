"""Market data service using yfinance."""
import yfinance as yf
from typing import Optional, Dict
from datetime import datetime, timedelta
from decimal import Decimal


class MarketDataCache:
    """Simple in-memory cache for market data."""
    
    def __init__(self, ttl_minutes: int = 15):
        self.cache: Dict[str, tuple] = {}
        self.ttl = timedelta(minutes=ttl_minutes)
    
    def get(self, key: str) -> Optional[Dict]:
        """Get cached data if not expired."""
        if key in self.cache:
            data, timestamp = self.cache[key]
            if datetime.now() - timestamp < self.ttl:
                return data
            else:
                del self.cache[key]
        return None
    
    def set(self, key: str, data: Dict):
        """Set cache data with timestamp."""
        self.cache[key] = (data, datetime.now())


# Global cache instance
market_cache = MarketDataCache()


def get_stock_price(ticker_symbol: str, exchange: str = "NS") -> Optional[Dict]:
    """
    Get current stock price from yfinance.
    
    Args:
        ticker_symbol: Stock ticker symbol (e.g., "RELIANCE")
        exchange: Exchange suffix ("NS" for NSE, "BO" for BSE)
    
    Returns:
        Dictionary with price data or None if not found
    """
    cache_key = f"{ticker_symbol}.{exchange}"
    
    # Check cache first
    cached_data = market_cache.get(cache_key)
    if cached_data:
        return cached_data
    
    try:
        # Fetch from yfinance
        ticker = yf.Ticker(f"{ticker_symbol}.{exchange}")
        hist = ticker.history(period="1d")
        
        if hist.empty:
            return None
        
        latest = hist.iloc[-1]
        info = ticker.info
        
        data = {
            "symbol": ticker_symbol,
            "exchange": exchange,
            "current_price": float(latest["Close"]),
            "open": float(latest["Open"]),
            "high": float(latest["High"]),
            "low": float(latest["Low"]),
            "volume": int(latest["Volume"]),
            "previous_close": float(info.get("previousClose", latest["Close"])),
            "change": float(latest["Close"] - info.get("previousClose", latest["Close"])),
            "change_percent": float(((latest["Close"] - info.get("previousClose", latest["Close"])) / info.get("previousClose", latest["Close"])) * 100),
            "currency": "INR",
            "timestamp": datetime.now().isoformat()
        }
        
        # Cache the result
        market_cache.set(cache_key, data)
        
        return data
    
    except Exception as e:
        print(f"Error fetching stock price for {ticker_symbol}: {e}")
        return None


def get_mutual_fund_nav(scheme_code: str) -> Optional[Dict]:
    """
    Get mutual fund NAV.
    Note: yfinance may not have all Indian mutual funds.
    This is a placeholder for integration with other APIs if needed.
    
    Args:
        scheme_code: Mutual fund scheme code
    
    Returns:
        Dictionary with NAV data or None if not found
    """
    # For now, return placeholder
    # In production, integrate with AMFI or other MF data APIs
    return {
        "scheme_code": scheme_code,
        "nav": None,
        "date": datetime.now().date().isoformat(),
        "message": "Mutual fund NAV data not available via yfinance. Integrate with AMFI API."
    }


def update_investment_values(investments: list) -> list:
    """
    Update current values for investments with ticker symbols.
    
    Args:
        investments: List of investment objects
    
    Returns:
        Updated list of investments
    """
    for investment in investments:
        if investment.ticker_symbol and investment.is_active:
            # Determine exchange based on investment type
            exchange = "NS"  # Default to NSE
            
            price_data = get_stock_price(investment.ticker_symbol, exchange)
            if price_data:
                # Update current value based on amount invested and current price
                # This is a simplified calculation
                # In production, track quantity separately
                investment.current_value = Decimal(str(price_data["current_price"]))
    
    return investments
