from zipfile import ZipFile

from loguru import logger

from tools.config import path_define, project, manifest


def make_release_zip() -> None:
    path_define.RELEASES_DIR.mkdir(parents=True, exist_ok=True)

    zip_file_path = path_define.RELEASES_DIR.joinpath(f'{project.FILE_NAME_PREFIX}-font-v{project.VERSION}.zip')
    with ZipFile(zip_file_path, 'w') as file:
        file.write(path_define.PROJECT_ROOT_DIR.joinpath('LICENSE-OFL'), 'OFL.txt')

        for font_name, file_names in sorted(manifest.LICENSE_CONFIGS.items()):
            for file_name in file_names:
                file.write(path_define.FONTS_DIR.joinpath(font_name, file_name), f'LICENSES/{font_name}/{file_name}')

        for font_file_path in sorted(path_define.OUTPUTS_DIR.glob('*.ttf')):
            if not font_file_path.is_file():
                continue
            file.write(font_file_path, font_file_path.name)
    logger.info("Make release zip: '{}'", zip_file_path)
