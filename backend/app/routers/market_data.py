"""Market data router for fetching stock and mutual fund data."""
from typing import Optional
from fastapi import APIRouter, HTTPException, status
from app.services.market_data import get_stock_price, get_mutual_fund_nav

router = APIRouter(prefix="/market", tags=["Market Data"])


@router.get("/stock/{ticker_symbol}")
def get_stock_data(ticker_symbol: str, exchange: str = "NS"):
    """
    Get current stock price data.
    
    Args:
        ticker_symbol: Stock ticker symbol (e.g., "RELIANCE")
        exchange: Exchange suffix ("NS" for NSE, "BO" for BSE)
    """
    data = get_stock_price(ticker_symbol, exchange)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stock data not found for {ticker_symbol}.{exchange}"
        )
    return data


@router.get("/mutual-fund/{scheme_code}")
def get_mf_nav(scheme_code: str):
    """
    Get mutual fund NAV.
    
    Args:
        scheme_code: Mutual fund scheme code
    """
    data = get_mutual_fund_nav(scheme_code)
    return data
