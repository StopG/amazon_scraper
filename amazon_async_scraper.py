from playwright.async_api import async_playwright
import pandas as pd
import asyncio
import random
urls = []
semaphore = asyncio.Semaphore(5)
product_names = [] 
prices = [] 
ratings = []
total_reviews =[]
stocks =[]
product_urls =[]
product_infos = []
image_urls =[]


item = "phones"


completed = 0
async def scrape_page(browser, url,total,retries=1):
    global completed
    async with semaphore:
        result = None
        for attempt in range(retries+1):
            product_info_q = []
            product_info_a = []
            product = {}
            page = await browser.new_page()
            await page.route("**/*", lambda route: (route.abort()
            if route.request.resource_type in ("image", "media", "font", "stylesheet")
            else route.continue_()))
            try:
                await asyncio.sleep(random.uniform(0.5, 1.5))
                await page.goto(url,wait_until="domcontentloaded", timeout=45000)
                await page.wait_for_selector("div#titleSection h1#title span#productTitle")
                # locator 
                title_locator = page.locator("div#titleSection h1#title span#productTitle")
                price_locator =  page.locator("#corePrice_feature_div .a-offscreen")
                rating_locator =  page.locator("#acrPopover")
                total_reviews_locator =  page.locator("div#averageCustomerReviews span.a-declarative a#acrCustomerReviewLink span#acrCustomerReviewText")
                stock_locator = page.locator("div#availability span")
                image_url_locator = page.locator("ul.a-unordered-list.a-nostyle.a-horizontal.list.maintain-height.desktop-media-mainView img")
                product_info_q_locator = page.locator("div.a-section.a-spacing-small.a-spacing-top-small tbody tr td.a-span9 span")
                product_info_a_locator = page.locator("div.a-section.a-spacing-small.a-spacing-top-small tbody tr td.a-span3 span")
            
                # title
                if await title_locator.count() == 1:
                    product_name = await title_locator.inner_text()
                elif await title_locator.count() > 1:
                    element = title_locator.first
                    product_name = await element.inner_text()
                else:
                    product_name= None

                # price
                if await price_locator.count() == 1:
                    price = await price_locator.inner_text()
                elif await price_locator.count() > 1:
                    element = price_locator.first
                    price = await element.inner_text()
                else:
                    price = None     
                
                # rating
                if await rating_locator.count() == 1:
                    rating = await rating_locator.inner_text()
                elif await rating_locator.count() > 1:
                    element =  rating_locator.first
                    rating = await element.inner_text()
                else:
                    rating = None

                # reviews
                if await total_reviews_locator.count() == 1:
                    total_review = await total_reviews_locator.inner_text()
                elif await total_reviews_locator.count() > 1:
                    element =  total_reviews_locator.first
                    total_review = await element.inner_text()
                else:
                    total_review = None


                # stock
                if await stock_locator.count() == 1:
                    stock = await stock_locator.inner_text()
                elif await stock_locator.count() > 1:
                    element =  stock_locator.first
                    stock = await element.inner_text() 
                else:
                    stock = None

                # url
                product_url = url

                # product info
                elements = await product_info_q_locator.all()
                if elements:
                    for element in elements:
                        product_info_q.append(await element.inner_text())
                else:
                    product_info_q.append(None)

                elements = await product_info_a_locator.all()
                if elements:
                    for element in elements:
                        product_info_a.append(await element.inner_text())
                else:
                    product_info_a.append(None)
                if len(product_info_q) != len(product_info_a):
                    print(f"Mismatched product_info lengths on {url}: {len(product_info_q)} questions vs {len(product_info_a)} answers")

                for a,q in zip(product_info_q,product_info_a):
                    product[q] = a
                product_info = product

                # image url
                if await image_url_locator.count()>0:
                    image_url = await image_url_locator.nth(0).get_attribute("src") 
                else:
                    image_url = None
                return product_name,price,rating,total_review,stock,product_url,product_info,image_url
            except Exception as e:
                if attempt == retries:
                    print(f"Failed on {url} after {attempt+1} attempts: {type(e).__name__}: {e}")
                else:
                    print(f"Retrying {url} (attempt {attempt+1} failed: {type(e).__name__})")
                    await asyncio.sleep(1.5 * (attempt + 1))
            finally:
                completed += 1
                print(f"done scraping : [{completed}/{total}]")
                await page.close()
async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = await browser.new_page()
        await page.goto("https://www.amazon.in/")
        search_box = page.locator("input#twotabsearchtextbox")
        await search_box.click()
        await search_box.fill(item)
        await search_box.press("Enter")
        await page.wait_for_selector("a.a-link-normal.s-line-clamp-2.puis-line-clamp-3-for-col-4-and-8.s-link-style.a-text-normal")
        next_locator = page.locator(".s-pagination-next")
        page_num = 1
        while True:
            new_urls = await page.locator("a.a-link-normal.s-line-clamp-2.puis-line-clamp-3-for-col-4-and-8.s-link-style.a-text-normal").evaluate_all("(elements) => elements.map(el => el.href)")
            urls.extend(new_urls)
            print(f"[Page {page_num}] +{len(new_urls)} urls | total so far: {len(urls)}")
            page_num += 1
            class_attr = await next_locator.get_attribute("class") or ""
            if "s-pagination-disabled" in class_attr:
                print(f"Done paginating — {page_num - 1} pages, {len(urls)} urls total")
                break
            await next_locator.click()
            await page.wait_for_selector("a.a-link-normal.s-line-clamp-2.puis-line-clamp-3-for-col-4-and-8.s-link-style.a-text-normal")
        seen = set()
        target_urls = []
        for u in urls:
            if u not in seen:
                seen.add(u)
                target_urls.append(u)
        tasks = [scrape_page(browser, url,len(target_urls)) for url in target_urls]
        result = await asyncio.gather(*tasks, return_exceptions=True)
        for url, r in zip(target_urls , result):
            if r is None:
                print(f"Dropped (returned None): {url}")
                continue
            if isinstance(r, Exception): 
                print(f"Dropped (uncaught exception) [{url}] -> {type(r).__name__}: {r}")
                continue
            product_name,price,rating,total_review,stock,product_url,product_info,image_url = r
            product_names.append(product_name)
            prices.append(price)
            ratings.append(rating)
            total_reviews.append(total_review)
            stocks.append(stock)
            product_urls.append(product_url)
            product_infos.append(product_info)
            image_urls.append(image_url)

        data = {
            'product_name' : product_names,
            'price':prices,
            'rating':ratings,
            'total_reviews':total_reviews,
            'stock':stocks,
            'product_info':product_infos,
            'image_url':image_urls,
            'product_url':product_urls,
        }
        df = pd.DataFrame(data)
        df.to_excel(item+"_amazon.xlsx", index=False)
        print("total sources scraped :",page_num-1)
        print("total links scraped :",len(target_urls))
        print("excel created")
        await page.close()


if __name__ == "__main__": 
    asyncio.run(main())