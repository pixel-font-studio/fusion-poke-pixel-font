import shutil

from pixel_font_knife.cmap.mapping.mapping import CmapMapping

from tools.config import path_define, manifest, options
from tools.config.dump import DumpConfig
from tools.config.fallback import FallbackConfig
from tools.extra import publish_service
from tools.font import font_service
from tools.resource import setup_service, dump_service


def main() -> None:
    if path_define.BUILD_DIR.exists():
        shutil.rmtree(path_define.BUILD_DIR)

    setup_service.setup_ark_pixel()

    mappings = [
        CmapMapping.load_yaml(
            file_path,
            allowed_flavors=options.LANGUAGE_FLAVORS,
        )
        for file_paths in manifest.SCOPE_MAPPING_FILE_PATHS.values()
        for file_path in file_paths
    ]

    dump_configs = DumpConfig.load()
    dump_service.dump_fonts(dump_configs)

    fallback_configs = FallbackConfig.load()
    dump_service.apply_fallbacks(fallback_configs)

    notdef_12, cmap_scope_contexts_12 = font_service.load_contexts(12)
    font_service.make_fonts(12, 'Normal', notdef_12, cmap_scope_contexts_12, mappings, False)
    font_service.make_fonts(12, 'Narrow', notdef_12, cmap_scope_contexts_12, mappings, True)

    notdef_10, cmap_scope_contexts_10 = font_service.load_contexts(10)
    font_service.make_fonts(10, 'Small', notdef_10, cmap_scope_contexts_10, mappings, False)

    publish_service.make_release_zip()


if __name__ == '__main__':
    main()
