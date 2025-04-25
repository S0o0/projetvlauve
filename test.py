def main():


    from DAO.DAOSession import DAOSession

    # Ouvrir la session DAO
    DAOSession.open()

    DAOSession.close()
if __name__ == "__main__":
    main()
