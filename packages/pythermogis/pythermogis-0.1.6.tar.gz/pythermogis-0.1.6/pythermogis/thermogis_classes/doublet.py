import numpy as np
import xarray as xr
from jpype import JClass

from pythermogis.physics.temperature_grid_calculation import calculate_temperature_from_gradient
from pythermogis.statistics.calculate_pvalues import generate_thickness_permeability_transmissivity_for_pvalue
from pythermogis.thermogis_classes.java_start import start_jvm


def calculate_performance_of_single_location(hydrocarbons: float, depth: float, thickness: float, porosity: float, ntg: float, temperature: float, transmissivity: float, transmissivity_with_ntg: float, doublet=None,
                                             input_params: dict = None):
    # Returns the values from a doublet simulation in order of;
    # power, heat_pump_power,  capex, opex, utc, npv, hprod, cop, cophp, pres, flow_rate, welld

    if np.isnan(thickness):
        return np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan

    if hydrocarbons == 0.0:
        return 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0

    set_doublet_parameters(doublet, transmissivity_with_ntg, depth, porosity, ntg, temperature, input_params["use_stimulation"], input_params["stimKhMax"], input_params["surface_temperature"],
                           input_params["return_temperature"], input_params["use_heat_pump"], input_params["max_cooling_temperature_range"], input_params["hp_minimum_injection_temperature"])

    doublet.calculateDoubletPerformance(-9999.0, thickness, transmissivity)

    if doublet.getUtcPeurctkWh() == -9999.0:  # If calculation was not successful, return all 0.0
        return 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0

    # calculate net-present-value using the utc-cutoffs
    if depth > input_params["utc_cutoff_depth"]:
        utc_cut = input_params["utc_cutoff_deep"]
    else:
        utc_cut = input_params["utc_cutoff_shallow"]

    hprod = doublet.economicalData.getDiscountedHeatProducedP()
    npv = 1e-6 * (utc_cut - doublet.getUtcPeurctkWh()) * 3.6 * hprod * (1 - doublet.economicalData.getTaxRate())

    # get values from doublet
    output_values = {"power": doublet.doubletCalc1DData.getHpP(),
                     "heat_pump_power": doublet.doubletCalc1DData.getHpPHeatPump(),
                     "capex": doublet.economicalData.getSumcapex(),
                     "opex": doublet.economicalData.getOpexFirstProdYear(),
                     "utc": doublet.getUtcPeurctkWh(),
                     "npv": npv,
                     "hprod": hprod,
                     "cop": doublet.doubletCalc1DData.getCop(),
                     "cophp": doublet.doubletCalc1DData.getCopHpP(),
                     "pres": doublet.doubletCalc1DData.getPresP() / 1e5,
                     "flow_rate": doublet.doubletCalc1DData.getFlowrate(),
                     "welld": doublet.doubletCalc1DData.getWellDistP(),
                     }

    # Reset doublet variables for next calculation
    doublet.setProjectVariables(False, 0.0)
    return output_values["power"], output_values["heat_pump_power"], output_values["capex"], output_values["opex"], output_values["utc"], output_values["npv"], output_values["hprod"], output_values["cop"], output_values[
        "cophp"], output_values["pres"], output_values["flow_rate"], output_values["welld"]


def calculate_performance_across_dimensions(input_data: xr.Dataset,
                                            input_params=None,
                                            rng_seed=None,
                                            p_values=None):
    """
    Given a set of input_parameters, and a dataset which contains the variables: thickness, thickness_sd, porosity,
    :param rng_seed:
    :param input_params:
    :param input_data:
    :return:
    """
    if p_values is None:
        p_values = [50.0]
    if input_params is None:    # If input parameters is none; then setup the BaseCase parameters
        input_params = {"hp_minimum_injection_temperature": 15,
                        "return_temperature": 30,
                        "surface_temperature": 10,
                        "degrees_per_km": 31,
                        "max_cooling_temperature_range": 100,
                        "stimKhMax": 20,
                        "use_stimulation": False,
                        "use_heat_pump": False,
                        "utc_cutoff_shallow": 5.1,
                        "utc_cutoff_deep": 6.5,
                        "utc_cutoff_depth": 4000.0}
    if "temperature" not in input_data:
        input_data["temperature"] = calculate_temperature_from_gradient(input_data.depth, input_data.thickness_mean, input_params["degrees_per_km"], input_params["surface_temperature"])

    # Start the jvm
    start_jvm()

    # Instantiate doublet class
    Logger = JClass("logging.Logger")
    Mockito = JClass("org.mockito.Mockito")
    RNG = JClass("tno.geoenergy.stochastic.RandomNumberGenerator")
    ThermoGISDoublet = JClass("thermogis.calc.doublet.ThermoGisDoublet")
    UTCPropertiesBuilder = JClass("thermogis.properties.builders.UTCPropertiesBuilder")

    # Instantiate the UTC properties class
    propsBuilder = UTCPropertiesBuilder()
    utc_properties = propsBuilder.build()

    # Instantiate random number generator:
    if rng_seed is None:
        rng = RNG()
    else:
        rng = RNG(rng_seed)

    # Create an instance of a ThermoGISDoublet
    doublet = ThermoGISDoublet(Mockito.mock(Logger), rng, utc_properties)


    # Setup output_data
    output_data = input_data.thickness_mean.copy().to_dataset(name="thickness")
    output_data = output_data.expand_dims({"p_value": p_values})

    # Calculate Thickness, Permeability and Transmissivity for each P-value
    thickness_data = []
    permeability_data = []
    transmissivity_data = []
    for i, p in enumerate(p_values):
        thickness, permeability, transmissivity = xr.apply_ufunc(generate_thickness_permeability_transmissivity_for_pvalue,
                                                                 input_data.thickness_mean,
                                                                 input_data.thickness_sd,
                                                                 input_data.ln_permeability_mean,
                                                                 input_data.ln_permeability_sd,
                                                                 p,
                                                                 input_core_dims=[[], [], [], [], []],
                                                                 output_core_dims=[[], [], []],
                                                                 vectorize=True,
                                                                 )
        thickness_data.append(thickness.data)
        permeability_data.append(permeability.data)
        transmissivity_data.append(transmissivity.data)

    output_data["thickness"] = (output_data.coords, thickness_data)
    output_data["permeability"] = (output_data.coords, permeability_data)
    output_data["transmissivity"] = (output_data.coords, transmissivity_data)
    output_data[f"transmissivity_with_ntg"] = (output_data[f"transmissivity"] * input_data.ntg) / 1e3

    # Calculate performance for each P-value
    power_data = []
    heat_pump_power_data = []
    capex_data = []
    opex_data = []
    utc_data = []
    npv_data = []
    hprod_data = []
    cop_data = []
    cophp_data = []
    pres_data = []
    flow_rate_data = []
    welld_data = []
    for i, p in enumerate(p_values):
        output_data_arrays = xr.apply_ufunc(calculate_performance_of_single_location,
                                            input_data.hc_accum,
                                            input_data.depth,
                                            output_data.thickness.isel(p_value=i),
                                            input_data.porosity,
                                            input_data.ntg,
                                            input_data.temperature,
                                            output_data.transmissivity.isel(p_value=i),
                                            output_data.transmissivity_with_ntg.isel(p_value=i),
                                            kwargs={"doublet": doublet, "input_params": input_params},
                                            input_core_dims=[[], [], [], [], [], [], [], []],
                                            output_core_dims=[[], [], [], [], [], [], [], [], [], [], [], []],
                                            vectorize=True,
                                            )

        # Assign values from calculate performance to their grids for each p-value
        power_data.append(output_data_arrays[0])
        heat_pump_power_data.append(output_data_arrays[1])
        capex_data.append(output_data_arrays[2])
        opex_data.append(output_data_arrays[3])
        utc_data.append(output_data_arrays[4])
        npv_data.append(output_data_arrays[5])
        hprod_data.append(output_data_arrays[6])
        cop_data.append(output_data_arrays[7])
        cophp_data.append(output_data_arrays[8])
        pres_data.append(output_data_arrays[9])
        flow_rate_data.append(output_data_arrays[10])
        welld_data.append(output_data_arrays[11])

    output_data["power"] = (output_data.coords, power_data)
    output_data["heat_pump_power"] = (output_data.coords, heat_pump_power_data)
    output_data["capex"] = (output_data.coords, capex_data)
    output_data["opex"] = (output_data.coords, opex_data)
    output_data["utc"] = (output_data.coords, utc_data)
    output_data["npv"] = (output_data.coords, npv_data)
    output_data["hprod"] = (output_data.coords, hprod_data)
    output_data["cop"] = (output_data.coords, cop_data)
    output_data["cophp"] = (output_data.coords, cophp_data)
    output_data["pres"] = (output_data.coords, pres_data)
    output_data["flow_rate"] = (output_data.coords, flow_rate_data)
    output_data["welld"] = (output_data.coords, welld_data)

    return output_data


def set_doublet_parameters(doublet, transmissivity_with_ntg, depth, porosity, ntg, temperature, useStimulation, stimKhMax, surface_temperature, return_temperature, use_heat_pump, max_cooling_temperature_range,
                           hp_minimum_injection_temperature):
    if not useStimulation or transmissivity_with_ntg > stimKhMax:
        doublet.setNoStimulation()

    doublet.doubletCalc1DData.setDepth(depth)
    doublet.doubletCalc1DData.setPorosity(porosity)
    doublet.doubletCalc1DData.setNtg(ntg)
    doublet.doubletCalc1DData.setSurfaceTemperature(surface_temperature)
    doublet.doubletCalc1DData.setReservoirTemp(temperature)
    doublet.doubletCalc1DData.setUseHeatPump(use_heat_pump)

    if use_heat_pump:
        injectionTemp = np.max([temperature - max_cooling_temperature_range, hp_minimum_injection_temperature])
    else:
        injectionTemp = np.max([temperature - max_cooling_temperature_range, return_temperature])

    doublet.doubletCalc1DData.setInjectionTemp(injectionTemp)
    doublet.doubletCalc1DData.setDhReturnTemp(return_temperature)
