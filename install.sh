#!/bin/bash

# ================================================================================
# File Name: install.sh
# Author: DaiDai
# Mail: daidai4269@aliyun.com
# Created Time: Tue Aug 20 14:54:22 2019
# ================================================================================


echo "Start install LeetCode.VIP!"

pip install -r requirements.txt
mv ../LeetCode.VIP ~/.LeetCode.VIP
echo >> ~/.bashrc
echo >> ~/.bashrc
echo \# +++++ LeetCode.VIP +++++ >> ~/.bashrc
echo alias lcvip=\"python ~/.LeetCode.VIP/LeetCode.VIP.py\" >> ~/.bashrc

echo "LeetCode.VIP install over!"
