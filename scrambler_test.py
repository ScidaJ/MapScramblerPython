import unittest
from pathlib import Path
import scrambler

MAP_LIST = "./test/map_list_test.txt"
FILTER = "./test/map_list_filter_test.txt"


class TestIngestFilter(unittest.TestCase):

    def test_file(self):
        my_argv = [MAP_LIST, "--Filter", FILTER]
        expected = "dMap 1,smap_3,pmap 1"
        args = scrambler.prase_args(my_argv)
        result = scrambler.ingest_filter(args)
        self.assertEqual(result, expected)

    def test_arguments(self):
        my_argv = [MAP_LIST, "--Filter", "dMap 1,vmap1,pmap 1"]
        args = scrambler.prase_args(my_argv)
        expected = "dMap 1,vmap1,pmap 1"
        result = scrambler.ingest_filter(args)
        self.assertEqual(result, expected)


class TestApplyFilter(unittest.TestCase):

    def test_no_filter(self):
        my_argv = [MAP_LIST]
        map_list = [
            "dmap_1,dMap 1",
            "smap_2,sMap 2",
            "sMap_3,smap_3",
            "vmap1,vmap1",
            "pmap_1,pmap 1",
            "pmap_2,pmap 2",
        ]
        expected = [
            "dmap_1,dMap 1",
            "smap_2,sMap 2",
            "sMap_3,smap_3",
            "vmap1,vmap1",
            "pmap_1,pmap 1",
            "pmap_2,pmap 2",
        ]
        args = scrambler.prase_args(my_argv)
        filter = scrambler.ingest_filter(args)
        scrambler.apply_filter(filter, map_list)
        self.assertEqual(map_list, expected)

    def test_filter(self):
        my_argv = [MAP_LIST, "--Filter", "dMap 1,vmap1,pmap 1"]
        map_list = [
            "dmap_1,dMap 1",
            "smap_2,sMap 2",
            "sMap_3,smap_3",
            "vmap1,vmap1",
            "pmap_1,pmap 1",
            "pmap_2,pmap 2",
        ]
        expected = [
            "smap_2,sMap 2",
            "sMap_3,smap_3",
            "pmap_2,pmap 2",
        ]
        args = scrambler.prase_args(my_argv)
        filter = scrambler.ingest_filter(args)
        scrambler.apply_filter(filter, map_list)
        self.assertEqual(map_list, expected)

    def test_filter_map_not_in_list(self):
        my_argv = [MAP_LIST, "--Filter", "dMap 1,Downturn,pmap 1"]
        map_list = [
            "dmap_1,dMap 1",
            "smap_2,sMap 2",
            "sMap_3,smap_3",
            "vmap1,vmap1",
            "pmap_1,pmap 1",
            "pmap_2,pmap 2",
        ]
        expected = [
            "smap_2,sMap 2",
            "sMap_3,smap_3",
            "vmap1,vmap1",
            "pmap_2,pmap 2",
        ]
        args = scrambler.prase_args(my_argv)
        filter = scrambler.ingest_filter(args)
        scrambler.apply_filter(filter, map_list)
        self.assertEqual(map_list, expected)


class TestRandomMapListBuilder(unittest.TestCase):

    def test_no_filter(self):
        expected = {
            "dMap 1": "dmap_1",
            "sMap 2": "smap_2",
            "smap_3": "sMap_3",
            "vmap1": "vmap1",
            "pmap 1": "pmap_1",
            "pmap 2": "pmap_2",
        }
        map_dict = {}
        random_map_dict = {}
        map_list = Path(MAP_LIST).read_text().split("\n")
        scrambler.apply_filter("", map_list)
        scrambler.random_map_list_builder(map_list, map_dict, random_map_dict)
        self.assertDictEqual(map_dict, expected)

    def test_filters(self):
        my_argv = [MAP_LIST, "--Filter", "dMap 1,vmap1,pmap 1"]
        map_list = [
            "dmap_1,dMap 1",
            "smap_2,sMap 2",
            "sMap_3,smap_3",
            "vmap1,vmap1",
            "pmap_1,pmap 1",
            "pmap_2,pmap 2",
        ]
        expected = {
            "sMap 2": "smap_2",
            "smap_3": "sMap_3",
            "pmap 2": "pmap_2",
        }
        map_dict = {}
        random_map_dict = {}
        args = scrambler.prase_args(my_argv)
        filter = scrambler.ingest_filter(args)
        scrambler.apply_filter(filter, map_list)
        scrambler.random_map_list_builder(map_list, map_dict, random_map_dict)
        self.assertDictEqual(map_dict, expected)
