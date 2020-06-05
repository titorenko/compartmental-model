from typeguard import typechecked
from typing import List, Dict, Any
from abc import ABC, abstractmethod


@typechecked
class ParamStore(ABC):

    @abstractmethod
    def get_models(self) -> List[str]:
        """
        Returns list of available models
        """
        pass


    @abstractmethod
    def get_profiles(self, model: str) -> List[str]:
        """
        Returns list of available profiles for given model
        """
        pass

    @abstractmethod
    def get_params(self, model: str, profile: str) -> Dict[str, Any]:
        """
        Given model name and profile return model specific parameter dictionary
        """
        pass


class InMemoryParamStore(ParamStore):

    profiles = {
        'compartmental-model':
            ['baseline', 'better_hygiene', 'custom', 'remove_highrisk', 'remove_symptomatic', 'shielding']
    }

    cm_params = {
        'baseline': {
            # if True, reduces transmission rate by params.better_hygiene
            better_hygiene = dict(value=params.better_hygiene,
                                  timing=[0, 0]),

                             ICU_capacity = dict(value=6 / population),

                                            # 4
                                            # move symptomatic cases off site
                                            remove_symptomatic = dict(rate=10 / population,  # people per day
                                                                      timing=[0, 0]),

                                                                 # 5
                                                                 # partially separate low and high risk
                                                                 # (for now) assumed that if do this, do for entire course of epidemic
                                                                 shielding = dict(used=False),

                                                                             # 6
                                                                             # move uninfected high risk people off site
                                                                             remove_high_risk = dict(
        rate=20 / population,  # people per day
        n_categories_removed=2,  # remove oldest n categories
        timing=[0, 0])
        }
    }


    def get_models(self) -> List[str]:
        return ['compartmental-model']

    def get_profiles(self, model: str) -> List[str]:
        return self.profiles[model]

    def get_params(self, model: str, profile: str) -> Dict[str, Any]:
        pass


    def get_camp_parameters(self):
