
from sqlalchemy.orm import declarative_base

Base = declarative_base()

from .users import User
from .categories import Category
from .products import Product
from .product_features import ProductFeature
from .catalogs import Catalog
from .category_photo import CategoryPhoto
from .product_video import ProductVideo

