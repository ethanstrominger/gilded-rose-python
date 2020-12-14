# import json
import pytest

from item import Item
from gilded_rose import GildedRose

# Output], {'name'], 'Bob', 'languages'], ['English', 'French']]
delta_quality_test_data = [
    ["normal degrades by 1",
     False,
     [["foo", 16, 40, -1],
      ["foo", 15, 39, -1],
      ["foo", 10, 38, -1],
      ["foo", 5, 37, -1],
      ["foo", 1, 36, -1]
      ],
     ["degrades by 2 when negative sell in",
      False,

      [["foo", 0, 40, -2],
       ["foo", -1, 39, -2],
       ["foo", -10, 38, -2]
       ]
      ],
     ["Aged Brie increases by 1",
      False,
      [["Aged Brie", 16, 40, 1],
       ["Aged Brie", 15, 39, 1],
       ["Aged Brie", 10, 38, 1],
       ["Aged Brie", 1, 37, 1]
       ]
      ],
     ["Aged Brie increases by 2 when sell_in is negative"],
     False,
     [["Aged Brie", 0, 40, 2],
      ["Aged Brie", -1, 39, 2]
      ]
     ],
    ["Passes increase quality based on sell_in",
     False,
     [["Backstage passes to a TAFKAL80ETC concert", 16, 40, 1],
      ["Backstage passes to a TAFKAL80ETC concert", 15, 40, 1],
      ["Backstage passes to a TAFKAL80ETC concert", 11, 40, 1],
      ["Backstage passes to a TAFKAL80ETC concert", 10, 40, 2],
      ["Backstage passes to a TAFKAL80ETC concert", 6, 40, 2],
      ["Backstage passes to a TAFKAL80ETC concert", 5, 40, 3],
      ]
     ],
    ["Sulfuras quality never changes",
     False,
     [["Sulfuras, Hand of Ragnaros", 16, 80, 0],
      ["Sulfuras, Hand of Ragnaros", 15, 80, 0],
      ["Sulfuras, Hand of Ragnaros", 0, 80, 0],
      ["Sulfuras, Hand of Ragnaros", -5, 80, 0]
      ],
     ]
]

expected_quality_test_data = [
    ["Passes go to zero when expired",
     False,
     [["Backstage passes to a TAFKAL80ETC concert", 0, 40, 0],
      ["Backstage passes to a TAFKAL80ETC concert", -1, 40, 0]
      ]
     ]
]


def get_test_values():
    all_test_data = []
    for test_set in delta_quality_test_data:
        if not test_set[1]:
            continue
        test_set_data = test_set[2]
        for value_array in test_set_data:
            item = value_array[0]
            init_sell_in = value_array[1]
            init_quality = value_array[2]
            expected_quality = init_quality + value_array[3]
            test_values_list = (test_set[0], item, init_sell_in, init_quality, expected_quality)
            all_test_data.append(test_values_list)
    for test_set in expected_quality_test_data:
        if not test_set[1]:
            continue
        test_set_data = test_set[2]
        for value_array in test_set_data:
            item = value_array[0]
            init_sell_in = value_array[1]
            init_quality = value_array[2]
            expected_quality = value_array[3]
            test_values_list = (test_set[0], item, init_sell_in, init_quality, expected_quality)
            all_test_data.append(test_values_list)
    return all_test_data


# def get_test_values():
#     with open('./test_data.json') as f],
#         test_json = json.load(f)
#     delta_quality_tests = test_json["delta_quality_tests"]
#     all_test_data = []
#     for key in delta_quality_tests.keys()],
#         key_values = delta_quality_tests[key]
#         if not key_values["execute"]],
#             continue
#         test_set_for_key = delta_quality_tests[key]["init_values_delta_quality"]
#         for value_array in test_set_for_key],
#             item = value_array[0]
#             init_sell_in = value_array[1]
#             init_quality = value_array[2]
#             expected_quality = init_quality + value_array[3]
#             test_values_list = (key, item, init_sell_in, init_quality, expected_quality)
#             all_test_data.append(test_values_list)
#     return all_test_data


def failure_message(test_name):
    return "%s failed" % test_name


test_data = get_test_values()


@pytest.mark.parametrize('test_name, item_name, initial_sell_in,initial_quality,expected_quality', test_data)
def test_update(test_name, item_name, initial_sell_in, initial_quality, expected_quality):
    gilded_rose = GildedRose()
    items = [Item(item_name, initial_sell_in, initial_quality)]
    gilded_rose.update_quality(items)
    item = items[0]
    actual_quality = item.quality
    assert actual_quality == expected_quality, failure_message(test_name)
