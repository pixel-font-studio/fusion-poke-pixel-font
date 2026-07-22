import shutil

from tools.configs import path_define
from tools.services import setup_service, dump_service, font_service, publish_service


def main():
    if path_define.build_dir.exists():
        shutil.rmtree(path_define.build_dir)

    setup_service.setup_ark_pixel()

    dump_service.dump_fonts()
    dump_service.apply_fallbacks()

    contexts_12 = font_service.load_contexts(12)
    font_service.make_fonts(12, 'Normal', contexts_12, False)
    font_service.make_fonts(12, 'Narrow', contexts_12, True)

    contexts_10 = font_service.load_contexts(10)
    font_service.make_fonts(10, 'Small', contexts_10, False)

    publish_service.make_release_zip()


if __name__ == '__main__':
    main()
