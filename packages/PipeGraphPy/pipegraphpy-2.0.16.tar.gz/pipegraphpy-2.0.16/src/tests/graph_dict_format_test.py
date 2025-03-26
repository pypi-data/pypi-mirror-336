
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PipeGraphPy.utils.format import verify_graph_dict_format

graph_dict = {
    "id": "g1",   #
    "params": {},   # 非必传
    "version": "v111",
    "name": "测试模型",
    "nodes": [    # 列表中节点名称不能有重复
        {
            "id": "n1", # 非必传，使用name作为id
            "name": "n1",
            "module_classification": "Regressor",
            "module_cls_name": "DataSVN",
            "params": {"eval": "RMSE"}, # 节点传参
        },
        {
            "id": "n2", # 非必传，使用name作为id
            "name": "n2",
            "module_classification": "Regressor",
            "module_cls_name": "DataSVN",
            "params": {"eval": "RMSE"}, # 节点传参
        }
    ],
    "edges": [
        {
            "source": "n1",      # 起始节点
            "target": "n2",      # 目标节点
            # "source_anchor": int,  # 起始节点锚点,可省略,默认是1
            # "target_anchor": int   # 目标节点锚点,可省略,默认为1
        },
        {
            "source": "n1",      # 起始节点
            "target": "n2",      # 目标节点
            # "source_anchor": int,  # 起始节点锚点,可省略,默认是1
            # "target_anchor": int   # 目标节点锚点,可省略,默认为1
        }
    ],
    "objects": [{"id": "12"}],   # 必传
    # "actuator": [
    #     # {
    #     #     "source": "n1",      # 起始节点
    #     #     "target": "n2",      # 目标节点
    #     # },
    #     {
    #         "source": "g1",      # 起始节点
    #         "target": "g1",      # 目标节点
    #     }
    # ]
}
if __name__ == "__main__":
    from pprint import pprint
    pprint(verify_graph_dict_format(graph_dict))
