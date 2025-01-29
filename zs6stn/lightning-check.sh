#!/bin/bash
export output=/home/hubzanet/weatherbug-spark/zs6stn/output.txt
cd /home/hubzanet/weatherbug-spark/zs6stn
rm output.txt
#echo -n "Lighting Warning! " > $output
#python3 /home/hubzanet/weatherbug-spark/zs6stn/check-stn-lightning.py >> $output
python3 /home/hubzanet/weatherbug-spark/zs6stn/multiple-site-check.py >> $output

export MSG=$(cat output.txt)

#echo $(xargs -I{lin} echo \"{lin}\" < $output) > $output

echo "Checking output..."
cat $output

if grep -q "No Lightning" "$output"; then
  echo "No Lightning!" #Some Actions # SomeString was found
#  asl-tts -n 603580 -t "${MSG}"
else
  echo "Lightning Detected!"
  /usr/bin/asl-tts -n 617050 -t "${MSG}"  >> /home/hubzanet/weatherbug-spark/zs6stn/log.log
fi

