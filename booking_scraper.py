"""
Ireland Hotel Data Scraper

This module contains the HotelScraper class for extracting hotel pricing and ratings data
from booking.com. It handles browser automation, data extraction, and saves to CSV.

Author: Dinesh Barri
Date: 2024
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time
import logging
import os
from typing import List, Dict, Optional

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraping.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class HotelScraper:
    """
    A web scraper for extracting hotel data from booking.com.
    
    Attributes:
        driver (WebDriver): Selenium WebDriver instance
        wait (WebDriverWait): Explicit wait instance
        data (List[Dict]): Collected hotel data
    """
    
    def __init__(self, headless: bool = True):
        """
        Initialize the scraper with Chrome options.
        
        Args:
            headless (bool): Run browser in headless mode if True
        """
        self.setup_driver(headless)
        self.wait = WebDriverWait(self.driver, 15)
        self.data = []
        logger.info("HotelScraper initialized successfully")
    
    def setup_driver(self, headless: bool = True) -> None:
        """Setup Chrome driver with appropriate options."""
        try:
            options = webdriver.ChromeOptions()
            
            if headless:
                options.add_argument('--headless')
            
            # Additional options for stability
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option('excludeSwitches', ['enable-automation'])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            
            # Use webdriver-manager to automatically handle ChromeDriver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            logger.info("WebDriver setup completed")
            
        except Exception as e:
            logger.error(f"Failed to initialize WebDriver: {e}")
            raise
    
    def accept_cookies(self) -> bool:
        """
        Accept cookies if cookie consent banner is present.
        
        Returns:
            bool: True if cookies were accepted, False otherwise
        """
        try:
            # Common cookie consent selectors for booking.com
            cookie_selectors = [
                "button#onetrust-accept-btn-handler",
                "button[id='onetrust-accept-btn-handler']",
                "button[aria-label*='cookie']",
                "button[class*='cookie']",
                "button[data-testid*='cookie']"
            ]
            
            for selector in cookie_selectors:
                try:
                    cookie_button = self.wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    cookie_button.click()
                    logger.info("Cookies accepted successfully")
                    time.sleep(1)
                    return True
                except TimeoutException:
                    continue
            
            logger.info("No cookie consent banner found")
            return False
            
        except Exception as e:
            logger.warning(f"Could not handle cookies: {e}")
            return False
    
    def scrape_hotel_data(self, url: str, max_pages: int = 5) -> pd.DataFrame:
        """
        Main method to scrape hotel data from multiple pages.
        
        Args:
            url (str): The URL to start scraping from
            max_pages (int): Maximum number of pages to scrape
            
        Returns:
            pd.DataFrame: DataFrame containing all scraped hotel data
        """
        try:
            logger.info(f"Starting scraping from: {url}")
            self.driver.get(url)
            time.sleep(5)  # Initial page load
            
            # Accept cookies on first page
            self.accept_cookies()
            
            for page in range(max_pages):
                logger.info(f"Scraping page {page + 1}/{max_pages}")
                
                # Wait for hotel elements to load
                try:
                    self.wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='property-card']"))
                    )
                    time.sleep(3)
                except TimeoutException:
                    logger.warning(f"No hotel cards found on page {page + 1}")
                    break
                
                # Extract data from current page
                page_hotels = self._scrape_current_page()
                logger.info(f"Extracted {page_hotels} hotels from page {page + 1}")
                
                # Try to go to next page
                if page < max_pages - 1:  # Don't try to go to next page on the last page
                    if not self._go_to_next_page():
                        logger.info("No more pages available")
                        break
                
                # Brief pause between pages
                time.sleep(3)
            
            logger.info(f"Scraping completed. Collected {len(self.data)} hotels total")
            return self._create_dataframe()
            
        except Exception as e:
            logger.error(f"Error during scraping: {e}")
            return pd.DataFrame()
    
    def _scrape_current_page(self) -> int:
        """Extract hotel data from the current page."""
        hotels_before = len(self.data)
        
        try:
            # Find all hotel cards on the page
            hotel_cards = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='property-card']")
            logger.info(f"Found {len(hotel_cards)} hotel cards on current page")
            
            for i, card in enumerate(hotel_cards):
                try:
                    hotel_data = self._extract_single_hotel(card)
                    if hotel_data and hotel_data['hotel_name']:  # Only append if we have valid data
                        self.data.append(hotel_data)
                        
                except Exception as e:
                    logger.warning(f"Failed to extract data from hotel card {i+1}: {e}")
                    continue
            
            hotels_after = len(self.data)
            return hotels_after - hotels_before
                    
        except Exception as e:
            logger.error(f"Error scraping current page: {e}")
            return 0
    
    def _extract_single_hotel(self, card) -> Optional[Dict]:
        """
        Extract data from a single hotel card.
        
        Args:
            card: WebElement of the hotel card
            
        Returns:
            Optional[Dict]: Dictionary containing hotel data or None if extraction fails
        """
        try:
            hotel_data = {}
            
            # Extract hotel name
            hotel_data['hotel_name'] = self._safe_extract_text(
                card, "[data-testid='title']"
            )
            
            # Extract price
            price_text = self._safe_extract_text(
                card, "[data-testid='price-and-discounted-price']"
            )
            hotel_data['price'] = self._clean_price(price_text)
            
            # Extract rating
            rating_text = self._safe_extract_text(
                card, "[data-testid='review-score']"
            )
            hotel_data['rating'] = self._clean_rating(rating_text)
            
            # Extract location
            hotel_data['location'] = self._safe_extract_text(
                card, "[data-testid='location']"
            )
            
            # Extract review count if available
            hotel_data['review_count'] = self._safe_extract_text(
                card, "[data-testid='review-score'] div:last-child"
            )
            
            # Extract distance from center
            hotel_data['distance'] = self._safe_extract_text(
                card, "[data-testid='distance']"
            )
            
            return hotel_data
                
        except Exception as e:
            logger.warning(f"Error extracting single hotel: {e}")
            return None
    
    def _safe_extract_text(self, parent_element, css_selector: str) -> str:
        """
        Safely extract text from an element if it exists.
        
        Args:
            parent_element: Parent WebElement to search within
            css_selector (str): CSS selector for the target element
            
        Returns:
            str: Extracted text or empty string if not found
        """
        try:
            element = parent_element.find_element(By.CSS_SELECTOR, css_selector)
            return element.text.strip()
        except NoSuchElementException:
            return ""
    
    def _clean_price(self, price_text: str) -> float:
        """Convert price text to float."""
        try:
            if not price_text:
                return 0.0
                
            # Remove currency symbols, commas, and extra spaces
            cleaned = ''.join(char for char in price_text if char.isdigit() or char == '.')
            
            # Extract first number found (in case of price ranges)
            numbers = cleaned.split()
            if numbers:
                return float(numbers[0])
            return 0.0
            
        except (ValueError, TypeError, IndexError):
            return 0.0
    
    def _clean_rating(self, rating_text: str) -> float:
        """Convert rating text to float."""
        try:
            if not rating_text:
                return 0.0
                
            # Look for numbers in the text
            import re
            numbers = re.findall(r"(\d+\.\d+|\d+)", rating_text)
            if numbers:
                return float(numbers[0])
            return 0.0
            
        except (ValueError, TypeError, IndexError):
            return 0.0
    
    def _go_to_next_page(self) -> bool:
        """
        Navigate to the next page of results.
        
        Returns:
            bool: True if successful, False if no next page exists
        """
        try:
            # Common selectors for next page button
            next_selectors = [
                "button[aria-label*='Next']",
                "a[aria-label*='Next']",
                "button[data-testid*='next']",
                "a[data-testid*='next']",
                "div[data-testid='pagination'] a:last-child"
            ]
            
            for selector in next_selectors:
                try:
                    next_button = self.wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    self.driver.execute_script("arguments[0].click();", next_button)
                    logger.info("Navigated to next page")
                    time.sleep(3)  # Wait for page to load
                    return True
                except TimeoutException:
                    continue
            
            logger.info("No next page button found")
            return False
            
        except Exception as e:
            logger.warning(f"Error navigating to next page: {e}")
            return False
    
    def _create_dataframe(self) -> pd.DataFrame:
        """Convert collected data to pandas DataFrame."""
        if not self.data:
            logger.warning("No data collected to create DataFrame")
            return pd.DataFrame()
        
        df = pd.DataFrame(self.data)
        
        # Add timestamp for when data was collected
        df['scraped_at'] = pd.Timestamp.now()
        
        # Ensure numeric columns are proper types
        df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0)
        df['rating'] = pd.to_numeric(df['rating'], errors='coerce').fillna(0)
        
        logger.info(f"Created DataFrame with {len(df)} rows and {len(df.columns)} columns")
        return df
    
    def save_to_csv(self, filename: str = "hotels.csv") -> None:
        """Save collected data to CSV file."""
        if self.data:
            # Create data directory if it doesn't exist
            os.makedirs('data', exist_ok=True)
            
            filepath = os.path.join('data', filename)
            df = self._create_dataframe()
            df.to_csv(filepath, index=False)
            logger.info(f"Data saved to {filepath}")
            print(f"\n✅ SUCCESS: {len(df)} hotels saved to {filepath}")
        else:
            logger.warning("No data to save")
            print("\n❌ WARNING: No data was collected to save")
    
    def close(self):
        """Close the browser driver."""
        if hasattr(self, 'driver'):
            self.driver.quit()
            logger.info("WebDriver closed")
    
    def __enter__(self):
        """Support context manager protocol."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Ensure driver is closed when exiting context."""
        self.close()


def main():
    """Main function to run the scraper and generate hotels.csv."""
    print("🚀 Starting Ireland Hotel Scraper...")
    print("This may take a few minutes...\n")
    
    # Updated Booking.com search URL for Ireland hotels
    SEARCH_URL = "https://www.booking.com/searchresults.html?ss=Ireland&ssne=Ireland&ssne_untouched=Ireland&efdco=1&label=gen173nr-1FCAEoggI46AdIM1gEaGyIAQGYAQm4ARfIAQzYAQHoAQH4AQuIAgGoAgO4ApCFjJwGwAIB0gIkYjVlN2JjY2MtZTIwOS00N2Y3LWIxY2QtZDI5Yjg2Y2M0YzJj2AIF4AIB&sid=8b3753ff1c70e6311d696a0f7c03cd08&aid=304142&lang=en-us&sb=1&src_elem=sb&src=searchresults&dest_id=37&dest_type=country&ac_position=0&ac_click_type=b&ac_langcode=en&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=5b2e3c3b5abe00b8&ac_meta=GhA1YjJlM2MzYjVhYmUwMGI4IAAoATICZW46B0lyZWxhbmRAAEoAUAA%3D&checkin=2024-03-15&checkout=2024-03-16&group_adults=2&no_rooms=1&group_children=0"
    
    # Initialize scraper
    scraper = HotelScraper(headless=False)  # Set to False to see browser, True for headless
    
    try:
        # Scrape data (3 pages to get a good sample)
        df = scraper.scrape_hotel_data(SEARCH_URL, max_pages=3)
        
        # Save to CSV
        if not df.empty:
            scraper.save_to_csv("hotels.csv")
            
            # Display summary
            print(f"\n📊 SCRAPING SUMMARY:")
            print(f"   • Total Hotels Collected: {len(df)}")
            print(f"   • Average Price: €{df['price'].mean():.2f}")
            print(f"   • Average Rating: {df['rating'].mean():.2f}/10")
            print(f"   • Unique Locations: {df['location'].nunique()}")
            
            print(f"\n📁 File saved: data/hotels.csv")
            print(f"📄 Log file: scraping.log")
            
        else:
            print("❌ No data was scraped. Check scraping.log for details.")
            
    except Exception as e:
        logger.error(f"Scraping failed: {e}")
        print(f"❌ Scraping failed: {e}")
        print("Check scraping.log for detailed error information.")
    
    finally:
        # Ensure driver is closed
        scraper.close()


if __name__ == "__main__":
    main()