import json


class Rate:
    """
    Class used to determine the correct taxation of a product.
    """
    class __Rate:
        def __init__(self):
            rate_file="../data/rate.json"
            with open(rate_file) as f:
                self.rate_data = json.load(f)
    
    instance = None
    
    def __init__(self):
        if not Rate.instance:
            Rate.instance = Rate.__Rate()

    def get_rate(self, group=None, imported=False):
        """
        Returns the right rate based on the group to which it belongs 
        and whether it is imported or not.

        The correct rate is made up of a fixed part and one dependent
        on the possible import. 
        
        For both the fixed part and the part dependent on the import, 
        the quota is decided on the basis of the group.

        Returns
        -------
    
        the percentage resulting from the sum of the two rates.
        """
        if group in self.instance.rate_data['fix']:
            fix_rate = self.instance.rate_data['fix'][group]
        else:
            fix_rate = self.instance.rate_data['fix']['default']
        
        if imported:
            if group in self.instance.rate_data['imported']:
                imported_rate = self.instance.rate_data['imported'][group]
            else:
                imported_rate = self.instance.rate_data['imported']['default']
        else:
            imported_rate = 0

        total_rate = fix_rate + imported_rate
        
        return total_rate


class Product:
    """
    A class used to represent a Product of Cart.

    Attributes
    ----------
    label : str
        product name
    group : str
        the group to which the product belongs
    price : float
        product price without taxes
    imported : bool
        is true if the product is imported
    count : int
        quantity in the cart

    """

    def __init__(self, label=None, group=None, price=0, imported=False, count=0):
        self.label = label
        self.group = group
        self.price = price
        self.imported = imported
        self.count = count
    
    def get_tax(self):
        """
        Calculates the amount of tax resulting from the rate applied.

        The tax is rounded up to the nearest 0.5.
        """
        rate = Rate()
        rate_calculated = rate.get_rate(group=self.group, imported=self.imported)
        if rate_calculated > 0:
            n_tax =  self.price * rate_calculated
            
            if n_tax % 5 > 0:
                # This step allows me to apply the desired rounding 
                # by working on integer values.
                n_tax = n_tax + (5 - (n_tax % 5))
            
            rounded_tax = n_tax / 100
            return rounded_tax
        else:
            return 0
        
    
    def __str__(self):
        """
        Allows the Product to be printed as formatted in the exercise description.
        """
        return '{count} {imported}{label}: {price:0.2f}'.format(
            count = self.count, 
            imported = 'imported ' if self.imported else '',
            label = self.label,
            price = self.price + self.get_tax()
        )
    
class Cart:
    """
    A class used to represent a Cart.

    Attributes
    ----------
    products : list
        list of products in the cart
    sales_taxes : float
        sum of taxes
    total : float
        sum of taxed prices
    """
    def __init__(self):
        self.products = list()
        self.sales_taxes = 0
        self.total = 0
    
    def add_product(self, product):
        """
        Adds a given product to your cart and updates tax and total summaries.
        """
        self.sales_taxes = self.sales_taxes + product.get_tax() * product.count
        self.total = self.total + (product.price + product.get_tax()) * product.count
        self.products.append(product)
    
    def __str__(self):
        """
        Allows the Cart to be printed as formatted in the exercise description.
        """
        p_str_list = list()
        for p in self.products:
            p_str_list.append(str(p))
        
        p_str_list.append('Sales Taxes: {sales_taxes:0.2f}'.format(sales_taxes = self.sales_taxes))
        p_str_list.append('Total: {total:0.2f}'.format(total = self.total))
        return '\n'.join(p_str_list)
