import csv


class Product:
    def __init__(self, product_id, name, price, category,
                 bogo_eligible=False, combo_group=None):
        self.product_id = product_id
        self.name = name
        self.price = float(price)
        self.category = category
        self.bogo_eligible = bool(bogo_eligible)
        self.combo_group = combo_group

    def line_total(self, quantity: int) -> float:
        """Price * quantity without any discounts."""
        return self.price * quantity

    @classmethod
    def from_csv_row(cls, row: dict):
        """Create a Product from one CSV row."""
        return cls(
            product_id=row["product_id"],
            name=row["name"],
            price=row["price"],
            category=row.get("category", "general"),
            bogo_eligible=row.get("bogo_eligible", "False").lower() == "true",
            combo_group=row.get("combo_group") or None,
        )


def load_products_from_csv(csv_path: str) -> dict:
    """Read products.csv and return {product_id: Product}."""
    products = {}
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            product = Product.from_csv_row(row)
            products[product.product_id] = product
    return products
