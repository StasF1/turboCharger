def run(project, engine, compressor):
    ''' Calculate compressor parameters using 0D method
    '''
    import math
    from etc.set_standard import set_standard
    from compressor.pre.plot2func import z_plot2func, H_plot2func, phi_plot2func,\
                                         relSpeeds_plot2func, relD_1H_plot2func,\
                                         relD_1B_plot2func, eta_plot2func
    from compressor.run.diffuser_outlet_T import diffuser_outlet_T
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

    class Compressor:
        ''' Class with calculated compressor parameters
        '''

        D_2Init = compressor['geometry']['D_2'] # [m]

        #1 Stagnation parameters of inlet | Параметры торможения на входе
        T_0Stagn = compressor['initial']['T_aStagn']
        p_0Stagn = compressor['losses']['sigma_0']\
                   *compressor['initial']['p_aStagn']

        #3 Static pressure & temperature of intake in compressor
        #  Статические температура и давление на входе в компрессор
        T_0 = T_0Stagn - compressor['initial']['c_0']**2\
                         /2/engine['inlet']['c_p']
        p_0 = p_0Stagn*pow(T_0/T_0Stagn,
                           engine['inlet']['k']\
                           /(engine['inlet']['k'] - 1)) #[Pa]

        #4 Isentropy compression work in compressor
        #  Изоэнтропная работа сжатия в компрессоре
        L_KsStagn = engine['inlet']['c_p']*T_0Stagn*(
            pow(compressor['pi'],
                (engine['inlet']['k'] - 1)/engine['inlet']['k'])
            - 1
        )

        #5 Wheel outer diameter circular velocity
        #  Окружная скорость на наружном диаметре колеса
        compressor['efficiency']['H_KsStagn'] = H_plot2func(
            compressor['efficiency']['H_KsStagn'],
            compressor['geometry']['D_2'])
        u_2 = math.sqrt(L_KsStagn/compressor['efficiency']['H_KsStagn'])
        if u_2 >= 550:
            exit('\033[91mERROR 5:\
                 Wheel outer diameter circular velocity is too high!\
                 \nTry to increase wheel diameter &/or set other ECE parameters'
                 .replace('                 ', ' '))

        #6 Абсолютная скорость потока на входе в рабочее колесо
        compressor['efficiency']['phi_flow'] = phi_plot2func(
            compressor['efficiency']['phi_flow'],
            compressor['geometry']['D_2'])
        c_1 = compressor['efficiency']['phi_flow']*u_2

        #7 Температура воздуха на входе в рабочее колесо
        T_1 = T_0 + (compressor['initial']['c_0']**2 - c_1**2)\
            /2/engine['inlet']['c_p']

        #8 Расчёт потерь энергии во впускном коллекторе
        L_inlet = compressor['losses']['dzeta_inlet']*c_1**2/2

        #9 Показатель политропы сжатия в компрессоре
        n_1 = (engine['inlet']['k']/(engine['inlet']['k'] - 1)
               - L_inlet/engine['inlet']['R']/(T_1 - T_0))\
              /(engine['inlet']['k']/(engine['inlet']['k'] - 1)
               - L_inlet/engine['inlet']['R']/(T_1 - T_0) - 1)

        #10 Давление на входе в колесо
        p_1 = p_0*pow(T_1/T_0, n_1/(n_1 - 1))

        #11 Плотность на входе в колесо
        rho_1 = p_1/engine['inlet']['R']/T_1

        #13 Наружный диаметр колеса на входе D_1H
        F_1 = compressor['G']/c_1/rho_1 # площадь поп. сечения в колесе

        compressor['geometry']['coefficients']['D_1Down_relative'] = \
            relD_1H_plot2func(compressor['geometry']['coefficients']
                                        ['D_1Down_relative'],
                              compressor['geometry']['D_2'])

        compressor['geometry']['coefficients']['D_1Up_relative'] = \
            relD_1B_plot2func(compressor['geometry']['coefficients']
                                        ['D_1Up_relative'],
                              compressor['geometry']['D_2'])
    
        relD_1BToH = compressor['geometry']['coefficients']\
                               ['D_1Up_relative']\
                     /compressor['geometry']['coefficients']\
                               ['D_1Down_relative']

        if relD_1BToH >= 1:
            exit('\033[91mERROR 13:\
                 Relation relD_1B/relD_1H = %0.2f > 1.\
                 \nSquare root argument is less than 0!'
                 .replace('                 ', ' ')
                 %(relD_1BToH))

        D_1H = math.sqrt(4*F_1/math.pi/(1 - relD_1BToH**2))

        #14 Внутренний диаметер на входе (втулочный диаметр)
        D_1B = relD_1BToH*D_1H

        #15 Наружный диаметр колеса на комперссора на выходе
        D_2estimated = D_1H\
                       /compressor['geometry']['coefficients']\
                                  ['D_1Down_relative']\
                       *1e+03 # [mm]

        if 'ON' in compressor['geometry']['coefficients']['DToSTD']:
            compressor['geometry']['D_2'] = set_standard(D_2estimated)\
                                            *1e-03 # [m]

        else:
            if D_2estimated <= 85:
                compressor['geometry']['D_2'] = round(D_2estimated*2, -1)/2\
                                                *1e-03 # [m]
            else:
                compressor['geometry']['D_2'] = round(D_2estimated, -1)\
                                                *1e-03 # [m]

        if 'TYPE2' in project['type']:
            compressor['efficiency']['eta_KsStagn'] = eta_plot2func(
                compressor['efficiency']['eta_KsStagn'],
                compressor['geometry']['D_2'])

        #16 Частота вращения турбокомпрессора
        RPM = 60*u_2/math.pi/compressor['geometry']['D_2'] # [1/min]

        #17 Средний диаметр на входе в колесо
        D_1 = math.sqrt((D_1B**2 + D_1H**2)/2)

        #18 Окружная скорость на среднем диаметре входа
        u_1 = math.pi*D_1*RPM/60

        #19 Угол входа потока в рабочее колесо на среднем диамметре в
        #   относительном движении
        beta_1 = math.degrees(math.atan(c_1/u_1))
        if issubclass(type(compressor['geometry']['iDeg']), str):
            exit('Degree of the wheel inlet flow is {0:.3f}\
                 \nNow you can set "i", using recomendations'
                 .format(beta_1))

        #20 Угол установки лопаток на среднем диаметре
        beta_1Blade = beta_1 + compressor['geometry']['iDeg']

        #21 Абсолютная скорость при учёте толщины лопаток
        c_1Tau = c_1/compressor['load']['tau_1']

        #22 Окружная скорость на наружном диаметре входа диаметре входа
        u_1H = math.pi*D_1H*RPM/60

        #23 Относительная скорость на наружном диаметре входа в колесо
        w_1H = math.sqrt(c_1Tau**2 + u_1H**2)

        #24 Число маха на наружном диаметре входа в колесо
        M_w1 = w_1H/math.sqrt(engine['inlet']['k']*engine['inlet']['R']*T_1)
        if M_w1 > 0.9:
            print('\033[93mWARNING 24:\
                  Mach number is too high!\
                  \nIt must be less than 0.9 but it equals {0:.3f}\
                  \nTry to increase "tau_1", "D_1Down_relative" &/or decrease\
                  "phi_flow", "D_1Up_relative".\033[0m\n'
                  .replace('                  ', ' ')
                  .format(M_w1))

        #25 Относительная скорость на среднем диаметре входа в колесо
        w_1 = math.sqrt(c_1Tau**2 + u_1**2)

        #26 Удельная работа потерь во входном вращающемся направляющем
        #   аппарате колеса
        L_BA = compressor['losses']['dzeta_BA']*w_1**2/2

        #27 Радиальная составляющая абсолютной/относительной скорости
        #   на выходе из колеса
        compressor['geometry']['coefficients']['w2r_c1a_ratio'] = \
            relSpeeds_plot2func(compressor['geometry']['coefficients']\
                                          ['w2r_c1a_ratio'],
                                compressor['geometry']['D_2'])
        c_2r = compressor['geometry']['coefficients']['w2r_c1a_ratio']*c_1

        #28 Потери на поворот и трение в межлопаточных каналах рабочего
        #   колеса
        L_TF = compressor['losses']['dzeta_TF']*c_2r**2/2

        #29 Потери на трение диска колеса о воздух
        #   в сумме с вентиляционными потерями
        L_TB = compressor['losses']['alpha_wh']*u_2**2

        #30 Проверка на число лопаток относительно диаметра (рис. 2.2)
        zLower = z_plot2func(0, compressor['geometry']['D_2'])
        zUpper = z_plot2func(1, compressor['geometry']['D_2'])

        if ((compressor['geometry']['blades'] < zLower)
            or (compressor['geometry']['blades'] > zUpper)):
            exit('\033[91mERROR 30:\
                Number of blades is not in the allowable diapason!\n\
                \nFor diameter of the wheel %0.0fmm this diapason from %1.0f\
                to %2.0f.'
                .replace('                 ', ' ')
                %(compressor['geometry']['D_2']*1e+03,
                  round(zLower + 0.5), int(zUpper)))

        #31 Коэффициент мощности учитывабщий число лопаток и проч.
        mu = 1/(1 + 2/3*math.pi/compressor['geometry']['blades']
                *math.sin(
                    math.radians(compressor['geometry']['beta_2Blade']))
                    /(1 - pow(D_1/compressor['geometry']['D_2'], 2)))

        #32 Температура воздуха за колесом
        T_2 = T_1 + ((mu + compressor['losses']['alpha_wh'] - 0.5*mu**2)
                     *u_2**2/engine['inlet']['c_p'])

        #33 Показатель политропы сжатия в колесе
        n_2 = (engine['inlet']['k']/(engine['inlet']['k'] - 1)
               - (L_BA + L_TF + L_TB)/engine['inlet']['R']/(T_2 - T_1))\
              /(engine['inlet']['k']/(engine['inlet']['k'] - 1)
               - (L_BA + L_TF + L_TB)/engine['inlet']['R']/(T_2 - T_1) - 1)

        #34 Давление на выходе из колеса
        p_2 = p_1*pow(T_2/T_1, n_2/(n_2 - 1))

        #35 Плотность на выходе из колеса
        rho_2 = p_2/engine['inlet']['R']/T_2

        #36 Окружная составляющая абсолютной скорости на выходе
        c_2u = mu\
               *(u_2 - c_2r/math.tan(math.radians(
                                compressor['geometry']['beta_2Blade'])))

        #37 Абсолютная скорость на выходе из колеса
        c_2 = math.sqrt(c_2u**2 + c_2r**2)

        #38 Окружная составляющая относительной скорости на выходе из колеса
        w_2u = u_2 - c_2u

        #39 Относительная скорость на выходе из колеса (c_2r = w_2r)
        w_2 = math.sqrt(w_2u**2 + c_2r**2)

        #40 Угол между векторами относительной/абсолютной и окружной скорости
        #   на выходе из колеса
        alpha_2 = math.degrees(math.acos(c_2u/c_2))
        beta_2  = math.degrees(math.acos(w_2u/w_2))

        #41 Ширина колеса на выходе из турбины
        b_2 = math.pi\
              /compressor['G']\
              /compressor['geometry']['D_2']\
              /compressor['load']['tau_2']\
              /c_2r/rho_2

        #43 Температура заторможенного потока на выходе из колеса
        T_2Stagn = T_2 + c_2**2/2/engine['inlet']['c_p']

        # Расчёт параметров безлопаточного диффузора
        if 'VANELESS' in compressor['diffuser']:
            #44 Ширина безлопаточного диффузора на выходе
            b_4 = compressor['geometry']['coefficients']\
                            ['diffuser']['vaneless_wide']\
                  *b_2

            #45 Диаметр безлопаточного диффузора на выходе
            D_4 = compressor['geometry']['coefficients']\
                            ['diffuser']['vaneless_diam']\
                  *compressor['geometry']['D_2']

            #46 Показатель политропы сжатия в диффузоре
            n_4 = (compressor['efficiency']['eta_diffuser']\
                   *engine['inlet']['k']
                   /(engine['inlet']['k'] - 1))\
                  /(compressor['efficiency']['eta_diffuser']\
                    *engine['inlet']['k']
                    /(engine['inlet']['k'] - 1) - 1)

            #47 Температура на выходе из диффузора
            # (методом последовательных приближений)
            T_4, acc = T_2, 1e-02
            while (
                abs(diffuser_outlet_T(engine['inlet'],
                                      compressor['geometry']['D_2'],
                                      b_2, T_2, c_2,
                                      D_4, b_4, T_4, n_4)
                - T_4) > acc
            ):
                T_4 += acc
                if T_4 > 1000:
                    exit('\033[91mERROR 47:\
                         Cannot find outlet diffuser temperature!'
                         .replace('                         ', " "))

            #48 Давление на выходе из диффузора
            p_4 = p_2*pow(T_4/T_2, n_4/(n_4 - 1))

            #49 Плотность на выходе из колеса
            rho_4 = p_4/engine['inlet']['R']/T_4

            #50 Скорость на выходе из диффузора
            c_4 = c_2*compressor['geometry']['D_2']*b_2*rho_2/D_4/b_4/rho_4

        else: # Расчёт параметров лопаточного диффузора (по МУ Федюшкина #FXX)
            n_4 = compressor['losses']['n_diffuser']

            #F50 Проверка на число лопаток относительно их количества в РК
            if (
                (compressor['geometry']['blades_diffuser']
                 < compressor['geometry']['blades'] - 5)
                or (compressor['geometry']['blades_diffuser']
                    > compressor['geometry']['blades'] + 2)
            ):
                exit('\033[91mERROR F50:\
                     Number of diffuser blades is not in the allowable\
                     diapason!\
                     \nFor %0.0f compressor blades this diapason\
                     from %1.0f to %2.0f.'
                     .replace('                     ', ' ')
                     %(compressor['geometry']['blades'],
                       compressor['geometry']['blades'] - 5,
                       compressor['geometry']['blades'] + 2))

            #44 Ширина безлопаточной части диффузора на выходе
            b_3 = compressor['geometry']['coefficients']\
                            ['diffuser']['vaneless_wide']\
                  *b_2

            #45 Диаметр безлопаточной части диффузора на выходе
            D_3 = compressor['geometry']['coefficients']\
                            ['diffuser']['vaneless_diam']\
                  *compressor['geometry']['D_2']

            #46 Показатель политропы сжатия безлопаточной части диффузора
            n_3 = (compressor['efficiency']['eta_diffuser']\
                   *engine['inlet']['k']
                   /(engine['inlet']['k'] - 1))\
                  /(compressor['efficiency']['eta_diffuser']\
                    *engine['inlet']['k']
                    /(engine['inlet']['k'] - 1) - 1)

            #47 Температура на выходе из диффузора (методом
            #   последовательных приближений)
            T_3, acc = T_2 - 40, 1e-02
            while (
                abs(diffuser_outlet_T(engine['inlet'],
                                      compressor['geometry']['D_2'],
                                      b_2, T_2, c_2,
                                      D_3, b_3, T_3, n_3)
                - T_3) > acc
            ):
                T_3 += acc
                if T_3 > 1000:
                    exit('\033[91mERROR 47:\
                         Cannot find outlet diffuser temperature!'
                         .replace('                         ', " "))

            else:
                T_3 = diffuser_outlet_T(engine['inlet'],
                                        compressor['geometry']['D_2'],
                                        b_2, T_2, c_2,
                                        D_3, b_3, T_3, n_3)

            #48 Давление на выходе из колеса
            p_3 = p_2*pow(T_3/T_2, n_3/(n_3 - 1))

            #49 Плотность на выходе из безлопаточной части диффузора
            rho_3 = p_3/engine['inlet']['R']/T_3

            #F46 Скорость на выходе из безлопаточной части диффузора
            c_3 = c_2*compressor['geometry']['D_2']*b_2*rho_2/D_3/b_3/rho_3

            #F47 Диаметр лопаточного диффузора на выходе
            D_4 = compressor['geometry']['coefficients']\
                            ['diffuser']['vaned_diam']\
                  *compressor['geometry']['D_2']

            #F48 Ширина лопаточного диффузора на выходе
            b_4 = compressor['geometry']['coefficients']\
                            ['diffuser']['vaned_wide']*b_3

            #F49 Угол наклона лопаток на выходе из диффузора
            alpha_4 = alpha_2 + compressor['geometry']['deltaDiffuser']

            #F51 Температура на выходе из лопаточной части диффузора
            b_3COEF = b_3*compressor['load']['tau_3']\
                      *math.sin(math.radians(alpha_2))
            b_4COEF = b_4*compressor['load']['tau_4']\
                      *math.sin(math.radians(alpha_4))

            T_4, acc = T_3, 1e-02
            while (
                abs(diffuser_outlet_T(engine['inlet'],
                                      D_3, b_3COEF, T_3, c_3,
                                      D_4, b_4COEF, T_4, n_4)
                - T_4) > acc
            ):
                T_4 += acc
                if T_4 > 1000:
                    exit('\033[91mERROR F51:\
                         Cannot find outlet blade diffuser temperature!'
                         .replace('                         ', ' '))

            #F54 Давление и плотность на выходе из лопаточной части диффузора
            p_4 = p_2*pow(T_4/T_3,
                          compressor['losses']['n_diffuser']/(n_4 - 1))
            rho_4 = p_4/engine['inlet']['R']/T_4

            #50 Скорость на выходе из диффузора
            c_4 = c_3*D_3*b_3COEF/D_4/b_4COEF/rho_4

        #51 Скорость на выходе из компрессора
        c_K = c_4\
              /compressor['geometry']['coefficients']\
                         ['diffuser']['c_out_ratio']

        #52 Температура на выходе из компрессора
        T_K = T_4 + (c_4**2 - c_K**2)/2/engine['inlet']['c_p']

        #54 Давление на выходе из компрессора
        p_K = p_4*pow(T_K/T_4, compressor['losses']['n_housing']
                               /(compressor['losses']['n_housing'] - 1))

        #55 Температура заторможенного потока на выходе
        T_KStagn = T_K + c_K**2/2/engine['inlet']['c_p']

        #56 давление заторможенного потока на выходе
        p_KStagn = p_K*pow(T_KStagn/T_K,
                           engine['inlet']['k']/(engine['inlet']['k'] - 1))

        #57 Действительная степень повышения давления в компрессоре
        pi_KStagn = p_KStagn/p_0Stagn

        #58 Изоэнтропная работа по расчётной степени повышения давления
        L_KsStagnRated = engine['inlet']['c_p']*T_0Stagn\
                         *(pow(pi_KStagn,
                               (engine['inlet']['k'] - 1)
                               /engine['inlet']['k'])
                         - 1)

        #59 Расчётный изоэнтропный КПД по заторможенным параметрам
        eta_KsStagnRated = (pow(pi_KStagn, (engine['inlet']['k'] - 1)
                                            /engine['inlet']['k']) - 1)\
                           /(T_KStagn/T_0Stagn - 1)

        #60 Расхождение с заданным КПД компрессора
        eta_error = (compressor['efficiency']['eta_KsStagn']
                     - eta_KsStagnRated)\
                    /compressor['efficiency']['eta_KsStagn']*100

        #61 Расчётный коэффициент напора по заторможенным параметрам
        H_KsStagnRated = L_KsStagnRated/u_2**2

        #62 Расхождение с заданным КПД компрессора
        H_error = (compressor['efficiency']['H_KsStagn']
                   - H_KsStagnRated)\
                  /compressor['efficiency']['H_KsStagn']*100

        #63 Мощность затрачиваемая на привод компрессора
        N_K = compressor['G']*L_KsStagn/eta_KsStagnRated

        #64 Полное давление перед впускными клапанами поршневой части
        p_vStagn = p_KStagn*compressor['losses']['sigma_c']\
                   *compressor['losses']['sigma_v']

        #65 Расхождение с предварительно оценнёной/заданной степенью повышения
        #   давления компрессора
        pi_KError = (pi_KStagn - compressor['pi'])/compressor['pi']*100

    return compressor, Compressor


# ''' (C) 2018-2020 Stanislau Stasheuski '''