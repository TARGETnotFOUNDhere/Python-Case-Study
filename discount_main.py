from product_class import load_products_from_csv
from discount_engine import DiscountEngine
import matplotlib.pyplot as plt


def plot_savings_bar_chart(result: dict):
    items = result["line_items"]
    names = [item["name"] for item in items]
    savings = [item["total_line_savings"] for item in items]

    if not names:
        print("No items to plot.")
        return

    plt.bar(names, savings, color="green")
    plt.xlabel("Products")
    plt.ylabel("Savings (₹)")
    plt.title("Savings per Product")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def main():
    print("=== Welcome to the Shopping Discount Calculator ===")

    products = load_products_from_csv("products.csv")
    engine = DiscountEngine(products, "coupons.json", tax_rate=0.18)

    print("\nAvailable Products:")
    for p in products.values():
        tag = " (BOGO)" if p.bogo_eligible else ""
        print(f"- {p.product_id}: {p.name} | ₹{p.price:.2f} | {p.category}{tag}")

    cart = {}
    print("\nStart adding items to the cart.")
    while True:
        pid = input("Enter product ID (or X to finish): ").strip()
        if pid.upper() == "X":
            break
        if pid not in products:
            print("Invalid product ID. Try again.")
            continue

        try:
            qty = int(input("Enter quantity: "))
            if qty <= 0:
                print("Quantity must be positive.")
                continue
        except ValueError:
            print("Please enter a valid integer quantity.")
            continue

        cart[pid] = cart.get(pid, 0) + qty
        print(f"Added {qty} x {products[pid].name} to cart.")

    if not cart:
        print("Cart is empty. Exiting.")
        return

    coupon_code = input("Enter coupon code (or press Enter to skip): ").strip()

    result = engine.calculate_total(cart, coupon_code)

    print("\n========== FINAL BILL ==========")
    for item in result["line_items"]:
        print(
            f"{item['name']} (x{item['quantity']})\n"
            f"  Raw total:    ₹{item['raw_total']:.2f}\n"
            f"  Final total:  ₹{item['final_line_total']:.2f}\n"
            f"  Savings:      ₹{item['total_line_savings']:.2f}\n"
        )

    print("--------------------------------")
    print(f"Subtotal (before discounts): ₹{result['subtotal_before_discounts']:.2f}")
    print(f"After item + BOGO discounts: ₹{result['subtotal_after_item_and_bogo']:.2f}")

    if result["coupon_applied"]:
        print(
            f"Coupon {result['coupon_code']} applied: "
            f"saved ₹{result['coupon_savings']:.2f}"
        )
    else:
        if coupon_code:
            print(f"Coupon not applied: {result['coupon_message']}")

    print(f"Subtotal (after coupon):     ₹{result['subtotal_after_coupon']:.2f}")
    print(f"Tax:                          ₹{result['tax_amount']:.2f}")
    print(f"GRAND TOTAL TO PAY:          ₹{result['grand_total']:.2f}")
    print(f"TOTAL SAVINGS:               ₹{result['total_savings']:.2f}")
    print("================================")

    show_chart = input("\nShow savings comparison bar chart? (y/n): ").strip().lower()
    if show_chart == "y":
        plot_savings_bar_chart(result)
        print("Chart closed. Thank you for shopping!")


if __name__ == "__main__":
    main()
