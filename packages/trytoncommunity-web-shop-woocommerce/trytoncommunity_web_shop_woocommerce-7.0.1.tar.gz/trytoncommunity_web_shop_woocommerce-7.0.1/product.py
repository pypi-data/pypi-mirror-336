# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.pyson import Eval
from trytond.tools import slugify

from .web import ShopWooCommerceIdMixin


class Category(ShopWooCommerceIdMixin, metaclass=PoolMeta):
    __name__ = 'product.category'

    woocommerce_tax_class = fields.Char("WooCommerce Tax Class",
        states={
            'invisible': ~Eval('accounting', False),
            })

    def get_woocommerce_entity(self):
        values = {
            'name': self.name,
            'slug': slugify(self.name).lower(),
            'parent': 0,
            }
        if self.parent:
            if self.parent.woocommerce_id:
                values['parent'] = self.parent.woocommerce_id
            else:
                return
        return values


class Product(ShopWooCommerceIdMixin, metaclass=PoolMeta):
    __name__ = 'product.product'

    @property
    def woocommerce_tax_class(self):
        if self.account_category:
            parent = self.account_category
            while parent:
                if parent.woocommerce_tax_class:
                    return parent.woocommerce_tax_class
                parent = parent.parent
            return ''

    def woocommerce_disable_data(self, shop):
        return {
            'status': 'private',
            'catalog_visibility': 'hidden',
            }

    def get_woocommerce_entity(self):
        short_description = description = (self.description or '')
        lines = description.splitlines()
        if len(lines) > 1:
            short_description = lines[0]
            description = '\n'.join(lines[1:])

        list_price = self.list_price
        sale_price = self.get_sale_price([self], 0)[self.id]
        if sale_price > list_price:
            list_price = sale_price
        values = {
            'name': self.name,
            'type': 'simple',
            'regular_price': str(list_price),
            'sale_price': str(sale_price),
            'description': description,
            'short_description': short_description,
            'status': 'publish',
        }
        if self.type != 'service':
            values['manage_stock'] = True
            values['stock_quantity'] = self.forecast_quantity
        if self.code:
            values['sku'] = self.code
        categories = []
        for category in self.categories:
            if category.woocommerce_id:
                categories.append({'id': category.woocommerce_id})
        values['categories'] = categories
        tax_class = self.woocommerce_tax_class
        if tax_class is not None:
            values['tax_class'] = tax_class
        return values
