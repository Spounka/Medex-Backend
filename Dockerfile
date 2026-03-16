FROM python:3.10-alpine

WORKDIR /app

COPY ./requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .
RUN python3 manage.py makemigrations --noinput && \
    python3 manage.py migrate --noinput

# Dummy Image Assets
RUN for f in product brand category; do mkdir -p media/"${f}"/images/placeholders/; done

RUN unzip -o fixtures/medicinal_asset_pack.zip -d fixtures/ && \
    mv fixtures/brand_images/* media/brand/images/placeholders/ && \
    mv fixtures/category_images/* media/category/images/placeholders/ && \
    mv fixtures/product_images/* media/product/images/placeholders/

# Fixtures to load dummy data
RUN python3 manage.py loaddata fixtures/min_seed.json && \
    python3 manage.py shell < fixtures/seed_medicinal_catalog.py && \
    python3 manage.py shell < fixtures/reassign_catalog_images.py

RUN --mount=type=secret,id=django

EXPOSE 8000
ENTRYPOINT [ "./entrypoint.sh" ]
