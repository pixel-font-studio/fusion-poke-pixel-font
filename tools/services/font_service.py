import math
from datetime import datetime

from loguru import logger
from pixel_font_builder import FontBuilder, WeightName, SerifStyle, SlantStyle, WidthStyle, Glyph
from pixel_font_knife import glyph_file_util, glyph_mapping_util
from pixel_font_knife.glyph_file_util import GlyphFlavorGroup

from tools import configs
from tools.configs import path_define, options, FontConfig
from tools.configs.options import FontSize, LanguageFlavor


def load_contexts(font_size: FontSize) -> dict[str, dict[int, GlyphFlavorGroup]]:
    contexts = {}
    for width_mode_dir_name in ('common', 'proportional', 'narrow'):
        context = glyph_file_util.load_context(path_define.fallback_glyphs_dir.joinpath(str(font_size), width_mode_dir_name))
        context.update(glyph_file_util.load_context(path_define.ark_pixel_glyphs_dir.joinpath(str(font_size), width_mode_dir_name)))
        context.update(glyph_file_util.load_context(path_define.patch_glyphs_dir.joinpath(str(font_size), width_mode_dir_name)))

        for flavor_group in context.values():
            if None not in flavor_group:
                for language_flavor in options.language_file_flavors:
                    if language_flavor in flavor_group:
                        flavor_group[None] = flavor_group[language_flavor]
                        break

        for mapping in configs.mappings:
            glyph_mapping_util.apply_mapping(context, mapping)

        for flavor_group in context.values():
            if 'zh_cn' in flavor_group:
                flavor_group['zh_hans'] = flavor_group['zh_cn']
            if 'zh_tr' in flavor_group:
                flavor_group['zh_hant'] = flavor_group['zh_tr']

        contexts[width_mode_dir_name] = context
    return contexts


def _create_builder(
        font_config: FontConfig,
        family_name_patch: str,
        glyph_files: dict[int, GlyphFlavorGroup],
        language_flavor: LanguageFlavor,
) -> FontBuilder:
    builder = FontBuilder()
    builder.font_metric.font_size = font_config.font_size
    builder.font_metric.horizontal_layout.ascent = font_config.ascent
    builder.font_metric.horizontal_layout.descent = font_config.descent
    builder.font_metric.vertical_layout.ascent = math.ceil(font_config.line_height / 2)
    builder.font_metric.vertical_layout.descent = -math.floor(font_config.line_height / 2)
    builder.font_metric.x_height = font_config.x_height
    builder.font_metric.cap_height = font_config.cap_height
    builder.font_metric.underline_position = font_config.underline_position
    builder.font_metric.underline_thickness = 1
    builder.font_metric.strikeout_position = font_config.strikeout_position
    builder.font_metric.strikeout_thickness = 1

    builder.meta_info.version = configs.version
    builder.meta_info.created_time = datetime.fromisoformat(f'{configs.version.replace('.', '-')}T00:00:00Z')
    builder.meta_info.modified_time = builder.meta_info.created_time
    builder.meta_info.family_name = f'Fusion Poke Pixel {family_name_patch} {language_flavor}'
    builder.meta_info.weight_name = WeightName.REGULAR
    builder.meta_info.serif_style = SerifStyle.SANS_SERIF
    builder.meta_info.slant_style = SlantStyle.NORMAL
    builder.meta_info.width_style = WidthStyle.PROPORTIONAL
    builder.meta_info.manufacturer = 'TakWolf'
    builder.meta_info.designer = 'TakWolf'
    builder.meta_info.description = 'Open source Pan-CJK pixel font'
    builder.meta_info.copyright_info = 'Copyright (c) 2026, TakWolf (https://takwolf.com)'
    builder.meta_info.license_info = 'This Font Software is licensed under the SIL Open Font License, Version 1.1'
    builder.meta_info.vendor_url = 'https://github.com/pixel-font-studio/fusion-poke-pixel-font'
    builder.meta_info.designer_url = 'https://takwolf.com'
    builder.meta_info.license_url = 'https://github.com/pixel-font-studio/fusion-poke-pixel-font/blob/master/LICENSE-OFL'

    glyph_sequence = glyph_file_util.get_glyph_sequence(glyph_files, [language_flavor])
    for glyph_file in glyph_sequence:
        horizontal_offset_x = 0
        horizontal_offset_y = font_config.baseline - font_config.font_size - (glyph_file.height - font_config.font_size) // 2
        advance_width = glyph_file.width

        builder.glyphs.append(Glyph(
            name=glyph_file.glyph_name,
            horizontal_offset=(horizontal_offset_x, horizontal_offset_y),
            advance_width=advance_width,
            bitmap=glyph_file.bitmap.data,
        ))

    character_mapping = glyph_file_util.get_character_mapping(glyph_files, language_flavor)
    builder.character_mapping.update(character_mapping)

    builder.opentype_config.px_to_units = 64
    builder.opentype_config.has_vertical_metrics = False

    return builder


def make_fonts(
        font_size: FontSize,
        family_name_patch: str,
        contexts: dict[str, dict[int, GlyphFlavorGroup]],
        include_narrow: bool,
):
    path_define.outputs_dir.mkdir(parents=True, exist_ok=True)

    font_config = configs.font_configs[font_size]

    glyph_files = contexts['common'] | contexts['proportional']
    if include_narrow:
        glyph_files.update(contexts['narrow'])

    for language_flavor in options.language_flavors:
        builder = _create_builder(font_config, family_name_patch, glyph_files, language_flavor)

        tt_font = builder.to_ttf_builder().font
        tb_head = tt_font['head']
        tb_hhea = tt_font['hhea']
        tb_os2 = tt_font['OS/2']
        if font_size == 12:
            tb_head.unitsPerEm = 832
            tb_hhea.ascent = 624
            tb_hhea.descent = 208
            tb_hhea.lineGap = 104
            tb_os2.sTypoAscender = 624
            tb_os2.sTypoDescender = 208
            tb_os2.sTypoLineGap = 104
            tb_os2.usWinAscent = 765
            tb_os2.usWinDescent = 232
        elif font_size == 10:
            tb_head.unitsPerEm = 704
            tb_hhea.ascent = 528
            tb_hhea.descent = 176
            tb_hhea.lineGap = 88
            tb_os2.sTypoAscender = 528
            tb_os2.sTypoDescender = 176
            tb_os2.sTypoLineGap = 88
            tb_os2.usWinAscent = 703
            tb_os2.usWinDescent = 88

        file_path = path_define.outputs_dir.joinpath(f'fusion-poke-pixel-{family_name_patch.lower()}-{language_flavor}.ttf')
        tt_font.save(file_path)
        logger.info("Make font: '{}'", file_path)
