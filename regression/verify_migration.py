import numpy.testing as npt
from base.configs.baseline import camp, population_frame, population, control_dict
from ai4good.models.cm.initialise_parameters import Parameters
from ai4good.params.param_store import SimpleParamStore
from base.functions import GenerateInfectionMatrix

if __name__ == '__main__':

    p = Parameters(SimpleParamStore(), 'Moria')

    assert population_frame.equals(p.population_frame)
    assert camp == p.camp
    assert population == p.population

    assert control_dict == p.control_dict

    infection_matrix, beta_list, largest_eigenvalue = GenerateInfectionMatrix(population_frame, camp, control_dict)
    npt.assert_almost_equal(infection_matrix, p.infection_matrix, decimal=8)
    npt.assert_almost_equal(beta_list, p.beta_list, decimal=8)
    npt.assert_almost_equal(largest_eigenvalue, p.largest_eigenvalue, decimal=8)

    print("All checks OK")