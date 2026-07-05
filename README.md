# 融合口袋像素字体 / Fusion Poke Pixel Font

[![License OFL](https://img.shields.io/badge/license-OFL--1.1-orange?style=flat-square)](LICENSE-OFL)
[![License MIT](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE-MIT)
[![Releases](https://img.shields.io/github/v/release/pixel-font-studio/fusion-poke-pixel-font?style=flat-square)](https://github.com/pixel-font-studio/fusion-poke-pixel-font/releases)

这是一个为同人游戏 [「宝可梦无限融合 / Pokémon Infinite Fusion」](https://discord.gg/infinitefusion) 定制的字体项目。

本字体基于 [「缝合像素字体」](https://github.com/TakWolf/fusion-pixel-font) 进行修改，目标是解决游戏中简体中文语言的显示问题。

尽管为简体中文而创建，但理论上该字体支持泛拉丁和泛中日韩语言，可以作为该游戏大部分多国语的字体解决方案，而且可能比游戏默认字体更好。

本字体主要基于 [「无限融合2：丰缘 / Infinite Fusion 2: Hoenn」](https://github.com/infinitefusion/infinitefusion-hoenn-public) 进行适配和测试。

本字体衍生自「Fusion Pixel Font」，因此字体名中带有「Fusion」单词。这只是一个巧合，和游戏名中的「Fusion」没有直接关系。

> [!WARNING]
> 
> 本项目不是 [Pokémon Infinite Fusion](https://discord.gg/infinitefusion) 的官方项目。
> 
> 本项目仅接受字体相关的问题反馈。有关游戏相关的问题反馈，请在 [游戏官方社区](https://discord.gg/infinitefusion) 进行提交。

> [!WARNING]
> 
> 本项目与「宝可梦」官方无任何关系。
> 
> 字体全部字形均来自于设计师原创，或衍生自其它开源字体。
> 
> 本仓库中亦不包含任何「宝可梦」著作权相关的素材。

> [!WARNING]
> 
> 为了适配 [Pokémon Essentials](https://github.com/Maruno17/pokemon-essentials) 字体布局引擎的一些怪癖，字体参数部分做了一些特殊处理。
> 
> 所以本字体可能不适用于常规项目。

## 使用方式

字体包含三个变种，与默认字体对应关系如下：

| 版本 | 对应 | 字号 |
|---|---|---|
| Fusion Poke Pixel Normal | Power Green | 13px |
| Fusion Poke Pixel Narrow | Power Green Narrow | 13px |
| Fusion Poke Pixel Small | Power Green Small | 11px |

对于多国语，请使用相应的版本：

| 版本 | 含义 |
|---|---|
| latin | 泛拉丁语 |
| zh_hans | 简体中文 |
| zh_hant | 繁體中文 |
| ja | 日语 |
| ko | 朝鲜语 |

[点击此链接](https://github.com/pixel-font-studio/fusion-poke-pixel-font/releases) 下载最新版本。

将压缩包所有字体，复制到 `游戏根目录/Fonts/` 文件夹中。

以简体中文为例，使用文本编辑器，打开脚本 `游戏根目录/Data/Scripts/007_Objects and windows/002_MessageConfig.rb`，找到并修改如下部分：

```ruby
module MessageConfig
    
    # Other configs...

    FONT_NAME               = "Fusion Poke Pixel Normal zh_hans"
    FONT_SIZE               = 29
    NARROW_FONT_NAME        = "Fusion Poke Pixel Narrow zh_hans"
    NARROW_FONT_SIZE        = 29
    SMALL_FONT_NAME         = "Fusion Poke Pixel Small zh_hans"
    SMALL_FONT_SIZE         = 25

    # Other configs...

end
```

实际上，对于多语言支持，通常需要添加额外的逻辑来实现根据不同语言启用不同的字体，这里不做详细说明。

## 点对点栅格化计算公式

游戏的字体渲染引擎有些不太清楚的细节。

如果需要在游戏中能够点对点的渲染字体，请尝试如下计算公式：

```text
游戏中设置的字号 = (字体字号 + 1) * 显示倍数 + 1
```

目前游戏使用 2x 显示字体，实际计算如下：

```text
FONT_SIZE = (13 + 1) * 2 + 1 = 29
SMALL_FONT_SIZE = (11 + 1) * 2 + 1 = 25
```

上述公式只是推理出来的，具体原理不详。

## 程序依赖

- [Pixel Font Builder](https://github.com/TakWolf/pixel-font-builder)
- [Pixel Font Knife](https://github.com/TakWolf/pixel-font-knife)
- [FontTools](https://github.com/fonttools/fonttools)
- [PyYAML](https://github.com/yaml/pyyaml)
- [Pillow](https://github.com/python-pillow/Pillow)
- [HTTPX](https://github.com/encode/httpx)
- [tqdm](https://github.com/tqdm/tqdm)
- [Loguru](https://github.com/Delgan/loguru)

## 许可证

分为「字体」和「构建程序」两个部分。

### 字体

使用 [「SIL 开放字体许可证第 1.1 版」](LICENSE-OFL) 授权。

上游字体许可证如下：

| 字体 | 许可证 | 备注 |
|---|---|---|
| [方舟像素字体 / Ark Pixel Font](https://github.com/TakWolf/ark-pixel-font) | [OFL-1.1](https://github.com/TakWolf/ark-pixel-font/blob/develop/LICENSE-OFL) | 提供 10、12 像素基础字形和参数 |
| [精品點陣體9×9 / BoutiqueBitmap9x9](https://github.com/scott0107000/BoutiqueBitmap9x9) | [OFL-1.1](https://github.com/scott0107000/BoutiqueBitmap9x9/blob/main/OFL.txt) | 提供 10 像素繁体中文汉字补充 |
| [俐方體11號／Cubic 11](https://github.com/ACh-K/Cubic-11) | [OFL-1.1](https://github.com/ACh-K/Cubic-11/blob/main/OFL.txt) | 提供 12 像素繁体中文汉字补充 |
| [Galmuri](https://github.com/quiple/galmuri) | [OFL-1.1](https://github.com/quiple/galmuri/blob/main/ofl.md) | 提供 10、12 像素朝鲜语相关字形 |

### 构建程序

使用 [「MIT 许可证」](LICENSE-MIT) 授权。
