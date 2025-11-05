from request_handler import RequestHandler
import asyncio
from parser import DomParser
import json


async def main(event, context):
    handler = RequestHandler()
    handler.proxy.enable("unblocker", "US")
    handler.proxy.switch()

    request_url = f"https://www.amazon.com/dp/{event['asin']}?th=1"
    response = await handler.requestGet(request_url)

    pq = DomParser(response.body)
    arr = dict()
    arr["title"] = pq("title").text()
    arr["bought_info"] = pq('span[id="social-proofing-faceout-title-tk_bought"]').text()

    # Check for variations.
    variation_mapping = dict()
    options = pq(
        'div[id="twister-plus-inline-twister"] ul[class*="dimension-values-list"]'
    )
    if options:
        for each_option in options:
            variant_type = each_option.attr("data-a-button-group")
            if variant_type:
                variant_type = json.loads(variant_type)["name"]
            else:
                continue
            variation_mapping[variant_type] = list()
            variations = each_option["li"]
            for each_variation in variations:
                variation_asin = each_variation.attr("data-asin")
                variation_name = each_variation.text()
                if not variation_name:
                    for each_img in each_variation["img"]:
                        variation_name = each_img.attr("alt")
                variation_mapping[variant_type].append(
                    [{"asin": variation_asin, "variation_name": variation_name}]
                )

    arr["variations"] = variation_mapping

    # Check for pricing info
    buy_box = pq('div[class*="twister-plus-buying-options-price-data"]')
    price_mapping = dict()
    if buy_box:
        pricing = json.loads(buy_box.text())
        for _, pricing_option in pricing.items():
            for each_pricing_option in pricing_option:
                option_type = each_pricing_option["buyingOptionType"]
                if option_type:
                    price_mapping[option_type] = list()

                price_mapping[option_type].append(
                    {
                        "display_price": each_pricing_option["displayPrice"],
                        "display_price_formatted": each_pricing_option["priceAmount"],
                    }
                )

    arr["price"] = price_mapping

    arr["about"] = [x.text() for x in pq('h3[class="product-facts-title"] + ul li')]

    return arr


def entrypoint(event, context):
    return asyncio.run(main(event, context))
