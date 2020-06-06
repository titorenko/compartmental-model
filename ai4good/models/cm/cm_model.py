from typeguard import typechecked
from ai4good.models.model import Model, ModelResult
from ai4good.params.param_store import ParamStore
from ai4good.models.cm.initialise_parameters import Parameters
from ai4good.models.cm.functions import Simulator
from math import ceil

t_sim = 200  # simulation runtime
numberOfIterations = 1000  # suggest 800-1000 for real thing


@typechecked
class CompartmentalModel(Model):
    RID_PATTERN = "Camp=%s_%shygieneT=%s_remInfRate=%s_remInfT=%s_Shield=%s_RemHrRate=%s_RemHrTime=%s_ICU=%s_NumIts=%s"
    ID = 'compartmental-model'

    def __init__(self, ps: ParamStore):
        Model.__init__(self, ps)

    def id(self) -> str:
        return self.ID

    def result_id(self, camp: str, profile: str) -> str:
        return self._result_id(Parameters(self.ps, camp, profile))

    def _result_id(self, p: Parameters) -> str:
        return self.RID_PATTERN % (
            p.camp,
            p.control_dict['better_hygiene']['value'],
            p.control_dict['better_hygiene']['timing'],
            ceil(p.population * p.control_dict['remove_symptomatic']['rate']),
            p.control_dict['remove_symptomatic']['timing'],
            p.control_dict['shielding']['used'],
            ceil(p.population * p.control_dict['remove_high_risk']['rate']),
            p.control_dict['remove_high_risk']['timing'],
            ceil(p.population * p.control_dict['ICU_capacity']['value']),
            numberOfIterations
        )

    def run(self, camp: str, profile: str) -> ModelResult:
        p = Parameters(self.ps, camp, profile)
        sim = Simulator(p)
        sols_raw, standard_sol, percentiles, config_dict = sim.simulate_over_parameter_range_parallel(
            numberOfIterations, t_sim)

        return ModelResult(self._result_id(p), {
            'sols_raw': sols_raw,
            'standard_sol': standard_sol,
            'percentiles': percentiles,
            'config_dict': config_dict,
            'params': p
        })
