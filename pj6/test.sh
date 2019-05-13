#!/bin/bash

function end_case {
    echo 'e1 echo "======"'
    echo e1 sleep 2
}

function test_tcp {
    echo $1 timeout 5 python test-tcp-client.py $2 $3
    end_case
}
function test_udp {
    echo $1 timeout 5 python test-udp-client.py $2 $3
    end_case
}
function test_ping {
    echo $1 ping -c 2 $2
    end_case
}

echo 'e1 echo -e "====== Ping All ======"'
echo pingall
echo 'e1 echo -e "====== Ping All ======"'
echo pingall

# Start servers on 1234 for connectivity tests
hosts="e1 e2 e3 mobile1 server1 server2 server3 w1 w2 w3"
for h in $hosts
do
    echo "$h python test-udp-server.py $h 1234 > /dev/null 2>&1 &"
    echo "$h python test-tcp-server.py $h 1234 > /dev/null 2>&1 &"
done
echo 'e1 echo -e "====== Wait for all servers on 1234 ======"'
echo e1 sleep 2

# Prohibit connections to PPTP service on server2 (TCP port 1723)
echo 'e1 echo -e "\n====== Prohibit connections to PPTP service on server2 (TCP port 1723) ======\n"'
echo "server2 python test-udp-server.py server2 1723 > /dev/null 2>&1 &"
echo "server2 python test-tcp-server.py server2 1723 > /dev/null 2>&1 &"
echo 'e1 echo -e "====== Wait for servers on server2:1723 ======"'
echo e1 sleep 2

echo 'e1 echo -e "====== Should NOT connect ======"'
end_case

test_tcp e1 server2 1723

echo 'e1 echo -e "====== Should connect ======"'
end_case

test_udp e1 server2 1234
test_tcp e1 server2 1234
test_udp e1 server2 1723
test_ping e1 server2

# Prohibit SSH connections to e1-e3 (TCP and UPD port 22)
echo 'e1 echo -e "\n====== Prohibit SSH connections to e1-e3 (TCP and UPD port 22) ======\n"'
hosts="e1 e2 e3"
for h in $hosts
do
    echo "$h python test-udp-server.py $h 22 > /dev/null 2>&1 &"
    echo "$h python test-tcp-server.py $h 22 > /dev/null 2>&1 &"
done
echo 'e1 echo -e "====== Wait for servers e1 e2 e3 on 22 ======"'
echo e1 sleep 2

echo 'e1 echo -e "====== Should NOT connect ======"'
end_case

test_tcp e2 e1 22
test_tcp e3 e2 22
test_tcp e1 e3 22

test_tcp w1 e1 22
test_tcp w1 e2 22
test_tcp w1 e3 22

test_udp e2 e1 22
test_udp e3 e2 22
test_udp e1 e3 22

test_udp w1 e1 22
test_udp w1 e2 22
test_udp w1 e3 22

echo 'e1 echo -e "====== Should connect ======"'
end_case

test_tcp e2 e1 1234
test_tcp e3 e2 1234
test_tcp e1 e3 1234

test_tcp w1 e1 1234
test_tcp w1 e2 1234
test_tcp w1 e3 1234

test_udp e2 e1 1234
test_udp e3 e2 1234
test_udp e1 e3 1234

test_udp w1 e1 1234
test_udp w1 e2 1234
test_udp w1 e3 1234

test_ping e2 e1
test_ping e3 e2
test_ping e1 e3

test_ping w1 e1
test_ping w1 e2
test_ping w1 e3

# Prohibit connections to DNS and NTP (UDP 53 and 123) on server1 and server2,
# but should be accessible on server3
echo 'e1 echo -e "\n====== Prohibit connections to DNS/NTP (UDP 53/123) on server1/server2 ======\n"'
hosts="server1 server2 server3"
for h in $hosts
do
    echo "$h python test-udp-server.py $h 53 > /dev/null 2>&1 &"
    echo "$h python test-udp-server.py $h 123 > /dev/null 2>&1 &"
    echo "$h python test-tcp-server.py $h 53 > /dev/null 2>&1 &"
    echo "$h python test-tcp-server.py $h 123 > /dev/null 2>&1 &"
done
echo 'e1 echo -e "====== Wait for UDP servers server1 server2 server3 on 53 123 ======"'
echo e1 sleep 2

echo 'e1 echo -e "====== Should NOT connect ======"'
end_case

test_udp e1 server1 53
test_udp e1 server1 123
test_udp e1 server2 53
test_udp e1 server2 123

echo 'e1 echo -e "====== Should connect ======"'
end_case

test_udp e1 server3 53
test_udp e1 server3 123

test_tcp e1 server1 53
test_tcp e1 server1 123
test_tcp e1 server2 53
test_tcp e1 server2 123
test_tcp e1 server3 53
test_tcp e1 server3 123

test_ping e1 server1
test_ping e1 server2
test_ping e1 server3

# Prohibit w1 and w2 from pinging mobile1 (response is not completed)
echo 'e1 echo -e "\n====== Prohibit w1 and w2 from pinging mobile1 ======\n"'
echo 'e1 echo -e "====== Should NOT connect ======"'
end_case

test_ping w1 mobile1
test_ping w2 mobile1

echo 'e1 echo -e "====== Should connect ======"'
end_case

test_ping w3 mobile1

test_tcp w1 mobile1 1234
test_tcp w2 mobile1 1234
test_tcp w3 mobile1 1234

test_udp w1 mobile1 1234
test_udp w2 mobile1 1234
test_udp w3 mobile1 1234

# Prohibit all traffic to TCP 9950-9952 on e3 from e1
echo 'e1 echo -e "\n====== Prohibit all traffic to TCP 9950-9952 on e3 from e1 ======\n"'
echo "e3 python test-udp-server.py e3 9950 > /dev/null 2>&1 &"
echo "e3 python test-udp-server.py e3 9951 > /dev/null 2>&1 &"
echo "e3 python test-udp-server.py e3 9952 > /dev/null 2>&1 &"
echo "e3 python test-tcp-server.py e3 9950 > /dev/null 2>&1 &"
echo "e3 python test-tcp-server.py e3 9951 > /dev/null 2>&1 &"
echo "e3 python test-tcp-server.py e3 9952 > /dev/null 2>&1 &"
echo 'e1 echo -e "====== Wait for servers e3 on 9950-9952 ======"'
echo e1 sleep 2

echo 'e1 echo -e "====== Should NOT connect ======"'
end_case

test_tcp e1 e3 9950
test_tcp e1 e3 9951
test_tcp e1 e3 9952

echo 'e1 echo -e "====== Should connect ======"'
end_case

test_ping e1 e3

test_udp e1 e3 9950
test_udp e1 e3 9951
test_udp e1 e3 9952

test_tcp e2 e3 9950
test_tcp e2 e3 9951
test_tcp e2 e3 9952

test_udp e2 e3 9950
test_udp e2 e3 9951
test_udp e2 e3 9952

test_ping e2 e3

# Prohibit mobile1 from communicating with e1-e3 on both TCP and UDP
echo 'e1 echo -e "\n====== Prohibit mobile1 from communicating with e1-e3 on both TCP/UDP ======\n"'
echo 'e1 echo -e "====== Should NOT connect ======"'
end_case

test_tcp mobile1 e1 1234
test_tcp mobile1 e2 1234
test_tcp mobile1 e3 1234

test_udp mobile1 e1 1234
test_udp mobile1 e2 1234
test_udp mobile1 e3 1234

echo 'e1 echo -e "====== Should connect ======"'
end_case

test_ping mobile1 e1
test_ping mobile1 e2
test_ping mobile1 e3

test_tcp mobile1 w1 1234
test_udp mobile1 w1 1234

test_tcp w1 e1 1234
test_tcp w1 e2 1234
test_tcp w1 e3 1234

test_udp w1 e1 1234
test_udp w1 e2 1234
test_udp w1 e3 1234
