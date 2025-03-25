import gs_web_server as gs

def main():
    print(gs.login("ke+1@gravitysketch.com", "Password1"))
    print(gs.get_user_profile())
    print(gs.list_docs(""))
    # print(gs.download_doc("4b2d0126-b558-4b7c-8cb7-477d485a744c", "test.png"))
    print(gs.logout())
    print(gs.authentication_status())


if __name__ == "__main__":
    main()
