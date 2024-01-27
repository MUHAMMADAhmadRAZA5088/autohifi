import scrapy
import pandas as pd
import re

class BrandAccessoriesSpider(scrapy.Spider):
    
    name = "autohifi_car_only"
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
                    "4 Connect",
                    "5 Connect",
                    "4 Power",
                    "4POWER",
                    "4 Connect",
                    "ACV",
                    "ACX",
                    "AH",
                    "AI-SONIC",
                    "Alpine",
                    "Antenne (DAB)",
                    "Antenne adapter",
                    "Antennesplitter",
                    "Asuka",
                    "Audio/Video interface",
                    "Audison",
                    "Aura",
                    "BLACKVUE",
                    "Blam",
                    "Blaupunkt",
                    "BOSS",
                    "Brax",
                    "Cadence",
                    "Caliber",
                    "CarAudio Systems",
                    "CDS",
                    "Cerwin Vega",
                    "Clarion",
                    "Comfort Modul",
                    "ConnectED",
                    "Connection",
                    "Connects2",
                    "Continental",
                    "Crunch",
                    "DAB integrering",
                    "DAB-antenne",
                    "DASHCAM",
                    "DD Audio",
                    "DEFA",
                    "Dension",
                    "ESX",
                    "Fiamm",
                    "Firefly",
                    "Focal",
                    "G4Audiio",
                    "Garmin",
                    "Ground Zero",
                    "Halo",
                    "Hardstone",
                    "Harman/Kardon",
                    "Helix",
                    "HELIX Q",
                    "Hertz",
                    "Hertz Marine",
                    "Hifonics",
                    "In2digi",
                    "JBL",
                    "Jensen",
                    "JL Audio",
                    "JVC",
                    "Kenwood",
                    "Kicker",
                    "Kram Telecom",
                    "Kufatec",
                    "Lukas",
                    "MAGNAT",
                    "Match",
                    "MB Quart",
                    "Metra",
                    "MTX Audio",
                    "MUSWAY",
                    "MOSCONI",
                    "Nextbase",
                    "NVX",
                    "PAC",
                    "Parrot",
                    "PhoenixGold",
                    "Pioneer",
                    "Polk Audio",
                    "Power",
                    "Prime",
                    "Punch",
                    "Pure",
                    "Pyle",
                    "QVIA",
                    "Renegade",
                    "Roberts",
                    "Rockford Fosgate",
                    "Sangean",
                    "Scosche",
                    "Sony",
                    "Sound Marine",
                    "Soundmagus",
                    "SoundQuest",
                    "Stinger",
                    "Strands",
                    "TARAMPS",
                    "Teleskopantenne",
                    "TFT",
                    "AutoDAB",
                    "Toma Carparts",
                    "uniDAB",
                    "VCAN",
                    "Video in motion",
                    "Xplore",
                    "Gladen",
                    "4Connect",
                    "SounDigital",
                    "Blam",
                    "SoundQubed",
                    "Diamond Audio",
                    "BLAM",
                    "DIRECTOR",
                    "FOUR Connect",
                    "GLADEN",
                    "PEXMAN",
                    "Boss",
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
       
        product_images = []

        images = response.xpath(
            ".//div[@id='PanelProductInfo']//div[@id='1']//img/@src"
            ).getall()
        
        for count in range(0,17):

            try:
                product_images.append(images[count].replace(
                    '/','https://www.autohifi.no/',1))

            except Exception as ex: 
                product_images.append("")
        
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
        
        product_Description = response.xpath('//div[@class="container section-content"][1]/div').get()
        
        web_data = ''.join(response.xpath('//div[@class="container section-content"][1]/div//text()').getall())
        final_brand = []
        final_model = []
        final_years = []
        
        if web_data: 
            
            df = pd.read_csv('C:\\car_scraper\\car_models.csv')

            brand_csv = []
            for brand in set(df['Brand']):
                if brand in web_data:
                    brand_csv.append(brand.strip())

            model_csv = []
            for model in set(df['Model']):
                if model in web_data:
                    model_csv.append(model)
            
            model_csv  = [item for item in model_csv if len(item.strip()) > 0]
            years = re.findall(r'\b(198[5-9]|199\d|200\d|202[0-3])\b', "".join(web_data))
            years = set(years)
            final_brand = []
            final_model = []
            final_years = []

            last_brand = []
            last_model = []
            last_years = []
            
            if  brand_csv and model_csv:
                for brands in brand_csv: 
                    brand_df = df[df["Brand"] == brands]

                    for model_df in set(brand_df["Model"]):
                        
                        for models in set(model_csv):
                            if model_df == models:
                                final_model.append(model_df)
                                final_brand.append(brands)

            if brand_csv and final_model == []:
                final_brand.extend(brand_csv)


            if years and  final_model:   
                for count in range(0,len(final_brand)):
                    inner_year = [] 
                    csv_year = df[(df['Brand'] == final_brand[count]) & (df['Model'] == final_model[count] )]
                
                    for  year in years:
                        for df_year in csv_year['Year']:
                            if str(df_year) == year:
                                inner_year.append(year)
                    

                    inner_year  = [item for item in inner_year if len(item.strip()) > 0]
                    try:
                        for year in inner_year:
                            last_brand.append(final_brand[count])
                            last_model.append(final_model[count])
                            last_years.append(year)
                    except :
                        last_brand.append(final_brand[count])
                        last_model.append(final_model[count]) 
                        last_years.append('')

            if last_brand and last_model:
                final_brand.clear()
                final_model.clear()
                final_years.clear()
                final_brand.extend(last_brand)
                final_model.extend(last_model)
                final_years.extend(last_years)
        if product_categories[1].strip() != "Dashcam universalt" and  product_categories[1].strip() != "Dashcam bilspesifikk":
            if final_brand and final_model and final_years:
                for i in range(len(final_brand)):
                    obj = {
                    "product Id" : response.css(
                                ".product-number-inner .prd-num-label::text"
                                    ).get(),
                    "Car Brand" : final_brand[i],
                    "Car Model" : final_model[i],
                    "Car Years" : final_years[i],
                                            }  
                    yield obj

                    self.data.append(obj)
                    # import pdb; pdb.set_trace()
                    if len(self.data) == 50000:

                        df = pd.DataFrame(self.data)
                        # Define the Excel file path
                        excel_file = f"only_carBrand_autohifi_{self.file_reading}_21_10.xlsx"
                        # Save the DataFrame to an Excel file
                        df.to_excel(excel_file, index=False)
                        
                        self.file_reading = self.file_reading + 1
                        self.data = []


    def close(self, reason):
        df = pd.DataFrame(self.data)
        excel_file = f"only_carBrand_autohifi_{self.file_reading}_15_11.xlsx"
        print(excel_file)
        df.to_excel(excel_file, index=False)
        self.file_reading = self.file_reading + 1
        self.data = []