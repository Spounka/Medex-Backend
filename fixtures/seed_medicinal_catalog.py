"""
Run with:
    python manage.py shell < /mnt/data/seed_medicinal_catalog.py

Optional: copy the generated placeholder images into your MEDIA_ROOT:
    mkdir -p uploads/images/placeholder/medicines
    cp /mnt/data/medicinal_placeholders/*.png uploads/images/placeholder/medicines/

What it does:
- Creates a parent "Medicines" category plus several child categories
- Creates several pharma-style brands
- Uses an existing supplier user (default: supplier@example.com)
- Creates many realistic dummy medicinal products
- Assigns shared placeholder image paths so the UI can render images if MEDIA is served
"""

import random
from decimal import Decimal

from django.db import transaction
from django.utils.text import slugify

from account.models import User
from product.models import Brand, Category, Product

SUPPLIER_EMAIL = "supplier@example.com"
RANDOM_SEED = 42
PRODUCTS_PER_CATEGORY = 40  # 10 categories x 40 = ~400 products

random.seed(RANDOM_SEED)

CATEGORY_DATA = {
    "Analgesics": [
        "Paracetamol",
        "Ibuprofen",
        "Diclofenac",
        "Naproxen",
        "Ketoprofen",
        "Celecoxib",
        "Mefenamic Acid",
        "Aspirin",
        "Meloxicam",
        "Tramadol",
    ],
    "Antibiotics": [
        "Amoxicillin",
        "Azithromycin",
        "Cefixime",
        "Ciprofloxacin",
        "Doxycycline",
        "Metronidazole",
        "Clarithromycin",
        "Levofloxacin",
        "Cefuroxime",
        "Clindamycin",
    ],
    "Antihistamines": [
        "Cetirizine",
        "Loratadine",
        "Fexofenadine",
        "Desloratadine",
        "Chlorpheniramine",
        "Levocetirizine",
        "Diphenhydramine",
        "Bilastine",
        "Hydroxyzine",
        "Promethazine",
    ],
    "Gastrointestinal": [
        "Omeprazole",
        "Pantoprazole",
        "Esomeprazole",
        "Famotidine",
        "Domperidone",
        "Ondansetron",
        "Loperamide",
        "Simethicone",
        "Lactulose",
        "Bisacodyl",
    ],
    "Vitamins & Supplements": [
        "Vitamin C",
        "Vitamin D3",
        "Magnesium",
        "Zinc",
        "Calcium",
        "Iron",
        "Folic Acid",
        "Vitamin B Complex",
        "Omega 3",
        "Multivitamin",
    ],
    "Cardiovascular": [
        "Amlodipine",
        "Losartan",
        "Valsartan",
        "Bisoprolol",
        "Atorvastatin",
        "Rosuvastatin",
        "Clopidogrel",
        "Furosemide",
        "Spironolactone",
        "Ramipril",
    ],
    "Diabetes Care": [
        "Metformin",
        "Gliclazide",
        "Glimepiride",
        "Sitagliptin",
        "Empagliflozin",
        "Linagliptin",
        "Pioglitazone",
        "Insulin Glargine",
        "Insulin Aspart",
        "Vildagliptin",
    ],
    "Respiratory": [
        "Salbutamol",
        "Budesonide",
        "Montelukast",
        "Theophylline",
        "Acetylcysteine",
        "Ambroxol",
        "Bromhexine",
        "Ipratropium",
        "Formoterol",
        "Fluticasone",
    ],
    "Dermatology": [
        "Clotrimazole",
        "Hydrocortisone",
        "Mupirocin",
        "Ketoconazole",
        "Adapalene",
        "Benzoyl Peroxide",
        "Tacrolimus",
        "Calamine",
        "Urea Cream",
        "Fusidic Acid",
    ],
    "First Aid & Antiseptics": [
        "Povidone Iodine",
        "Chlorhexidine",
        "Hydrogen Peroxide",
        "Silver Sulfadiazine",
        "Alcohol Swabs",
        "Sterile Saline",
        "Burn Gel",
        "Wound Ointment",
        "Antiseptic Spray",
        "Gauze Kit",
    ],
}

BRANDS = [
    "Medixa",
    "NovaCure",
    "PharmaZen",
    "BioRelief",
    "CuraPlus",
    "Healora",
    "Vitalis",
    "Remedica",
    "Zenomed",
    "Alphacare",
    "CoreMeds",
    "Clinovia",
    "EverPharm",
    "PureDose",
    "MediSphere",
]

FORMS = [
    "Tablets",
    "Capsules",
    "Syrup",
    "Suspension",
    "Cream",
    "Gel",
    "Ointment",
    "Drops",
    "Spray",
    "Injection",
    "Inhaler",
    "Powder",
    "Sachets",
]

STRENGTHS = [
    "5mg",
    "10mg",
    "20mg",
    "25mg",
    "50mg",
    "75mg",
    "100mg",
    "200mg",
    "250mg",
    "400mg",
    "500mg",
    "625mg",
    "850mg",
    "1g",
    "2mg/5ml",
    "5mg/5ml",
]

PACK_SIZES = [
    "10 units",
    "14 units",
    "20 units",
    "28 units",
    "30 units",
    "50 units",
    "60 units",
    "100ml",
    "120ml",
    "150ml",
]

DESCRIPTORS = [
    "for symptomatic relief",
    "for daily therapeutic use",
    "for physician-guided treatment",
    "for moderate case management",
    "for routine pharmacy stock",
    "for adult outpatient care",
    "for general household use",
    "for short treatment cycles",
    "for supportive therapy",
    "for common seasonal conditions",
]

IMAGE_POOL = [
    "images/placeholder/medicines/product_1.png",
    "images/placeholder/medicines/product_2.png",
    "images/placeholder/medicines/product_3.png",
    "images/placeholder/medicines/product_4.png",
]

CATEGORY_IMAGE = "images/placeholder/medicines/category.png"
BRAND_IMAGE = "images/placeholder/medicines/brand.png"


def money(value: float) -> Decimal:
    return Decimal(str(round(value, 2)))


def ensure_supplier(email: str) -> User:
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        raise SystemExit(
            f"Supplier user {email!r} was not found. " "Create or seed that user first."
        )


def get_or_create_categories():
    root, _ = Category.objects.get_or_create(
        name="Medicines",
        defaults={
            "slug": "medicines",
            "image": CATEGORY_IMAGE,
            "is_featured": True,
            "parent": None,
        },
    )
    categories = {}
    for name in CATEGORY_DATA.keys():
        category, created = Category.objects.get_or_create(
            name=name,
            defaults={
                "slug": slugify(name),
                "image": CATEGORY_IMAGE,
                "is_featured": random.choice([True, False]),
                "parent": root,
            },
        )
        if not created:
            changed = False
            if category.parent_id != root.id:
                category.parent = root
                changed = True
            if not category.slug:
                category.slug = slugify(name)
                changed = True
            if not category.image:
                category.image = CATEGORY_IMAGE
                changed = True
            if changed:
                category.save()
        categories[name] = category
    return categories


def get_or_create_brands():
    brand_map = {}
    for name in BRANDS:
        brand, _ = Brand.objects.get_or_create(
            name=name,
            defaults={
                "slug": slugify(name),
                "image": BRAND_IMAGE,
            },
        )
        if not brand.slug:
            brand.slug = slugify(name)
            brand.save()
        brand_map[name] = brand
    return brand_map


def build_product_name(base_name: str, strength: str, form: str) -> str:
    return f"{base_name} {strength} {form}"


def build_description(base_name: str, strength: str, form: str, descriptor: str) -> str:
    return (
        f"{base_name} {strength} in {form.lower()} form, intended {descriptor}. "
        "Dummy catalog entry for local development and UI testing only. "
        "Not real prescribing guidance."
    )


def choose_price(category_name: str):
    base_map = {
        "Analgesics": 3.5,
        "Antibiotics": 7.5,
        "Antihistamines": 4.5,
        "Gastrointestinal": 5.0,
        "Vitamins & Supplements": 6.0,
        "Cardiovascular": 9.0,
        "Diabetes Care": 12.0,
        "Respiratory": 8.5,
        "Dermatology": 6.5,
        "First Aid & Antiseptics": 4.0,
    }
    base = base_map.get(category_name, 5.0)
    price = money(random.uniform(base, base * 8))
    sale_price = money(float(price) * random.uniform(0.70, 1.00))
    range_min = money(max(0.5, float(sale_price) * random.uniform(0.85, 0.97)))
    range_max = money(float(price) * random.uniform(1.03, 1.22))
    return price, sale_price, range_min, range_max


@transaction.atomic
def run():
    supplier = ensure_supplier(SUPPLIER_EMAIL)
    categories = get_or_create_categories()
    brands = get_or_create_brands()

    created_count = 0
    updated_count = 0

    for category_name, actives in CATEGORY_DATA.items():
        category = categories[category_name]
        for idx in range(PRODUCTS_PER_CATEGORY):
            base_name = actives[idx % len(actives)]
            strength = random.choice(STRENGTHS)
            form = random.choice(FORMS)
            brand = brands[random.choice(BRANDS)]
            pack_size = random.choice(PACK_SIZES)
            descriptor = random.choice(DESCRIPTORS)
            image_path = random.choice(IMAGE_POOL)

            display_name = build_product_name(base_name, strength, form)
            unique_name = f"{display_name} - {pack_size} - {brand.name}"

            price, sale_price, range_min, range_max = choose_price(category_name)

            defaults = {
                "supplier": supplier,
                "description": build_description(base_name, strength, form, descriptor),
                "price": price,
                "sale_price": sale_price,
                "price_range_min": range_min,
                "price_range_max": range_max,
                "category": category,
                "brand": brand,
                "stock_quantity": random.randint(10, 500),
                "is_available": True,
                "is_returnable": random.choice([True, True, True, False]),
                "return_deadline": random.choice([7, 14, 21, 30]),
                "thumbnail": image_path,
                "image1": image_path,
                "image2": random.choice(IMAGE_POOL),
                "image3": random.choice(IMAGE_POOL),
                "image4": random.choice(IMAGE_POOL),
            }

            obj, created = Product.objects.get_or_create(
                name=unique_name,
                supplier=supplier,
                defaults=defaults,
            )
            if created:
                created_count += 1
            else:
                changed = False
                for field, value in defaults.items():
                    current = getattr(obj, field)
                    if current != value:
                        setattr(obj, field, value)
                        changed = True
                if changed:
                    obj.save()
                    updated_count += 1

    total = Product.objects.filter(
        supplier=supplier, category__name__in=CATEGORY_DATA.keys()
    ).count()

    print("=" * 60)
    print("Medicinal catalog seed completed")
    print(f"Supplier: {supplier.email}")
    print(f"Created:  {created_count}")
    print(f"Updated:  {updated_count}")
    print(f"Total matching products now: {total}")
    print("=" * 60)


run()
