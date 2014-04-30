The GUI was created using Qt 4 Designer

AutoPi.py & Media_Buttons_rc.py are auto generated using the qt4 dev utils

If you make any changes to the GUI, run these commands to regen the required python files.

"pyuic4 AutoPi.ui -o AutoPi.py"
"pyrcc4 Media_Buttons.qrc -o Media_Buttons_rc.py"

After that, you can execute the GUI, by calling the script I created.

"python AutoPiGui.py"
