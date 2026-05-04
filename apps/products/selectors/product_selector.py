from products.models.product import Product

class ProductSelector:
    
    @staticmethod
    def list_products():
        return Product.objects.prefetch_related("images", "variants")

    @staticmethod
    def get_product(pk):
        return Product.objects.prefetch_related(
            "images",
            "varinants"
        ).get(pk=pk)
        

