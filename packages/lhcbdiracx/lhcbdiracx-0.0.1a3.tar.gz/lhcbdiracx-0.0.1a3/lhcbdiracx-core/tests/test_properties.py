from diracx.core.properties import SecurityProperty


def test_properties():
    """Checks that both gubbins and diracx properties are available"""
    all_properties = SecurityProperty.available_properties()

    assert "BookkeepingPlaceholder" in all_properties
    assert "NormalUser" in all_properties
