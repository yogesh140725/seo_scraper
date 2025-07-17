import scrapy


class SeoItem(scrapy.Item):
    """Comprehensive SEO item for storing detailed website analysis data"""
    # Basic info
    url = scrapy.Field()
    timestamp = scrapy.Field()
    user_agent = scrapy.Field()
    
    # Page performance
    status_code = scrapy.Field()
    content_type = scrapy.Field()
    content_length = scrapy.Field()
    load_time = scrapy.Field()
    
    # Title analysis
    title = scrapy.Field()
    title_length = scrapy.Field()
    title_optimal = scrapy.Field()
    
    # Meta tags
    meta_description = scrapy.Field()
    meta_description_length = scrapy.Field()
    meta_description_optimal = scrapy.Field()
    meta_keywords = scrapy.Field()
    
    # Open Graph
    og_title = scrapy.Field()
    og_description = scrapy.Field()
    og_image = scrapy.Field()
    og_url = scrapy.Field()
    
    # Twitter Cards
    twitter_card = scrapy.Field()
    twitter_title = scrapy.Field()
    twitter_description = scrapy.Field()
    
    # Links
    canonical_url = scrapy.Field()
    alternate_links = scrapy.Field()
    
    # Headings
    h1_count = scrapy.Field()
    h1_texts = scrapy.Field()
    h2_count = scrapy.Field()
    h2_texts = scrapy.Field()
    h3_count = scrapy.Field()
    h4_count = scrapy.Field()
    h5_count = scrapy.Field()
    h6_count = scrapy.Field()
    
    # Content
    total_words = scrapy.Field()
    unique_words = scrapy.Field()
    paragraph_count = scrapy.Field()
    paragraphs_with_text = scrapy.Field()
    
    # Links analysis
    total_links = scrapy.Field()
    internal_links = scrapy.Field()
    external_links = scrapy.Field()
    
    # Images
    total_images = scrapy.Field()
    images_without_alt = scrapy.Field()
    images_with_alt = scrapy.Field()
    image_sources = scrapy.Field()
    
    # Forms and tables
    form_count = scrapy.Field()
    table_count = scrapy.Field()
    
    # Lists
    unordered_lists = scrapy.Field()
    ordered_lists = scrapy.Field()
    
    # Technical SEO
    robots_directive = scrapy.Field()
    viewport = scrapy.Field()
    language = scrapy.Field()
    charset = scrapy.Field()
    
    # Structured data
    schema_scripts = scrapy.Field()
    
    # Analytics and tracking
    google_analytics = scrapy.Field()
    facebook_pixel = scrapy.Field()
    
    # Social and contact
    social_media_links = scrapy.Field()
    contact_links = scrapy.Field()
    
    # Performance indicators
    has_ssl = scrapy.Field()
    mobile_friendly = scrapy.Field()
    seo_score = scrapy.Field() 