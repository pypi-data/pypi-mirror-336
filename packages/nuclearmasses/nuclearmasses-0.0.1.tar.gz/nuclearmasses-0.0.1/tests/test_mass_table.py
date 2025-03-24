from nuclearmasses.mass_table import MassTable


def test_get_nubase_datafile():
    mt = MassTable()

    year = 2003
    assert mt._get_nubase_datafile(year) == mt.data_path / str(year) / "nubtab03.asc"
    year = 2012
    assert mt._get_nubase_datafile(year) == mt.data_path / str(year) / "nubtab12.asc"
    year = 2016
    assert mt._get_nubase_datafile(year) == mt.data_path / str(year) / "nubase2016.txt"
    year = 2020
    assert mt._get_nubase_datafile(year) == mt.data_path / str(year) / "nubase_1.mas20"


def test_get_ame_datafiles():
    mt = MassTable()

    year = 2003
    data_path = mt.data_path / str(year)
    mass, reaction01, reaction02 = mt._get_ame_datafiles(2003)
    assert mass == data_path / "mass.mas03"
    assert reaction01 == data_path / "rct1.mas03"
    assert reaction02 == data_path / "rct2.mas03"

    year = 2012
    data_path = mt.data_path / str(year)
    mass, reaction01, reaction02 = mt._get_ame_datafiles(2012)
    assert mass == data_path / "mass.mas12"
    assert reaction01 == data_path / "rct1.mas12"
    assert reaction02 == data_path / "rct2.mas12"

    year = 2016
    data_path = mt.data_path / str(year)
    mass, reaction01, reaction02 = mt._get_ame_datafiles(2016)
    assert mass == data_path / "mass16.txt"
    assert reaction01 == data_path / "rct1-16.txt"
    assert reaction02 == data_path / "rct2-16.txt"

    year = 2020
    data_path = mt.data_path / str(year)
    mass, reaction01, reaction02 = mt._get_ame_datafiles(2020)
    assert mass == data_path / "mass.mas20"
    assert reaction01 == data_path / "rct1.mas20"
    assert reaction02 == data_path / "rct2.mas20"


def test_validate_year():
    mt = MassTable()

    assert mt._validate_year(2003) == 2003
    assert mt._validate_year(2012) == 2012
    assert mt._validate_year(2016) == 2016
    assert mt._validate_year(2020) == 2020
    assert mt._validate_year(2000) == mt.existing_years[-1]
