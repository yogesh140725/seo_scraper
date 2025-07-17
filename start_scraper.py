import os
import sys
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from fake_useragent import UserAgent
from urllib.parse import urlparse


def run_spider(url):
    """Run the SEO spider for a given URL using requests and BeautifulSoup"""
    # Add the current directory to Python path
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    # Create a fake user agent
    ua = UserAgent()
    user_agent = ua.random
    
    # Configure headers
    headers = {
        'User-Agent': user_agent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
    }
    
    try:
        # Make the request
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Create comprehensive SEO item
        item = {}
        item['url'] = url
        item['timestamp'] = datetime.now().isoformat()
        item['user_agent'] = user_agent
        
        # Basic page info
        item['status_code'] = response.status_code
        item['content_type'] = response.headers.get('content-type', '')
        item['content_length'] = len(response.content)
        item['load_time'] = response.elapsed.total_seconds()
        
        # Title analysis
        title_tag = soup.find('title')
        item['title'] = title_tag.get_text().strip() if title_tag else ''
        item['title_length'] = len(item['title'])
        item['title_optimal'] = 50 <= len(item['title']) <= 60
        
        # Meta tags analysis
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        item['meta_description'] = meta_desc.get('content', '') if meta_desc else ''
        item['meta_description_length'] = len(item['meta_description'])
        item['meta_description_optimal'] = 150 <= len(item['meta_description']) <= 160
        
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        item['meta_keywords'] = meta_keywords.get('content', '') if meta_keywords else ''
        
        # Open Graph tags
        og_title = soup.find('meta', attrs={'property': 'og:title'})
        item['og_title'] = og_title.get('content', '') if og_title else ''
        
        og_description = soup.find('meta', attrs={'property': 'og:description'})
        item['og_description'] = og_description.get('content', '') if og_description else ''
        
        og_image = soup.find('meta', attrs={'property': 'og:image'})
        item['og_image'] = og_image.get('content', '') if og_image else ''
        
        og_url = soup.find('meta', attrs={'property': 'og:url'})
        item['og_url'] = og_url.get('content', '') if og_url else ''
        
        # Twitter Card tags
        twitter_card = soup.find('meta', attrs={'name': 'twitter:card'})
        item['twitter_card'] = twitter_card.get('content', '') if twitter_card else ''
        
        twitter_title = soup.find('meta', attrs={'name': 'twitter:title'})
        item['twitter_title'] = twitter_title.get('content', '') if twitter_title else ''
        
        twitter_description = soup.find('meta', attrs={'name': 'twitter:description'})
        item['twitter_description'] = twitter_description.get('content', '') if twitter_description else ''
        
        # Canonical and alternate links
        canonical = soup.find('link', attrs={'rel': 'canonical'})
        item['canonical_url'] = canonical.get('href', '') if canonical else ''
        
        alternate_links = soup.find_all('link', attrs={'rel': 'alternate'})
        item['alternate_links'] = [link.get('href', '') for link in alternate_links]
        
        # Heading analysis
        h1_tags = soup.find_all('h1')
        item['h1_count'] = len(h1_tags)
        item['h1_texts'] = [h1.get_text().strip() for h1 in h1_tags]
        
        h2_tags = soup.find_all('h2')
        item['h2_count'] = len(h2_tags)
        item['h2_texts'] = [h2.get_text().strip() for h2 in h2_tags]
        
        h3_tags = soup.find_all('h3')
        item['h3_count'] = len(h3_tags)
        item['h3_texts'] = [h3.get_text().strip() for h3 in h3_tags]
        
        h4_tags = soup.find_all('h4')
        item['h4_count'] = len(h4_tags)
        item['h4_texts'] = [h4.get_text().strip() for h4 in h4_tags]
        
        h5_tags = soup.find_all('h5')
        item['h5_count'] = len(h5_tags)
        
        h6_tags = soup.find_all('h6')
        item['h6_count'] = len(h6_tags)
        
        # Content analysis
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        text = soup.get_text()
        words = re.findall(r'\b\w+\b', text.lower())
        item['total_words'] = len(words)
        item['unique_words'] = len(set(words))
        
        # Advanced content analysis
        # Keyword density analysis
        word_freq = {}
        for word in words:
            if len(word) > 2:  # Skip short words
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Get top keywords
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        item['top_keywords'] = sorted_words[:20]  # Top 20 keywords
        
        # Keyword density
        item['keyword_density'] = {word: round((count/len(words)*100), 2) for word, count in sorted_words[:10]}
        
        # Readability analysis
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        item['sentence_count'] = len(sentences)
        item['avg_sentence_length'] = round(sum(len(s.split()) for s in sentences) / len(sentences), 2) if sentences else 0
        
        # Reading level estimation
        syllables = 0
        for word in words:
            syllables += len(re.findall(r'[aeiouy]+', word.lower()))
        item['avg_syllables_per_word'] = round(syllables / len(words), 2) if words else 0
        
        # Flesch Reading Ease (simplified)
        if item['avg_sentence_length'] > 0 and item['avg_syllables_per_word'] > 0:
            item['flesch_reading_ease'] = round(206.835 - (1.015 * item['avg_sentence_length']) - (84.6 * item['avg_syllables_per_word']), 2)
        else:
            item['flesch_reading_ease'] = 0
        
        # Paragraph analysis
        paragraphs = soup.find_all('p')
        item['paragraph_count'] = len(paragraphs)
        item['paragraphs_with_text'] = len([p for p in paragraphs if p.get_text().strip()])
        
        # Link analysis
        all_links = soup.find_all('a', href=True)
        item['total_links'] = len(all_links)
        
        internal_links = [link for link in all_links if url in link.get('href', '')]
        item['internal_links'] = len(internal_links)
        
        external_links = [link for link in all_links if url not in link.get('href', '') and link.get('href', '').startswith('http')]
        item['external_links'] = len(external_links)
        
        # Advanced link analysis
        link_texts = [link.get_text().strip() for link in all_links if link.get_text().strip()]
        item['link_texts'] = link_texts[:20]  # First 20 link texts
        
        # Nofollow links
        nofollow_links = [link for link in all_links if link.get('rel') and 'nofollow' in link.get('rel')]
        item['nofollow_links'] = len(nofollow_links)
        
        # External domains
        external_domains = set()
        for link in external_links:
            try:
                domain = urlparse(link.get('href')).netloc
                external_domains.add(domain)
            except:
                pass
        item['external_domains'] = list(external_domains)
        
        # Internal page links
        internal_pages = []
        for link in internal_links:
            href = link.get('href', '')
            if href and not href.startswith('#') and not href.startswith('mailto:'):
                internal_pages.append(href)
        item['internal_pages'] = internal_pages[:20]  # First 20 internal pages
        
        # Image analysis
        images = soup.find_all('img')
        item['total_images'] = len(images)
        
        images_without_alt = [img for img in images if not img.get('alt')]
        item['images_without_alt'] = len(images_without_alt)
        item['images_with_alt'] = item['total_images'] - item['images_without_alt']
        
        # Advanced image analysis
        image_details = []
        for img in images[:10]:  # First 10 images
            img_info = {
                'src': img.get('src', ''),
                'alt': img.get('alt', ''),
                'title': img.get('title', ''),
                'width': img.get('width', ''),
                'height': img.get('height', ''),
                'loading': img.get('loading', ''),
                'decoding': img.get('decoding', '')
            }
            image_details.append(img_info)
        item['image_details'] = image_details
        
        # Image sources
        image_srcs = [img.get('src', '') for img in images if img.get('src')]
        item['image_sources'] = image_srcs[:10]  # First 10 image sources
        
        # Video analysis
        videos = soup.find_all(['video', 'iframe'])
        item['video_count'] = len(videos)
        video_sources = []
        for video in videos:
            if video.name == 'video':
                sources = video.find_all('source')
                for source in sources:
                    video_sources.append(source.get('src', ''))
            elif video.name == 'iframe':
                video_sources.append(video.get('src', ''))
        item['video_sources'] = video_sources
        
        # Audio analysis
        audio = soup.find_all('audio')
        item['audio_count'] = len(audio)
        
        # Form analysis
        forms = soup.find_all('form')
        item['form_count'] = len(forms)
        
        # Table analysis
        tables = soup.find_all('table')
        item['table_count'] = len(tables)
        
        # List analysis
        ul_lists = soup.find_all('ul')
        ol_lists = soup.find_all('ol')
        item['unordered_lists'] = len(ul_lists)
        item['ordered_lists'] = len(ol_lists)
        
        # CSS and JS analysis
        css_files = soup.find_all('link', rel='stylesheet')
        js_files = soup.find_all('script', src=True)
        item['css_files'] = [css.get('href', '') for css in css_files]
        item['js_files'] = [js.get('src', '') for js in js_files]
        
        # Inline CSS and JS
        inline_css = soup.find_all('style')
        inline_js = soup.find_all('script', src=False)
        item['inline_css_count'] = len(inline_css)
        item['inline_js_count'] = len(inline_js)
        
        # Meta robots
        robots = soup.find('meta', attrs={'name': 'robots'})
        item['robots_directive'] = robots.get('content', '') if robots else ''
        
        # Viewport
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        item['viewport'] = viewport.get('content', '') if viewport else ''
        
        # Language
        lang = soup.get('lang', '')
        item['language'] = lang
        
        # Character encoding
        charset = soup.find('meta', attrs={'charset': True})
        if charset:
            item['charset'] = charset.get('charset', '')
        else:
            charset_meta = soup.find('meta', attrs={'http-equiv': 'content-type'})
            item['charset'] = charset_meta.get('content', '').split('charset=')[-1] if charset_meta else ''
        
        # All meta tags analysis
        all_meta_tags = soup.find_all('meta')
        meta_analysis = {}
        for meta in all_meta_tags:
            name = meta.get('name', meta.get('property', ''))
            content = meta.get('content', '')
            if name and content:
                meta_analysis[name] = content
        item['all_meta_tags'] = meta_analysis
        
        # Schema.org structured data
        schema_scripts = soup.find_all('script', type='application/ld+json')
        item['schema_scripts'] = len(schema_scripts)
        
        # Structured data content
        structured_data = []
        for script in schema_scripts:
            try:
                import json
                data = json.loads(script.string)
                structured_data.append(data)
            except:
                pass
        item['structured_data_content'] = structured_data
        
        # Google Analytics
        ga_scripts = soup.find_all('script', src=re.compile(r'google-analytics|gtag|googletagmanager'))
        item['google_analytics'] = len(ga_scripts) > 0
        
        # Facebook Pixel
        fb_scripts = soup.find_all('script', src=re.compile(r'facebook|fbevents'))
        item['facebook_pixel'] = len(fb_scripts) > 0
        
        # Social media links
        social_links = []
        for link in all_links:
            href = link.get('href', '').lower()
            if any(social in href for social in ['facebook.com', 'twitter.com', 'linkedin.com', 'instagram.com', 'youtube.com', 'tiktok.com', 'pinterest.com']):
                social_links.append(href)
        item['social_media_links'] = social_links
        
        # Contact information
        contact_info = []
        for link in all_links:
            href = link.get('href', '').lower()
            if any(contact in href for contact in ['mailto:', 'tel:', 'contact', 'about', 'support']):
                contact_info.append(href)
        item['contact_links'] = contact_info
        
        # Performance indicators
        item['has_ssl'] = url.startswith('https://')
        item['mobile_friendly'] = bool(item['viewport'])
        
        # Page speed indicators
        item['has_minified_css'] = any('min.css' in css for css in item['css_files'])
        item['has_minified_js'] = any('min.js' in js for js in item['js_files'])
        item['has_compressed_resources'] = item['has_minified_css'] or item['has_minified_js']
        
        # Security headers check
        security_headers = {
            'x-frame-options': response.headers.get('x-frame-options', ''),
            'x-content-type-options': response.headers.get('x-content-type-options', ''),
            'x-xss-protection': response.headers.get('x-xss-protection', ''),
            'strict-transport-security': response.headers.get('strict-transport-security', ''),
            'content-security-policy': response.headers.get('content-security-policy', '')
        }
        item['security_headers'] = security_headers
        
        # Server information
        server_info = {
            'server': response.headers.get('server', ''),
            'x-powered-by': response.headers.get('x-powered-by', ''),
            'cache-control': response.headers.get('cache-control', ''),
            'expires': response.headers.get('expires', ''),
            'last-modified': response.headers.get('last-modified', '')
        }
        item['server_info'] = server_info
        
        # Advanced SEO scoring
        seo_score = 0
        
        # Basic SEO (25 points)
        if item['title']: seo_score += 5
        if item['meta_description']: seo_score += 5
        if item['canonical_url']: seo_score += 3
        if item['h1_count'] == 1: seo_score += 5
        if item['images_with_alt'] > 0: seo_score += 3
        if item['has_ssl']: seo_score += 4
        
        # Content quality (25 points)
        if item['total_words'] > 300: seo_score += 5
        if item['total_words'] > 1000: seo_score += 5
        if item['paragraph_count'] > 5: seo_score += 3
        if item['sentence_count'] > 10: seo_score += 3
        if item['flesch_reading_ease'] > 60: seo_score += 4
        if item['unique_words'] > 100: seo_score += 5
        
        # Technical SEO (25 points)
        if item['mobile_friendly']: seo_score += 5
        if item['og_title']: seo_score += 3
        if item['og_description']: seo_score += 3
        if item['twitter_card']: seo_score += 3
        if item['schema_scripts'] > 0: seo_score += 5
        if item['robots_directive']: seo_score += 3
        if item['language']: seo_score += 3
        
        # Link structure (15 points)
        if item['internal_links'] > 5: seo_score += 5
        if item['external_links'] > 0: seo_score += 3
        if item['total_links'] > 10: seo_score += 4
        if item['nofollow_links'] < item['total_links'] * 0.5: seo_score += 3
        
        # Media optimization (10 points)
        if item['images_with_alt'] > item['total_images'] * 0.8: seo_score += 5
        if item['video_count'] > 0: seo_score += 3
        if item['css_files']: seo_score += 2
        
        item['seo_score'] = min(seo_score, 100)  # Cap at 100
        
        # SEO recommendations
        recommendations = []
        if not item['title']: recommendations.append("Missing page title")
        if not item['meta_description']: recommendations.append("Missing meta description")
        if item['h1_count'] == 0: recommendations.append("Missing H1 tag")
        if item['h1_count'] > 1: recommendations.append("Multiple H1 tags found")
        if item['images_without_alt'] > 0: recommendations.append(f"{item['images_without_alt']} images missing alt text")
        if not item['has_ssl']: recommendations.append("Website not using HTTPS")
        if not item['mobile_friendly']: recommendations.append("No viewport meta tag for mobile")
        if item['total_words'] < 300: recommendations.append("Content too short (less than 300 words)")
        if item['flesch_reading_ease'] < 60: recommendations.append("Content may be too complex to read")
        if item['nofollow_links'] > item['total_links'] * 0.5: recommendations.append("Too many nofollow links")
        if not item['og_title']: recommendations.append("Missing Open Graph title")
        if not item['og_description']: recommendations.append("Missing Open Graph description")
        if not item['twitter_card']: recommendations.append("Missing Twitter Card")
        if item['schema_scripts'] == 0: recommendations.append("No structured data found")
        if not item['robots_directive']: recommendations.append("No robots meta tag")
        
        item['seo_recommendations'] = recommendations
        
        return [item]
        
    except Exception as e:
        raise Exception(f"Failed to scrape {url}: {str(e)}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python start_scraper.py <url>")
        sys.exit(1)
    
    url = sys.argv[1]
    print(f"Starting SEO scraping for: {url}")
    
    try:
        results = run_spider(url)
        print(f"Scraping completed. Found {len(results)} results.")
        for result in results:
            print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error during scraping: {e}")
        sys.exit(1) 