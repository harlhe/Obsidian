#!/usr/bin/env python3
"""
Wiki技能路由器
根据用户输入确定子命令和参数
"""

import sys
import json
import re

def get_subcommand_from_intent(user_input):
    """从用户输入判断意图并映射到子命令"""
    input_lower = user_input.lower().strip()

    # 收录/添加素材
    if any(keyword in input_lower for keyword in ['收录', '添加', '加到', '导入', 'ingest']):
        return 'ingest', user_input

    # 提问/查询/对比/整理
    if any(keyword in input_lower for keyword in ['是什么', '怎么样', '如何', '为什么', '对比', '比较', '整理', '分析', 'query', '问', '查询']):
        return 'query', user_input

    # 反馈/偏好/纠正
    if any(keyword in input_lower for keyword in ['回答', '你说错了', '不对', '应该', '建议', '反馈']):
        return 'query', user_input

    # 检查/审计
    if any(keyword in input_lower for keyword in ['检查', '审计', '问题', '健康检查', 'lint']):
        return 'lint', user_input

    # 删除/清空/重置
    if any(keyword in input_lower for keyword in ['删除', '清空', '重置', '删掉', '清除', 'wipe', '删除']):
        return 'wipe', user_input

    # 初始化
    if any(keyword in input_lower for keyword in ['创建', '初始化', 'init', '新建']):
        return 'init', user_input

    # 默认情况
    return 'query', user_input

def route_command():
    """路由函数"""
    if len(sys.argv) < 2:
        # 自然语言触发
        user_input = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else ""
        subcommand, args = get_subcommand_from_intent(user_input)
    else:
        # 命令式触发
        subcommand = sys.argv[1]
        args = ' '.join(sys.argv[2:]) if len(sys.argv) > 2 else ""

    # 加载知识库配置
    try:
        with open('/Users/gaozhiyang/projects/ObsidianProjects/Obsidian/.claude/skills/wiki/registries.json', 'r', encoding='utf-8') as f:
            registries = json.load(f)
    except FileNotFoundError:
        return {
            "status": "no_kb",
            "message": "未找到知识库配置文件，请先初始化知识库"
        }

    kb_list = list(registries['knowledge_bases'].values())

    if not kb_list:
        return {
            "status": "no_kb",
            "message": "未注册任何知识库，请先初始化知识库"
        }

    if len(kb_list) == 1:
        kb = kb_list[0]
        multiple_kbs = False
    else:
        kb = kb_list[0]  # 默认第一个
        multiple_kbs = True

    # 构建路由结果
    result = {
        "status": "ok",
        "subcommand": subcommand,
        "args": args,
        "workflow": f"workflows/{subcommand}.yaml",
        "schema": None,
        "kb": {
            "id": kb['id'],
            "name": kb['name'],
            "root": kb['root'],
            "wiki": kb['wiki'],
            "raw": kb['raw'],
            "lang": kb['lang']
        },
        "skill_dir": "/Users/gaozhiyang/projects/ObsidianProjects/Obsidian/.claude/skills/wiki",
        "multiple_kbs": multiple_kbs,
        "kb_list": kb_list
    }

    return result

if __name__ == "__main__":
    result = route_command()
    print(json.dumps(result, ensure_ascii=False, indent=2))