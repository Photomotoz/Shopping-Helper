#!/usr/bin/env python
'''
Shopping Helper

Given a list of store inventories and a shopping list, return the minimum number of
store visits required to satisfy the shopping list.

For example, given the following stores & shopping list:

  Shopping List: 10 apples, 4 pears, 3 avocados, 1 peach

  Kroger: 4 apples, 5 pears, 10 peaches
  CostCo: 3 oranges, 4 apples, 4 pears, 3 avocados
  ALDI: 1 avocado, 10 apples
  Meijer: 2 apples

The minimum number of stores to satisfy this shopping list would be 3:
Kroger, CostCo and ALDI.
or
Kroger, CostCo and Meijer.

Shopping lists and store inventories will be passed in JSON format,
an example of which will be attached in the email.  Sample outputs for the
given inputs should also be attached as well.

Usage: shopping_helper.py (shopping_list.json) (inventories.json)
'''

import argparse
import copy
import json

def choose_store(current_shopping_list, master_shopping_list, store_inventories):

    chosen_store = "None"
    highest_value = 0
    results = dict()

    for index, store in enumerate(store_inventories):

        store_has = master_shopping_list.viewkeys() & (store["inventory"])
        current_value = 0

        for available_item in store_has:
            if available_item not in current_shopping_list :
                current_shopping_list[available_item] = 0

            current_value += min(master_shopping_list[available_item] - current_shopping_list[available_item], store["inventory"][available_item])

        if current_value > highest_value:
            highest_value = current_value
            chosen_store = store["name"]
            store_index = index

    results["store"] = chosen_store
    results["store_index"] = store_index

    return results


# to help you get started, we have provided some boiler plate code
def satisfy_shopping_list(shopping_list_json, inventory_json):

    # if shopping list is impossible to satisfy
    shopping_list_satisfiable = True

    shopping_list_dict_orig = dict(shopping_list_json)
    shopping_list_dict = dict()

    temp_inventory = inventory_json["stores"]

    chosen_stores = list()

    while(shopping_list_dict_orig != shopping_list_dict):

        results = choose_store(shopping_list_dict, shopping_list_dict_orig, temp_inventory)

        chosen_store = results["store"];
        store_index = results["store_index"];

        chosen_stores.append(chosen_store)

        store_ref = inventory_json["stores"][store_index]

        store_has = shopping_list_json.viewkeys() & (store_ref["inventory"])

        for available_item in store_has:
            if available_item not in shopping_list_dict:
                shopping_list_dict[available_item] = 0

            shopping_list_dict[available_item] = min(shopping_list_dict_orig[available_item], shopping_list_dict[available_item] + temp_inventory[store_index]["inventory"][available_item])

        del temp_inventory[store_index]

        if(len(temp_inventory) == 1):
            shopping_list_satisfiable = False
            break

    if shopping_list_satisfiable:
        # print out number of stores and corresponding combinations
        num_stores = len(chosen_stores)
        print "The shopping list can be satisfied by visiting {} store(s):".format(num_stores)
        # for each valid store_combination:
        print_store_combination(chosen_stores)
        pass
    else:
        print "No combination of given stores can satisfy this shopping list :("
        pass


def print_store_combination(store_combination):
    '''
    Print store combination in the desired format.

    Args:
        store_combination: store list to print
        type: list of str
    '''
    store_combination_copy = copy.deepcopy(store_combination)
    store_combination_copy.sort()
    print ', '.join(store_combination_copy)


def main():
    args = parse_args()
    with open(args.shopping_list_json_path) as shopping_list_json_file, open(args.inventory_json_path) as inventory_json_file:
        shopping_list_json = json.load(shopping_list_json_file)
        inventory_json = json.load(inventory_json_file)
        satisfy_shopping_list(shopping_list_json, inventory_json)


def parse_args():
    p = argparse.ArgumentParser()

    p.add_argument('shopping_list_json_path')
    p.add_argument('inventory_json_path')

    args = p.parse_args()
    return args

if __name__ == '__main__':
    main()
