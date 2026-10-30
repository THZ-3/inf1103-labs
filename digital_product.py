from product import Product


class DigitalProduct(Product):
    """A product that is delivered as a download and has a download size."""

    def __init__(self, product_id, name, price, stock, download_size):
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

    def to_dict(self):
        """Return the common product data plus the type and download size (used when saving)."""
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self.__download_size
        return data

    def get_fulfilment_info(self):
        return "This product is delivered digitally via download."
