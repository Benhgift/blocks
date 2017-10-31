open -a Xquartz

docker build -t hi .

# Socat likes to stick around and hog the port
killall socat
kill $(lsof -i tcp:6000 | grep LISTEN | awk '{print $2}')
sleep .3
# BLAST IT TO SPACE
kill -9 $(lsof -i tcp:6000 | grep LISTEN | awk '{print $2}')

socat TCP-LISTEN:6000,reuseaddr,fork UNIX-CLIENT:\"$DISPLAY\" &

# get the IP address for the display
docker run -e DISPLAY=$((ifconfig en0 && ifconfig en1) | grep 'inet '|awk '{print $2}'):0 hi

killall socat
