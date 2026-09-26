import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

REPO=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('trl_nmf_diagnostics',REPO/'pipelines/nmf500/experiments.py')
diagnostics=importlib.util.module_from_spec(spec)
spec.loader.exec_module(diagnostics)


class DiagnosticsTests(unittest.TestCase):
    def test_withdrawal_does_not_mutate_input_or_relax_gate(self):
        r={'axes':{'TRL':[{'gates':[{'key':'qualification','status':'met','observation_ids':['A','B'],'measurements':[{'observation_id':'A'}]}]}],
                   'CRL':[{'gates':[{'key':'sales','status':'met','observation_ids':['C']}]}]}}
        observations=[{'observation_id':i} for i in ['A','B','C']]
        rr,obs=diagnostics.ablate_review(r,observations,['A'])
        self.assertEqual(r['axes']['TRL'][0]['gates'][0]['status'],'met')
        g=rr['axes']['TRL'][0]['gates'][0]
        self.assertEqual(g['key'],'qualification')
        self.assertEqual(g['status'],'unknown')
        self.assertEqual(g['measurements'],[])
        self.assertEqual([o['observation_id'] for o in obs],['B','C'])
        self.assertEqual(rr['axes']['CRL'],r['axes']['CRL'])

    def test_actual_evidence_and_mapping_diagnostics(self):
        with tempfile.TemporaryDirectory(prefix='trl-experiment-test-') as tmp:
            diagnostics.run(REPO/'data',REPO/'results/nmf500/theme_context_top3.csv',Path(tmp))
            result=json.loads((Path(tmp)/'SUMMARY.json').read_text())
            self.assertEqual(result['scenario_count'],724)
            self.assertEqual(result['upgrades'],0)
            self.assertTrue(result['cross_axis_ablation_independence_passed'])


if __name__=='__main__':
    unittest.main()
