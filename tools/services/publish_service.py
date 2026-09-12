from zipfile import ZipFile

from loguru import logger

from tools import configs
from tools.configs import path_define


def make_release_zip() -> None:
    path_define.RELEASES_DIR.mkdir(parents=True, exist_ok=True)

    file_path = path_define.RELEASES_DIR.joinpath(f'fusion-poke-pixel-font-v{configs.VERSION}.zip')
    with ZipFile(file_path, 'w') as file:
        file.write(path_define.PROJECT_ROOT_DIR.joinpath('LICENSE-OFL'), 'OFL.txt')

        for font_name, file_names in sorted(configs.LICENSE_CONFIGS.items()):
            for file_name in file_names:
                file.write(path_define.FONTS_DIR.joinpath(font_name, file_name), f'LICENSES/{font_name}/{file_name}')

        for output_file_path in path_define.OUTPUTS_DIR.iterdir():
            if output_file_path.suffix != '.ttf':
                continue
            file.write(output_file_path, output_file_path.name)
    logger.info("Make release zip: '{}'", file_path)
