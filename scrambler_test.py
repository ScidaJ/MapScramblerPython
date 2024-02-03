import unittest
from pathlib import Path
import scrambler

MAP_LIST = "./test/map_list_test.txt"
MAP_LIST_SIZE = 6
FILTER = "./test/map_list_filter_test.txt"


class TestScramblerFunctions(unittest.TestCase):

    def test_ingest_filter_file(self):
        my_argv = [MAP_LIST, "--Filter", FILTER]
        args = scrambler.prase_args(my_argv)
        expected = "dMap 1,smap_3,pmap 1"
        result = scrambler.ingest_filter(args)
        self.assertEqual(result, expected)

    def test_ingest_filter_arguments(self):
        my_argv = [MAP_LIST, "--Filter", "dMap 1,vmap1,pmap 1"]
        args = scrambler.prase_args(my_argv)
        expected = "dMap 1,vmap1,pmap 1"
        result = scrambler.ingest_filter(args)
        self.assertEqual(result, expected)

    def test_random_map_list_builder_no_filter(self):
        my_argv = [MAP_LIST]
        args = scrambler.prase_args(my_argv)
        map_file = Path(MAP_LIST).read_text().split("\n")
        maps = {}
        random_map_list = {}
        maps_expected = {
            "dMap 1": "dmap_1",
            "sMap 2": "smap_2",
            "smap_3": "sMap_3",
            "vmap1": "vmap1",
            "pmap 1": "pmap_1",
            "pmap 2": "pmap_2",
        }
        scrambler.random_map_list_builder(
            "", map_file, maps, random_map_list, MAP_LIST_SIZE
        )
        self.assertDictEqual(maps, maps_expected)
        self.assertEqual(len(maps), max(list(random_map_list.keys())) + 1)

    def test_random_map_list_builder_filters(self):
        my_argv = [MAP_LIST, "--Filter", "dMap 1,vmap1,pmap 1"]
        args = scrambler.prase_args(my_argv)
        filter = ["dMap 1", "vmap1", "pmap 1"]
        map_file = Path(MAP_LIST).read_text().split("\n")
        maps = {}
        random_map_list = {}
        maps_expected = {"sMap 2": "smap_2", "smap_3": "sMap_3", "pmap 2": "pmap_2"}
        scrambler.random_map_list_builder(filter, map_file, maps, random_map_list, 3)
        self.assertEqual(len(maps), max(list(random_map_list.keys())) + 1)
        self.assertDictEqual(maps, maps_expected)
