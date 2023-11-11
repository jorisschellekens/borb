import keyring


def populate_keyring() -> None:
    """
    This method populates the keyring with the credentials for unsplash
    :return:    None
    """
    keyring.set_password(
        "unsplash", "access_key", "FgpGELvBVuBuz3caU8wLz-_gkKa08hwDMb9QGR5AiMg"
    )
