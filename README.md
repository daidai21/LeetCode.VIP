# LeetCode.VIP

### Introduction & Feature

This is a simple shell tool about algorithms problem information of LeetCode. This tool support windows, linux and Mac OX.

`company.csv` file

- The first column is the company name.
- The other column is the company's question problem-id.

`problem.csv` file

- The first column is the problem-id.
- The second column is the title of problem.
- The third column is the whether it is vip.
- The fourth column is the difficulty, in [easy, median, hard]
- The fifth column is the frequency of problem appear.

### Install & Uninstall

install: `wget https://github.com/daidai21/LeetCode.VIP; sudo ./LeetCode.VIP/install.sh`
uninstall: `~/.LeetCode.VIP/uninstall.sh`

### Usage

```bash
➜  leetcode.VIP git:(master) ✗ ./LeetCode.VIP.py

usage: LeetCode.VIP.py [-h] [-U] [-P] [-C] [--proxy] [-O] [-Sid SHOW_ID]
                       [-Sc SHOW_COMPANY]

This is a simple shell tool about algorithms problem information of LeetCode.
Github URL: https://github.com/daidai21/LeetCode.VIP

optional arguments:
  -h, --help            show this help message and exit
  -U, --update          run spider to download the newest data information.
  -P, --problem         show problem information.
  -C, --company         show company information.
  --proxy               usage proxy.
  -O, --open-browser    open problem in browser.
  -Sid SHOW_ID, --show-id SHOW_ID
                        show problem information of id.
  -Sc SHOW_COMPANY, --show-company SHOW_COMPANY
                        show problem information of company name.
```

### CopyRight & Disclaimer

All copyright is owned by individuals, for learning only. `github@daidai21` This tool is only for learning (spider) use, refuse piracy LeetCode. I am not responsible for any other person's use of this tool.
