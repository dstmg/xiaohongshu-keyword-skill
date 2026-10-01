# 小红书下拉关键词采集 Skill

给 AI Agent 一个商品词，让它操作真实浏览器，采集小红书搜索框的两层下拉联想词，截图留证并整理成 Excel。适用于不同类目的电商关键词整理，不限定烘焙。

**这是 Agent 技能，不是独立爬虫或浏览器扩展。** 浏览器操作由安装该技能的 Agent 执行；仓库中的 Python 脚本负责验证记录与导出表格，不会自行打开网页。

## 能做什么

- 输入一个或多个词根，采集第一层联想词，再逐个输入第一层词采第二层。
- 保存真实截图、下拉位置、时间与来源路径，去重但不丢失路径。
- 每次采集保存 JSON 检查点，续采保留完成项；受阻及未完成项如实列出。
- 导出关键词表、采集记录、截图索引、去重词库、待采集五张表。
- 可选通用电商解读：购买渠道、选购比较、商品信息、使用方法、售后等分类；采购意图/内容价值评分及运营检查建议。

联想词不是搜索量、热度、销量或成交预测。评分和建议是规则推断，未覆盖的词留给人工判断。不要把词条直接当成商品事实或销售承诺。

## 安装与前提

1. 下载仓库（Code → Download ZIP），将解压后的目录作为一个 Skill 放入 Agent 的技能目录。Codex 通常为 `$CODEX_HOME/skills/yao-geo-xiaohongshu`；未设置 CODEX_HOME 时通常使用 `~/.codex/skills/yao-geo-xiaohongshu`。避免同时安装原版和此版造成同名冲突。
2. 按所用 Agent 的要求刷新技能或重开对话，确认它能读取 `SKILL.md`。
3. 配好该 Agent 可用的浏览器操作工具。本项目不捆绑 BrowserSkill 或其他浏览器连接器，其安装与费用需单独确认。
4. 准备 Python 3.10+，安装导出依赖：

```bash
python -m pip install -r requirements.txt
```

本项目代码使用 MIT 许可证。运行时的 AI 模型、浏览器工具和其他服务可能有各自费用，不承诺整个运行链路免费。

## 对 Agent 这样说

> 帮我采集小红书“我的商品词”的下拉联想词，做两层扩展，保留截图并导出 Excel。遇到登录或验证码叫我，最后告诉我哪些没采完。

Agent 检查浏览器连接后打开小红书；登录和验证码由你处理。登录正常后采词、截图、记录检查点并导出。默认最多200个不同检索词，每个下拉最多10个可见词，不扩到第三层。出现平台限制时暂停，不绕过验证码或访问控制。

只要关键词表时，不必要求电商分析；需要时再说“按我的商品类目做通用电商解读”。通用规则不等于所有类目的专用知识。

## 从已有记录导出

将 `capture.json`、`evidence/` 截图目录和输出 Excel 放在同一目录。格式见 [数据契约](references/data-contract.md)。

```bash
python scripts/build_workbook.py --input capture.json --output keywords.xlsx --industry ecommerce
python scripts/build_ecommerce_workbook.py --input capture.json --output ecommerce.xlsx
```

增强表输出新文件名，保留原五张表，另加四张解读表。烘焙专用脚本仅是可选案例，不是通用默认规则。

## 检查

```bash
python scripts/check_scoring.py
python scripts/check_workbook.py
python scripts/check_ecommerce.py
python scripts/check_baking.py
```

这些是离线检查，不验证当前平台页面结构。真实采集后仍应核对截图、输入值、顺序和来源。仓库不包含私人账号截图、Cookie、登录信息或实测采集数据。

## 来源与改进

基于 [yaojingang/yao-geo-skills 中的 yao-geo-xiaohongshu](https://github.com/yaojingang/yao-geo-skills/tree/main/skills/yao-geo-xiaohongshu) 改进，保留原版权和 MIT 许可证。原版提供两层采集规程、证据记录、行业评分与五表导出；此版新增可选通用电商解读、双评分、运营建议、烘焙案例与相应检查，并明确采集与解读的边界。
