#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    API:            Python 3.x
    Project:        https://github.com/StasF1/turboCharger
    Version:        2.x
    License:        GNU General Public License 3.0 ( see LICENSE )
    Author:         Stanislau Stasheuski

    Script:         radialCompressor
    Description:    Calculate compressor parameters using 0D method

'''
from __future__         import division
import math, os, shutil, sys
from PIL                import ImageFont, Image, ImageDraw

from piK                import piK
from diffOutTemp        import diffOutTemp
from standardisedSize   import standardisedSize
from os                 import path;\
    sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from defaultValue       import defaultValue
from plotToFunction     import zPlot, etaPlot, HPlot, phiPlot,\
                               relSpeedsPlot, relD_1HPlot, relD_1BPlot

# Loading input data from project dictionaries
from commonConfig       import *
from compressorConfig   import *

# Converting data to SI dimensions
N_e = N_e*1e03 # -> [W]
g_e = g_e*1e-03 # -> [kg/W/h] or [g/kW/h]
p_aStagn = p_aStagn*1e06 # -> [Pa]
D = D*1e-02;      S = S*1e-02 # -> [m]

# Set default values
exec(compile(open('include/defaultValuesCoefficients.py', "rb").read(),
                  'include/defaultValuesCoefficients.py', 'exec'))
# Output the logo
exec(compile(open('../etc/logo.py', "rb").read(),
                  '../etc/logo.py', 'exec'))

# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

# Теоретическое количество воздуха, необходимое для сгорания 1 кг топлива
if 'SI' in engineType:
    l_0 = 14.84 # [kg]
elif 'DIESEL' in engineType:
    l_0 = 14.31 # [kg]
else:
    exit('Set type of the engine correctly ("DIESEL" or "SI")\
 in commonConfig.py dictionary!\n')

# Effective pressure | Среднее эффективное давление
p_e = 0.12*1e03*N_e*strokeNumber/(math.pi*pow(D, 2)*S*n*pistonNumber) # [Pa]

# Flow volume | Расход
if 'TYPE1' in projectType:
    G_K = N_e*g_e*l_0*alpha*phi/3600 # [kg/s]

# Wheel diameter
# Оценка диаметра рабочего колеса и установка параметров зависящих от него
if issubclass(type(estimD_2), str):
    D_2 = (160*G_K + 40)*1e-03 # [m]
else:
    D_2 = estimD_2*1e-02 # [m]
D_2_mm0 = D_2*1e+03 # [mm]

# Calculation pressure degree increase with successive approximation method
# Определение степени повышения давления методом последовательных приближений
if 'TYPE1' in projectType:
    eta_KsStagn = etaPlot(eta_KsStagn, D_2)
    Pi_K = 1
    validity = 1e-04
    while abs(piK(l_0, p_e, eta_KsStagn, Pi_K) - Pi_K) > validity:
        Pi_K = Pi_K + validity
    else:
        Pi_K = piK(l_0, p_e, eta_KsStagn, Pi_K)


# Compressor parameters
# ~~~~~~~~~~~~~~~~~~~~~
#1 Stagnation parameters of inlet | Параметры торможения на входе
T_0Stagn = T_aStagn
p_0Stagn = sigma_0*p_aStagn

#3 Static pressure & temperature of intake in compressor
#  Статические температура и давление на входе в компрессор
T_0 = T_0Stagn - pow(c_0, 2)/2/c_p
p_0 = p_0Stagn*pow(T_0/T_0Stagn, k/(k - 1)) #[Pa]


#4 Isentropy compression work in compressor
#  Изоэнтропная работа сжатия в компрессоре
L_KsStagn = c_p*T_0Stagn*(pow(Pi_K, (k - 1)/k) - 1)

#5 Wheel outer diameter circular velocity
#  Окружная скорость на наружном диаметре колеса
H_KsStagn = HPlot(H_KsStagn, D_2)
u_2 = math.sqrt(L_KsStagn / H_KsStagn)
if u_2 >= 550:    exit('Error 5:\n\
 Wheel outer diameter circular velocity is too high!\n\
Try to increase wheel diameter &/or set other ECE parameters')

#6 Абсолютная скорость потока на входе в рабочее колесо 
phi_flow = phiPlot(phi_flow, D_2)
c_1 = phi_flow*u_2

#7 Температура воздуха на входе в рабочее колесо
T_1 = T_0 + (pow(c_0, 2) - pow(c_1, 2))/2/c_p 

#8 Расчёт потерь энергии во впускном коллекторе
L_inlet = dzeta_inlet*pow(c_1, 2)/2

#9 Показатель политропы сжатия в компрессоре
n_1 = ( k/(k - 1) - L_inlet/R/(T_1 - T_0) )/ \
( k/(k - 1) - L_inlet/R/(T_1 - T_0) - 1)

#10 Давление на входе в колесо
p_1 = p_0*pow(T_1/T_0, n_1/(n_1 - 1))

#11 Плотность на входе в колесо
rho_1 = p_1/R/T_1


#13 Наружный диаметр колеса на входе D_1H
F_1 = G_K/c_1/rho_1 # площадь поперечного сечения в колесе

relD_1H = relD_1HPlot(relD_1H, D_2)
relD_1B = relD_1BPlot(relD_1B, D_2)
if relD_1B/relD_1H >= 1:
    exit('Error 13: Relation relD_1B/relD_1H = %0.2f > 1.\n\
Square root argument is less than 0!' %(relD_1B/relD_1H) )

D_1H = math.sqrt( 4*F_1/math.pi/(1 - pow(relD_1B/relD_1H, 2)) )

#14 Внутренний диаметер на входе (втулочный диаметр)
D_1B = relD_1B/relD_1H*D_1H

#15 Наружный диаметр колеса на комперссора на выходе
D_2estimated = D_1H/relD_1H*1e+03 # [mm]
if 'ON' in roundDiamToSTD:
    D_2 = standardisedSize( D_2estimated )*1e-03 # [m]
else:
    if D_2estimated <= 85:
        D_2 = round( D_2estimated*2, -1 )/2*1e-03 # [m]
    else:
        D_2 = round( D_2estimated, -1 )*1e-03 # [m]

if 'TYPE2' in projectType: eta_KsStagn = etaPlot(eta_KsStagn, D_2)

#16 Частота вращения турбокомпрессора
n_tCh = 60*u_2/math.pi/D_2 # [1/min]

#17 Средний диаметр на входе в колесо
D_1 = math.sqrt(( pow(D_1B, 2) + pow(D_1H, 2) )/2)

#18 Окружная скорость на среднем диаметре входа
u_1 = math.pi*D_1*n_tCh/60

#19 Угол входа потока в рабочее колесо на среднем диамметре в
#   относительном движении
beta_1 = math.degrees(math.atan( c_1/u_1 ))
if issubclass(type(iDeg), str):    
    print('Degree of the wheel inlet flow is {0:.3f}' .format(beta_1))
    print('Now you can set "i", using recomendations')
    exit()

#20 Угол установки лопаток на среднем диаметре
beta_1Blade = beta_1 + iDeg

#21 Абсолютная скорость при учёте толщины лопаток
c_1Tau = c_1 / tau_1

#22 Окружная скорость на наружном диаметре входа диаметре входа
u_1H = math.pi*D_1H*n_tCh/60

#23 Относительная скорость на наружном диаметре входа в колесо
w_1H = math.sqrt(pow(c_1Tau, 2) + pow(u_1H, 2)) 

#24 Число маха на наружном диаметре входа в колесо
M_w1 = w_1H/math.sqrt(k*R*T_1)
if M_w1 > 0.9:
    print('Warning 24: Mach number is too high!\n\
It must be less than 0.9 but it equals {0:.3f}\n\
Try to increase "tau_1", "relD_1H" &/or decrease "phi_flow", "relD_1B".\n'\
    .format(M_w1))

#25 Относительная скорость на среднем диаметре входа в колесо
w_1 = math.sqrt(pow(c_1Tau, 2) + pow(u_1, 2))

#26 Удельная работа потерь во входном вращающемся направляющем аппарате колеса
L_BA = dzeta_BA*pow(w_1, 2)/2

#27 Радиальная составляющая абсолютной/относительной скорости
#   на выходе из колеса
relW_2rToC_1a = relSpeedsPlot(relW_2rToC_1a, D_2)
c_2r = relW_2rToC_1a*c_1

#28 Потери на поворот и трение в межлопаточных каналах рабочего колеса
L_TF = dzeta_TF*pow(c_2r, 2)/2

#29 Потери на трение диска колеса о воздух в сумме с вентиляционными потерями
L_TB = alpha_wh*pow(u_2, 2)

#30 Проверка на число лопаток относительно диаметра (рис. 2.2)
zLower = zPlot(0, D_2)
zUpper = zPlot(1, D_2)
if (z_K < zLower) | (z_K > zUpper):
    exit('Error 30: Number of blades is not in the allowable diapason!\n\
For diameter of the wheel %0.0fmm this diapason is from %1.0f to %2.0f.'
%(D_2*1e+03, round(zLower + 0.5), int(zUpper)) )

#31 Коэффициент мощности учитывабщий число лопаток и проч.
mu = 1/(1+2/3*math.pi/z_K \
    *math.sin(math.radians(beta_2Blade))/(1 - pow(D_1/D_2, 2)) )

#32 Температура воздуха за колесом
T_2 = T_1 + (mu + alpha_wh - 0.5*pow(mu, 2))*pow(u_2, 2)/c_p

#33 Показатель политропы сжатия в колесе
n_2 = ( k/(k - 1) - (L_BA + L_TF + L_TB)/R/(T_2 - T_1) )/ \
( k/(k - 1) - (L_BA + L_TF + L_TB)/R/(T_2 - T_1) - 1)

#34 Давление на выходе из колеса
p_2 = p_1*pow(T_2/T_1, n_2/(n_2 - 1))

#35 Плотность на выходе из колеса
rho_2 = p_2/R/T_2

#36 Окружная составляющая абсолютной скорости на выходе
c_2u = mu*(u_2 - c_2r/math.tan(math.radians(beta_2Blade)))

#37 Абсолютная скорость на выходе из колеса
c_2 = math.sqrt(pow(c_2u, 2) + pow(c_2r, 2))

#38 Окружная составляющая относительной скорости на выходе из колеса
w_2u = u_2 - c_2u

#39 Относительная скорость на выходе из колеса (c_2r = w_2r)
w_2 = math.sqrt(pow(w_2u, 2) + pow(c_2r, 2))

#40 Угол между векторами относительной/абсолютной и окружной скорости
#   на выходе из колеса
beta_2  = math.degrees(math.acos( w_2u/w_2 ))
alpha_2 = math.degrees(math.acos( c_2u/c_2 ))

#41 Ширина колеса на выходе из турбины
b_2 = G_K/math.pi/D_2/c_2r/rho_2/tau_2

#43 Температура заторможенного потока на выходе из колеса
T_2Stagn = T_2 + pow(c_2, 2)/2/c_p

if 'VANELESS' in diffuserType: # Расчёт параметров безлопаточного диффузора
    #44 Ширина безлопаточного диффузора на выходе
    b_4 = vanelessWideCoef*b_2

    #45 Диаметр безлопаточного диффузора на выходе
    D_4 = vanelessDiamCoef*D_2

    #46 Показатель политропы сжатия в диффузоре
    n_4 = (eta_diff*k/(k - 1))/(eta_diff*k/(k - 1) - 1)

    #47 Температура на выходе из диффузора
    # (методом последовательных приближений)
    T_4 = T_2
    validity = 1e-02
    while abs(diffOutTemp(b_2, D_2, T_2, c_2, b_4, D_4, T_4, n_4) - T_4) > validity:
        T_4 = T_4 + validity
    else:
        T_4 = diffOutTemp(b_2, D_2, T_2, c_2, b_4, D_4, T_4, n_4)

    #48 Давление на выходе из диффузора
    p_4 = p_2*pow(T_4/T_2, n_4/(n_4 - 1))

    #49 Плотность на выходе из колеса
    rho_4 = p_4/R/T_4

    #50 Скорость на выходе из диффузора
    c_4 = c_2*D_2*b_2*rho_2/D_4/b_4/rho_4

else: # Расчёт параметров лопаточного диффузора по МУ Федюшкина (F##)
    n_4 = n_diffuser

    #F50 Проверка на число лопаток относительно их количества в РК
    if (z_diffuser < z_K - 5) | (z_diffuser > z_K + 2):    exit('Error F50:\
 Number of diffuser vanes is not in the allowable diapason!\n\
It must be less than number of %0.0f blades the wheel.' %z_K)

    #44 Ширина безлопаточной части диффузора на выходе
    b_3 = vanelessWideCoef*b_2

    #45 Диаметр безлопаточной части диффузора на выходе
    D_3 = vanelessDiamCoef*D_2

    #46 Показатель политропы сжатия безлопаточной части диффузора
    n_3 = (eta_diff*k/(k - 1))/(eta_diff*k/(k - 1) - 1)

    #47 Температура на выходе из диффузора (методом
    #   последовательных приближений)
    T_3 = T_2 - 40
    validity = 1e-02
    while abs(diffOutTemp(b_2,D_2,T_2,c_2,b_3,D_3,T_3,n_3) - T_3) > validity:
        T_3 = T_3 + validity
    else:
        T_3 = diffOutTemp(b_2,D_2,T_2,c_2,b_3,D_3,T_3,n_3)

    #48 Давление на выходе из колеса
    p_3 = p_2*pow(T_3/T_2, n_3/(n_3 - 1))

    #49 Плотность на выходе из безлопаточной части диффузора
    rho_3 = p_3/R/T_3

    #F46 Скорость на выходе из безлопаточной части диффузора
    c_3 = c_2*D_2*b_2*rho_2/D_3/b_3/rho_3 

    #F47 Диаметр лопаточного диффузора на выходе
    D_4 = vanedDiamCoef*D_2

    #F48 Ширина лопаточного диффузора на выходе
    b_4 = vanedWideCoef*b_3

    #F49 Угол наклона лопаток на выходе из диффузора
    alpha_4 = alpha_2 + deltaDegDiff

    #F51 Температура на выходе из лопаточной части диффузора
    T_4 = T_3
    validity = 1e-02
    b_3COEF = b_3*tau_3*math.sin(math.radians(alpha_2))
    b_4COEF = b_4*tau_4*math.sin(math.radians(alpha_4))
    while abs(diffOutTemp(b_3COEF, D_3, T_3, c_3, b_4COEF, D_4, T_4, n_4) - T_4) > validity:
        T_4 = T_4 + validity
    else:
        T_4 = diffOutTemp(b_3COEF, D_3, T_3, c_3, b_4COEF, D_4, T_4, n_4)

    #F54 Давление и плотность на выходе из лопаточной части диффузора
    p_4 = p_2*pow(T_4/T_3, n_diffuser/(n_4 - 1))
    rho_4 = p_4/R/T_4

    #50 Скорость на выходе из диффузора
    c_4 = c_3*D_3*b_3COEF/D_4/b_4COEF/rho_4

#51 Скорость на выходе из компрессора
c_K = c_4/relDiffOutToCompOut 

#52 Температура на выходе из компрессора
T_K = T_4 + (pow(c_4, 2) - pow(c_K, 2))/2/c_p

#54 Давление на выходе из компрессора
p_K = p_4*pow(T_K/T_4, n_housing/(n_housing - 1))

#55 Температура заторможенного потока на выходе
T_KStagn = T_K + pow(c_K, 2)/2/c_p

#56 давление заторможенного потока на выходе
p_KStagn = p_K*pow(T_KStagn/T_K, k/(k - 1))

#57 Действительная степень повышения давления в компрессоре
Pi_KStagn = p_KStagn/p_0Stagn

#58 Изоэнтропная работа по расчётной степени повышения давления
L_KsStagnRated = c_p*T_0Stagn*(pow(Pi_KStagn, (k - 1)/k) - 1)

#59 Расчётный изоэнтропный КПД по заторможенным параметрам
eta_KsStagnRated = (pow(Pi_KStagn, (k - 1)/k) - 1) / (T_KStagn/T_0Stagn - 1)

#60 Расхождение с заданным КПД компрессора
differenceEta = abs(eta_KsStagnRated - eta_KsStagn)/eta_KsStagn*100

#61 Расчётный коэффициент напора по заторможенным параметрам
H_KsStagnRated = L_KsStagnRated/pow(u_2, 2)

#62 Расхождение с заданным КПД компрессора
differenceH = abs(H_KsStagnRated - H_KsStagn)/H_KsStagn*100

#63 Мощность затрачиваемая на привод компрессора
N_K = G_K*L_KsStagn/eta_KsStagnRated

#64 Полное давление перед впускными клапанами поршневой части
p_vStagn = p_KStagn*sigma_c*sigma_v

#65 Расхождение с предварительно оценнёной/заданной степенью повышения
#   давления компрессора
differencePi_K = abs(Pi_KStagn - Pi_K)/Pi_K*100 


# Displaying the results
# ~~~~~~~~~~~~~~~~~~~~~~
# Display some results right in the Terminal window
D_2_mm = D_2*1e+03
print('Diameter of the wheel is {0:.0f} mm\n' .format(D_2_mm)) # (15)

print('Parameters by cuts:')
if 'VANELESS' in diffuserType:  print('\
    1-1: T_1 = {0:.0f} K,   p_1 = {1:.4f} MPa\n\
    2-2: T_2 = {2:.0f} K,   p_2 = {3:.4f} MPa\n\
    4-4: T_4 = {4:.0f} K,   p_4 = {5:.4f} MPa\n'\
    .format(T_1, p_1*1e-06, T_2, p_2, T_4, p_4*1e-06))
else:   print('\
    1-1: T_1 = {0:.0f} K,   p_1 = {1:.4f} MPa\n\
    2-2: T_2 = {2:.0f} K,   p_2 = {3:.4f} MPa\n\
    3-3: T_3 = {4:.0f} K,   p_3 = {5:.4f} MPa\n\
    4-4: T_4 = {6:.0f} K,   p_4 = {7:.4f} MPa\n'\
    .format(T_1, p_1*1e-06, T_2, p_2*1e-06, T_3, p_3*1e-06, T_4, p_4*1e-06))
        
print('Actual pressure degree increase is {0:.2f}, when\n\
precalculated/set pressure degree increase is {1:.2f}'\
    .format(Pi_KStagn, Pi_K)) # (57)
print('Error of calculation between them is {0:.3f}%\n'\
    .format(differencePi_K)) # (60)
    
print("Energy conversion efficiency coeficients are:\n\
    eta_Ks*  = {0:.4f} - set\n\
    eta_Ks*' = {1:.4f} - rated"\
    .format(eta_KsStagn, eta_KsStagnRated)) # (dict) & (59)
print('Error of calculation between them is {0:.3f}%\n'\
    .format(differenceEta)) # (60)

print("Isentropy head coeficients are:\n\
    H_Ks*  = {0:.4f} - set\n\
    H_Ks*' = {1:.4f} - rated"\
    .format(H_KsStagn, H_KsStagnRated)) # (dict) & (61)
print('Error of calculation between them is {0:.3f}%\n'\
    .format(differenceH)) # (62)

print("If something doesn't work correctly make a new issue or check the others:\n\
https://github.com/StasF1/turboCharger/issues")

# Make extra dictionary for turbine calculation
exec(compile(open('include/savingParametersForTurbine.py', "rb").read(),
                  'include/savingParametersForTurbine.py', 'exec'))


# Generate report
# ~~~~~~~~~~~~~~~
# Create a report
if 'VANELESS' in diffuserType: # Vaneless diffuser | БЛД
    exec(compile(open('include/reportGeneratorVANELESS.py', "rb").read(),
                      'include/reportGeneratorVANELESS.py', 'exec'))
else: # Vaned diffuser | ЛД
    exec(compile(open('include/reportGeneratorVANED.py', "rb").read(),
                      'include/reportGeneratorVANED.py', 'exec'))

# Edit pictures
exec(compile(open('include/picturesEditor.py', "rb").read(),
                  'include/picturesEditor.py', 'exec'))
# Save the results to the results/ folder
exec(compile(open('include/createResultsFolder.py', "rb").read(),
                  'include/createResultsFolder.py', 'exec'))


# ''' (C) 2018-2020 Stanislau Stasheuski '''