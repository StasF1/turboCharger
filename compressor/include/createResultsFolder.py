# -*- coding: utf-8 -*-
# Creates folder with compressorResults and move them there

# Creating directory if needed 
if not os.path.exists("compressorResults"):   os.makedirs("compressorResults")

shutil.move("solvedParameters.py",   "../turbine/solvedParameters.py")

shutil.copyfile("compressorDict.py", "compressorResults/compressorDict.py")
shutil.move("compressorReport.md",   "compressorResults/compressorReport.md")
shutil.move("axisCut.png",           "compressorResults/axisCut.png")
shutil.move("blades.png",            "compressorResults/blades.png")
shutil.move("outWheel.png",          "compressorResults/outWheel.png")