set -e
BASE=`pwd`

choco install python

"C:\\Program Files (x86)\\Microsoft Visual Studio 14.0\\VC\\vcvarsall.bat"
export CL="\"-FIC:\\Program Files (x86)\\Microsoft Visual Studio 14.0\\VC\\include\\stdint.h\" $CL"
"C:\\Python37\\Scripts\\pip.exe" install pywin32
python=""C:\\Python37\\python.exe"
git clone https://github.com/anthony-tuininga/cx_Freeze/
cd cx_Freeze
git checkout v6.0b1
$python setup build
$python setup install
cd $BASE
$python setup.py bdist_msi
ls -la dist/
cp dist/*.msi "Open Media Library.msi"
