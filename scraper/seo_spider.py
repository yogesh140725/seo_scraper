import scrapy
from bs4 import BeautifulSoup
from datetime import datetime
from .items import SeoItem
import re


class SeoSpider(scrapy.Spider):
    name = 'seo_spider'
    
    def __init__(self, url=None, *args, **kwargs):
        super(SeoSpider, self).__init__(*args, **kwargs)
        self.start_urls = [url] if url else []
    
    def parse(self, response):
        """Parse the response and extract SEO data"""
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Create SEO item
        item = SeoItem()
        item['url'] = response.url
        item['timestamp'] = datetime.now().isoformat()
        item['user_agent'] = response.request.headers.get('User-Agent', b'').decode('utf-8')
        
        # Extract title
        title_tag = soup.find('title')
        item['title'] = title_tag.get_text().strip() if title_tag else ''
        
        # Extract meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        item['meta_description'] = meta_desc.get('content', '') if meta_desc else ''
        
        # Extract meta keywords
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        item['meta_keywords'] = meta_keywords.get('content', '') if meta_keywords else ''
        
        # Extract canonical URL
        canonical = soup.find('link', attrs={'rel': 'canonical'})
        item['canonical_url'] = canonical.get('href', '') if canonical else ''
        
        # Count H1 tags
        h1_tags = soup.find_all('h1')
        item['h1_count'] = len(h1_tags)
        
        # Count total words (excluding script and style content)
        for script in soup(["script", "style"]):
            script.decompose()
        
        text = soup.get_text()
        words = re.findall(r'\b\w+\b', text.lower())
        item['total_words'] = len(words)
        
        # Count images and images without alt
        images = soup.find_all('img')
        item['total_images'] = len(images)
        
        images_without_alt = [img for img in images if not img.get('alt')]
        item['images_without_alt'] = len(images_without_alt)
        
        yield item 