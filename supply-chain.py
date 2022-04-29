import requests


def get_sellers_data(buyer_domain: str = 'openx.com') -> list:
    """
    Returns sellers data dictionary for given domain.
        default domain: openx.com
    """
    url = "https://" + buyer_domain + '/sellers.json'

    try:
        r = requests.get(url)
        r.raise_for_status()
        json_data = r.json()

    except requests.exceptions.RequestException:
        raise ValueError("Cannot get sellers data from given domain", buyer_domain)

    if 'sellers' not in json_data.keys():
        raise ValueError("Cannot get sellers data from given domain", buyer_domain)
    else:
        sellers_data_list = json_data['sellers']

    for seller_data in sellers_data_list:
        if 'domain' not in seller_data.keys() or 'seller_type' not in seller_data.keys():
            raise ValueError("Cannot get sellers data from given domain", buyer_domain)

    return sellers_data_list


def is_seller_indirect(seller_domain: str, all_sellers_data: list) -> bool:

    """Returns True if seller with given domain is indirect otherwise returns False"""

    seller_data = [seller for seller in all_sellers_data if seller['domain'] == seller_domain]

    if len(seller_data) == 0:
        raise ValueError("Provided seller domain does not exist. Try other domain.")

    seller_types = [seller['seller_type'] for seller in seller_data]

    if len(seller_types) == 0:
        raise Exception('seller_type key does not exist for given domain')

    if "INTERMEDIARY" in seller_types or "BOTH" in seller_types:
        return True
    else:
        return False


def indirect_sellers_domains_list(buyer_domain: str) -> list:
    """Returns list of indirect sellers domains for buyer domain"""

    sellers_data = get_sellers_data(buyer_domain)
    sellers_domains = [seller['domain'] for seller in sellers_data]
    unique_sellers_domains = list(dict.fromkeys(sellers_domains))
    return [seller_domain for seller_domain in unique_sellers_domains if
            is_seller_indirect(seller_domain, sellers_data)]


def number_of_indirect_sellers(buyer_domain: str) -> int:
    return len(indirect_sellers_domains_list(buyer_domain))


def max_supply_chain_depth_list(buyer_domain: str = 'openx.com', depth: int = 0, global_list: list = []):
    """
    Returns list of supply chain depths for a given domain.
    default:
        buyer_domain = openx.com
    """

    try:
        if number_of_indirect_sellers(buyer_domain) != 0:
            depth += 1
            for seller in indirect_sellers_domains_list(buyer_domain):
                if seller == buyer_domain:
                    continue
                else:
                    max_supply_chain_depth_list(seller, depth, global_list)
        else:
            depth += 1
            global_list.append(depth)
            depth = 0
            return global_list
    except ValueError as err:
        global_list.append(
            'Buyer with domain {} does not publish his sellers. Depth count stopper at {}'.format(err.args[1], depth))


def max_supply_chain_depth(domain: str = 'openx.com'):
    """Return maximum supply chain depth for the given domain"""
    depths_list = max_supply_chain_depth_list(domain)
    depths_list = list(filter(lambda e: type(e) is int, depths_list))
    return max(depths_list)

