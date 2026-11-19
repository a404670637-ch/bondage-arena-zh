# 游戏更新后的维护流程

游戏更新会用官方 zh.csv 覆盖补丁，中文随即失效。以下流程假设你已 git clone 本仓库。

> 本作通过 **Patreon / itch.io** 分发（Steam 上也有同款，安装方式一致）。新版本通常是压缩包，
> 解压覆盖到同一目录即可；发布包里不含 `BepInEx/` 与 `winhttp.dll`，所以字体修复插件通常会保留，
> 但 `zh.csv` 会被官方文件覆盖，需要重跑 `install.py`。

## 1. 看差异

    python tools/check_update.py --game "<游戏目录>"

输出四项：
- **命中**：按俄文原文 SHA-1 匹配上的条数（序号位移不影响）；
- **改动**：同一位置但俄文变了；
- **全新**：新版本新增的文本；
- **消失**：新版本删掉的行。

明细写入 out/untranslated.csv（列：state / row / index / russian）。

## 2. 补译

打开 out/untranslated.csv，按 [STYLE.md](STYLE.md) 的术语表翻译。
注意占位符与 [2525] 换行。

## 3. 写回翻译库

在 data/strings.json 对应行的 items 里新增条目：

    {"i": 123, "h": "<俄文原文 sha1 前 16 位>", "n": 42, "zh": "译文"}

- i：列号（0 起）；h：俄文原文 sha1 前 16 位；n：原文字符数；zh：译文。
- 若某条原文被改动，**保留 i 不变、更新 h 和 zh**。

## 4. 重新生成并安装

    python tools/build.py
    python tools/verify.py
    python tools/install.py --game "<游戏目录>"

verify.py 会用游戏自身的加载规则（按分号切分、遇空单元格截断、单个减号视为空）
检查行长度是否一致、合并后有没有空洞。

## 5. 发布

打 tag 后 CI 会自动构建并附加 zh.csv 到 Release：

    git tag v1.x.x
    git push origin v1.x.x

## 注意事项

- **不要**把游戏文件提交进仓库。
- 更新前的官方 zh.csv 不必保留，install.py 会自己备份为 .official。
- 如果更新后连 ru.csv 结构都变了（新增行、列数变化），check_update.py 会报出来，
  需要在 data/strings.json 里新增对应行。
