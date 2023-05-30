source ./env/bin/activate

rm -f fifo
mkfifo fifo


python3 registry_server.py $1 > fifo &


for i in $(seq $1); do

    python3 server.py > fifo &
done

tail fifo