# 融合口袋像素字体 / Fusion Poke Pixel Font

[![License OFL](https://img.shields.io/badge/license-OFL--1.1-orange?style=flat-square)](LICENSE-OFL)
[![License MIT](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE-MIT)
[![Releases](https://img.shields.io/github/v/release/pixel-font-studio/fusion-poke-pixel-font?style=flat-square)](https://github.com/pixel-font-studio/fusion-poke-pixel-font/releases)

这是一个为同人游戏 [「宝可梦无限融合 / Pokémon Infinite Fusion」](https://discord.gg/infinitefusion) 定制的字体项目。

设计上用于替换游戏的默认字体，以提供更好的显示效果。字符范围支持泛拉丁和泛中日韩语言，可用于游戏大部分多国语的字体解决方案。

本项目构建修改自 [「缝合像素字体」](https://github.com/TakWolf/fusion-pixel-font) 项目，并以 [「无限融合2：丰缘 / Infinite Fusion 2: Hoenn」](https://github.com/infinitefusion/infinitefusion-hoenn-public) 作为适配目标。

由于衍生自「Fusion Pixel Font」字体，因此字体名中带有「Fusion」单词。这只是一个巧合，和游戏名中的「Fusion」没有直接关系。

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
> 为了适配 [mkxp-z](https://github.com/mkxp-z/mkxp-z) 字体渲染相关的一些特殊行为，本字体参数做了一些特殊处理，所以可能无法正常用于普通项目。

## 字体变种

字体包含三个变种，与默认字体对应关系如下：

| 字体名称 | 对应的默认字体 | 栅格化字号 |
|---|---|---|
| Fusion Poke Pixel Normal | Power Green | 13px |
| Fusion Poke Pixel Narrow | Power Green Narrow | 13px |
| Fusion Poke Pixel Small | Power Green Small | 11px |


## 语言支持

目前支持以下语言特定字形版本：

| 版本 | 含义 |
|---|---|
| latin | 泛拉丁语 |
| zh_hans | 简体中文 |
| zh_hant | 繁體中文 |
| ja | 日语 |
| ko | 朝鲜语 |

## 使用方式

[点击此链接](https://github.com/pixel-font-studio/fusion-poke-pixel-font/releases) 下载最新版本。

将压缩包所有字体，复制到 `游戏/Fonts/` 文件夹中。

使用文本编辑器打开 `游戏/Data/Scripts/007_Objects and windows/002_MessageConfig.rb`，找到并修改如下部分：

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

以上仅以简体中文作为示例。实际上，对于多语言支持，通常需要添加额外的逻辑来实现根据不同语言启用不同的字体，这里不做详细说明。

## 点对点栅格化计算公式

游戏的运行时在字体渲染部分存在一些特殊行为，需要特殊化处理才能正常显示。

根据游戏脚本 [scripts/001_Technical/001_MKXP_Compatibility.rb#L1](https://github.com/infinitefusion/scripts/blob/main/001_Technical/001_MKXP_Compatibility.rb#L1) 可知：

```ruby
# Using mkxp-z v2.2.0 - https://gitlab.com/mkxp-z/mkxp-z/-/releases/v2.2.0
```

游戏使用 [mkxp-z v2.2.0](https://github.com/mkxp-z/mkxp-z/tree/v2.2.0) 作为运行时。

该版本中，存在一处对字体的特殊处理，见 [src/display/font.cpp#L198-L201](https://github.com/mkxp-z/mkxp-z/blob/v2.2.0/src/display/font.cpp#L198-L201)：

```cpp
//  FIXME 0.9 is guesswork at this point
//  float gamma = (96.0/45.0)*(5.0/14.0)*(size-5);
//  font = TTF_OpenFontRW(ops, 1, gamma /** .90*/);
    font = TTF_OpenFontRW(ops, 1, size* 0.90f);
```

这意味着，所有加载的字体，其尺寸都会先乘以 0.9 再交给 SDL_ttf 进行栅格化。

这大概率是为了接近原版 RGSS/Windows GDI 的字体显示效果，但这是一个经验修正，并不是基于字体度量的精确换算。因此对于像素字体，需要额外反向补偿。

因此，为了让字体能够点对点栅格化显示，需要使用以下公式计算游戏中的字体字号，以抵消其缩放影响：

```text
游戏中设置的字号 = ceil(字体字号 * 显示倍数 / 0.9)
```

游戏中的字体目前以 2 倍显示，在使用本字体时，相关字号应该设置为：

```text
FONT_SIZE = ceil(13 * 2 / 0.9) = 29
SMALL_FONT_SIZE = ceil(11 * 2 / 0.9) = 25
```

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
