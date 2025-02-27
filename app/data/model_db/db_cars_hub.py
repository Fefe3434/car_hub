from sqlalchemy import Column, ForeignKey, Integer, String, func, Text, Float, DECIMAL, Boolean, Date, TIMESTAMP, Enum, ForeignKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()
metadata = Base.metadata


# Transmission Enum
class TransmissionEnum(enum.Enum):
    manuelle = 'manuelle'
    automatique = 'automatique'

# Seller Type Enum
class SellerTypeEnum(enum.Enum):
    professionnel = 'professionnel'
    particulier = 'particulier'

# Role Enum
class RoleEnum(enum.Enum):
    acheteur = 'vendeur'
    vendeur = 'acheteur'
    admin = 'admin'

# Model: Brand
class Brand(Base):
    __tablename__ = 'brands'

    brand_id = Column(Integer, primary_key=True, autoincrement=True)
    brand_name = Column(String(255), nullable=False, unique=True)

# Model: FuelType
class FuelType(Base):
    __tablename__ = 'fuel_types'

    fuel_type_id = Column(Integer, primary_key=True, autoincrement=True)
    fuel_type_name = Column(String(255), nullable=False, unique=True)

# Model: EmissionClass
class EmissionClass(Base):
    __tablename__ = 'emission_classes'

    emission_class_id = Column(Integer, primary_key=True, autoincrement=True)
    emission_class_name = Column(String(10), nullable=False, unique=True)

# Model: User
class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    phone_number = Column(String(20))
    role = Column(Enum(RoleEnum), default=RoleEnum.acheteur)
    created_at = Column(TIMESTAMP, server_default=func.now())
    seller_type = Column(Enum(SellerTypeEnum), default=SellerTypeEnum.particulier)
    is_admin = Column(Boolean,  nullable=False,  default=0)
    
class Car(Base):
    __tablename__ = 'cars'

    car_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    brand_id = Column(Integer, ForeignKey('brands.brand_id'), nullable=False)
    model_id = Column(Integer, ForeignKey('models.model_id'), nullable=False)
    engine_type = Column(String(255))
    price = Column(DECIMAL(10, 2), nullable=False)
    mileage = Column(Integer, nullable=False)
    transmission = Column(Enum(TransmissionEnum), nullable=False)
    description = Column(Text)
    location = Column(String(255), nullable=False)
    primary_image_id = Column(Integer, ForeignKey('car_images.image_id'), nullable=True)  # Link to the primary image    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=True)
    power = Column(Integer, nullable=False)
    first_immatriculation = Column(Date, nullable=False)
    fuel_type_id = Column(Integer, ForeignKey('fuel_types.fuel_type_id'), nullable=False)
    latitude = Column(DECIMAL(10, 8))
    longitude = Column(DECIMAL(11, 8))
    emission_class_id = Column(Integer, ForeignKey('emission_classes.emission_class_id'))
    announcement_title = Column(String(255))

    # Relationships
    user = relationship("User")
    brand = relationship("Brand")
    model = relationship("Model")
    fuel_type = relationship("FuelType")
    emission_class = relationship("EmissionClass")
    favorites = relationship("Favorite", back_populates="car")
    images = relationship("CarImage", back_populates="car", cascade="all, delete-orphan")  # Link to all images
    images = relationship(
        "CarImage",
        back_populates="car",
        foreign_keys="[CarImage.car_id]"
    )
    primary_image = relationship(
        "CarImage",
        foreign_keys="[Car.primary_image_id]",
        uselist=False
    )
    
class CarImage(Base):
    __tablename__ = 'car_images'

    image_id = Column(Integer, primary_key=True, autoincrement=True)
    car_id = Column(Integer, ForeignKey('cars.car_id'), nullable=False)
    image_url = Column(String(255), nullable=False)

    # Relationships
    car = relationship(
        "Car",
        back_populates="images",
        foreign_keys=[car_id]
    )



# Model: BrandModelMap (Mapping between brands and models)
class BrandModelMap(Base):
    __tablename__ = 'brand_model_map'

    brand_id = Column(Integer, ForeignKey('brands.brand_id'), primary_key=True)
    model_id = Column(Integer, ForeignKey('models.model_id'), primary_key=True)

# Model: Model
class Model(Base):
    __tablename__ = 'models'

    model_id = Column(Integer, primary_key=True, autoincrement=True)
    model_name = Column(String(255), nullable=False, unique=True)

# Model: FeatureCategory
class FeatureCategory(Base):
    __tablename__ = 'feature_categories'

    category_id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String(255), nullable=False, unique=True)

# Model: Feature
class Feature(Base):
    __tablename__ = 'features'

    feature_id = Column(Integer, primary_key=True, autoincrement=True)
    feature_name = Column(String(255), nullable=False, unique=True)
    category_id = Column(Integer, ForeignKey('feature_categories.category_id'), nullable=False)

    category = relationship("FeatureCategory")

# Model: CarFeatureMap (Mapping between cars and features)
class CarFeatureMap(Base):
    __tablename__ = 'car_features_map'

    car_id = Column(Integer, ForeignKey('cars.car_id'), primary_key=True)
    feature_id = Column(Integer, ForeignKey('features.feature_id'), primary_key=True)

# Model: Favorite (Tracks user favorites)
class Favorite(Base):
    __tablename__ = 'favorites'

    favorite_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    car_id = Column(Integer, ForeignKey('cars.car_id'), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=True)

    car = relationship("Car", back_populates="favorites")

# Model: Message (Messages between users about cars)
class Message(Base):
    __tablename__ = 'messages'

    message_id = Column(Integer, primary_key=True, autoincrement=True)
    sender_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    receiver_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    message_body = Column(Text, nullable=False)
    car_id = Column(Integer, ForeignKey('cars.car_id'))
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=True)

    sender = relationship('User', foreign_keys=[sender_id])
    receiver = relationship('User', foreign_keys=[receiver_id])
    car = relationship('Car', foreign_keys=[car_id])

# Model: Review (User reviews of cars)
class Review(Base):
    __tablename__ = 'reviews'

    review_id = Column(Integer, primary_key=True, autoincrement=True)
    reviewer_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)  
    reviewed_user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)  
    rating = Column(DECIMAL(2, 1), nullable=True)  
    review_text = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=True)

    reviewer = relationship("User", foreign_keys=[reviewer_id]) 
    reviewed_user = relationship("User", foreign_keys=[reviewed_user_id]) 

    __table_args__ = (
        ForeignKeyConstraint(['rating'], ['reviews.rating'], name='reviews_chk_1', use_alter=True),
    )

# Model: Transaction (Tracks sales transactions)
class Transaction(Base):
    __tablename__ = 'transactions'

    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    buyer_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    seller_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    car_id = Column(Integer, ForeignKey('cars.car_id'), nullable=False)
    sale_price = Column(DECIMAL(10, 2), nullable=False)
    transaction_date = Column(TIMESTAMP, server_default=func.now(), nullable=True)
