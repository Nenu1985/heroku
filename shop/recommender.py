import redis
from django.conf import settings

from .models import Product

# connect to redis
r = redis.StrictRedis(host=settings.REDIS_BACKEND['HOST'],
                      port=settings.REDIS_BACKEND['PORT'],
                      db=settings.REDIS_BACKEND['DB'])


class Recommender(object):
    """
    class will allow us to store product
    purchases and retrieve product suggestions for a given product or
    products.
    """

    def get_product_key(self, id):
        """
            builds the Redis key for the sorted set where related
            products are stored
        """
        return 'product:{}:purchased_with'.format(id)

    def products_bought(self, products):
        """
        Builds the Redis key for the sorted set where related
        products are stored
        1. We get the product IDs for the given Product objects.
        2. We iterate over the product IDs. For each ID, we iterate over
        the product IDs and skip the same product so that we get the
        products that are bought together with each product.
        3. We get the Redis product key for each product bought using
        the get_product_id() method. For a product with an ID of 33, this
        method returns the key product:33:purchased_with.
        4. We increment the score of each product ID contained in the
        sorted set by 1. The score represents the times another
        product has been bought together with the given product
        :param products: list of Product objects
        :return: None
        """
        product_ids = [p.id for p in products]
        for product_id in product_ids:
            for with_id in product_ids:
                # get the other products bought with each product
                if product_id != with_id:
                    # increment score for product purchased together
                    r.zincrby(self.get_product_key(product_id),
                              with_id,
                              amount=1)

    def suggest_products_for(self, products, max_results=6):
        """
        retrieve the products
        that are bought together for a list of given products
        :param products: list of Product objects to get recommendations for
        :return:

        """
        product_ids = [p.id for p in products]
        # If only one product is given, we retrieve the ID of the
        # products that were bought together with the given product,
        # ordered by the total number of times that they were bought
        # together. To do so, we use Redis' ZRANGE command. We limit
        # the number of results to the number specified in the
        # max_results attribute (6 by default)
        if len(products) == 1:
            # only 1 product
            suggestions = r.zrange(
                self.get_product_key(product_ids[0]),
                0, -1, desc=True)[:max_results]
        # If more than one product is given, we generate a temporary
        # Redis key built with the IDs of the products
        else:
            # generate a temporary key
            flat_ids = ''.join([str(id) for id in product_ids])
            tmp_key = 'tmp_{}'.format(flat_ids)
            # multiple products, combine scores of all products
            # store the resulting sorted set in a temporary key
            # The ZUNIONSTORE
            # command performs a union of the sorted sets with the given
            # keys, and stores the aggregated sum of scores of the
            # elements in a new Redis key
            keys = [self.get_product_key(id) for id in product_ids]
            r.zunionstore(tmp_key, keys)
            # remove ids for the products the recommendation is for
            r.zrem(tmp_key, *product_ids)
            # get the product ids by their score, descendant sort
            suggestions = r.zrange(tmp_key, 0, -1,
                                   desc=True)[:max_results]
            # remove the temporary key
            r.delete(tmp_key)
        suggested_products_ids = [int(id) for id in suggestions]
        # get suggested products and sort by order of appearance
        suggested_products = list(Product.objects.filter(id__in=suggested_products_ids))
        suggested_products.sort(key=lambda x: suggested_products_ids.index(x.id))
        return suggested_products

    def clear_purchases(self):
        for id in Product.objects.values_list('id', flat=True):
            r.delete(self.get_product_key(id))
