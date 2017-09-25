open -a Xquartz

docker build -t hi .

# start this socat thing that lets docker send data to the XQuartz
# if it errors about the port in use then get the PID with this: lsof -i tcp:6000
socat TCP-LISTEN:6000,reuseaddr,fork UNIX-CLIENT:\"$DISPLAY\" &

# get the IP address for the display
docker run -e DISPLAY=$((ifconfig en0 && ifconfig en1) | grep 'inet '|awk '{print $2}'):0 hi

killall socat
