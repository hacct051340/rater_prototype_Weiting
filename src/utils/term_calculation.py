"""
Term calculation utilities for pro-rata adjustments.
"""
from datetime import datetime, date
from typing import Tuple


def calculate_term_factor(policy_start: str, policy_end: str, 
                         rate_date: str = None) -> float:
    """
    Calculate pro-rata term factor for non-annual policies.
    
    Args:
        policy_start: Policy start date (YYYY-MM-DD)
        policy_end: Policy end date (YYYY-MM-DD)
        rate_date: Rate effective date (YYYY-MM-DD), defaults to policy_start
    
    Returns:
        Term factor (1.0 for annual, <1.0 for shorter terms)
    """
    if rate_date is None:
        rate_date = policy_start
    
    start_date = date.fromisoformat(policy_start)
    end_date = date.fromisoformat(policy_end)
    rate_dt = date.fromisoformat(rate_date)
    
    # Calculate policy term in days
    policy_days = (end_date - start_date).days
    
    # Calculate days in the rate year
    rate_year_start = date(rate_dt.year, 1, 1)
    rate_year_end = date(rate_dt.year + 1, 1, 1)
    days_in_rate_year = (rate_year_end - rate_year_start).days
    
    # Calculate term factor
    term_factor = policy_days / days_in_rate_year
    
    return term_factor


def get_policy_years(policy_start: str, policy_end: str) -> list:
    """
    Get list of policy years for multi-year policies.
    
    Args:
        policy_start: Policy start date (YYYY-MM-DD)
        policy_end: Policy end date (YYYY-MM-DD)
    
    Returns:
        List of (year, start_date, end_date) tuples
    """
    start_date = date.fromisoformat(policy_start)
    end_date = date.fromisoformat(policy_end)
    
    years = []
    current_year = start_date.year
    
    while current_year <= end_date.year:
        year_start = max(start_date, date(current_year, 1, 1))
        year_end = min(end_date, date(current_year + 1, 1, 1) - date.resolution)
        
        years.append((current_year, year_start.strftime("%Y-%m-%d"), year_end.strftime("%Y-%m-%d")))
        current_year += 1
    
    return years


def is_annual_policy(policy_start: str, policy_end: str) -> bool:
    """
    Check if policy is exactly one year.
    
    Args:
        policy_start: Policy start date (YYYY-MM-DD)
        policy_end: Policy end date (YYYY-MM-DD)
    
    Returns:
        True if policy is exactly one year
    """
    start_date = date.fromisoformat(policy_start)
    end_date = date.fromisoformat(policy_end)
    
    # Check if it's exactly one year
    if start_date.month == end_date.month and start_date.day == end_date.day:
        return end_date.year - start_date.year == 1
    
    return False
