import item_filter.amazon_funcs as amazon_funcs
import item_filter.amazon_fba_calculator as amazon_fba_calculator
import keepa.keepa_price_chart_analyzer as keepa_price_chart_analyzer

class AmazonProduct:

    def __init__(self, url, price=0):
        self.ean = amazon_funcs.get_ean(url).strip()
        self.price = price 
        self.soup = -1
        self.fba_costs = -1
        self.avgr30 = -1


    def get_bsr(self):
        if self.soup == -1:
            self.soup = amazon_funcs.get_amazon_json(self.ean)
        return amazon_funcs.get_bsr(self.soup)
    
    def get_rating_count(self):
        if self.soup == -1:
            self.soup = amazon_funcs.get_amazon_json(self.ean)
        return amazon_funcs.get_rating_count(self.soup)
    
    def get_amazon_soup(self):
        return amazon_funcs.get_amazon_json(self.ean)
    
    def get_cost(self, idealo_price):
        if self.fba_costs == -1:
            self.fba_costs = amazon_fba_calculator.get_shipping_fees(self, idealo_price)
        return self.fba_costs
    
    def get_cat_gl(self):
        if self.soup == -1:
            self.soup = amazon_funcs.get_amazon_json(self.ean)
        return amazon_funcs.get_cat(self.soup)
    
    def get_rating(self):
        if self.soup == -1:
            self.soup = amazon_funcs.get_amazon_json(self.ean)
        return amazon_funcs.get_rating(self.soup)
    
    def get_avgr30(self, amz_price):
        if self.avgr30 == -1:
            try:
                self.avgr30 =  keepa_price_chart_analyzer.get_30_day_avg(self.ean, amz_price)
            except:
                self.avgr30 = -1
        return self.avgr30
    

