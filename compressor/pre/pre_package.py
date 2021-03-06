def pre(run, engine, compressor):
    ''' Extend compressor dictionary with its relative parameters and
        precalculate some compressor parameters
    '''
    import sys
    from os import path
    from compressor.pre.set_default import set_default
    from compressor.pre.plot2func import eta_plot2func
    from compressor.run.pressure_increase_ratio import pressure_increase_ratio
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
    set_default(compressor)

    # Convert data to SI dimensions
    compressor['initial']['p_aStagn'] *= 1e+06 # -> [Pa]

    # Flow volume | Расход
    if 'TYPE1' in run['type']:
        compressor['G'] = engine['efficiency']['N_e']\
                          *engine['efficiency']['b_e']\
                          *engine['combustion']['l_0']\
                          *engine['combustion']['alpha']\
                          *engine['combustion']['phi']/3600
                          # [kg/s]

    # Wheel diameter
    # Оценка диаметра рабочего колеса и установка параметров зависящих от него
    if issubclass(type(compressor['geometry']['estimD_2']), str):
        compressor['geometry']['D_2'] = (160*compressor['G'] + 40)\
                                        *1e-03 # [m]
    else:
        compressor['geometry']['D_2'] = compressor['geometry']['estimD_2']\
                                        *1e-02 # [m]

    # Calculation pressure degree increase with successive approximation method
    # Опр. степени повышения давления методом последовательных приближений
    if 'TYPE1' in run['type']:
        compressor['efficiency']['eta_KsStagn'] = eta_plot2func(
            compressor['efficiency']['eta_KsStagn'],
            compressor['geometry']['D_2'])

        compressor['pi'], acc = 1, 1e-05
        while (abs(pressure_increase_ratio(engine, compressor)
                   - compressor['pi']) > acc):
            compressor['pi'] += acc

        pressure_increase_ratio(engine, compressor)

    return compressor


# ''' (C) 2018-2020 Stanislau Stasheuski '''