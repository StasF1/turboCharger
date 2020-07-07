#!/usr/bin/env python3
'''
    API:            Python 3.x
    Project:        https://github.com/StasF1/turboCharger
    Version:        2.x
    License:        GNU General Public License 3.0 ( see LICENSE )
    Author:         Stanislau Stasheuski

    File:           turbocharger
    Description:    Calculate turbocharger parameters using 0D method

'''
import sys
import math
sys.path.append('etc/')
sys.path.extend(['compressor/', 'compressor/radial/',
                 'turbine/', 'turbine/axial/', 'turbine/radial/'])
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

def turbocharger_compressor(run, engine, compressor):
    '''
        Calculate compressor part of the turbocharger
    '''
    from compressor_radial_pre import compressor_radial_pre
    from compressor_radial_run import compressor_radial_run
    from compressor_radial_post import compressor_radial_post

    sys.path.extend(['compressor/radial/pre',
                     'compressor/radial/run',
                     'compressor/radial/post'])
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
 
    compressor_radial_pre(run, engine,
                          compressor)

    (compressor, Compressor) = compressor_radial_run(run, engine,
                                                     compressor)

    compressor_radial_post(run, engine,
                           compressor, Compressor)

    return Compressor


def turbocharger_turbine(run, ambient, engine,
        compressor, Compressor,
        turbine):
    '''
        Calculate turbine part of the turbocharger
    '''
    from default_value import default_value
    from output_calc_error import output_calc_error
    from turbine_radial_pre import turbine_radial_pre
    from turbine_radial_run import turbine_radial_run
    from turbine_radial_post import turbine_radial_post
    from turbine_axial_pre import turbine_axial_pre
    from turbine_axial_run import turbine_axial_run
    from turbine_axial_post import turbine_axial_post
    sys.path.append('etc/turbine/')
    sys.path.extend(['turbine/radial/pre',
                     'turbine/radial/run',
                     'turbine/radial/post'])
    sys.path.extend(['turbine/axial/pre',
                     'turbine/axial/run',
                     'turbine/axial/post'])
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

    print(turbine['type'])
    if turbine['type'] == 'radial':
        (run, ambient, engine, turbine) = turbine_radial_pre(run, ambient, engine,
                                                            compressor,
                                                            turbine)

        (turbine, Turbine) = turbine_radial_run(ambient, engine,
                                                compressor, Compressor,
                                                turbine)

        turbine_radial_post(run, engine,
                            compressor, Compressor,
                            turbine, Turbine)

    elif turbine['type'] == 'axial':
        turbine = turbine_axial_pre(run, ambient, engine,
                                    compressor,
                                    turbine)

        (turbine, Turbine) = turbine_axial_run(ambient, engine,
                                            compressor, Compressor,
                                            turbine)

        turbine_axial_post(run, engine,
                        compressor, Compressor,
                        turbine, Turbine)

    else:
        exit(f"\033[91mError: turbine['type'] variable is incorrect!")

def main():
    '''
        Calculate turbocharger parameters using 0D method
    '''
    from logo import logo
    from engine_extend import engine_extend

    from commonConfig import run, ambient
    from engineConfig import engine
    from compressorConfig import compressor
    from turbineConfig import turbine
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

    # Precalculations
    logo()
    engine_extend(engine)

    Compressor = turbocharger_compressor(run, engine,
                                         compressor)

    turbocharger_turbine(run, ambient, engine,
                         compressor, Compressor,
                         turbine)

if __name__ == '__main__':
    main()


# ''' (C) 2018-2020 Stanislau Stasheuski '''