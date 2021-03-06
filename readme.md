# 机械设计求解器使用说明

## 介绍
本项目是一个专门为北航机械设计实践课程编写的设计参数求解器，可以较为方便的获得诸如传动带基准长度、齿轮直径以及齿轮模数之类的设计结果，从而帮你省去了手动计算的繁琐与不便。除此之外，本项目还会生成一个output文档，可以作为撰写设计报告的参考。  
需要注意的是，机械设计的过程并没有标准答案，本项目的结果只能作为一种参考，并不是最合理的，甚至可能存在一定的错误。另外，本项目目前还在开发阶段，暂时只适应带传动加二级齿轮传动的计算，也有诸多的不足，欢迎感兴趣的同学一同维护和更新。

## 需求
要使用本项目辅助你的设计，目前阶段你需要：<br>
* python3.x解释器

## 使用方式
更改主目录下的params.json文件，可以修改输入的参数，具体参数含义和选取方式见注释以及课本相应公式。

## 未来展望
* 完善带传动和齿轮传动（比如更多的带型和更精准的估计）
* 加入更多传动零件的设计（比如蜗轮蜗杆和轴承）
* 加入GUI设计
