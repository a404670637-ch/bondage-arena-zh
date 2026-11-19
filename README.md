# Bondage Arena 简体中文补丁 / Chinese (Simplified) Patch

> **Mature content.** This patch is translation data for an adult game (BDSM themes). 18+ only.
> This repository contains **no game assets** — only the translator's own Chinese text.

一款俄罗斯独立团队 **Captive DreamDev** 开发的成人向科幻/竞技游戏《Bondage Arena》的**非官方简体中文重译**。

- 游戏原文是**俄语**，官方英文是二次翻译；本补丁以俄文为准重译。
- 覆盖 **7,993 条**全部可本地化文本（官方中文只覆盖 2,402 条，且大量错译）。
- 通过替换 `StreamingAssets/Localizations/zh.csv` 实现，**不修改任何 .assets / 可执行文件 / 存档**。
- 安装脚本会自动备份原文件，一条命令即可还原。

---

## 安装

### 方式一：脚本（推荐）

需要 Python 3.8+（Windows 上 `py -3` 或 `python` 均可）。

```bat
git clone https://github.com/a404670637-ch/bondage-arena-zh.git
cd bondage-arena-zh
python tools/install.py --game "G:Bondage Arena 24.0 premium"
```

脚本会：
1. 把游戏原版 `zh.csv` 备份为 `zh.csv.official`；
2. 把 `dist/zh.csv` 复制进去。

不带 `--game` 时脚本会自动在 C–J 盘和 Steam 常见目录里找游戏。

### 方式二：手动

把 `dist/zh.csv` 覆盖到：

```
<游戏目录>Bondage Arena_DataStreamingAssetsLocalizationszh.csv
```

**覆盖前请自己先备份原文件。**

### 还原

```bat
python tools/install.py --game "G:Bondage Arena 24.0 premium" --restore
```

---

## 启用中文

进入游戏后，在语言菜单中选择 **中文 / Chinese**（代码 `zh`）。
切换语言通常需要重启游戏，或至少回到标题画面重新载入。

> 若你之前选过其他语言，游戏会把选择存在本地设置里；选一次中文即可长期生效。

---

## 覆盖范围与已知限制

| 项目 | 状态 |
|---|---|
| 剧情对话 | ✅ 3,829 条 |
| 系统 UI / 菜单 / 提示 | ✅ 1,730 条 |
| 队伍名与队伍介绍 | ✅ 208 条 |
| 模式 / 地图 / 武器 / 道具 / 编年史 / 日记 | ✅ 全部 |
| 人名 / 地名 / 术语 | ✅ 统一 |
| **预制体里硬编码的界面文字** | ⚠️ **约 45 处仍是英文/俄文**（如 Settings、Save game、Loading…），这些不在 csv 里，需要另外打 .assets 补丁，见 `docs/HARDCODED.md` |

---

## 游戏更新后怎么办

游戏更新会用官方文件覆盖 `zh.csv`，中文会失效。处理步骤：

```bat
python tools/check_update.py --game "<游戏目录>"
```

它会比对游戏新的 `ru.csv` 与本项目的翻译库，输出：
- 命中多少条（按俄文原文的哈希匹配，**即使序号整体位移也能对上**）
- 有多少条原文被改动
- 有多少条是全新文本（写入 `out/untranslated.csv`，可直接拿去翻译）

然后：补译 → 更新 `data/strings.json` → `python tools/build.py` → 重新安装。

详见 [docs/UPDATE.md](docs/UPDATE.md)。

---

## 仓库结构

```
data/strings.json        翻译库：每条含 行名 + 列号 + 俄文原文哈希 + 中文
dist/zh.csv              生成产物，可直接复制进游戏
tools/build.py           strings.json -> dist/zh.csv（不需要游戏也能跑）
tools/install.py         备份并安装 / 还原
tools/check_update.py    游戏更新后的差异报告
tools/verify.py          用游戏自身的加载规则校验生成的 csv
docs/STYLE.md            译名与体例说明（术语表、命名规则）
docs/UPDATE.md           版本维护流程
docs/HARDCODED.md        未覆盖的预制体文字说明
```

翻译库**按俄文原文哈希匹配**，而不是只按列号，所以游戏调整条目顺序时不会串行。

---

## 为什么是替换 csv 而不是打二进制补丁

游戏的 `Txt.Load_text()` 是运行时从 `StreamingAssets/Localizations/<lang>.csv` 读文件，
完全不经过 .assets 或资源包。所以：

- **零二进制修改**：不碰 exe、不碰 .assets、不碰存档；
- **升级友好**：游戏更新后官方 csv 会覆盖我们的文件，重跑一次安装即可；
- **可回滚**：原文件是纯文本，备份还原零风险；
- **可审查**：整个补丁就是一份 csv + 一份 json，任何人都能 diff。

---

## 许可证

- **代码**（tools/、CI）：MIT，见 [LICENSE](LICENSE)。
- **译文文本**（data/、dist/）：CC BY-NC-SA 4.0，见 [LICENSE-TEXT](LICENSE-TEXT)。
- 游戏本体及其资产版权归 **Captive DreamDev** 所有，本仓库不包含任何游戏资产。
- 本项目与开发商无任何关联。若权利方要求，会立即下架。

---

## English summary

Unofficial Simplified Chinese retranslation for *Bondage Arena* (Captive DreamDev). The game's
source language is Russian; the official English is a second-hand translation, so this patch
retranslates from Russian. It works by replacing `StreamingAssets/Localizations/zh.csv` —
no binary patching, no save-file touching, fully reversible. Select **Chinese** in the in-game
language menu after installing.

```bat
python tools/install.py --game "<game folder>"
python tools/install.py --game "<game folder>" --restore
```
