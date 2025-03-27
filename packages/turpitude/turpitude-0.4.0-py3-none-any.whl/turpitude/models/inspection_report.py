from datetime import date
from decimal import Decimal
from enum import Enum
from typing import Annotated, List

from pydantic import BaseModel, ConfigDict, Field


# Keys
class InspectionReportKeyType(str, Enum):
    PRINCIPAL = "principal"
    PASS = "pass"
    CELLAR = "cellar"
    COMMON = "common"
    MAILBOX = "mailbox"
    GARAGE = "garage"
    PORTAL = "portal"
    BIKE_SHED = "bike_shed"
    BIN_STORAGE_AREA = "bin_storage_area"
    OTHER = "other"


class InspectionReportKeyModel(BaseModel):
    comment: Annotated[
        str | None,
        Field(default=None, examples=["Clé sécurisée"]),
    ]
    count: Annotated[
        int | None,
        Field(default=None, ge=0, examples=[2]),
    ]
    delivery_date: Annotated[
        date | None,
        Field(default=None, examples=["2025-12-23"]),
    ]
    pictures: Annotated[
        List[str],
        Field(default_factory=list),
    ]
    type: Annotated[
        InspectionReportKeyType,
        Field(examples=[InspectionReportKeyType.PRINCIPAL]),
    ]


# Meters
class InspectionReportMeterType(str, Enum):
    WATER = "water"
    ELECTRICITY = "electricity"
    GAS = "gas"
    THERMAL_ENERGY = "thermal_energy"


class InspectionReportMeterModel(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)

    comment: Annotated[
        str | None,
        Field(default=None, examples=["Dans le placard du couloir"]),
    ]
    number: Annotated[
        str | None,
        Field(default=None, examples=["16123511191798"]),
    ]
    index_1: Annotated[
        Decimal | None,
        Field(default=None, ge=0, max_digits=100, decimal_places=10, examples=[7734]),
    ]
    index_2: Annotated[
        Decimal | None,
        Field(default=None, ge=0, max_digits=100, decimal_places=10),
    ]
    type: Annotated[
        InspectionReportMeterType,
        Field(examples=[InspectionReportMeterType.ELECTRICITY]),
    ]


# Elements
class InspectionReportElementCondition(str, Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    USED = "used"
    POOR = "poor"
    MISSING = "missing"


class InspectionReportElementOperatingState(str, Enum):
    WORKING = "working"
    NOT_WORKING = "not_working"
    NOT_TESTED = "not_tested"
    UNABLE_TO_TEST = "unable_to_test"


class InspectionReportElementCleanlinessState(str, Enum):
    CLEAN = "clean"
    TO_CLEAN = "to_clean"


class InspectionReportElementModel(BaseModel):
    name: Annotated[
        str,
        Field(examples=["Réfrigérateur"]),
    ]
    characteristics: Annotated[
        List[str],
        Field(
            default_factory=list,
            examples=[["Compartiment congélation", "3 étages", "Marque Smeg"]],
        ),
    ]
    cleanliness_state: Annotated[
        InspectionReportElementCleanlinessState | None,
        Field(
            default=None, examples=[InspectionReportElementCleanlinessState.TO_CLEAN]
        ),
    ]
    colors: Annotated[
        List[str],
        Field(default_factory=list, examples=[["Blanc", "Beige"]]),
    ]
    comment: Annotated[
        str | None,
        Field(default=None),
    ]
    condition: Annotated[
        InspectionReportElementCondition | None,
        Field(default=None),
    ]
    count: Annotated[
        int | None,
        Field(default=None, examples=[1]),
    ]
    defects: Annotated[
        List[str],
        Field(default_factory=list, examples=[["Moisissures"]]),
    ]
    operating_state: Annotated[
        InspectionReportElementOperatingState | None,
        Field(default=None, examples=[InspectionReportElementOperatingState.WORKING]),
    ]
    photo_ids: Annotated[
        List[int],
        Field(default_factory=list),
    ]


# Rooms
class InspectionReportRoomType(str, Enum):
    ENTRANCE = "entrance"
    TOILET = "toilet"
    BATHROOM = "bathroom"
    LIVING_ROOM = "living_room"
    KITCHEN = "kitchen"
    BEDROOM = "bedroom"
    BALCONY = "balcony"
    TERRASSE = "terrasse"
    CELLAR = "cellar"
    CARPARK = "carpark"
    BOX = "box"
    GARAGE = "garage"
    GARDEN = "garden"
    LAUNDRY_ROOM = "laundry_room"
    PRIVATE_OFFICE = "private_office"
    OPEN_SPACE = "open_space"
    MEETING_ROOM = "meeting_room"
    PHONE_BOOTH = "phone_booth"
    HALL = "hall"
    SHARED_AREAS = "shared_areas"
    OTHER = "other"


class InspectionReportRoomModel(BaseModel):
    elements: List[InspectionReportElementModel]
    name: Annotated[
        str | None,
        Field(default=None, examples=["Salle de bain"]),
    ]
    type: InspectionReportRoomType


# Signatories
class InspectionReportSignatoryType(str, Enum):
    OWNER = "owner"
    REPRESENTATIVE = "representative"
    TENANT = "tenant"


class InspectionReportSignatoryPersonType(str, Enum):
    NATURAL_PERSON = "natural_person"
    LEGAL_PERSON = "legal_person"


class InspectionReportSignatoryAddressModel(BaseModel):
    city: Annotated[
        str | None,
        Field(default=None),
    ]
    line_1: Annotated[
        str | None,
        Field(default=None),
    ]
    line_2: Annotated[
        str | None,
        Field(default=None),
    ]
    postal_code: Annotated[
        str | None,
        Field(default=None),
    ]


class InspectionReportSignatoryModel(BaseModel):
    address: InspectionReportSignatoryAddressModel
    email: Annotated[
        str | None,
        Field(default=None, json_schema_extra={"format": "email"}),
    ]
    first_name: Annotated[
        str | None,
        Field(default=None),
    ]
    last_name: Annotated[
        str | None,
        Field(default=None),
    ]
    legal_name: Annotated[
        str | None,
        Field(default=None),
    ]
    person_type: InspectionReportSignatoryPersonType
    type: InspectionReportSignatoryType


# Inspection report
class InspectionReportType(str, Enum):
    RESIDENTIAL_LEASE_CHECK_IN = "residential_lease_check_in"
    RESIDENTIAL_LEASE_CHECK_OUT = "residential_lease_check_out"
    RESIDENTIAL_LEASE_TEMPLATE = "residential_lease_template"


class InspectionReportPropertyType(str, Enum):
    FLAT = "flat"
    HOUSE = "house"
    BOX = "box"
    PARKING = "parking"
    BUSINESS_PREMISE = "business_premise"
    OFFICE = "office"
    OTHER = "other"


class InspectionReportPropertyAddressModel(BaseModel):
    city: Annotated[str | None, Field(default=None, examples=["Paris"])]
    door: Annotated[str | None, Field(default=None, examples=["A3"])]
    floor_number: Annotated[int | None, Field(default=None, examples=[2])]
    line_1: Annotated[str | None, Field(default=None, examples=["16 rue de la Banque"])]
    line_2: Annotated[str | None, Field(default=None)]
    postal_code: Annotated[str | None, Field(default=None, examples=["75002"])]


class InspectionReportHeatingEnergyModel(BaseModel):
    is_air_conditioning: Annotated[bool | None, Field(default=None)]
    is_district_heating: Annotated[bool | None, Field(default=None)]
    is_electric: Annotated[bool | None, Field(default=None)]
    is_gas: Annotated[bool | None, Field(default=None)]
    is_oil: Annotated[bool | None, Field(default=None)]
    is_other: Annotated[bool | None, Field(default=None)]


class InspectionReportHotWaterEnergyModel(BaseModel):
    is_district_hot_water: Annotated[bool | None, Field(default=None)]
    is_electric: Annotated[bool | None, Field(default=None)]
    is_gas: Annotated[bool | None, Field(default=None)]
    is_oil: Annotated[bool | None, Field(default=None)]
    is_other: Annotated[bool | None, Field(default=None)]


class InspectionReportPropertyEnergyModel(BaseModel):
    heating_source: InspectionReportHeatingEnergyModel
    hot_water_source: InspectionReportHotWaterEnergyModel


class InspectionReportPropertyModel(BaseModel):
    address: InspectionReportPropertyAddressModel
    energy: InspectionReportPropertyEnergyModel
    furnished: Annotated[bool | None, Field(default=None)]
    rooms_count: Annotated[int | None, Field(default=None, ge=0, examples=[3])]
    surface_area: Annotated[
        Decimal | None,
        Field(default=None, ge=0, max_digits=10, decimal_places=2, examples=[42.5]),
    ]
    type: Annotated[
        InspectionReportPropertyType | None,
        Field(default=None, examples=[InspectionReportPropertyType.FLAT]),
    ]


class InspectionReportModel(BaseModel):
    date: Annotated[date, Field(examples=["2025-12-23"])]
    keys: List[InspectionReportKeyModel]
    meters: List[InspectionReportMeterModel]
    property: InspectionReportPropertyModel
    rooms: List[InspectionReportRoomModel]
    signatories: List[InspectionReportSignatoryModel]
    type: InspectionReportType
