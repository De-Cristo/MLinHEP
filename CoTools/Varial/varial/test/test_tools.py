#!/usr/bin/env python

import varial.tools
import unittest
import shutil
import os


class ResultCreator(varial.tools.Tool):
    def run(self):
        self.result = varial.wrp.Wrapper(name=self.name)


class ResultSearcher(varial.tools.Tool):
    def __init__(self, name, input_path):
        super(ResultSearcher, self).__init__(name)
        self.input_path = input_path

    def reuse(self):
        with self.io.block_of_files:
            self.result = self.io.get('result')

    def run(self):
        self.result = self.lookup_result(self.input_path)


class _Prntr(varial.tools.Tool):
    def run(self):
        varial.analysis.print_tool_tree()


class TestTools(unittest.TestCase):
    def __init__(self, methodName='runTest'):
        super(TestTools, self).__init__(methodName)
        self.base_name = 'VanillaChain'

    def setUp(self):
        super(TestTools, self).setUp()
        varial.monitor.current_error_level = 2

    def tearDown(self):
        super(TestTools, self).tearDown()
        varial.monitor.current_error_level = 0
        if os.path.exists(self.base_name):
            shutil.rmtree(self.base_name)

    def _setup_chains(self, chain_class):
        searchers = [
            ResultSearcher(
                'ResultSearcher0',
                '../../../Creators/InnerCreators/ResultCreator'
            ),
            ResultSearcher(
                'ResultSearcher1',
                '../.././../Creators/./InnerCreators/./ResultCreator'
            ),
            ResultSearcher(
                'ResultSearcher3',
                'BaseChain/Creators/ResultCreator'
            ),
            ResultSearcher(
                'ResultSearcher4',
                '/BaseChain/Creators/ResultCreator'
            ),
            ResultSearcher(
                'ResultSearcher5',
                self.base_name + '/BaseChain/Creators/ResultCreator'
            ),
        ]
        chain = varial.tools.ToolChain('BaseChain', [
            chain_class('Creators', [
                chain_class('InnerCreators', [
                    ResultCreator(),
                ]),
                ResultCreator(),
            ]),
            chain_class('Searchers', [
                chain_class('InnerSearchers', searchers[:2]),
            ] + searchers[2:]),
        ])
        return searchers, chain

    def test_analysis_reset(self):
        # this will reset analysis
        varial.analysis.reset()
        with varial.tools.ToolChainVanilla(self.base_name):
            varial.analysis.fs_aliases.append('TESTVALUE')
        self.assertListEqual(varial.analysis.fs_aliases, [])

    def test_lookup_result(self):
        searchers, chain = self._setup_chains(varial.tools.ToolChain)
        chain = varial.tools.ToolChainVanilla(self.base_name, [chain])
        varial.tools.Runner(chain)
        for srchr in searchers:
            self.assertIsNotNone(
                srchr.result,
                'Result not found for input_path: %s' % srchr.input_path
            )

    def test_lookup_result_parallel(self):
        searchers, chain = self._setup_chains(varial.tools.ToolChainParallel)
        chain = varial.tools.ToolChainVanilla(self.base_name, [chain])
        varial.tools.Runner(chain)
        for srchr in searchers:
            self.assertIsNotNone(
                srchr.result,
                'Result not found for input_path: %s' % srchr.input_path
            )


suite = unittest.TestLoader().loadTestsFromTestCase(TestTools)
if __name__ == '__main__':
    unittest.main()
