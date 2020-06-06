import argparse
import logging
import plotly.graph_objects as go
from typeguard import typechecked
from ai4good.models.model import Model, ModelResult
from ai4good.models.model_registry import get_models
from ai4good.models.cm.cm_model import CompartmentalModel
from ai4good.runner.facade import Facade
from ai4good.models.cm.plotter import figure_generator
import os

facade = Facade.simple()


@typechecked
def run_model(_model: str, _profile: str, camp: str, load_from_cache: bool, save_to_cache: bool, save_plots: bool):
    logging.info('Running %s model with %s profile', _model, _profile)
    _mdl: Model = get_models()[_model](facade.ps)
    res_id = _mdl.result_id(camp, _profile)
    if load_from_cache and facade.rs.exists(_mdl.id(), res_id):
        logging.info("Loading from model result cache")
        mr: ModelResult = facade.rs.load(_mdl.id(), res_id)
    else:
        logging.info("Running model for camp %s", camp)
        mr: ModelResult = _mdl.run(camp, _profile)
        if save_to_cache:
            logging.info("Saving model result to cache")
            facade.rs.store(_mdl.id(), res_id, mr)
    if save_plots:
        save_plots(mr, res_id)

def save_plots(mr, res_id):  #TODO: make specific to model
    multiple_categories_to_plot = ['E', 'A', 'I', 'R', 'H', 'C', 'D', 'O', 'Q', 'U']  # categories to plot
    single_category_to_plot = 'C'  # categories to plot in final 3 plots

    # plot graphs
    fig_multi_lines = go.Figure(figure_generator(mr, multiple_categories_to_plot))  # plot with lots of lines
    # fig_age_structure = go.Figure(
    #     age_structure_plot(StandardSol, single_category_to_plot, population, population_frame))  # age structure
    # fig_bar_chart = go.Figure(stacked_bar_plot(StandardSol, single_category_to_plot, population,
    #                                            population_frame))  # bar chart (age structure)
    # fig_uncertainty = go.Figure(uncertainty_plot(StandardSol, single_category_to_plot, population, population_frame,
    #                                              percentiles))  # uncertainty

    #plotString = "_%s_%s" % (categories[single_category_to_plot]['longname'], param_string)
    fig_multi_lines.write_image(os.path.join(os.path.dirname(os.getcwd()), "Figs/Disease_progress_%s.png" % res_id))
    # fig_age_structure.write_image(os.path.join(os.path.dirname(cwd), "Figs/Age_structure" + plotString + ".png"))
    # fig_bar_chart.write_image(
    #     os.path.join(os.path.dirname(cwd), "Figs/Age_structure_(bar_chart)" + plotString + ".png"))
    # fig_uncertainty.write_image(os.path.join(os.path.dirname(cwd), "Figs/Uncertainty" + plotString + ".png"))

#TODO: add save csv
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser(description='AI4Good model runner')
    parser.add_argument('--model', type=str, choices=get_models().keys(), help='Model to run',
                        default=CompartmentalModel.ID)
    parser.add_argument('--profile', type=str, help='Model profile to run, by default first one will be run')
    parser.add_argument('--camp', type=str, help='Camp to run model for', default='Moria')
    parser.add_argument('--do_not_load_from_model_result_cache', dest='load_from_cache', action='store_false',
                        help='Do not load from cache, re-compute everything', default=True)
    parser.add_argument('--do_not_save_to_model_result_cache', dest='save_to_cache', action='store_false',
                        help='Do save results to cache', default=True)
    parser.add_argument('--save_plots', dest='save_plots', action='store_true', help='Save plots', default=False)
    args = parser.parse_args()

    model = args.model
    assert model in facade.ps.get_models()
    if args.profile is None:
        profile = facade.ps.get_profiles(model)[0]
    else:
        profile = args.profile
    run_model(model, profile, args.camp, args.load_from_cache, args.save_to_cache, args.save_plots)

    logging.info('Model Runner finished normally')