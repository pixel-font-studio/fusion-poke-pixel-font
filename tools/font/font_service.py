from collections.abc import Mapping, Sequence
from datetime import datetime

from loguru import logger
from pixel_font_builder import FontBuilder, WeightName, SerifStyle, SlantStyle, WidthStyle, Glyph
from pixel_font_knife.cmap.context import CmapContext
from pixel_font_knife.cmap.mapping.mapping import CmapMapping
from pixel_font_knife.named.file import NamedGlyphFile

from tools.config import path_define, project, manifest, options
from tools.config.font import FontConfig
from tools.config.options import FontSize, GlyphScope, LanguageFlavor


def load_contexts(font_size: FontSize) -> tuple[NamedGlyphFile, Mapping[GlyphScope, CmapContext]]:
    notdef_glyph_file = NamedGlyphFile.load_notdef(path_define.PATCH_GLYPHS_DIR.joinpath(str(font_size), 'notdef.png'))

    cmap_scope_contexts = {
        glyph_scope: CmapContext().merge_by_code_point(
            CmapContext.load(
                path_define.FALLBACK_GLYPHS_DIR.joinpath(str(font_size), 'cmap', glyph_scope),
                allowed_flavors=options.LANGUAGE_FLAVORS,
            ).with_default_flavor(options.LANGUAGE_FLAVORS),
            CmapContext.load(
                path_define.ARK_PIXEL_GLYPHS_DIR.joinpath(str(font_size), 'cmap', glyph_scope),
                allowed_flavors=options.LANGUAGE_FLAVORS,
            ),
            CmapContext.load(
                path_define.PATCH_GLYPHS_DIR.joinpath(str(font_size), 'cmap', glyph_scope),
                allowed_flavors=options.LANGUAGE_FLAVORS,
            ),
            CmapContext.load(
                path_define.POKE_GLYPHS_DIR.joinpath(str(font_size), 'cmap', glyph_scope),
                allowed_flavors=options.LANGUAGE_FLAVORS,
            ),
            conflict='replace',
        )
        for glyph_scope in options.GLYPH_SCOPES
    }

    return notdef_glyph_file, cmap_scope_contexts


def _create_builder(
        font_config: FontConfig,
        family_name_patch: str,
        notdef_glyph_file: NamedGlyphFile,
        cmap_context: CmapContext,
        language_flavor: LanguageFlavor,
) -> FontBuilder:
    builder = FontBuilder()
    builder.font_metric.font_size = font_config.font_size
    builder.font_metric.horizontal_layout.ascent = font_config.ascent
    builder.font_metric.horizontal_layout.descent = font_config.descent
    builder.font_metric.x_height = font_config.x_height
    builder.font_metric.cap_height = font_config.cap_height
    builder.font_metric.underline_position = font_config.underline_position
    builder.font_metric.underline_thickness = 1
    builder.font_metric.strikeout_position = font_config.strikeout_position
    builder.font_metric.strikeout_thickness = 1

    builder.meta_info.version = project.VERSION
    builder.meta_info.created_time = datetime.fromisoformat(f'{project.VERSION.replace('.', '-')}T00:00:00Z')
    builder.meta_info.modified_time = builder.meta_info.created_time
    builder.meta_info.family_name = f'{project.FAMILY_NAME_PREFIX} {family_name_patch} {manifest.LANGUAGE_FLAVOR_TO_FONT_NAME[language_flavor]}'
    builder.meta_info.weight_name = WeightName.REGULAR
    builder.meta_info.serif_style = SerifStyle.SANS_SERIF
    builder.meta_info.slant_style = SlantStyle.NORMAL
    builder.meta_info.width_style = WidthStyle.PROPORTIONAL
    builder.meta_info.manufacturer = project.MANUFACTURER
    builder.meta_info.designer = project.DESIGNER
    builder.meta_info.description = project.DESCRIPTION
    builder.meta_info.copyright_info = project.COPYRIGHT_INFO
    builder.meta_info.license_info = project.LICENSE_INFO
    builder.meta_info.vendor_url = project.VENDOR_URL
    builder.meta_info.designer_url = project.DESIGNER_URL
    builder.meta_info.license_url = project.LICENSE_URL

    glyph_sequence = [notdef_glyph_file] + cmap_context.get_glyph_sequence(language_flavor)
    for glyph_file in glyph_sequence:
        builder.glyphs.append(Glyph(
            name=glyph_file.glyph_name,
            horizontal_offset=glyph_file.canvas.horizontal_offset_for_trimmed(font_config.font_size, font_config.baseline),
            advance_width=glyph_file.canvas.advance_width(),
            bitmap=glyph_file.canvas.trimmed_bitmap.data,
        ))

    character_mapping = cmap_context.get_character_mapping(language_flavor)
    builder.character_mapping.update(character_mapping)

    builder.opentype_config.px_to_units = 64
    builder.opentype_config.has_vertical_metrics = False

    return builder


def make_fonts(
        font_size: FontSize,
        family_name_patch: str,
        notdef_glyph_file: NamedGlyphFile,
        cmap_scope_contexts: Mapping[GlyphScope, CmapContext],
        mappings: Sequence[CmapMapping],
        include_narrow: bool,
) -> None:
    path_define.OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

    font_config = FontConfig.load(font_size)

    cmap_context = CmapContext().merge_by_code_point(
        cmap_scope_contexts['common'],
        cmap_scope_contexts['proportional'],
        conflict='replace',
    )
    if include_narrow:
        cmap_context = cmap_context.merge_by_code_point(
            cmap_scope_contexts['narrow'],
            conflict='replace',
        )
    cmap_context = cmap_context.apply_mapping_by_flavor(
        *mappings,
        conflict='replace',
    )

    for language_flavor in options.LANGUAGE_FLAVORS:
        builder = _create_builder(font_config, family_name_patch, notdef_glyph_file, cmap_context, language_flavor)

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

        file_path = path_define.OUTPUTS_DIR.joinpath(f'{project.FILE_NAME_PREFIX}-{family_name_patch.lower()}-{language_flavor}.ttf')
        tt_font.save(file_path)
        logger.info('Make font: {!r}', str(file_path))
