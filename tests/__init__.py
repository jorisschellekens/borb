try:
    from tests.populate_keyring import populate_keyring

    populate_keyring()
except ImportError:
    pass
