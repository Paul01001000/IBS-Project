#database_0
import pandas as pd
import os

from typing import List

class Database():
    # File paths
    ROOT: str = "C:/Users/paul8/Documents/Uni/7. Thesis/Project Seminar/IBS-Project/"
    USER_FILE: str = ROOT + "users.csv"
    CLIENT_FILE: str = ROOT + "client_database.csv"
    THERAPISTS_FILE: str = "therapists.csv"
    APPOINTMENTS_FILE: str = ROOT + "appointments.csv"

    USER_HEADERS: List[str] = ["Username", "Password", "Firstname", "Lastname", "Date_of_Birth"]
    CLIENT_HEADERS: List[str] = ["Patienten ID", "Vor & Nachname", "Telefonnummer", "Handynummer", "Adresse",
                    "Arzt", "Pfleger", "Versicherung", "Versicherungsnummer",
                    "Geschlecht", "Rezept Details", "Beschwerde"]
    APPOINTMENTS_HEADERS: List[str] = ["therapist","date","time","client_name","type"]
    
    __user: str = "" #current user
    __key: str = "SecureKey" 
    __salt: bytes = b'm\xde\x84\xb2\x17\xa7\xeb\x16\xd4\x8a\x15\xad*\xb1Pt' #needed later for cryptpandas

    
    def __init__(self):
        # Initialize user and client and appointments database files if they don't exist
        if not os.path.exists(self.USER_FILE):
            pd.DataFrame(columns=self.USER_HEADERS).to_csv(self.USER_FILE, index=False)

        if not os.path.exists(self.CLIENT_FILE):
            pd.DataFrame(columns=self.CLIENT_HEADERS).to_csv(self.CLIENT_FILE, index=False)
        
        if not os.path.exists(self.THERAPISTS_FILE):
            pd.Series().to_csv(self.THERAPISTS_FILE,index=False)

        if not os.path.exists(self.APPOINTMENTS_FILE):
            pd.DataFrame(columns=self.APPOINTMENTS_HEADERS).to_csv(self.APPOINTMENTS_FILE, index=False)


    def verify_user(self,username: str, password: str) -> bool:
        users = pd.read_csv(self.USER_FILE)
        if ((users['Username'] == username) & (users['Password'] == password)).any():
            self.__set_user(username)
            return True
        else: 
            return False
    
    def log_out(self) -> None:
        self.__set_user("")
    
    def create_new_user(self,user_data: dict) -> bool:
        users = pd.read_csv(self.USER_FILE)
        if user_data["Username"] in users['Username'].values:
            return False
        else:
            users = pd.concat([users, pd.DataFrame([user_data])], ignore_index=True)
            users.to_csv(self.USER_FILE, index=False)
            return True
    
    def create_new_client(self,client_data: dict) -> bool:
        df = pd.read_csv(self.CLIENT_FILE)
        df = pd.concat([df, pd.DataFrame([client_data])], ignore_index=True)
        df.to_csv(self.CLIENT_FILE, index=False)
        return True
    
    def delete_client(self,client_name: str) -> bool:
        df = pd.read_csv(self.CLIENT_FILE)
        if client_name not in df["Vor & Nachname"].values:
            return False
        df[df["Vor & Nachname"] != client_name].to_csv(self.CLIENT_FILE, index=False)
        return True
    
    def update_client(self,client_name: str ,updated_data: dict) -> bool:
        df = pd.read_csv(self.CLIENT_FILE)
        if all(updated_data.values()):
            # Update the specific client's data in the DataFrame
            df.loc[df["Vor & Nachname"] == client_name, :].update(updated_data.values())
            df.to_csv(self.CLIENT_FILE, index=False)
            return True
        else:
            return False
    @property
    def get_all_clients(self) -> pd.DataFrame:
        return pd.read_csv(self.CLIENT_FILE)
    
    @property
    def get_all_therapists(self) -> pd.Series:
        return pd.read_csv(self.THERAPISTS_FILE)
    
    def save_therapists(self,therapists: List[str]) -> bool:
        pd.Series(therapists).to_csv(self.THERAPISTS_FILE,index=False)
        return True
    
    def __set_user(self,username:str) -> None:
        self.__user = username
    
    @property
    def get_user(self) -> str:
        return self.__user

if "__main__" == __name__:
    db = Database()
    #Unit Test