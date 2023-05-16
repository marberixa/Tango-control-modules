# Управление датчиком массы через Sardana
## Описание
Последовательное выполнение приведенных в таблице команд ("spec commands") позволяет осуществить считывание показаний датчика массы и запуск их автоматического измерения во времени. Запуск команд осуществляется из командной строки. Результаты выполнения этих команд приведены в папке Visualization.
## spec commands
| Команда  | Назначение | Пример использования |
| :--- | :--- | :--- |
| lsctrl  | вывод всех доступных управляющих модулей  | lsctrl
| defctrl  | объявление управляющего модуля | defctrl WeightSensorController wsensor1
| defelem | объявление экземпляра управляющего модуля  | defelem ws1 wsensor1 1
| defmeas | объявление измерительной группы | defmeas meas2 ws1 zerod01
| lsmeas | вывод всех доступных измерительных групп | lsmeas
| set_meas | назначение главной измерительной группы (считывание происходит только с тех устройств, которые к ней относятся) | set_meas meas2
| dscan | запуск сканирования с заданным кол-вом измерений | dscan mot01 2 -2 10
Подробнее о разных командах можно узнать из [документации](https://sardana-controls.org/devel/api/sardana/macroserver/macros.html).