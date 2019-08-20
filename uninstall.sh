#!/bin/bash

# ================================================================================
# File Name: uninstall.sh
# Author: DaiDai
# Mail: daidai4269@aliyun.com
# Created Time: Tue Aug 20 14:54:22 2019
# ================================================================================


echo "Start uninstall LeetCode.VIP!"

rm -rf ~/.LeetCode.VIP
sed -e '/+++++ LeetCode.VIP +++++/d' ~/.bashrc > ~/.bashrc.backup
sed -e '/python ~/.LeetCode.VIP/LeetCode.VIP.py/d' ~/.bashrc.backup > ~/.bashrc
rm ~/.bashrc.backup

echo "LeetCode.VIP uninstall over!"
