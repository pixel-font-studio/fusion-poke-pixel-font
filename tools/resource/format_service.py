import sys

from pixel_font_knife.cmap.context import CmapContext
from pixel_font_knife.cmap.mapping.mapping import CmapMapping
from pixel_font_knife.utils import fs_util

from tools.config import path_define, options
from tools.config.options import FontSize


def normalize_cmap_glyphs(font_size: FontSize) -> None:
    for glyphs_dir in (path_define.PATCH_GLYPHS_DIR, path_define.POKE_GLYPHS_DIR):
        for glyph_scope in options.GLYPH_SCOPES:
            glyph_scope_dir = glyphs_dir.joinpath(str(font_size), 'cmap', glyph_scope)
            context = CmapContext.load(glyph_scope_dir, allowed_flavors=options.LANGUAGE_FLAVORS)
            context.normalize(glyph_scope_dir, flavor_order=options.LANGUAGE_FLAVORS)


def format_glyphs() -> None:
    if sys.platform != 'win32':
        for glyphs_dir in (path_define.PATCH_GLYPHS_DIR, path_define.POKE_GLYPHS_DIR):
            fs_util.format_glyph_files(glyphs_dir)


def format_mappings() -> None:
    for file_path in path_define.CONFIGS_MAPPINGS_DIR.rglob('*.yaml'):
        if not file_path.is_file():
            continue

        mapping = CmapMapping.load_yaml(file_path, allowed_flavors=options.LANGUAGE_FLAVORS)
        mapping.save_yaml(file_path, flavor_order=options.LANGUAGE_FLAVORS)
