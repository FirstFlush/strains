from datetime import date
from tortoise import Tortoise
from tortoise.transactions import in_transaction

from strains.config import POSTGRES_CONNECTION_STRING
from strains.models import (
    ExistingStrain,
    Breeder,
    Strain,
    Ailment,
    Effect,
    Flavor
)


class DBHandler:

    @staticmethod
    async def init_db():
        await Tortoise.init(
            db_url=POSTGRES_CONNECTION_STRING,
            modules={'models': ['strains.models']}
        )



class StrainInitHandler(DBHandler):

    def __init__(self, existing_strains:list[ExistingStrain]):
        self.existing_strains =existing_strains


    async def generate_schemas(self):
        """Only run this once when you are ready to build the tables"""
        await Tortoise.generate_schemas()


    @classmethod
    async def initialize(cls) -> "StrainInitHandler":
        """Factory method to instantiate self"""
        return cls(await StrainInitHandler.get_existing_strains())


    @staticmethod
    async def get_existing_strains() -> list[ExistingStrain]:
        return await ExistingStrain.all()


    async def _create_strain(self, existing_strain:ExistingStrain, breeder:Breeder=None) -> Strain|None:
        """Create a Strain DB object"""
        if not await Strain.exists(name=existing_strain.name):
            return await Strain.create(
                name = existing_strain.name,
                breeder = breeder,
                type = existing_strain.type,
                # crosses = existing_strain.crosses
            )



    async def _create_or_get_breeder(self, breeder: str|None) -> Breeder:
        if breeder and breeder.lower().strip() != "unknown breeder":
            breeder_tuple = await Breeder.get_or_create(breeder=breeder)
            return breeder_tuple[0]


    async def _create_or_get_ailments(self, ailments:list) -> list[Ailment]:
        ailment_objects = []
        for ailment in ailments:
            ailment_tuple = await Ailment.get_or_create(ailment=ailment)
            ailment_object = ailment_tuple[0]
            ailment_objects.append(ailment_object)
        return ailment_objects


    async def _create_or_get_effects(self, effects:list) -> list[Effect]:
        effect_objects = []
        for effect in effects:
            effect_tuple = await Effect.get_or_create(effect=effect)
            effect_object = effect_tuple[0]
            effect_objects.append(effect_object)
        return effect_objects


    async def _create_or_get_flavors(self, flavors:list) -> list[Flavor]:
        flavor_objects = []
        for flavor in flavors:
            flavor_tuple = await Flavor.get_or_create(flavor=flavor)
            flavor_object = flavor_tuple[0]
            flavor_objects.append(flavor_object)
        return flavor_objects


    async def populate_tables(self):
        """Iterate throug self.existing_strains and perform the following:
            -create Strain object
            -atomize the data in the ailment, effects, and flavor columns, then create individual
            objects in the Ailment, Effect, and Flavor tables.
            -Add those objects to Strain's MTM relationships.
        """
        async with in_transaction(): #as connection:
            for existing_strain in self.existing_strains:
                breeder = await self._create_or_get_breeder(existing_strain.breeder)
                
                strain = await self._create_strain(existing_strain, breeder)
                if not strain:
                    continue
                ailments = await self._create_or_get_ailments(self.atomize_field(existing_strain.ailment))
                print(existing_strain.id, " : ", existing_strain.name)
                effects = await self._create_or_get_effects(self.atomize_field(existing_strain.effects))
                flavors = await self._create_or_get_flavors(self.atomize_field(existing_strain.flavor))
                await strain.ailments.add(*ailments)
                await strain.effects.add(*effects)
                await strain.flavors.add(*flavors)
                await strain.save()




    def atomize_field(self, field_data:str) -> list[str]:
        """Converts 'sweet, lavender, skunk' into ['sweet', 'lavender', 'skunk']"""
        if field_data:
            return field_data.split(', ')
        return []
