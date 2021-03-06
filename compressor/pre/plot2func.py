# Method to set the value
def value_btw_two_plots(balance_coef, upper_value, lower_value):
    ''' Set value using two interpolated functions and balance coefficient
    '''

    if (balance_coef < 0) | (balance_coef > 1):
        exit('\033[91mERROR:\
             Balance coefficient is incorrect!\
             \nValid values are from 0.0 to 1.0'
             .replace('             ', ' '))

    return balance_coef*upper_value + (1 - balance_coef)*lower_value


def value_range_of_plot(balance_coef, delta, lower_value):
    ''' Set value using the interpolated function, range 
        and balance coefficient
    '''
    return lower_value + balance_coef*delta


# Coeficients
def H_plot2func(balance_coef, D):
    import math

    if (D < 0.04) | (D > 0.8):
        exit('\033[91mERROR 5:\
             No data for that wheel diameter!\
             \nIt equals %0.0f cm but must be from 4 to 80 cm.'
             .replace('             ', ' ')
             %(D*1e+02))

    return value_btw_two_plots(
        balance_coef,
        0.0485923*math.log(D) + 0.80737,
        -2.28399*D**3 + 5.05698*D**3 - 4.02875*D**2 + 1.40783*D + 0.478618)


def phi_plot2func(balance_coef, D):
    if (D < 0.04) | (D > 0.8):
        exit('\033[91mERROR 6:\
             No data for that wheel diameter!\
             \nIt equals %0.0f cm but must be from 4 to 80 cm.'
             .replace('             ', ' ')
             %(D*1e+02))

    return value_btw_two_plots(
        balance_coef,
        1.21576*D**3 - 2.47517*D**3 + 1.77501*D**2 - 0.528671*D + 0.365277,
        0.84364*D**3 - 1.74951*D**3 + 1.27749*D**2 - 0.384933*D + 0.292871)


def eta_plot2func(balance_coef, D):
    if (D < 0.04) | (D > 0.8):
        exit('\033[91mERROR 15:\
             No data for that wheel diameter!\
             \nIt equals %0.0f cm but must be from 4 to 80 cm.'
             .replace('             ', ' ')
             %(D*1e+02))

    return value_btw_two_plots(
        balance_coef,
        -1.41956*D**3 + 3.59445*D**3 - 3.19974*D**2 + 1.20019*D + 0.70186,
        -2.54297*D**3 + 5.79527*D**3 - 4.69133*D**2 + 1.64249*D + 0.603052)


def relD_1H_plot2func(balance_coef, D):
    if (D < 0.04) | (D > 0.8):
        exit('\033[91mERROR 13:\
             No data for that wheel diameter!\
             \nIt equals %0.0f cm but must be from 4 to 80 cm.'
             .replace('             ', ' ')
             %(D*1e+02))

    return value_btw_two_plots(
        balance_coef,
        -0.05*D + 0.712,
        -0.35*D + 0.634)


def relD_1B_plot2func(balance_coef, D):
    if (D < 0.04) | (D > 0.8):
        exit('\033[91mERROR 13:\
             No data for that wheel diameter!\
             \nIt equals %0.0f cm but must be from 4 to 80 cm.'
             .replace('             ', ' ')
             %(D*1e+02))

    return value_range_of_plot(
        balance_coef,
        0.06,
        0.260417*D**2 + 0.0280449*D + 0.198365)


def relSpeeds_plot2func(balance_coef, D):
    if (D < 0.04) | (D > 0.8):
        exit('\033[91mERROR 27:\
             No data for that wheel diameter!\
             \nIt equals %0.0f cm but must be from 4 to 80 cm.'
             .replace('             ', ' ')
             %(D*1e+02))

    return value_btw_two_plots(
        balance_coef,
        1.71023 *D**3 - 3.78212*D**3 + 2.99991*D**2 - 1.05122*D + 1.23182,
        -6.37691*D**3 + 12.3393*D**3 - 8.57209*D**2 + 2.54654*D + 0.734892)


def z_plot2func(balance_coef, D):
    if (D < 0.04) | (D > 0.8):
        exit('\033[91mERROR 30:\
             No data for that wheel diameter!\
             \nIt equals %0.0f cm but must be from 4 to 80 cm.'
             .replace('             ', ' ')
             %(D*1e+02))

    return value_range_of_plot(
        balance_coef,
        9,
        141.063*D**3 - 228.472*D**2 + 134.588*D + 2.44075)


# ''' (C) 2018-2020 Stanislau Stasheuski '''