import pytest


@pytest.mark.parametrize(
    "groupname,gid",
    [
        ("group1", 1234),
        ("group2", 1235),
    ],
)
def test_groups_exist(host, groupname, gid):
    group = host.group(groupname)
    assert group.exists
    assert group.gid == gid


@pytest.mark.parametrize(
    "username,groupname",
    [
        ("user1", "group1"),
        ("user2", "group2"),
        ("user3", "group2"),
    ],
)
def test_users_exist(host, username, groupname):
    user = host.user(username)
    assert user.exists
    assert user.group == groupname


def test_user2_has_uid(host):
    user = host.user("user2")
    assert user.uid == 2000


def test_user2_in_multiple_groups(host):
    user = host.user("user2")
    assert "group1" in user.groups
    assert "group2" in user.groups


def test_user3_is_system_user(host):
    user = host.user("user3")
    assert user.exists
    # System users typically have UID < 1000
    assert user.uid < 1000


@pytest.mark.parametrize(
    "username,home",
    [
        ("user1", "/home/user1"),
        ("user2", "/home/user2"),
    ],
)
def test_user_homes_exist(host, username, home):
    home_dir = host.file(home)
    assert home_dir.exists
    assert home_dir.is_directory
    assert home_dir.user == username


def test_user3_home_does_not_exist(host):
    home_dir = host.file("/home/user3")
    assert not home_dir.exists
