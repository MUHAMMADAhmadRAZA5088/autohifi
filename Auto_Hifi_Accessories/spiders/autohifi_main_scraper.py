import scrapy
import pandas as pd
import re

class BrandAccessoriesSpider(scrapy.Spider):
    
    name = "autohifi"
    allowed_domains = ["www.autohifi.no"]
    data = []
    file_reading = 1
    start_urls = [
        "https://www.autohifi.no/bilunderholdning_1",
        "https://www.autohifi.no/bilmerke-tilbeh%C3%B8r-v2",
        "https://www.autohifi.no/marineunderholdning",
        "https://www.autohifi.no/ekstralys",
        "https://www.autohifi.no/dashcam",
        "https://www.autohifi.no/spillere-/-headunits",
        "https://www.autohifi.no/antenner",
        "https://www.autohifi.no/nyheter",
        "https://www.autohifi.no/bilspesifikke-basskasser"
        ]

    def parse(self, response):
        anchors = response.xpath(
            '//div[@class="StandardArticleMainExBorder"]//a/@href'
            ).getall()
        
        sidebar_anchor = response.xpath(
            '//div[@class="ProductMenu"]/ul/li[@class="Level1"]/a/@href'
            ).getall()
        
        if anchors :
            yield from response.follow_all(anchors, self.parse_brand)
        elif sidebar_anchor :
            yield from response.follow_all(sidebar_anchor, self.parse_brand)

        product_link = response.xpath('//div[@class="AddHeaderContainer"]/a')
        if product_link is not None:
            yield from response.follow_all(
                product_link,
                callback = self.parse_product_scraper
                )
        
        pagination = response.xpath(
            '//div[@class="FieldPaging"]/a[.=">"]/@href'
            ).get()
        
        if pagination is not None:
            yield response.follow(pagination, callback=self.parse)
            
    def parse_brand(self, response):
        anchors = response.xpath(
            '//div[@class="StandardArticleMainExBorder"]//a/@href'
            ).getall()

        if anchors is not None:
            yield from response.follow_all(anchors, self.parse_author)

        product_link = response.xpath('//div[@class="AddHeaderContainer"]/a')

        if product_link is not None:
            yield from response.follow_all(
                product_link, 
                callback = self.parse_product_scraper
                )

    def parse_author(self, response):
        main_scraper = response.xpath(
            '//div[@class="StandardArticleMainExBorder"]//a'
            )

        if main_scraper is not None:
            yield from response.follow_all(main_scraper, self.parse_author_year)

        product_link = response.xpath('//div[@class="AddHeaderContainer"]/a')

        if product_link is not None:
            yield from response.follow_all(
                product_link, callback = self.parse_product_scraper
                )

    
    def parse_author_year(self, response):
        product_link = response.xpath('//div[@class="AddHeaderContainer"]/a')
        yield from response.follow_all(
            product_link, callback=self.parse_product_scraper
            )
    

    def parse_product_scraper(self, response):
        brand_names = [
            '4 Connect',
            '4 Power',
            '4Connect',
            '4POWER',
            '5 Connect',
            'ACV',
            'ACX',
            'AH',
            'AI-SONIC',
            'Alpine',
            'Alpine',
            'Ampire',
            'Antenne (DAB)',
            'Antenne adapter',
            'Antennepisk',
            'Antennesplitter',
            'Asuka',
            'Audio/Video interface',
            'Audison',
            'Aura',
            'AutoDAB',
            'Axton',
            'BeatSonic',
            'BLACKVUE',
            'Blam',
            'Blam',
            'BLAM',
            'Blaupunkt',
            'BOSS',
            'Boss',
            'Brax',
            'Cadence',
            'Caliber',
            'CarAudio Systems',
            'CDS',
            'Cerwin Vega',
            'Clarion',
            'Comfort Modul',
            'ConnectED',
            'Connection',
            'Connects2',
            'Continental',
            'Crunch',
            'DAB integrering',
            'DAB-antenne',
            'DASHCAM',
            'DD Audio',
            'DEFA',
            'Dension',
            'Diamond Audio',
            'DIRECTOR',
            'Dynamat',
            'EMPHASER',
            'ESX',
            'Eton',
            'Fiamm',
            'Firefly',
            'Focal',
            'FOUR Audio',
            'FOUR Connect',
            'G4Audiio',
            'Garmin',
            'Gladen',
            'GLADEN',
            'Ground  Zero',
            'Ground Zero',
            'Halo',
            'Hardstone',
            'Harman/Kardon',
            'Helix',
            'HELIX Q',
            'Hertz',
            'Hertz Marine',
            'Hifonics',
            'In2digi',
            'JBL',
            'Jensen',
            'JL Audio',
            'JL Audio',
            'JVC',
            'JVC',
            'Kenwood',
            'Kicker',
            'Kicker',
            'Kram Telecom',
            'Kufatec',
            'Lukas',
            'MAGNAT',
            'Match',
            'MB Quart',
            'Metra',
            'MOSCONI',
            'MTX',
            'MTX Audio',
            'MUSWAY',
            'Nextbase',
            'NVX',
            'PAC',
            'PAC',
            'Parrot',
            'PEXMAN',
            'PhoenixGold',
            'Pioneer',
            'Polk Audio',
            'Power',
            'Prime',
            'Punch',
            'Pure',
            'Pyle',
            'QVIA',
            'Renegade',
            'RetroSound',
            'Roberts',
            'Rockford Fosgate',
            'Sangean',
            'Scosche',
            'Sony',
            'Sound Marine',
            'SounDigital',
            'Soundmagus',
            'SoundQubed',
            'SoundQuest',
            'Stinger',
            'Stinger',
            'Strands',
            'TARAMPS',
            'Teleskopantenne',
            'TFT',
            'Toma Carparts',
            'uniDAB',
            'VCAN',
            'Video in motion',
            'Xplore',
            'Xzent',
            'Zenec'
        ]
        company_brand = ""   
        heading = response.xpath(".//h1/text()").get()
        
        for brand in brand_names:

            try:
                if brand.upper() in heading.upper():
                    if brand:
                        company_brand = brand
                        break
            except Exception as ex:
                company_brand = ""
        
        file_pdf = []
        product_images = []

        images =  response.xpath('//div[@class="product-image-container"]/div/img/@data-rsbigimg').getall()
        
        for count in range(0,17):

            try:
                product_images.append(images[count].replace(
                    '/','https://www.autohifi.no/',1))

            except Exception as ex: 
                product_images.append("")
        
        for pdf in product_images:

            if pdf.endswith(".pdf"):
                file_pdf.append(pdf)
        
        categories = response.xpath('//div[@class="BreadCrumb"]/a/text()').getall()
        categories.pop()
        categories.pop(0)
        product_categories = []

        for i in range(0,6):

            try:
                product_categories.append(categories[i])
            except:
                product_categories.append("")

        current = response.xpath(
            '//span[@class="RrpLabel rrp-price-api"]//text()'
            ).get()
        
        current = current.replace(",-","")
        
        product_Description = response.xpath('//div[@class="ProductInfo"]/div[position() >= 5]').getall()
        product_Description = "".join(product_Description)


        if product_categories[1].strip() != "Dashcam universalt" and  product_categories[1].strip() != "Dashcam bilspesifikk":
                
            obj = {
                "product Id" : response.css(".product-number-inner .prd-num-label::text").get(),
                "Main Category" : product_categories[0].strip(),
                "Category 1" : product_categories[1].strip(),
                "Category 2" : product_categories[2].strip(),
                "Category 3" : "",
                "Category 4" : "",
                "Category 5" : "",
                "Product Brand" :company_brand,
                "Product Name" : response.xpath(".//h1/text()").get(),
                "Product Information" : response.xpath(".//h2/text()").get(),
                "url": response.url,
                "Main Price" : current,
                "Discount Price" : "",
                "Product Discription" : product_Description,
                "file_pdf" : "".join(file_pdf),
                "source" : "https://www.autohifi.no/",
                }
                
            for i in range(1,18):
                obj[f"picture {i}"] = product_images[i-1]

            yield obj

            self.data.append(obj)
            
            if len(self.data) == 50000:

                df = pd.DataFrame(self.data)
                # Define the Excel file path
                excel_file = f"simple_all_data_autohifi_{self.file_reading}_20_01_2024.xlsx"
                # Save the DataFrame to an Excel file
                df.to_excel(excel_file, index=False)
                
                self.file_reading = self.file_reading + 1
                self.data = []
            

                    
    def close(self, reason):
        df = pd.DataFrame(self.data)
        excel_file = f"simple_all_data_autohifi_{self.file_reading}_20_01_2024.xlsx"
        print(excel_file)
        df.to_excel(excel_file, index=False)
        self.file_reading = self.file_reading + 1
        self.data = []      
   