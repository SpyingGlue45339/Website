from pathlib import Path
import pygame


PHOTO_DIR = Path(__file__).resolve().parent / "photos"

SECTION_CODES = {
    "Economy": "e",
    "Government": "g",
    "Society": "s",
    "Culture": "c",
}

PHOTO_BOX = (720, 342)


def photo_path(section_name, question_number):
    code = SECTION_CODES.get(section_name)
    if code is None:
        return None
    return PHOTO_DIR / f"{code}{question_number}.jpg"


def fit_photo(image, box_size=PHOTO_BOX):
    """Scale an image proportionally so it fits a fixed visual box.

    This is a 'contain' fit rather than a stretch or crop. The image keeps
    its original aspect ratio and uses as much of the box as possible.
    """
    box_w, box_h = box_size
    iw, ih = image.get_size()

    if iw <= 0 or ih <= 0:
        return None

    scale = min(box_w / iw, box_h / ih)
    new_size = (
        max(1, round(iw * scale)),
        max(1, round(ih * scale)),
    )

    return pygame.transform.smoothscale(image, new_size)


def photo_for_question(section_name, question_number):
    """Return the proportionally fitted JPG, or None if it is absent."""
    path = photo_path(section_name, question_number)
    if path is None or not path.exists():
        return None

    try:
        image = pygame.image.load(str(path)).convert()
        return fit_photo(image)
    except (pygame.error, OSError):
        return None
