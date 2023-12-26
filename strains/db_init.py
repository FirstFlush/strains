from tortoise import Tortoise, run_async

from strains.config import POSTGRES_CONNECTION_STRING
from strains.db_handler import StrainInitHandler
from strains.atomized_sets import *
from strains.models import Flavor, Effect, Ailment, ExistingStrain, Strain

async def main():
    await Tortoise.init(
        db_url=POSTGRES_CONNECTION_STRING,
        modules={'models': ['strains.models']}
    )
    

    # await StrainInitHandler.init_db()
    handler = await StrainInitHandler.initialize()
    await handler.populate_tables()
    strains = await Strain.all()
    print(len(strains))
    # await handler.generate_schemas()
    # for strain in handler.existing_strains:
    #     print(strain.name)
    




run_async(main())
