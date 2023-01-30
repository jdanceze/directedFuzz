#!/bin/bash
for i in {65433..65483..2}
do
    echo killing $i
    kill $(lsof -t -i:$i)
done
