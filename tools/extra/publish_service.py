from zipfile import ZipFile

from loguru import logger

from tools.config import paths, project, manifest


def make_release_zip() -> None:
    paths.RELEASES_DIR.mkdir(parents=True, exist_ok=True)

    zip_file_path = paths.RELEASES_DIR.joinpath(f'{project.FILE_NAME_PREFIX}-font-v{project.VERSION}.zip')
    with ZipFile(zip_file_path, 'w') as file:
        file.write(paths.PROJECT_ROOT_DIR.joinpath('LICENSE-OFL'), 'OFL.txt')

        for font_name, file_names in sorted(manifest.LICENSE_CONFIGS.items()):
            for file_name in file_names:
                file.write(paths.FONTS_DIR.joinpath(font_name, file_name), f'LICENSES/{font_name}/{file_name}')

        for font_file_path in sorted(paths.OUTPUTS_DIR.glob('*.ttf')):
            if not font_file_path.is_file():
                continue
            file.write(font_file_path, font_file_path.name)
    logger.info('Make release zip: {!r}', str(zip_file_path))
