set -e
BASE=`pwd`

choco install python

"C:\\Program Files (x86)\\Microsoft Visual Studio 14.0\\VC\\vcvarsall.bat"
export CL="\"-FIC:\\Program Files (x86)\\Microsoft Visual Studio 14.0\\VC\\include\\stdint.h\" $CL"
"C:\\Python37\\Scripts\\pip.exe" install -r requirements.txt
"C:\\Python37\\python.exe setup.py bdist_msi
ls -la dist/
cp dist/*.msi "Open Media Library.msi"
