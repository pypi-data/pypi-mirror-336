from cqrs.core.src.properties.developer_mode_props import (
    DeveloperModeProps,
)


def test_developer_mode_props():
    # Test initialization
    props = DeveloperModeProps()
    assert props.is_developer_mode() == False
    assert props.get_devid() == None

    # Test setting developer mode
    props.set_developer_mode(True)
    assert props.is_developer_mode() == True

    # Test setting devid
    devid = "12345"
    props.set_devid(devid)
    assert props.get_devid() == devid
