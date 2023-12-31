# IPCode

  *IPCode* 是一个主要使用自然语言进行IP地址编码压缩的项目，其旨意包括：

1. 为非英语使用者提供更简洁、更易于口头表达、更方便记忆的标记方式。
2. 简化全场景交流IPv6的方式。

开发进度：早期。

## 故事背景

  众所周知，IPv6拥有128 bit，未进行常规意义上的压缩其常规表示将是8部各16 bit、4 十六进制字符的一长串代码，非常不利于记忆。在网络状况复杂的地区，一个固定IPv6前缀可能无法（或很难）被获得（比如默认每隔一段时间强制更换分配给你的前缀），IPv6其公网IP的优势变成了空中阁楼，相当令人难受。在有的地区，前缀可能才3天就变化，如此糟糕的频率让任何家庭设置都成为一种灾难。

> 很多时候，我只是想和我的朋友联机玩游戏而已。

  ICMPv6能不能通我已经不想管了，我只想每次换IP的时候，我的朋友可以很方便地告诉我那一长串64 bit的前缀。迫于一些旧电脑“看似落后”的性能和某些软件极其臃肿的设计和实现，我不能要求他在电脑登录某些通讯软件来告知我信息，我需要设计一个新的、合适的解决方案，这便是我产生想法并决定开发这个项目的初始动机。

  我知道，可以使用DDNS服务来解决这件事，但是我不想浪费IPv6那庞大的地址池带来的安全性，我只想点对点通告、通过其他通讯方式（如：社交软件、私密聊天），我不想让别人也知道我的地址，这样就能更好地避开DDoS攻击，保护好我的设备。这么做意味着一个好处：我大概不需要各种防DDoS的措施，比如昂贵的CDN、流量清洗设备……

  此外，这个项目还可以配合社交软件的机器人（或是我的*FetchRPlayer*项目的设想）进行动态分配地址和端口，组成一个安全的、可控的、灵活可变的联机网络机制。在这种体系下，由玩家提供自己的地址，服务器进行端口转发，就可以检测到本地的什么地址和端口被攻击，进而追溯和管理玩家。同时，检测到DDoS攻击，或者更加地严格（超过一定连接数），就弃用这个地址和端口。使用IPv6，不就是为了”来无影，去无踪“吗？

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
- [x] 可以从指定IPv6地址根据指定前缀长度得到前缀。
- [ ] 加入前缀转换模式，仅处理前缀。
- [ ] 加入完整地址转换模式，处理完整IPv6地址。 
- [ ] 可以自动识别正在使用的IPv6前缀并转换。
  - [x] 自动识别正在使用的IPv6地址
- [ ] 可以支持至少两种中文的编码方式。
- [ ] 可以设置偏移量，主要用于方便表述和避开生僻字。
- [ ] 可以支持除顺序以外的编码映射，提高避开生僻字的成功率。  
- [ ] 拥有预设集，预设好配置组合方式。
- [ ] 拥有一个清晰的GUI。
- [ ] GUI支持编码输入。  
- [ ] 可以加入色彩表达以进一步压缩"IP Code"长度。
- [ ] 色彩表达支持GUI。
- [ ] 开发Web版本，为全平台支持做好准备。 
  - [ ] 限定版
    - [x] 简化的内置服务器，支持直接展示IPv6地址。
    - [x] 支持自定义配置
    - [x] 完成后端cache开发
    - [x] 添加特性：提示新信息。
    - [ ] 提供转换后的数据
    - [ ] 能够接受转换后的数据
  - [ ] 泛化版
    - [ ] 提供完整前端（即限定版全功能）
    - [ ] 能够指定通信的设备
    - [ ] 能够储存设备地址
  - [ ] 引导用途服务器，储存相应信息并提供本地引导。（提供泛化版分发）
- [ ] 开发Android Application版本，充分发挥手写输入法的优势。（可能被放弃）
- [ ] 支持生成QR Code形式的常规代码。  
- [ ] 移动应用可以识别从其他软件打开的QR Code形式的常规代码并可以传输到已连接的电脑上相关的服务端。  
- [ ] 提供可用的服务端，供所有人部署。
- [ ] 提供公用服务（体验用途）。



## 许可证 License

”无“。本许可证可能不符合一些人心中对开源的定义并被认为仅属于“公开源代码”。事实上，此许可可授予的权利范围可能相当不同（这取决于额外许可的内容）。**大体上，此许可证不反对商业使用**。详见许可具体内容：

``` 
Copyright (c) 2023 LiuJiewenTT

没有任何权利首先被授权，您只能使用，但不能对私自修改的代码和修改后的相关产品进行分发，同时作者不对你个人修改的代码担保、不承担由此造成的任何责任。不管是否是用于商业用途，一切对修改版本的分发都要事先取得作者的授权。在此基础上，以下列出包含默认授权的情形：

1. 您可以在有限的情况下在您的产品中包含此项目的产品。对于您的包含此项目相关产品的产品，未修改本项目的任何代码，原样提供此项目发布的产品，使本项目产品在独立的进程中运行，在声明中表明使用了此项目的产品、提供此项目的相关链接，同时将此许可证原样包含，此时您的产品被默认授予再分发的自由。

2. 指定的限定条件仍然有效的许可将自动对新的修改版本进行许可。如果您曾经得到过一份许可，在许可中指定的限定条件仍然有效的情形下，您对此项目的产品的新的修改会继承您得到的许可。

3. 新的许可将以此许可为基础，对于冲突部分应以此许可和新许可随附的指示为准。如果您得到了额外的许可（以下我们称为“新的许可”），那么新的许可的级别将高于此许可，并以新许可为准（如果遇到冲突）。新的许可可能会在其它许可上随附内容用以指定权利的授予和限制，这些随附内容称为“指定的限定条件”，属于新的许可的不可分割的一部分，并将自动覆盖其它许可带来的矛盾点，即以这些“指定的限定条件”为准，任何许可不得违反这些限定条件，否则冲突内容将视为无效内容。在包含新的许可时，您应当同时包含此许可，用以确保新许可的效力。

以下是关于此许可的补充说明：

1. 此许可证可能未被包含在分发的产品中，但如果产品提供了指向包含此许可声明的页面，则认为分发的产品遵循此许可。如果没有包含此许可且未提供相应链接，应视为没有得到任何授权。

2. 公开修改版本的完整源码的行为也被视作分发。作者反对未经授权使用此项目的修改版本进行盈利目的的经营性活动和分发未授权的修改版本。此情形亦有例外：当在项目主页、指导文件和运行时的某种展现方式（或其它任何面向开发者和用户的展现方式）明确了所有原作者以及现作者，此许可保证您的未经授权的公开行为将被排除在此情形外。

3. 如果此许可随附一个NOTICE文件，您也应当保留其内容。此许可对该文件的要求为记录所有原作者和现作者，且要求无时间先后异议的作者应当按照时间先后从起始排至末尾。如果这是您自己的项目，那么“现作者”不应该标记您的项目以外的人。在您的名称后面，您可以选择附加您的联系方式。

作者保留追究未授权情形的权利，如果您违反了此许可证提到的内容，授予您的所有权利将被收回，您可能将需要承担相关法律责任。
```