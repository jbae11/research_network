import scrapy

class GSScraper(scrapy.Spider):
    name = "google_scholar"
    # start with Jin Whan Bae
    base_url = 'https://scholar.google.com'
    #start_urls = ['https://scholar.google.com/citations?user=M4wdbikAAAAJ&hl=en', #Jin Whan Bae,
    #              'https://scholar.google.com/citations?user=wWCoUEAAAAAJ&hl=en', #Andrew Worrall,
    #              'https://scholar.google.com/citations?user=uqlgX0IAAAAJ&hl=en' #Benjamin Betzler
    #              ]

    def __init__(self, start_url_file, *args, **kwargs):
        super(GSScraper, self).__init__(*args, **kwargs)
        lines = [q.split('#')[0].strip() for q in open(start_url_file).readlines()]
        self.start_urls = lines



    def parse(self, response):
        collaborators = response.css('.gsc_rsb_a > li > div > span > a::attr(href)').getall()
        # add myself in collaborators
        collaborators = [self.base_url + url for url in collaborators]
        collaborators.append(response.url)
       
        for url in collaborators:
            yield scrapy.Request(url, callback=self.parse_page)


    def parse_page(self, response):
        print("procesing: "+response.url)
        #Extract data using css selectors
        name = response.css('title::text').get().replace(' - Google Scholar', '')
        collaborators = response.css('.gsc_rsb_a > li > div > span > a::text').getall()
        collaborators_link = response.css('.gsc_rsb_a > li > div > span > a::attr(href)').getall()
        citations = response.css('#gsc_rsb_st > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2)::text').get()
        hindx = response.css('#gsc_rsb_st > tbody:nth-child(2) > tr:nth-child(2) > td:nth-child(2)::text').get()
        i10_index = response.css('#gsc_rsb_st > tbody:nth-child(2) > tr:nth-child(3) > td:nth-child(2)::text').get()
        organization = response.css('div.gsc_prf_il:nth-child(2) > a:nth-child(1)::text').get()
        image = response.css('#gsc_prf_pup-img').attrib['src']
        yield {
            'Name': name,
            'Collaborators': collaborators,
            'ImageLink': image,
            'Citations': int(citations),
            'Hindx': int(hindx),
            'I10_index': int(i10_index),
            'Organization': organization,
            'CollaboratorsLink': collaborators_link
        }