from playwright.sync_api import sync_playwright
import time

PRODUCTS = [
    {
        'url': 'https://pk.sapphireonline.pk/collections/rtw-shirts/products/2PRDYS25V24S-XSM-999.html',
        'size': 'LRG'
    },
    {
        'url': 'https://pk.sapphireonline.pk/collections/rtw-flared-pants/products/2PRDYS25V24T-XSM-999.html',
        'size': 'LRG'
    },
    {
        'url': ' https://pk.sapphireonline.pk/collections/rtw-shirts/products/2PBDF25V31ST_999.html?source=plp&catid=matching-separates',
        'size': 'LRG'
    },
   
]

CONFIG = {
    'email': 'tooba.saeed954@gmail.com',
    'first_name': 'Sara',
    'last_name': 'Saeed',
    'address1': 'K Mustafa Town',
    'address2': 'Lahore',
    'province': 'Punjab',
    'city': 'Lahore',
    'postal_code': '54000',
    'phone': '03001234567',
    'payment_method': 'cod'
}

def run_bot():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        start = time.time()
        try:
            for product in PRODUCTS:
                print(f"🛒 Visiting product page: {product['url']}...")
                page.goto(product['url'], timeout=60000)

                print(f"🔘 Selecting size {product['size']}...")
                page.wait_for_selector(f"input[data-attr-value='{product['size']}']", timeout=15000)
                page.click(f"input[data-attr-value='{product['size']}']")

                print("🛍️ Adding to cart...")
                page.click("button.add-to-cart")
                page.wait_for_timeout(2000)

            print("➡️ Going to checkout...")
            page.goto("https://pk.sapphireonline.pk/checkout")

            print("📧 Filling email...")
            page.wait_for_selector("input#email-guest", timeout=15000)
            page.fill("input#email-guest", CONFIG['email'])

            print("➡️ Proceeding to shipping form...")
            page.click("button.submit-customer")
            page.wait_for_timeout(3000)

            print("📦 Filling shipping form...")
            page.fill("input#shippingFirstNamedefault", CONFIG['first_name'])
            page.fill("input#shippingLastNamedefault", CONFIG['last_name'])
            page.fill("input#shippingAddressOnedefault", CONFIG['address1'])
            page.fill("input#shippingAddressTwodefault", CONFIG['address2'])

            page.select_option("select#shippingCountrydefault", value="PK")
            page.select_option("select#shippingStatedefault", label=CONFIG['province'])

            page.click("#shippingCitydefault_chosen")
            page.fill("#shippingCitydefault_chosen .chosen-search-input", CONFIG['city'])
            page.keyboard.press("Enter")

            page.fill("input.shippingZipCode", CONFIG['postal_code'])
            page.fill("input#shippingPhoneNumberdefault", CONFIG['phone'])

            print("🚚 Proceeding to delivery options...")
            page.locator("div.btn-proceed-delivery", has_text="Proceed to Delivery Options").first.click()
            page.wait_for_timeout(3000)

            print("💸 Proceeding to payment...")
            page.locator("button.submit-shipping", has_text="Proceed to payment").click()
            page.wait_for_timeout(2000)

            print("💰 Selecting payment method...")
            page.click("a.cod-tab")
            page.wait_for_timeout(1000)

            print("🧾 Placing the order...")
            page.click("button.submit-payment")

            print("✅ Order placed! Waiting for confirmation page...")
            page.wait_for_selector("text=Thank you for your order", timeout=30000)
            print("🎉 Order confirmation page loaded!")

            # Optionally: pause to manually review order confirmation
            print("🔍 Please review your order confirmation. Press ENTER to close the browser.")
            input()

        except Exception as e:
            print(f"❌ Bot encountered an error: {e}")
        finally:
            print(f"⏱️ Total time taken: {time.time() - start:.2f} seconds")
            browser.close()

if __name__ == "__main__":
    run_bot()
