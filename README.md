# IPCode

  *IPCode* 是一个使用自然语言进行IP地址编码压缩的项目，旨在为非英语使用者提供更简洁、更易于口头表达、更方便记忆的标记方式。

## 故事背景

  众所周知，IPv6拥有128 bit，未进行常规意义上的压缩其常规表示将是8部各16 bit、4 十六进制字符的一长串代码，非常不利于记忆。在网络状况复杂的中国，普通家庭连一个本来就应该有的固定IPv6前缀都得不到（至少很多地区会默认每隔一段时间强制更换分配给你的前缀），IPv6其公网IP的优势变成了空中阁楼，相当令人生气。在有的地区，前缀可能才3天就变化，如此糟糕的频率让任何家庭设置都成为一种灾难。甚至很多时候，我只是想和我的朋友联机玩游戏而已。ICMPv6能不能通我已经不想管了，我只想每次换IP的时候，我的朋友可以很方便地告诉我那一长串64 bit的前缀。迫于一些旧电脑“看似落后”的性能和某些通讯软件极其臃肿的设计，我需要让他只需要口头表述信息而不需要在电脑登录某些通讯软件，这便是我产生想法并决定开发这个项目的初始理由。

  我知道，可以使用DDNS服务来解决这件事，但是我不想把浪费IPv6那庞大的地址池带来的安全性，我只想点对点通告、通过其他通讯方式（如：社交软件、私密聊天），我不想让别人也知道我的地址，这样就能更好地避开DDoS攻击，保护好我的设备。

  此外，这个项目还可以配合社交软件的机器人和我的*FetchRPlayer*项目（的设想）和动态分配地址和端口，组成一个安全的、可控的、灵活可变的联机网络机制。在这种体系下，由玩家提供自己的地址，服务器进行端口转发，就可以检测到本地的什么地址和端口被攻击，进而追溯和管理玩家。同时，检测到DDoS攻击，或者更加地严格（超过一定连接数），就弃用这个地址和端口。IPv6，不就是为了”来无影，去无踪“吗？

## 名称由来

  当今时代“二维码”(QR Code)十分流行，那我就简单地命名为“IPCode”吧。（为了与实际用语"IP Code"区分，项目名称不加入空格。）

## 压缩优势

常规的16进制表达，由于是16进制，每一位仅限16种字符，因此信息密度比较低。（这里的”信息密度“，按照显示的单独字作为基本单位进行计数，非传统意义上的"bit"。）考虑到汉字那么那么地多，不好好利用一下汉字可太浪费了。虽然汉字在计算机中的占位可能是二到四个字节，但是写出来、显示出来、表达上却仅仅那么几位”字符“，这对人类来说是有优势的。

这里有个常规的压缩计算公式:

```python
from math import *
# 此处以gb2312、64位IPv6前缀进行举例
character_number_in_gb2312 = 6763
min_character_number = log(2**64, character_number_in_gb2312) 
print(min_character_number)
```

此处得到结果为`5.0300831833291415`，也就是说，原本可能多达$4*4=16$个字符缩短为`ceil(5.030)=6`个字符；如果改用`gb18030-2005`（$27484$个汉字），那么结果为`ceil(4.340)=5`。

我们知道，*GB 18030*还收录了一些少数民族文字，处于输入和表达的便利性以及本开发者的学识水平考虑，暂时没有支持的计划。（即便支持，那么是$70244$个汉字，结果是`ceil(3.975)=4`，但是还有更好的表达方式又为何要这样呢？）

如果我们加入色彩支持，即便只是很少的几种颜色，经过乘法运算那么可用”字符“数量也大大增加了。比如10种颜色，使用*GB2312*的6763个汉字加上26个英文字母的大小写符号再加上10个阿拉伯数字，这就是$6825*10$了，结果就已经能达到：`ceil(3.9854)=4`了，这就很优秀了。

想想，一个64位的前缀被压缩到4个汉字+4种颜色，这样表述起来还难吗？什么？生僻字？这个优化是基于*GB 2312*的，据统计，*GB 2312*满足了日常99%的使用需求，它的一级和二级汉字区本就是按常用度分类的，一级区过半，而且顺序编码，那如果真的遇到了不想要的字，可以通过修改映射算法或是改变偏移量来实现替换，完全可以胜任这项工作！

## 使用建议

1. 如果设备有触摸输入设备，有手写输入法或合适的OCR或墨迹转文字，那么将其搭配使用是极好的！

## 计划的语言及编码

- [ ] 中文
  - [ ] gb2312 (6763个汉字)
    - [ ] gb2312 (6763个汉字+26个字母的大小写+10个阿拉伯数字）
  - [ ] gbk
  - [ ] gb18030 (gb18030-2005)
    - [ ] gb18030-2022
  - [ ] utf-8
  - [ ] CNS 11643
    
## 计划的特性

- [ ] 可以自动列出设备的所有IPv6地址以供选择。
- [ ] 可以从指定IPv6地址根据指定前缀长度得到前缀。
- [ ] 加入前缀转换模式，仅处理前缀。
- [ ] 加入完整地址转换模式，处理完整IPv6地址。 
- [ ] 可以自动识别正在使用的IPv6前缀并转换。
- [ ] 可以支持至少两种中文的编码方式。
- [ ] 可以设置偏移量，主要用于方便表述和避开生僻字。
- [ ] 可以支持除顺序以外的编码映射，提高避开生僻字的成功率。  
- [ ] 拥有预设集，预设好配置组合方式。
- [ ] 拥有一个清晰的GUI。
- [ ] GUI支持编码输入。  
- [ ] 可以加入色彩表达以进一步压缩"IP Code"长度。
- [ ] 色彩表达支持GUI。
- [ ] 开发Web版本，为全平台支持做好准备。 
- [ ] 开发Android Application版本，充分发挥手写输入法的优势。（可能被放弃）
- [ ] 支持生成QR Code形式的常规代码。  
- [ ] 移动应用可以识别从其他软件打开的QR Code形式的常规代码并可以传输到已连接的电脑上相关的服务端。  
- [ ] 提供可用的服务端，供所有人部署。
- [ ] 提供公用服务（体验用途）。
