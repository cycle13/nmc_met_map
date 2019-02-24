# 天气分析图工具
Collections of circulation, dynamic, thermal, moisture, instability, meso-scale and
others analysis or diagnostic graphics for map disccusion. All data comes from
CIMISS or Micaps data server.

用于制作天气讨论的环流, 动力, 热力, 水汽, 不稳定性, 中尺度等诊断分析图形产品. 通过
nmc_met_io程序包调用CIMISS或MICAPS服务器数据.

Only Python 3 is supported.

## Dependencies
Other required packages:

- numpy
- matplotlib
- basemap
- pandas
- cartopy
- nmc_met_io          请预先安装, 见https://github.com/nmcdev/nmc_met_io
- nmc_met_graphics    请预先安装, 见https://github.com/nmcdev/nmc_met_graphics

## Install
Using the fellowing command to install packages:
```
  pip install git+git://github.com/nmcdev/nmc_met_map.git
```

or download the package and install:
```
  git clone --recursive https://github.com/nmcdev/nmc_met_map.git
  cd nmc_met_map
  python setup.py install
```


