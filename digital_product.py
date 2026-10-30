from product import Product


class DigitalProduct(Product):
    """A product that is delivered as a download and has a download size."""

    def __init__(self, product_id, name, price, stock, download_size):
        # Reuse Product's constructor for the common attributes
        super().__init__(product_id, name, price, stock)

        if download_size < 0:
            raise ValueError("Download size cannot be negative.")
        self.__download_size = float(download_size)

    def get_download_size(self):
        return self.__download_size

    def display_information(self):
        """Print the common product information, then the download size."""
        super().display_information()
        print(f"    Download Size: {self.__download_size:.2f} MB")
