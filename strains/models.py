
from tortoise.models import Model
from tortoise import fields


class ExistingStrain(Model):
    name = fields.CharField(max_length=255)
    type = fields.CharField(max_length=255, default="hybrid")  # Indica, Sativa, Hybrid
    crosses = fields.IntField()
    breeder = fields.CharField(max_length=255, null=True)
    effects = fields.CharField(max_length=512, null=True)
    ailment = fields.CharField(max_length=512, null=True)
    flavor = fields.CharField(max_length=512, null=True)

    class Meta:
        table = 'strains'      


class Breeder(Model):
    breeder = fields.CharField(max_length=255, unique=True)


class Ailment(Model):
    ailment = fields.CharField(max_length=255, unique=True)


class Flavor(Model):
    flavor = fields.CharField(max_length=255, unique=True)


class Effect(Model):
    effect = fields.CharField(max_length=255, unique=True)

# class StrainEffect(Model):
#     strain = fields.ForeignKeyField('models.Strain', related_name='effects')
#     effect = fields.ForeignKeyField('models.Effect', related_name='strains')


class Strain(Model):
    name = fields.CharField(max_length=255, unique=True)
    type = fields.CharField(max_length=50)  # Indica, Sativa, Hybrid
    # crosses = fields.IntField()
    breeder = fields.ForeignKeyField('models.Breeder', related_name='strains', on_delete=fields.SET_NULL, null=True)
    ailments = fields.ManyToManyField('models.Ailment', related_name='strains')
    effects = fields.ManyToManyField('models.Effect', related_name='strains')
    flavors = fields.ManyToManyField('models.Flavor', related_name='strains')
    date_added = fields.DatetimeField(auto_now_add=True)

