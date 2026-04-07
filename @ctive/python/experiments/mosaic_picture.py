import argparse
import os
from pathlib import Path
from typing import List, Tuple, Optional
from PIL import Image
import numpy as np


def center_crop_to_aspect(img: Image.Image, target_aspect_w_over_h: float) -> Image.Image:
    w, h = img.size
    current_aspect = w / h
    if abs(current_aspect - target_aspect_w_over_h) < 1e-9:
        return img

    if current_aspect > target_aspect_w_over_h:
        # Too wide -> crop width
        new_w = int(round(h * target_aspect_w_over_h))
        left = (w - new_w) // 2
        return img.crop((left, 0, left + new_w, h))
    else:
        # Too tall -> crop height
        new_h = int(round(w / target_aspect_w_over_h))
        top = (h - new_h) // 2
        return img.crop((0, top, w, top + new_h))


def average_color(img: Image.Image) -> np.ndarray:
    # Convert to RGB, downsample to speed up, compute mean per channel
    arr = np.asarray(img.convert("RGB"))
    # Flatten and mean over spatial dims; result shape (3,)
    return arr.reshape(-1, 3).mean(axis=0).astype(np.float32)


def list_images(folder: Path) -> List[Path]:
    exts = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}
    return [p for p in folder.rglob("*") if p.suffix.lower() in exts]


def prepare_small_images(
    smalls_dir: Path,
    target_aspect: float,
    tile_w: int,
    tile_h: int,
    save_cropped_dir: Optional[Path] = None,
) -> Tuple[List[Image.Image], np.ndarray]:
    paths = list_images(smalls_dir)
    if not paths:
        raise RuntimeError(f"No images found in: {smalls_dir}")

    processed_imgs: List[Image.Image] = []
    features: List[np.ndarray] = []

    if save_cropped_dir:
        save_cropped_dir.mkdir(parents=True, exist_ok=True)

    for p in paths:
        try:
            with Image.open(p) as im:
                im = im.convert("RGB")
                im = center_crop_to_aspect(im, target_aspect)
                im = im.resize((tile_w, tile_h), Image.Resampling.LANCZOS)
                feat = average_color(im)
                processed_imgs.append(im)
                features.append(feat)
                if save_cropped_dir:
                    out_path = save_cropped_dir / p.name
                    im.save(out_path, quality=90)
        except Exception:
            # Skip unreadable/corrupt files
            continue

    if not processed_imgs:
        raise RuntimeError("No valid small images after preprocessing.")

    return processed_imgs, np.vstack(features)


def crop_big_to_grid(big: Image.Image, rows: int, cols: int) -> Tuple[Image.Image, int, int]:
    W, H = big.size
    tile_w = W // cols
    tile_h = H // rows
    new_W = tile_w * cols
    new_H = tile_h * rows
    # Center-crop big to exact grid multiple to avoid partial tiles
    left = (W - new_W) // 2
    top = (H - new_H) // 2
    big_cropped = big.crop((left, top, left + new_W, top + new_H))
    return big_cropped, tile_h, tile_w


def tile_average_colors(big: Image.Image, rows: int, cols: int) -> np.ndarray:
    big_rgb = big.convert("RGB")
    W, H = big_rgb.size
    tile_w = W // cols
    tile_h = H // rows

    # Compute mean color per tile
    means = np.zeros((rows * cols, 3), dtype=np.float32)
    idx = 0
    for r in range(rows):
        for c in range(cols):
            x0 = c * tile_w
            y0 = r * tile_h
            tile = big_rgb.crop((x0, y0, x0 + tile_w, y0 + tile_h))
            means[idx] = average_color(tile)
            idx += 1
    return means


def assign_tiles(
    tile_feats: np.ndarray,  # (M,3)
    img_feats: np.ndarray,   # (N,3)
) -> np.ndarray:
    # For each tile, find nearest small image by Euclidean distance in RGB space
    # tile_feats: Mx3, img_feats: Nx3
    # Compute distances in blocks to be memory friendly if needed
    M = tile_feats.shape[0]
    N = img_feats.shape[0]
    assignments = np.empty(M, dtype=np.int32)

    # Simple full-matrix vectorized nearest neighbor
    # dist^2 = sum((tile - img)^2)
    # Expand dims: (M,1,3) vs (1,N,3) -> (M,N,3) -> (M,N)
    dists = ((tile_feats[:, None, :] - img_feats[None, :, :]) ** 2).sum(axis=2)  # (M,N)
    assignments = dists.argmin(axis=1)
    return assignments


def build_mosaic(
    big_cropped: Image.Image,
    rows: int,
    cols: int,
    tile_w: int,
    tile_h: int,
    small_imgs: List[Image.Image],
    assignments: np.ndarray,
) -> Image.Image:
    mosaic = Image.new("RGB", (tile_w * cols, tile_h * rows))
    idx = 0
    for r in range(rows):
        for c in range(cols):
            small_im = small_imgs[assignments[idx]]
            # Already at tile size; paste
            mosaic.paste(small_im, (c * tile_w, r * tile_h))
            idx += 1
    return mosaic


def main():
    parser = argparse.ArgumentParser(description="Create a photo mosaic from a big image and many small images.")
    parser.add_argument("--big", required=True, help="Path to the big image.")
    parser.add_argument("--smalls", required=True, help="Path to folder containing small images.")
    parser.add_argument("--out", required=True, help="Output mosaic image path (e.g., mosaic.jpg).")
    parser.add_argument("--rows", type=int, default=55, help="Number of rows in the mosaic grid (default: 55).")
    parser.add_argument("--cols", type=int, default=55, help="Number of columns in the mosaic grid (default: 55).")
    parser.add_argument("--save-cropped-smalls", default=None, help="Optional directory to save cropped smalls.")
    parser.add_argument("--resize-big", type=int, nargs=2, metavar=("WIDTH", "HEIGHT"),
                        help="Optional target size for the big image before tiling (WIDTH HEIGHT).")
    args = parser.parse_args()

    big_path = Path(args.big)
    smalls_dir = Path(args.smalls)
    out_path = Path(args.out)
    save_cropped_dir = Path(args.save_cropped_smalls) if args.save_cropped_smalls else None

    if not big_path.exists():
        raise FileNotFoundError(f"Big image not found: {big_path}")
    if not smalls_dir.exists():
        raise FileNotFoundError(f"Smalls folder not found: {smalls_dir}")

    # Load big image
    with Image.open(big_path) as big_img:
        big_img = big_img.convert("RGB")
        if args.resize_big:
            big_img = big_img.resize((args.resize_big[0], args.resize_big[1]), Image.Resampling.LANCZOS)

        # Ensure big image fits grid perfectly (center-crop to multiple of rows/cols)
        big_cropped, tile_h, tile_w = crop_big_to_grid(big_img, args.rows, args.cols)
        target_aspect = (tile_w * args.cols) / (tile_h * args.rows)  # same as big_cropped aspect

        # Prepare small images: center-crop to target aspect, then resize to tile size
        small_imgs, img_feats = prepare_small_images(
            smalls_dir=smalls_dir,
            target_aspect=tile_w / tile_h,  # aspect for each tile equals big's aspect
            tile_w=tile_w,
            tile_h=tile_h,
            save_cropped_dir=save_cropped_dir,
        )

        # Compute average color per tile of big image
        tile_feats = tile_average_colors(big_cropped, args.rows, args.cols)

        # Nearest neighbor assignment
        assignments = assign_tiles(tile_feats, img_feats)

        # Build mosaic
        mosaic = build_mosaic(
            big_cropped=big_cropped,
            rows=args.rows,
            cols=args.cols,
            tile_w=tile_w,
            tile_h=tile_h,
            small_imgs=small_imgs,
            assignments=assignments,
        )

        # Save
        out_path.parent.mkdir(parents=True, exist_ok=True)
        # JPEG default quality; adjust if PNG is desired
        if out_path.suffix.lower() in {".jpg", ".jpeg"}:
            mosaic.save(out_path, quality=90, subsampling=1, optimize=True)
        else:
            mosaic.save(out_path)

        print(f"Saved mosaic to: {out_path}")


if __name__ == "__main__":
    main()