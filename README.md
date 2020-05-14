## 分词、词性标注工具

- **[安装与使用介绍](./lac_tools.md)**，整理包括以下工具

  1. Jieba
  2. THULAC
  3. pkuseg
  4. pyhanlp
  5. StandfordNLP
  6. LTP
  7. SnowNLP
  8. PyNLPIR
  9. foolnltk

- **调用分词**

  依照上述介绍安装好工具后，可通过我们封装好的接口，以统一的形式调用任一个工具的分词，代码如下所示：

  ```python
  from tools_wapper import *
  
  # 若使用StandfordNLP或者pyltp需要设置字典路径
  standforddict = "./stanford-corenlp-4.0.0/"
  pyltpdict = "./ltp_data_v3.4.0/"
  
  # 选择想要调用的分词工具，需要安装，若未安装工具从列表中删除即可
  tools = ['lac', 'jieba', 'pkuseg', 'thulac',
           'pynlpir', 'pyhanlp', 'foolnltk', 'snownlp',
           ('standfordnlp', standforddict), ('pyltp', pyltpdict)]
  
  # 遍历调用所有工具
  for tool in tools:
      if isinstance(tool, tuple):
          cutter = eval(tool[0] + "_impl")(tool[1])
          tool = tool[0]
      else:
          cutter = eval(tool + "_impl")()
  
      print(tool, cutter.cut("人生自古谁无死，留取丹心照汗青"))
  ```

- **调用词性标注**

  依照上述介绍安装好工具后，可通过我们封装好的接口，以统一的形式调用任一个工具的词性标注，代码如下所示：

  ```python
  from tools_wapper import *

  # 若使用StandfordNLP或者pyltp需要设置字典路径
  standforddict = "./stanford-corenlp-4.0.0/"
  pyltpdict = "./ltp_data_v3.4.0/"

  # 选择想要调用的分词工具，需要安装，若未安装工具从列表中删除即可
  tools = ['lac', 'jieba', 'pkuseg', 'thulac',
           'pynlpir', 'pyhanlp', 'foolnltk', 'snownlp',
           ('standfordnlp', standforddict), ('pyltp', pyltpdict)]

  # 遍历调用所有工具
  for tool in tools:
    if isinstance(tool, tuple):
      cutter = eval(tool[0] + "_impl")(tool[1], 'postag')
      tool = tool[0]
    else:
      cutter = eval(tool + "_impl")('postag')

    print(tool, cutter.cut("人生自古谁无死，留取丹心照汗青"))
  ```

