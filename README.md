# Shopping Discount Calculator
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A **professional-grade Object-Oriented Python application** for retail billing that handles **flat discounts, percentage discounts, BOGO offers, coupon validation, and tax computation** with **matplotlib visualization**. Developed as a **B.Tech CSE Semester I case study** at **ITM Skills University**.

## 🎯 Project Overview

Retail customers often face confusion during festival sales with multiple discount types. This **Shopping Discount Calculator** provides:

- **Transparency**: Clear breakdown of original price vs final payable amount
- **Speed**: Instant calculation for faster checkout
- **Accuracy**: Handles complex discount stacking (item → BOGO → coupon → tax)
- **Visualization**: Bar chart showing savings per product line

**Key Features Demonstrated:**
- Object-Oriented Programming (OOP) with `Product` and `DiscountEngine` classes
- File I/O with CSV (products) and JSON (coupons)
- Decorators for price validation
- Lambda functions for tax computation
- List comprehensions for efficient data processing
- Matplotlib for data visualization

## 📋 Requirements & Discount Types

### Supported Discounts:
  1.	Item-level: Category-based percentage (Electronics: 10%, Clothing: 5%)
	2.	BOGO: Buy 1 Get 1 Free (every 2nd item free for eligible products)
	3.	Coupons: Percentage/Flat discounts with validation (min cart value, expiry)
	4.	Tax: 18% GST applied after all discounts


### Data Files:
- `products.csv`: Product catalog (ID, name, price, category, BOGO eligibility)
- `coupons.json`: Coupon rules (code, type, value, validity dates)

## 🏗️ System Architecture
discount_main.py  ← User Input/Output + Visualization ↓ DiscountEngine    ← Business Logic (discounts + tax) ↓ Product      ← Data Model (loaded from CSV) ↓ products.csv + coupons.json

## 🚀 Quick Start

### Prerequisites
Python 3.8+ matplotlib (pip install matplotlib)


### Setup & Run
Clone/download the repo
cd shopping_discount_calculator
Install dependencies
pip install matplotlib
Run the billing system
python3 discount_main.py


### Sample Usage
Available Products:
	•	P101: Smartphone | ₹30000.00 | electronics
	•	P102: Headphones | ₹2000.00 | electronics (BOGO)
	•	P103: Casual Shirt | ₹1500.00 | clothing (BOGO)
Enter product ID: P101    # 1 Smartphone Enter quantity: 1 Enter product ID: P102    # 3 Headphones Enter quantity: 3 Enter product ID: X       # Finish cart
Enter coupon code: FEST10


**Sample Bill Output:**
========== FINAL BILL ========== 
Smartphone (x1) Raw total:    ₹30000.00 Final total:  ₹27000.00 Savings:      ₹3000.00
Headphones (x3) Raw total:    ₹6000.00 Final total:  ₹3600.00 Savings:      ₹2400.00
GRAND TOTAL TO PAY: ₹34090.20 TOTAL SAVINGS:      ₹10110.00


## 💻 Code Structure

### 1. `product_class.py`
class Product: def init(self, product_id, name, price, category, bogo_eligible=False): # Product data model + line_total(quantity) method
def load_products_from_csv(csv_path): # CSV → {product_id: Product} dictionary


### 2. `discount_engine.py` (Core Business Logic)
class DiscountEngine: def init(self, products, coupons_path, tax_rate=0.18): self.apply_tax = lambda amt: amt * tax_rate  # Lambda requirement self.add_tax = lambda amt: amt + self.apply_tax(amt)

def calculate_total(self, cart, coupon_code):
    # 1. Item discounts (category-based)
    # 2. BOGO processing  
    # 3. Coupon validation + application
    # 4. Tax computation
    # Returns detailed breakdown dictionary


**Discount Flow:**
Raw Subtotal → Item Discounts → BOGO → Coupon → Tax → GRAND TOTAL


### 3. `discount_main.py`
def main():
#### 1. Load products + coupons 
#### 2. Interactive cart building 
#### 3. Calculate + print itemized bill 
#### 4. Optional savings visualization


## 📊 Sample Calculation Walkthrough

**Cart:** 1×Smartphone(P101), 3×Headphones(P102) | Coupon: FEST10

| Step | Description | Amount |
|------|-------------|---------|
| 1 | Raw subtotal | ₹39,000 |
| 2 | Item discounts (10% electronics) | ₹35,400 |
| 3 | BOGO (Headphones: 3→pay for 2) | ₹32,100 |
| 4 | FEST10 (10% coupon) | ₹28,890 |
| 5 | 18% Tax | ₹5,200 |
| **6** | **Grand Total** | **₹34,090** |
| **Savings** | **vs original** | **₹10,110** |

## 🎨 Visualization

**Savings Comparison Bar Chart:**

Shows which products contributed most to customer savings.

## 🛠️ Technical Highlights

### OOP Principles Demonstrated:
- **Encapsulation**: `Product` holds product data + methods
- **Single Responsibility**: `DiscountEngine` handles only discount logic
- **Dependency Injection**: Engine receives products externally

### Advanced Python Features:
Decorator
def calculate_total(self, cart): …
Lambda for tax
self.apply_tax = lambda amount: amount * 0.18
List comprehension for chart data
names = [item“name” for item in line_items]


## 📁 File Structure
shopping_discount_calculator/ 
├── discount_main.py      - User interface + visualization 
├── discount_engine.py    - Core discount/tax engine 
├── product_class.py      - Product model + CSV loader 
├── products.csv          - Product catalog 
├── coupons.json          - Coupon rules 
└── README.md             - You’re reading it!


## 🎓 Learning Outcomes (B.Tech CSE Case Study)

✅ **OOP**: Classes, methods, classmethods  
✅ **File I/O**: CSV parsing, JSON processing  
✅ **Decorators**: Cross-cutting validation logic  
✅ **Lambda**: Compact tax computation  
✅ **List Comprehensions**: Efficient data transformation  
✅ **Visualization**: Matplotlib bar charts  
✅ **Error Handling**: Input validation, negative price protection  
✅ **Modularity**: Separation of concerns across files  

## 🔮 Future Enhancements

- [ ] Combo offers (buy shirt+jeans together)
- [ ] Tiered discounts (buy more, save more)
- [ ] Inventory management
- [ ] GUI with Tkinter
- [ ] Database backend (SQLite)
- [ ] Export bills to PDF

## 📝 Academic Credits

**Course**: B.Tech CSE Python Case Study, Semester I  
**University**: ITM Skills University  
**Author**: Lakshya Purohit  
**Date**: December 2025  

## 📄 License
MIT License - see [LICENSE](LICENSE) file.

---

**⭐ Star this repo if it helped your learning!**  
**🐛 Found issues?** Open a PR or Issue.

---

<div align="center">
  <img src="https://img.shields.io/badge/built%20with-%E2%9D%A4%EF%B8%8F-brightgreen.svg" alt="Built with Love">
</div>


