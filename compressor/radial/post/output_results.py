def output_results(compressor, Compressor):
    '''
        Output results in the Terminal window
    '''

    from output_calc_error import output_calc_error

    print('Diameter of the wheel is {0:.0f} mm\n' .format(compressor['geometry']['D_2']*1e+03)) # (15)

    print('Parameters by cuts:')
    if 'VANELESS' in compressor['diffuser']:  print('\
        1-1: T_1 = {0:.0f} K,   p_1 = {1:.4f} MPa\n\
        2-2: T_2 = {2:.0f} K,   p_2 = {3:.4f} MPa\n\
        4-4: T_4 = {4:.0f} K,   p_4 = {5:.4f} MPa\n'
        .format(Compressor.T_1, Compressor.p_1*1e-06, Compressor.T_2, Compressor.p_2*1e-06, Compressor.T_4, Compressor.p_4*1e-06))
    else:   print('\
        1-1: T_1 = {0:.0f} K,   p_1 = {1:.4f} MPa\n\
        2-2: T_2 = {2:.0f} K,   p_2 = {3:.4f} MPa\n\
        3-3: T_3 = {4:.0f} K,   p_3 = {5:.4f} MPa\n\
        4-4: T_4 = {6:.0f} K,   p_4 = {7:.4f} MPa\n'
        .format(Compressor.T_1, Compressor.p_1*1e-06, Compressor.T_2, Compressor.p_2*1e-06, Compressor.T_3, p_3*1e-06, Compressor.T_4, Compressor.p_4*1e-06))

    print('Actual pressure degree increase is {0:.2f}, when\n\
    precalculated/set pressure degree increase is {1:.2f}'\
        .format(Compressor.pi_KStagn, compressor['pi_K'])) # (57)
    output_calc_error(Compressor.pi_KError) # (60)

    print("Energy conversion efficiency coeficients are:\n\
        eta_Ks*  = {0:.4f} - set\n\
        eta_Ks*' = {1:.4f} - rated"
        .format(compressor['efficiency']['eta_KsStagn'], Compressor.eta_KsStagnRated)) # (dict) & (59)
    output_calc_error(Compressor.errorEta) # (60)

    print("Isentropy head coeficients are:\n\
        H_Ks*  = {0:.4f} - set\n\
        H_Ks*' = {1:.4f} - rated"
        .format(compressor['efficiency']['H_KsStagn'], Compressor.H_KsStagnRated)) # (dict) & (61)
    output_calc_error(Compressor.errorH) # (62)

    print("If something doesn't work correctly make a new issue or check the others:\n\
    https://github.com/StasF1/turboCharger/issues")

