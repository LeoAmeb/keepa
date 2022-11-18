from django.forms import ValidationError
import keepa
import numpy as np
from core.settings import KEEPA_KEY


def format_json_keepa(json_keepa):
    """Function to parser a json keepa to json with the info that matters."""
    dictionary = dict()
    dictionary["categories"] = json_keepa['categories']
    dictionary["imagesCSV"] = json_keepa['imagesCSV']
    dictionary["manufacturer"] = json_keepa['manufacturer']
    dictionary["title"] = json_keepa['title']
    dictionary["lastUpdate"] = json_keepa['lastUpdate']
    dictionary["lastPriceChange"] = json_keepa['lastPriceChange']
    dictionary["rootCategory"] = json_keepa['rootCategory']
    dictionary["productType"] = json_keepa['productType']
    dictionary["parentAsin"] = json_keepa['parentAsin']
    dictionary["variationCSV"] = json_keepa['variationCSV']
    dictionary["asin"] = json_keepa['asin']
    dictionary["domainId"] = json_keepa['domainId']
    dictionary["type"] = json_keepa['type']
    dictionary["hasReviews"] = json_keepa['hasReviews']
    dictionary["trackingSince"] = json_keepa['trackingSince']
    dictionary["brand"] = json_keepa['brand']
    dictionary["productGroup"] = json_keepa['productGroup']
    dictionary["partNumber"] = json_keepa['partNumber']
    dictionary["model"] = json_keepa['model']
    dictionary["color"] = json_keepa['color']
    dictionary["size"] = json_keepa['size']
    dictionary["edition"] = json_keepa['edition']
    dictionary["format"] = json_keepa['format']
    dictionary["packageHeight"] = json_keepa['packageHeight']
    dictionary["packageLength"] = json_keepa['packageLength']
    dictionary["packageWidth"] = json_keepa['packageWidth']
    dictionary["packageWeight"] = json_keepa['packageWeight']
    dictionary["packageQuantity"] = json_keepa['packageQuantity']
    dictionary["isAdultProduct"] = json_keepa['isAdultProduct']
    dictionary["isEligibleForTradeIn"] = json_keepa['isEligibleForTradeIn']
    dictionary["isEligibleForSuperSaverShipping"] = json_keepa['isEligibleForSuperSaverShipping']
    dictionary["offers"] = json_keepa['offers']
    dictionary["buyBoxSellerIdHistory"] = json_keepa['buyBoxSellerIdHistory']
    dictionary["isRedirectASIN"] = json_keepa['isRedirectASIN']
    dictionary["isSNS"] = json_keepa['isSNS']
    dictionary["author"] = json_keepa['author']
    dictionary["binding"] = json_keepa['binding']
    dictionary["numberOfItems"] = json_keepa['numberOfItems']
    dictionary["numberOfPages"] = json_keepa['numberOfPages']
    dictionary["publicationDate"] = json_keepa['publicationDate']
    dictionary["releaseDate"] = json_keepa['releaseDate']
    dictionary["languages"] = json_keepa['languages']
    dictionary["lastRatingUpdate"] = json_keepa['lastRatingUpdate']
    dictionary["ebayListingIds"] = json_keepa['ebayListingIds']
    dictionary["lastEbayUpdate"] = json_keepa['lastEbayUpdate']
    dictionary["eanList"] = json_keepa['eanList']
    dictionary["upcList"] = json_keepa['upcList']
    dictionary["liveOffersOrder"] = json_keepa['liveOffersOrder']
    dictionary["frequentlyBoughtTogether"] = json_keepa['frequentlyBoughtTogether']
    dictionary["features"] = json_keepa['features']
    dictionary["description"] = json_keepa['description']
    dictionary["promotions"] = json_keepa['promotions']
    dictionary["newPriceIsMAP"] = json_keepa['newPriceIsMAP']
    dictionary["coupon"] = json_keepa['coupon']
    dictionary["availabilityAmazon"] = json_keepa['availabilityAmazon']
    dictionary["listedSince"] = json_keepa['listedSince']
    dictionary["fbaFees"] = json_keepa['fbaFees']
    dictionary["variations"] = json_keepa['variations']
    dictionary["itemHeight"] = json_keepa['itemHeight']
    dictionary["itemLength"] = json_keepa['itemLength']
    dictionary["itemWidth"] = json_keepa['itemWidth']
    dictionary["itemWeight"] = json_keepa['itemWeight']
    dictionary["salesRankReference"] = json_keepa['salesRankReference']
    dictionary["salesRanks"] = json_keepa['salesRanks']
    dictionary["salesRankReferenceHistory"] = json_keepa['salesRankReferenceHistory']
    dictionary["launchpad"] = json_keepa['launchpad']
    dictionary["isB2B"] = json_keepa['isB2B']
    dictionary["stats"] = json_keepa['stats']
    dictionary["offersSuccessful"] = json_keepa['offersSuccessful']
    dictionary["g"] = json_keepa['g']
    dictionary["categoryTree"] = json_keepa['categoryTree']

    dictionary["data"] = {}
    dictionary["data"]["NEW"] = [(i if np.logical_not(np.isnan(i)) else None) for i in json_keepa['data']['NEW']]
    return dictionary

def get_data_keepa(asin):
    try:
        api = keepa.Keepa(KEEPA_KEY)
        product = api.query(asin, progress_bar=False, domain='US')

        # If not data in csv means that no information of that product in that region
        if all(element == None for element in product[0]['csv']):
            return False, ValidationError('asin', 'There is not information of this ASIN in USA')

        return True, format_json_keepa(product[0])
    except Exception as exc:
        return False, exc
