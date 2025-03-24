import asyncio
import aiohttp
from datetime import datetime
from urllib.parse import urlencode
from tqdm import tqdm
from .eftsquery import EFTSQuery

class TextSearchEFTSQuery(EFTSQuery):
    """
    Extended EFTSQuery class that adds text search capabilities.
    """
    def __init__(self, text_query, requests_per_second=5.0):
        super().__init__(requests_per_second=requests_per_second)
        self.text_query = text_query
        
    def _prepare_params(self, cik=None, submission_type=None, filing_date=None):
        # Get base parameters from parent class
        params = super()._prepare_params(cik, submission_type, filing_date)
        
        # Add text query parameter
        params['q'] = self.text_query
        
        return params

async def extract_accession_numbers(hits):
    """
    Extract accession numbers from hits.
    
    Parameters:
    -----------
    hits : list
        List of hit objects from the EFTS API.
        
    Returns:
    --------
    list
        List of accession numbers extracted from the hits.
    """
    accession_numbers = []
    for hit in hits:
        if '_id' in hit:
            # Extract accession number (part before the colon)
            doc_id = hit['_id']
            if ':' in doc_id:
                acc_no = doc_id.split(':')[0]
                accession_numbers.append(acc_no)
    return accession_numbers

def query(text_query, cik=None, submission_type=None, filing_date=None, requests_per_second=5.0):
    """
    Search SEC filings for text and return the full search results.
    
    Parameters:
    -----------
    text_query : str
        The text to search for in filings. To search for an exact phrase, use double quotes.
        Example: 'covid' or '"climate change"'
    cik : str, list, optional
        CIK number(s) to filter by. Will be zero-padded to 10 digits.
    submission_type : str, list, optional
        Filing type(s) to filter by (e.g., '10-K', '10-Q').
        Defaults to '-0' for primary documents only.
    filing_date : str, tuple, list, optional
        Date or date range to filter by. Can be a single date string ('YYYY-MM-DD'),
        a tuple of (start_date, end_date), or a list of dates.
    requests_per_second : float, optional
        Maximum number of requests per second to make to the SEC API.
        Default is 5.0.
        
    Returns:
    --------
    list
        Complete search results with all hit data.
    """
    async def run_query():
        query = TextSearchEFTSQuery(text_query, requests_per_second=requests_per_second)
        return await query.query(cik, submission_type, filing_date)
    
    return asyncio.run(run_query())

def filter_text(text_query, cik=None, submission_type=None, filing_date=None, requests_per_second=5.0):
    """
    Search SEC filings for text and return matching accession numbers.
    
    Parameters:
    -----------
    text_query : str
        The text to search for in filings. To search for an exact phrase, use double quotes.
        Example: 'covid' or '"climate change"'
    cik : str, list, optional
        CIK number(s) to filter by. Will be zero-padded to 10 digits.
    submission_type : str, list, optional
        Filing type(s) to filter by (e.g., '10-K', '10-Q').
        Defaults to '-0' for primary documents only.
    filing_date : str, tuple, list, optional
        Date or date range to filter by. Can be a single date string ('YYYY-MM-DD'),
        a tuple of (start_date, end_date), or a list of dates.
    requests_per_second : float, optional
        Maximum number of requests per second to make to the SEC API.
        Default is 5.0.
        
    Returns:
    --------
    list
        List of accession numbers (as strings) for filings that match the text query.
    """
    async def run_query():
        query_obj = TextSearchEFTSQuery(text_query, requests_per_second=requests_per_second)
        
        # Create a collector for accession numbers
        all_acc_nos = []
        
        async def collect_acc_nos(hits):
            acc_nos = await extract_accession_numbers(hits)
            all_acc_nos.extend(acc_nos)
        
        # Run the query with our callback
        await query_obj.query(cik, submission_type, filing_date, collect_acc_nos)
        
        return all_acc_nos
    
    return asyncio.run(run_query())