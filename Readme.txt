运行环境配置
	1. 安装Cygwin, 添加环境变量C:\cygwin64\bin，根据安装目录不同而具体设定。
		http://www.cygwin.com/
	2. 安装HTK3.4, 添加环境变量C:\htk，根据安装目录不同而具体设定。
	3. 安装Sox, 添加环境变量C:\Software\sox-14.4.1，根据安装目录不同而具体设定。
		http://sox.sourceforge.net/

使用说明
	标注单个wav：
		1. 使用命令行转到p2fa文件夹下
		2. 在p2fa/test放入待标注的wav（例如142.wav）和对应的文本文档（例如142.txt）
		3. 运行如下命令
			python align.py ./test/142.wav ./test/142.txt ./test/142.TextGrid
		4. 对应的结果为142.TextGrid
	批处理标注wav：
		1. 在p2fa文件夹下找到TextGridFileGetter.py程序，使用notepad++打开
		2. 修改getTextGridFile函数参数，第一个参数为wav和对应txt在的文件夹, 修改第一个参数为wav和txt所在的文件夹（该文件夹下没有子文件夹）
注意事项：
1.编码格式：UTF-8无BOM格式
2.在cmd命令行下调用
3.配置好python 27