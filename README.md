# sentence-simulator 1.0.0
根据语法规则生成模拟句子
> 语法规则及交互树详见 [interactive-syntax-tree](https://wzyjerry.github.io/interactive-syntax-tree/)
---
## 输入规则
一个json文件，通过-f参数传入，格式如下:
{
    "rule": {
        "type": "root",
        "children": [{
            "type":"intent",
            "weight":1,
            "intent":"intent 1",
            ...
        },
        ...]
    },
    "entity": [{
        "id": "entity id 1",
        "name": "entity name",
        "entries": ["string1", ...]
    },
    ...]
}
---
## 输出规则
-c: 生成模拟句子的数量，默认值1000
-w：词级别输出，%word\t%entity\n
-s：句级别输出，%intent\t%sentence
---
## 模拟步骤
1. 编译语法树（编译错误给出提示，结束）
    1. 删除holder节点及其子节点
    2. 对于每个intent进行编译，检查每个节点类型，对于每种类型的节点，补全初始值，删除无效字段
    3. 对于每个content->isSlot节点，汇总entityID生成 **【实体集合】**
    4. 删除后代中不包含content节点的节点
    5. 对需要权重采样的节点抽取后代weight字段生成对应数组
    6. 先序标记节点id（根节点标记为0）
    7. 给出统计信息：各类节点总数，实体集合，content节点上的tag总数
    8. 检查文件集合1中文件是否存在
2. （调试模式）输出编译后的语法树规则
3. （调试模式）将调试输出模板追加到输出模板后
3. 将规则转化为模拟器树节点
4. 从根节点用generator模拟n次，沿输出链输出结果

## 示例
python main.py -f data/input.json -c 10 -w data/out/word.txt -s data/out/sent.txt

---
v1.0.0 修改标记类型为iob2，修改entity content node