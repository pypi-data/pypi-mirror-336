from typing import Optional, Tuple


def calc_new_size(
    cur_w, cur_h, target_w: int, target_h: int, keep_ratio=False
) -> tuple:
    if target_w is not None and target_w < 1:
        target_w = None
    if target_h is not None and target_h < 1:
        target_h = None
    if target_w is None and target_h is None:
        raise ValueError("At least one of w or h must be given")
    if target_w is None:
        ratio = target_h / cur_h
        target_w = int(cur_w * ratio)
    elif target_h is None:
        ratio = target_w / cur_w
        target_h = int(cur_h * ratio)

    if keep_ratio:
        ratio_w = target_w / cur_w
        ratio_h = target_h / cur_h
        ratio = min(ratio_w, ratio_h)
        target_w = int(cur_w * ratio)
        target_h = int(cur_h * ratio)

    new_w, new_h = target_w, target_h

    return new_w, new_h


def calc_crop_values(
    img_width: int,
    img_height: int,
    x1: Optional[int] = None,
    y1: Optional[int] = None,
    x2: Optional[int] = None,
    y2: Optional[int] = None,
) -> Tuple[int, int, int, int]:
    if x1 is None:
        x1 = 0
    if y1 is None:
        y1 = 0
    if x2 is None:
        x2 = img_width
    if y2 is None:
        y2 = img_height

    if x1 < 0 or x1 > img_width:
        x1 = x1 % img_width
    if y1 < 0 or y1 > img_height:
        y1 = y1 % img_height
    if x2 < 0 or x2 > img_width:
        x2 = x2 % img_width
    if y2 < 0 or y2 > img_height:
        y2 = y2 % img_height

    return x1, y1, x2, y2
