-- DROP TABLE IF EXISTS flavor;
-- DROP TABLE IF EXISTS effect;
-- DROP TABLE IF EXISTS ailment;
-- DROP TABLE IF EXISTS breeder;
-- DROP TABLE IF EXISTS strain;

-- DROP TABLE IF EXISTS strain_ailment;
-- DROP TABLE IF EXISTS strain_breeder;
-- DROP TABLE IF EXISTS strain_effect;
-- DROP TABLE IF EXISTS strain_flavor;



select * from strains where name = '';
select * from strains;

select breeder from strains where breeder is not NULL;

-- DELETE FROM strain WHERE name = '';

-- ALTER TABLE strain DROP COLUMN crosses; 