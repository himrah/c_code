# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector
class MySQLPipeline(object):
    def open_spider(self, spider):
        self.conn = mysql.connector.connect('localhost', 'root', '', 
                                    'holiday', charset="utf8",
                                    use_unicode=True)
        self.cursor = self.conn.cursor()
        
    def close_spider(self, spider):
        self.conn.close()
        
    def process_item(self, item, spider):    
        # import pdb;pdb.set_trace()
        try:
            query = "INSERT INTO holiday_us(Super_category, Category, Retailer, Brand, Media_type, Market, Sale_start_date, Sale_end_date, Page_position, Promotion_category, Promotion, Additional_offers_1, Additional_offers_2, Model_name, Model_number, SKU, MPN, Product_description, Promotion_title, Ecoupon_code, Regular_price, Sales_price, Unit_price, NOR_price, Dollar_off, Percentage_off, Coupon_amount, Rebate_amount, Gift_card_amount, Limit1, Adtype, MT_value_index,Extraction_date, html_content) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            # import pdb;pdb.set_trace()
            # values= (str(item.get("Super_category")[0]), str(item.get("Category")[0]), str(item.get("Retailer")[0]), str(item.get("Brand")[0]), str(item.get("Media_type")[0]), str(item.get("Market")[0]), str(item['Sale_start_date'][0]), str(item['Sale_end_date'][0]), str(item['Page_position'][0]),str(item['Promotion_category'][0]),str(item['Promotion'][0]), str(item['Additional_offers_1'][0]), str(item.get("Additional_offers_2")[0]),str(item.get("Model_name")[0]),str(item.get("Model_number")[0]),str(item.get("SKU")[0]),str(item.get("MPN")[0]),str(item.get("Product_description")[0]), str(item.get("Promotion_title")[0]), str(item.get("Ecoupon_code")[0]),str(item.get("Regular_price")[0][0]),str(item.get("Sales_price")[0]),str(item.get("Unit_price")[0]),str(item.get("NOR_price")[0]),str(item.get("Dollar_off")[0]),str(item.get("Percentage_off")[0]),str(item.get("Coupon_amount")[0]),str(item.get("Rebate_amount")[0]),str(item.get("Gift_card_amount")[0]),str(item.get("Limit1")[0]),str(item.get("Adtype")[0]),str(item.get("MT_value_index")[0]),'',str(item.get("Product_url_link")))
            # values= (str(item.get("Super_category")), str(item.get("Category")), str(item.get("Retailer")), str(item.get("Brand")), str(item.get("Media_type")), str(item.get("Market")), str(item['Sale_start_date']), str(item['Sale_end_date']), str(item['Page_position']),str(item['Promotion_category']),str(item['Promotion']), str(item['Additional_offers_1']), str(item.get("Additional_offers_2")),str(item.get("Model_name")),str(item.get("Model_number")),str(item.get("SKU")),str(item.get("MPN")),str(item.get("Product_description")), str(item.get("Promotion_title")), str(item.get("Ecoupon_code")),str(item.get("Regular_price")),str(item.get("Sales_price")),str(item.get("Unit_price")),str(item.get("NOR_price")),str(item.get("Dollar_off")),str(item.get("Percentage_off")),str(item.get("Coupon_amount")),str(item.get("Rebate_amount")),str(item.get("Gift_card_amount")),str(item.get("Limit1")),str(item.get("Adtype")),str(item.get("MT_value_index")),str(item.get("Extraction_date")),str(item.get("Product_url_link")))
            values= (str(item['Super_category']), str(item['Category']), str(item['Retailer']), str(item['Brand']), str(item['Media_type']), str(item['Market']), str(item['Sale_start_date']), str(item['Sale_end_date']), str(item['Page_position']),str(item['Promotion_category']),str(item['Promotion']), str(item['Additional_offers_1']), str(item['Additional_offers_2']),str(item['Model_name']),str(item['Model_number']),str(item['SKU']),str(item['MPN']),str(item['Product_description']), str(item['Promotion_title']), str(item['Ecoupon_code']),str(item['Regular_price']),str(item['Sales_price']),str(item['Unit_price']),str(item['NOR_price']),str(item['Dollar_off']),str(item['Percentage_off']),str(item['Coupon_amount']),str(item['Rebate_amount']),str(item['Gift_card_amount']),str(item['Limit1']),str(item['Adtype']),str(item['MT_value_index']),item['Extraction_date'],str(item['Product_url_link']),str(item["html_content"]))
            
            # self.cursor.execute("""INSERT INTO example_book_store (book_name, price)  
                        # VALUES (%s, %s)""", 
                       # (item['book_name'].encode('utf-8'), 
                        # item['price'].encode('utf-8')))            
            self.cursor.execute(query, values)
            self.conn.commit()            
        except :
            print("error...")
            # print "Error %d: %s" % (e.args[0], e.args[1])
        return item