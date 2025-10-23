import unittest
from .gen_bin_tree import gen_bin_tree

class TestGenBinTree(unittest.TestCase):
    def test_height0(self):
        tree = gen_bin_tree(height=0, root=1)
        expected = {1: []}
        self.assertDictEqual(expected, tree)

    def test_height1(self):
        tree = gen_bin_tree(height=1, root=5,
                            left_node_value=lambda x: x + 1,
                            right_node_value=lambda x: x * x)
        expected = {5: [{6: []}, {25: []}]}
        self.assertDictEqual(expected, tree)

    def test_height2(self):
        tree = gen_bin_tree(height=2, root=10,
                            left_node_value=lambda x: x * x,
                            right_node_value=lambda x: 2 * (x + 4))
        expected = {10: [
            {100: [
                {10000: []},
                {208: []}
            ]},
            {28: [
                {784: []},
                {64: []}
            ]}
        ]}
        self.assertEqual(expected, tree)

    def test_height3(self):
        tree = gen_bin_tree(height=3, root=11,
                            left_node_value=lambda x: x * x,
                            right_node_value=lambda x: x * x + 2)
        expected = {11: [
            {121: [
                {14641: [
                    {214358881: []},
                    {214358883: []}
                ]},
                {14643: [
                    {214417449: []},
                    {214417451: []}
                ]}
            ]},
            {123: [
                {15129: [
                    {228886641: []},
                    {228886643: []}
                ]},
                {15131: [
                    {228947161: []},
                    {228947163: []}
                ]}
            ]}
        ]}
        self.assertDictEqual(expected, tree)
    maxDiff = None
    def test_default(self):
        tree = gen_bin_tree()
        expected = {10: [{31: [{94: [{283: [{850: [{2551: []}, {2549: []}]},
                          {848: [{2545: []}, {2543: []}]}]},
                   {281: [{844: [{2533: []}, {2531: []}]},
                          {842: [{2527: []}, {2525: []}]}]}]},
             {92: [{277: [{832: [{2497: []}, {2495: []}]},
                          {830: [{2491: []}, {2489: []}]}]},
                   {275: [{826: [{2479: []}, {2477: []}]},
                          {824: [{2473: []}, {2471: []}]}]}]}]},
       {29: [{88: [{265: [{796: [{2389: []}, {2387: []}]},
                          {794: [{2383: []}, {2381: []}]}]},
                   {263: [{790: [{2371: []}, {2369: []}]},
                          {788: [{2365: []}, {2363: []}]}]}]},
             {86: [{259: [{778: [{2335: []}, {2333: []}]},
                          {776: [{2329: []}, {2327: []}]}]},
                   {257: [{772: [{2317: []}, {2315: []}]},
                          {770: [{2311: []}, {2309: []}]}]}]}]}]}
        self.assertDictEqual(expected, tree)

if __name__ == "__main__":
    unittest.main()
