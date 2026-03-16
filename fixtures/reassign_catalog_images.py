"""
Run with:
    python manage.py shell < /mnt/data/reassign_catalog_images.py

What it does:
- Reassigns existing Product thumbnails/images randomly from:
    media/product/images/placeholders/
- Reassigns existing Brand images randomly from:
    media/brand/images/placeholders/
- Optionally reassigns existing Category images from:
    media/category/images/placeholders/

Adjust the flags below if needed.
"""

import random
from pathlib import Path
from django.conf import settings

from product.models import Product, Brand, Category

RANDOM_SEED = 42
UPDATE_PRODUCTS = True
UPDATE_BRANDS = True
UPDATE_CATEGORIES = True  # set to False if you do not want this

PRODUCT_DIR = "product/images/placeholders"
BRAND_DIR = "brand/images/placeholders"
CATEGORY_DIR = "category/images/placeholders"

random.seed(RANDOM_SEED)


def rel_files(relative_dir: str):
    base = Path(settings.MEDIA_ROOT) / relative_dir
    if not base.exists():
        raise SystemExit(f"Missing directory: {base}")
    files = sorted([p for p in base.iterdir() if p.is_file() and p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}])
    if not files:
        raise SystemExit(f"No image files found in: {base}")
    return [str(Path(relative_dir) / p.name) for p in files]


product_images = rel_files(PRODUCT_DIR) if UPDATE_PRODUCTS else []
brand_images = rel_files(BRAND_DIR) if UPDATE_BRANDS else []
category_images = rel_files(CATEGORY_DIR) if UPDATE_CATEGORIES else []

updated_products = 0
updated_brands = 0
updated_categories = 0

if UPDATE_PRODUCTS:
    for i, product in enumerate(Product.objects.all(), start=1):
        product.thumbnail = random.choice(product_images)
        product.image1 = random.choice(product_images)
        product.image2 = random.choice(product_images)
        product.image3 = random.choice(product_images)
        product.image4 = random.choice(product_images)
        product.save(update_fields=["thumbnail", "image1", "image2", "image3", "image4"])
        updated_products += 1

if UPDATE_BRANDS:
    for brand in Brand.objects.all():
        brand.image = random.choice(brand_images)
        brand.save(update_fields=["image"])
        updated_brands += 1

if UPDATE_CATEGORIES:
    for category in Category.objects.all():
        category.image = random.choice(category_images)
        category.save(update_fields=["image"])
        updated_categories += 1

print("=" * 60)
print("Image reassignment complete")
print(f"Products updated:   {updated_products}")
print(f"Brands updated:     {updated_brands}")
print(f"Categories updated: {updated_categories}")
print("=" * 60)
