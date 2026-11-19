# BA_ZH.dll — 可选插件（修复下拉菜单方框）

## 它解决什么

游戏只在 Txt.Write(text_id) 里给文本换字体。下拉菜单的选项文字是代码直接赋值的，
**不经过** Txt.Write，所以永远停在默认字体 cuyabra（162 个字形，**0 个汉字**）→ 全部显示方框。

这个插件把游戏**自带的** zh_white / zh_black（21,375 字形，20,992 汉字）
加进 TMP 的全局 fallback 列表，缺字形时自动回退。**不改任何游戏文件、不分发任何游戏资产。**

## 前置

- 需要 [BepInEx 5.4.23.6 x64](https://github.com/BepInEx/BepInEx/releases/tag/v5.4.23.6)
  （**不要用 BepInEx 6**，那是 IL2CPP 版本；本作是 Mono）。
- 把 BepInEx 解压到游戏根目录（会出现 winhttp.dll、doorstop_config.ini、BepInEx 文件夹）。

## 编译

    plugin\build.cmd "G:\Bondage Arena 24.0 premium"

产物 BA_ZH.dll 放进 游戏目录\BepInEx\plugins\ 。

编译只需 Windows 自带的 csc.exe，不需要安装 .NET SDK。

## 卸载

删掉 BepInEx\plugins\BA_ZH.dll 即可（整个 BepInEx 也可以删）。

## 日志

BepInEx\LogOutput.log 里应能看到：

    BA_ZH: loaded
    BA_ZH: CJK fallback injected
