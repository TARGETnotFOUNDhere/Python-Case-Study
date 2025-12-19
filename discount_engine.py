import json
from functools import wraps
from datetime import datetime
from typing import Dict, Tuple

from product_class import Product


def validate_price(fn):
    """Decorator to ensure calculated grand_total is not negative."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        result = fn(*args, **kwargs)
        total = result.get("grand_total", 0)
        if total < 0:
            raise ValueError("Calculated total cannot be negative")
        return result
    return wrapper


class DiscountEngine:
    def __init__(self, products: Dict[str, Product], coupons_path: str, tax_rate: float = 0.18):
        self.products = products
        self.coupons = self._load_coupons(coupons_path)
        self.tax_rate = tax_rate

        # Lambda functions for tax
        self.apply_tax = lambda amount: amount * self.tax_rate
        self.add_tax = lambda amount: amount + self.apply_tax(amount)

    def _load_coupons(self, path: str) -> Dict[str, dict]:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        return {c["code"].upper(): c for c in data.get("coupons", [])}

    def validate_coupon(self, code: str, cart_total: float) -> Tuple[bool, dict, str]:
        if not code:
            return False, {}, "No coupon entered."

        coupon = self.coupons.get(code.upper())
        if not coupon:
            return False, {}, "Invalid coupon code."

        now = datetime.now().date()
        start = datetime.fromisoformat(coupon["start_date"]).date()
        end = datetime.fromisoformat(coupon["end_date"]).date()
        if not (start <= now <= end):
            return False, {}, "Coupon is expired or not yet active."

        if cart_total < coupon.get("min_cart_value", 0):
            return False, {}, f"Cart value must be at least {coupon['min_cart_value']} for this coupon."

        return True, coupon, "Coupon applied successfully."

    def _apply_item_discounts(self, product: Product, quantity: int):
        base_price = product.price
        cat = product.category.lower()

        if cat == "electronics":
            percent = 10
        elif cat == "clothing":
            percent = 5
        else:
            percent = 0

        discounted_price = base_price * (1 - percent / 100)
        line_total = discounted_price * quantity
        savings = (base_price - discounted_price) * quantity
        return line_total, savings

    def _apply_bogo(self, product: Product, quantity: int, discounted_line_total: float):
        if not product.bogo_eligible or quantity < 2:
            return discounted_line_total, 0.0

        unit_price = discounted_line_total / quantity
        free_items = quantity // 2
        chargeable_qty = quantity - free_items

        new_line_total = chargeable_qty * unit_price
        bogo_savings = free_items * unit_price
        return new_line_total, bogo_savings

    def _apply_coupon_discount(self, subtotal_after_item_and_bogo: float, coupon: dict):
        if not coupon:
            return subtotal_after_item_and_bogo, 0.0

        ctype = coupon.get("type", "percent")
        value = coupon.get("value", 0)

        if ctype == "percent":
            discount_amount = subtotal_after_item_and_bogo * (value / 100)
        else:
            discount_amount = value

        discount_amount = min(discount_amount, subtotal_after_item_and_bogo)
        new_subtotal = subtotal_after_item_and_bogo - discount_amount
        return new_subtotal, discount_amount

    @validate_price
    def calculate_total(self, cart: Dict[str, int], coupon_code: str = "") -> dict:
        line_items = []
        subtotal_before_discounts = 0.0
        subtotal_after_item_and_bogo = 0.0
        per_line_savings = []

        for product_id, qty in cart.items():
            product = self.products[product_id]

            raw_line_total = product.line_total(qty)
            subtotal_before_discounts += raw_line_total

            item_disc_line_total, item_savings = self._apply_item_discounts(product, qty)
            bogo_line_total, bogo_savings = self._apply_bogo(
                product, qty, item_disc_line_total
            )

            subtotal_after_item_and_bogo += bogo_line_total
            total_line_savings = item_savings + bogo_savings
            per_line_savings.append(total_line_savings)

            line_items.append(
                {
                    "product_id": product.product_id,
                    "name": product.name,
                    "quantity": qty,
                    "raw_total": raw_line_total,
                    "final_line_total": bogo_line_total,
                    "item_savings": item_savings,
                    "bogo_savings": bogo_savings,
                    "total_line_savings": total_line_savings,
                }
            )

        valid, coupon, coupon_msg = self.validate_coupon(coupon_code, subtotal_after_item_and_bogo)
        subtotal_after_coupon, coupon_savings = self._apply_coupon_discount(
            subtotal_after_item_and_bogo, coupon if valid else {}
        )

        tax_amount = self.apply_tax(subtotal_after_coupon)
        grand_total = self.add_tax(subtotal_after_coupon)

        total_savings = subtotal_before_discounts - subtotal_after_coupon

        return {
            "line_items": line_items,
            "subtotal_before_discounts": subtotal_before_discounts,
            "subtotal_after_item_and_bogo": subtotal_after_item_and_bogo,
            "subtotal_after_coupon": subtotal_after_coupon,
            "coupon_applied": valid,
            "coupon_code": coupon_code.upper() if valid else "",
            "coupon_message": coupon_msg,
            "coupon_savings": coupon_savings,
            "tax_amount": tax_amount,
            "grand_total": grand_total,
            "total_savings": total_savings,
            "per_line_savings": per_line_savings,
        }
