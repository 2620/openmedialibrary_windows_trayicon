set -e
BASE=`pwd`

choco install python

python="C:\\Python37\\python.exe"

"C:\\Program Files (x86)\\Microsoft Visual Studio 14.0\\VC\\vcvarsall.bat"
export CL="\"-FIC:\\Program Files (x86)\\Microsoft Visual Studio 14.0\\VC\\include\\stdint.h\" $CL"
"C:\\Python37\\Scripts\\pip.exe" install -r requirements.txt
$python setup.py bdist_msi
ls -la dist/
mv dist/*.msi "Open_Media_Library.msi"
