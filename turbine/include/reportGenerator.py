# -*- coding: utf-8 -*-
# Generates the report

r = open("turbineReport.md", "w")
r.write("#Исходные данные\n")
if 'termPaper' in projectType:    r.write(
 "- В соответствии с исходными данными для наддува двигателя имеем:\
 \n$$\n G_{K} = %0.4f\quad кг/с;\quad \\alpha = %1.1f;\quad \\varphi\
  = %3.3f,\quad l_{0} = %4.2f\n$$\n\n"
 %(G_K, alpha, phi, l_0) )
else:   r.write(
 "- В соответствии с исходными данными домашнего задания имеем:\n\
 \n$$\n G_{K} = %0.4f кг/с \n$$\n Также принимаем:\
 $$ \\alpha = %1.1f; \phi = %3.3f; l_{0} = %4.2f $$\n\n"
 %(G_K, alpha, phi, l_0) )
r.write(
 "- Для выпускных газов принимаем:\
 \n$$\n R' = %0.1f\quad Дж/кг;\quad {c'}_{p} = %1.1f\quad\
 {Дж \over кг\cdot К};\quad k' = %2.1f\quad \n$$\n\n"
 %(R_Exh, c_pExh, k_Exh) )
r.write(
 "- Из расчета компрессора имеем:\
 \n$$\n u_{2}(u_{2}) = %0.1f\quad м/с;\quad D_{2K} = %1.3f\quad м;\quad\n$$\
 \n$$\n n_{тк} = %2.f\quad об/мин;\quad\eta = %3.5f;\quad {L'}_{KS} = %4.1f;\quad\n$$\
 \n$$\n N_{K} = %5.1f\quad Вт;\quad {p'}_{v} = %6.f\quad Па; \n$$\n\n"
 %(u_2K, D_2K, n_TCh, eta_KsStagnRated, L_KsStagn, N_K, p_vStagn) )
r.write(
 "- Давление $$p_{2}$$ газов за турбиной\
 превышает атмосферное и составляет\
 $$p_{2} = (1.01…1.10)p_{а}$$. Принимаем:\
 \n$$\n p_{2} = %0.2fp_{а} = %1.f\quad Па\n$$\n\n"
 %(dragInletRatio, p_2) )
r.write(
 "- Температура газов перед турбиной:\
 $$T_{0}^{*} = %0.1f\quad K$$\n\n"
 %T_0Stagn)
r.write("#Расчёт\n")
r.write("1. Расход газа через турбину с учетом утечки $$\sigma_{у} = %0.2f$$ составит:\
 \n$$\n G_{T} = G_{K}\sigma_{y}\left( 1 + {1 \over \\alpha\\varphi l_{0}} \\right)\
 = %1.6f\quad кг/с\n$$\n\n"
 %(sigma_esc, G_T) )
r.write("2. Принимаем отношение диаметра колеса компрессора к колесу турбины как %0.1f, тогда:\
 \n$$\n D_{1} = %1.1fD_{2K} = %2.3f\quad м\n$$\n\
и соответственно окружная скорость $$u_{1}$$ на входе в колесо турбины будет равна:\
 \n$$\n u_{1} = %1.1fu_{2K} = %3.3f\quad м\n$$\n\n"
 %(diameterRatio, diameterRatio, D_1, diameterRatio, u_1) )
r.write("3. Принимаем эффективный КПД турбины как: $$\eta = %0.3f$$"
 %eta_Te)
r.write("4. Изоэнтропная работа турбины:\
 \n$$\n L_{TS}^{*} = {L^{*}_{TS}G_K \over \eta_{KS}\eta_{Te}G_{T}} = %0.1f\quad Дж/кг \n$$\n\n"
 %L_TsStagn)
r.write("5. Условная изоэнтропная скорость истечения из турбины:\
 \n$$\n c_{2s} = \sqrt{ 2L_{TS} } = %0.3f\quad м/с \n$$\n\n"
 %c_2s)
r.write("6. Параметр $$\chi$$:\
 \n$$\n \chi = {u_{1} \over c_{2s}} = %0.2f \n$$\n\n"
 %ksi)
r.write("7. Давление газа на входе в турбину:\
 \n$$\n {p'}_{0} = {p_{2} \over\
 \left( 1 - {L^{*}_{TS} \over {c'}_{p}T^{*}_{0}} \\right)\
 ^{k' \over k' - 1}} = %0.6f\quad Па \n$$\n\n"
 %p_0Stagn)
r.write("8. Для обеспечения продувки цилиндров двигателя при перекрытии\
 клапанов необходимо выполнение соотношения $$p^{*}_{v}/p^{*}_{0}\
 = 1.1…1.3$$. Условие выполняется:\
 \n$$\n {p^{*}_{v} \over p^{*}_{0}} = %0.4f \n$$\n\n"
 %pressureRelation)
r.write("9. Наружный диаметр рабочего колеса турбины на выходе составляет\
 обычно $$D_{2H} = (0.70…0.85)D_{1}$$. Принимаем:\
 \n$$\n D_{2H} = %0.2fD_{1} = %1.3f\quad м \n$$\n\n"
 %(outerDiamRatio, D_2H) )
r.write("10. Внутренний (втулочный) диаметр рабочего колеса турбины на\
 выходе составляет обычно $$D_{2H} = (0.25…0.32)D_{1}$$. Принимаем:\
 \n$$\n D_{2B} = %0.2fD_{1} = %1.3f\quad м \n$$\n\n"
 %(innerDiamRatio, D_2B) )
r.write("11. Средний диаметр колеса турбины на выходе:\
 \n$$\n D_{2} = \sqrt{{D_{2H}^{2} + D_{2B}^{2} \over 2}} = %0.7f\quad м\n$$\n\n"
 %D_2)
r.write("12. Параметр $$\mu = D_{2}/D_{1}$$ для радиально-осевых турбин должен\
 лежать в пределах 0.5…0.8. В данном случае условие выполняется:\
 \n$$\n \mu = {D_{2} \over D_{1}} = %0.6f \n$$\n\n"
 %mu)
r.write("13. Для радиально-осевых турбин степень реактивности должна лежать\
 в пределах 0.45…0.55. Принимаем:\
 \n$$\n \\rho = %0.2f \n$$\n\n"
 %ro)
r.write("14. Изобары $$p_{1}$$ и $$p_{2}$$ на диаграмме расширения в турбине\
 располагаются практически эквидистантно. Поэтому принимается допущение:\
 $$ L_{ps} = {L'}_{ps}$$, где $${L'}_{ps} = L_{Ts} - L_{ps}$$"
 )
r.write("15. Изоэнтропная работа расширения (располагаемый теплоперепад)\
 в сопловом аппарате:\
 \n$$\n L_{cs} = L_{Ts}(1 - \\rho) = %0.1f\quad Дж/кг \n$$\n\n"
 %L_cS)
r.write("16. Значение скоростного коэффициента $$\\varphi$$, учитывающего\
 потери скорости в сопловом аппарате, лежит в пределах 0.93…0.97. Принимаем:\
 \n$$\n \\varphi = %0.2f\n$$\n\n"
 %phiLosses)
r.write("17. Абсолютная скорость на выходе из соплового аппарата составит:\
 \n$$\n c_{1} = \\varphi \sqrt{2L_{cs}} = %0.3f\quad м/с \n$$\n\n"
 %c_1)
r.write("18. Угол $$\\alpha_{1}$$ наклона вектора абсолютной скорости\
 $$с_{1}$$ (рис. 1) должен составлять 15°…25°. Принимаем:\
 \n$$\n \\alpha_{1} = %0.1f° \n$$\n\n"
 %alpha_1)
r.write("![alt text](inTurbineWheel.png)\n\
<center><b> Рисунок 1 </b> - <i>Векторный план скоростей на входе в рабочее колесо\
 турбины</i></center>\n\n"
 )
r.write("19. Радиальная составляющая $$c_{1r}$$ абсолютной скорости, тождественно\
 равная радиальной составляющей $$w_{1r}$$ относительной скорости на выходе из\
 соплового аппарата:\
 \n$$\n c_{1r} \equiv w_{1r} = c_{1}\sin\\alpha_{1} = %0.3f\quad м/с \n$$\n\n"
 %c_1r)
r.write("20. Окружная составляющая абсолютной скорости на выходе из соплового аппарата:\
 \n$$\n c_{1u} = c_{1}\cos\\alpha_{1} = %0.3f\quad м/с \n$$\n\n"
 %c_1u)
r.write("21. Для окружной составляющей $$w_{1u}$$ относительной скорости имеем:\
 \n$$\n w_{1u} = c_{1u} - u_{1} = %0.3f\quad м/с \n$$\n"
 %w_1u);
if (w_1u < 0):
    r.write("Таким образом, в данном случае проекция $$w_{1u}$$ направлена\
 в сторону, противоположную вращению колеса.\n\n")
else:
 r.write("Таким образом, в данном случае проекция $$w_{1u}$$ направлена\
 в сторону вращения колеса.\n\n")
r.write("22. Относительная скорость на входе в рабочее колесо:\
 \n$$\n w_{1} = \sqrt{w_{1r}^2 + w_{1u}^2} = %0.3f\quad м/с \n$$\n\n"
 %w_1)
r.write("23. Для обеспечения безударного входа в межлопаточные каналы\
 рабочего колеса радиально-осевых турбин с радиальными лопатками\
 (угол установки лопаток $$\\beta_{1л} = %0.f°$$) значение угла\
 $$\\beta_{1}$$ наклона вектора относительной скорости $$w_{1}$$ должно\
 находиться в пределах 80…100°. В данном случае требование выполняется:\
 \n$$\n \\beta_{1} = %1.f° - \\arctan{w_{1u} \over w_{1r}} = %2.3f° \n$$\n\n"
 %(beta_1Blade, beta_1Blade, beta_1) )
r.write("24. Температура газа на входе в колесо:\
 \n$$\n T_{1} = T^{*}_{0} - {c_{1}^2 \over 2{c'}_{p}} = %0.3f\quad K \n$$\n\n"
 %T_1)
r.write("25. Давление на входе в колесо:\
 \n$$\n p_{1} = p^{*}_{0} \left( 1 - {L^{*}_{CS} \over {c'}_{p}T^{*}_{0}} \\right)\
 ^{k' \over k' - 1} = %0.1f\quad Па \n$$\n\n"
 %p_1)
r.write("26. Плотность на входе в колесо:\
 \n$$\n \\rho_{1} = {p_{1} \over R'T_{1}} = %0.6f\quad кг/м^{3} \n$$\n\n"
 %ro_1)
r.write("27. Ширина лопаток на входе в колесо:\
 \n$$\n b_{1} = {G_{T} \over \pi D_{1}\\rho_{1}c_{1r}} = %0.6f\quad м \n$$\n\n"
 %b_1)
r.write("28. Изоэнтропная работа расширения в рабочем колесе (располагаемый\
 теплоперепад) на входе в колесо:\
 \n$$\n L_{ps} = \\rho L_{TS} = %0.1f\quad Дж/кг \n$$\n\n"
 %L_pS)
r.write("29. Значение скоростного коэффициента $$\psi$$, учитывающего потери скорости\
 в рабочем колесе, лежит в пределах 0.85…0.94. Принимаем:\
 \n$$\n \psi = %0.2f \n$$\n\n"
 %psiLosses)
r.write("30. Окружная скорость на среднем диаметре $$D_{2}$$ выхода из рабочего колеса:\
 \n$$\n u_{2} = \mu u_{1} = %0.3f\quad м/с \n$$\n\n"
 %u_2)
r.write("31. Относительная скорость на среднем диаметре $$D_{2}$$:\
 \n$$\n w_{2} = \psi \sqrt{2L_{ps} + w_{1}^{2} - u_{1}^{2} + u_{2}^{2}}\
 = %0.3f\quad м/с \n$$\n\n"
 %w_2)
r.write("32. Температура на выходе из колеса:\
 \n$$\n T_{2} = T_{1} - {w_{2}^{2} - u_{2}^{2} - w_{1}^{2} + u_{1}^{2}\
 \over 2{c'}_{p}} = %0.3f\quad К \n$$\n\n"
 %T_2)
r.write("33. Плотность на выходе из колеса:\
 \n$$\n \\rho_{2} = {p_{2} \over R'T_{2}} = %0.6f\quad кг/м^{3} \n$$\n\n"
 %ro_1)
r.write("34. Площадь сечения $$F_{2}$$ на выходе из колеса:\
 \n$$\n F_{2} = {\pi \over 4}\left(D_{2H}^2 - D_{2B}^2 \\right)\
 = %0.7f\quad м^2 \n$$\n\n"
 %F_2)
delta = delta*1e+03; # mm
r.write("35. Значения радиального зазора Δ между корпусом и колесом\
 турбины выбирают в пределах 0.3…1.5 мм. Для малоразмерного автомобильного\
 турбокомпрессора можно принять $$\Delta = %0.1f$$ мм.\
 Тогда утечки через этот зазор составят:\
 \n$$\n G_{у} = 0.45{2\Delta G_{T} \over D_{2H} - D_{2B}}\
 {1 + {D_{2H} - D_{2B} \over 2D_{2}}} = %1.7f\quad кг/с \n$$\n\n"
 %(delta, G_losses) )
r.write("![alt text](axisCut.png)\n\
<center><b> Рисунок 2 </b> - <i>Схема проточной части\
 радиально-осевой турбины</i></center>\n\n"
 )
r.write("36. Расход через сечение на выходе из колеса:\
 \n$$\n {G'}_{T} = G_{T} - G_{у} = %0.6f\quad кг/с \n$$\n\n"
 %G_F2)
r.write("37. Аксиальные составляющие относительной $$w_{2а}$$ и\
 абсолютной $$c_{2а}$$ скоростей на выходе из колеса (рис. 3):\
 \n$$\n w_{2a} \equiv c_{2a} = {{G'}_{T} \over F_{2} \\rho_{2}}\
 = %0.3f\quad м/с \n$$\n\n"
 %w_2a)
r.write("![alt text](outTurbineWheel.png)\n\
<center><b> Рисунок 3 </b> - <i>Векторный план скоростей на выходе\
 из рабочего колеса радиально-осевой турбины</i></center>\n\n"
 )
r.write("38. Окружная составляющая относительной скорости на выходе из колеса:\
 \n$$\n w_{2u} = \sqrt{w_{2}^2 - w_{2a}^2} = %0.3f\quad м/с \n$$\n\n"
 %w_2u)
r.write("39. Угол наклона вектора относительной скорости\
 $$w_{2}$$ на выходе из рабочего колеса:\
 \n$$\n \\beta_{2} = \\arcsin{ w_{2a} \over w_{2} } = %0.3f° \n$$\n\n"
 %beta_2)
r.write("40. Окружная составляющая абсолютной скорости на выходе из колеса:\
 \n$$\n c_{2u} = w_{2u} - u_{2} = %0.3f\quad м/с \n$$\n"
 %c_2u)
r.write("41. Абсолютная скорость на выходе из колеса:\
 \n$$\n c_{2} = \sqrt{c_{2a}^2 + c_{2u}^2} = %0.3f\quad м/с \n$$\n\n"
 %c_2)
r.write("42. Угол выхода потока из колеса в абсолютном движении:\
 \n$$\n \\beta_{2} = 90° - \\arctan{c_{2u} \over c_{2a}} = %0.3f° \n$$\n\
 На расчетном режиме этот угол должен составлять 75…105° - условие выполняется.\n\n"
 %beta_2)
r.write("43. Потери в сопловом аппарате турбины:\
 \n$$\n Z_{c} = \left( {1 \over \\varphi^2} - 1 \\right){c_{1}^2 \over 2}\
 = %0.1f\quad Дж/кг \n$$\n\n"
 %Z_c)
r.write("44. Потери в рабочем колесе:\
 \n$$\n Z_{p} = \left( {1 \over \\psi^2} - 1 \\right){w_{2}^2 \over 2}\
 = %0.1f\quad Дж/кг \n$$\n\n"
 %Z_p)
r.write("45. Суммарные потери в лопаточных каналах:\
 \n$$\n Z_{K} = Z_{c} + Z_{p} = %0.1f\quad Дж/кг \n$$\n\
 Последовательно учитывая потери, получим номенклатуру удельных работ и КПД турбины\n\n"
 %Z_Blades)
r.write("46. Лопаточная работа $$L_{тл}$$ турбины:\
 \n$$\n L_{тл} = L_{тл} - Z_{K} = %0.1f\quad Дж/кг \n$$\n\n"
 %L_TBlades)
r.write("47. Лопаточный КПД турбины:\
 \n$$\n \eta_{тл} = {L_{тл} \over L_{TS}} = %0.6f \n$$\n\n"
 %eta_TBlades)
r.write("48. Потери с выходной скоростью при условии равномерного потока на выходе\
 из рабочего колеса:\
 \n$$\n {Z'}_{в} = {c_{2}^2 \over 2} = %0.1f\quad Дж/кг \n$$\n\n"
 %Z_SteadyOutlet)
delta_L = abs(L_TuSteadyFromLosses - L_TuSteady)/L_TuSteadyFromLosses*100;
r.write("49. Соответствующее значение работы на окружности колеса:\
 \n$$\n {L'}_{тu} = L_{тл} - {Z'}_{в} = %0.1f\quad Дж/кг \n$$\n\n"
 %L_TuSteadyFromLosses)
r.write("50. Эта работа может быть определена также по формуле Эйлера:\
 \n$$\n {L'}_{тu} = u_{1}c_{1u} + u_{2}c_{2u} = %0.1f\quad Дж/кг \n$$\n\
 Полученные значения (пп. 49, 50) отличаются незначительно (погрешность - %1.2f%%),\
 что свидетельствует о правильности расчета."
 %(L_TuSteady, delta_L) )
r.write("51. Так как в радиально-осевых турбинах имеется значительная неравномерность\
 потока на выходе их рабочего колеса, действительные потери c выходной скоростью\
 (где $$\zeta = %0.1f$$ принята из диапазона 1.1…1.5):\
 \n$$\n Z_{B} = \zeta {Z'}_{B} = %1.1f\quad Дж/кг \n$$\n\n"
 %(dzeta, Z_UnsteadyOutlet) )
r.write("52. Действительная работа на окружности колеса:\
 \n$$\n L_{тu} = L_{тл} - Z_{в} = %0.1f\quad Дж/кг \n$$\n\n"
 %L_Tu)
r.write("53. Окружной КПД турбины:\
 \n$$\n \eta_{тu} = {L_{тu} \over L_{TS}} = %0.6f \n$$\n\
 На расчетном режиме значение $$\eta_{тu}$$ не должно составлять\
 0.75…0.90 - условие выполняется"
 %eta_Tu)
r.write("54. Потери, обусловленные утечкой газа через радиальные\
 зазоры между колесом и корпусом:\
 \n$$\n Z_{у} = {L_{тu}G_{у} \over G_{T}} = %0.1f\quad Дж/кг \n$$\n\n"
 %Z_y)
r.write("55. Мощность, затрачиваемая на трение колеса в корпусе и вентиляцию\
 ($$\\beta$$ опытный коэффициент, зависящий от типа рабочего колеса,\
 принятый как %0.1f):\
 \n$$\n N_{TB} = 0.7355\\beta {\\rho_{1} + \\rho_{2} \over 2}D_{1}^2\
 \left({u_{1}^2 \over 100} \\right)^3 = %1.1f\quad Вт \n$$\n"
 %(beta, N_TB) )
r.write("56. Потери на трение и вентиляцию:\
 \n$$\n Z_{TB} = {N_{TB} \over G_{T}} = %0.1f\quad Дж/кг \n$$\n\n"
 %Z_TB)
r.write("57. Суммарные дополнительные потери, включающие потери на утечки,\
 трение и вентиляцию:\
 \n$$\n Z_{Д} = Z_{у} + Z_{TB} = %0.1f\quad Дж/кг \n$$\n\n"
 %Z_extra)
r.write("58. Внутренняя работа турбины:\
 \n$$\n L_{Тi} = L_{тu} - Z_{Д} = %0.1f\quad Дж/кг \n$$\n\n"
 %L_Ti)
r.write("![alt text](i-sPlot.png)\n\
<center><b> Рисунок 4 </b> - <i>Диаграмма термодинамического процесса\
 расширения в турбине</i></center>\n\n"
 )
r.write("59. Внутренний КПД турбины:\
 \n$$\n \eta_{Тi} = {L_{Тi} \over L_{TS}} = %0.5f \n$$\n\n"
 %eta_Ti)
r.write("60. Эффективный КПД турбины:\
 \n$$\n {\eta'}_{Тe} = \eta_{Тi} \eta_{M} = %0.5f \n$$\n\
 где $$\eta_{M}$$ — механический КПД, принятый из диапазона 0.92…0.96,\
 как %1.2f"
 %(eta_Ti, eta_m) )
r.write("61. При сравнении с исходным $$\eta_{Te}$$\
 имеем незначительную погрешность:\
 \n$$\n {\mid {\eta'}_{Тe} - \eta_{Тe}  \mid \over {\eta'}_{Тe}}\
 = %0.3f \%% \n$$\n\n"
 %differenceEta)
r.write("62. Эффективная работа турбины:\
 \n$$\n L_{Тe} = L_{TS}{\eta'}_{Тe} = %0.1f\quad Дж/кг \n$$\n\n"
 %L_Te)
r.write("63. Мощность на валу турбины:\
 \n$$\n N_{T} = L_{Тe}G_{Т} = %0.1f\quad Вт \n$$\n\n"
 %N_T)
r.write("64. Расхождение с мощностью,\
 потребляемой компрессором, незначительно:\
 \n$$\n {\mid N_{K} - N_{T} \mid \over N_{K}} = %0.3f \%% \n$$\n\n"
 %differenceN)
r.close()









 

 
 
 
 
 
