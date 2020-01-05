dpi_info=`identify -verbose screen.png | grep 'Resolution\|Units'`;
threshold_dpi=`expr 600 \* 600`;
dpi_info=${dpi_info#*:};
dpi_info=${dpi_info%Units:*};
dipw=${dpi_info%x*};
dipw=`(echo $dipw | awk '{printf("%d",$1 + 0.5)}')`
diph=${dpi_info#*x};
diph=`(echo $diph | awk '{printf("%d",$1 + 0.5)}')`
dpi_size=`expr $dipw \* $diph`;
echo $dipw x $diph = $dpi_size \>= $threshold_dpi;
if [ $dpi_size -lt $threshold_dpi ] || [ $dipw == Undefined ]; then
  echo convert screen.png -density 600 -units PixelsPerInch screen.png;
  convert screen.png -density 600 -units PixelsPerInch screen.png;
fi;
w=`identify -format %[width] screen.png`;
h=`identify -format %[height] screen.png`;
threshold=`expr 1000 \* 1000`;
size=`expr $w \* $h`;
echo $w x $h = $size \>= $threshold;
if [ $size -lt $threshold ]; then 
  percent=`expr $threshold \/ $size \* 100`;
  convert -geometry "${percent}"% screen.png screen.png;
  echo convert -geometry "${percent}"% screen.png screen.png;
fi;
tesseract screen.png res -l jpn+eng txt;
echo Done OCR;
python3 modifyText.py $1