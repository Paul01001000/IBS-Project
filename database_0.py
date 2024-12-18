#database_0
import pandas as pd
import os
import json

from typing import List

class Database():
    # File paths
    ROOT: str = "C:/Users/paul8/Documents/Uni/7. Thesis/Project Seminar/IBS-Project/"
    USER_FILE: str = ROOT + "users.csv"
    CLIENT_FILE: str = ROOT + "client_database.csv"
    THERAPISTS_FILE: str = "therapists.csv"
    APPOINTMENTS_FILE: str = ROOT + "appointments.csv"

    USER_HEADERS: List[str] = ["Username", "Password", "Firstname", "Lastname", "Date_of_Birth"]
    CLIENT_HEADERS: List[str] = ["Nachname", "Vorname", "Telefonnummer", "Handynummer", "Adresse",
                    "Arzt", "Pfleger", "Versicherung", "Versicherungsnummer",
                    "Geschlecht", "Rezept Details", "Beschwerde"]
    APPOINTMENTS_HEADERS: List[str] = ["therapist","date","time","client_name","type"]
    
    __user: str = "" #current user
    __client: int = None
    __appointment: int = None
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
    
    @property
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
        df.sort_values("Nachname").to_csv(self.CLIENT_FILE, index=False)
        return True
    
    def create_new_appointment(self,appointment_data: dict) -> bool:
        df = pd.read_csv(self.APPOINTMENTS_FILE)
        df = pd.concat([df, pd.DataFrame([appointment_data])], ignore_index=True)
        df.to_csv(self.APPOINTMENTS_FILE, index=False)
        return True
    
    def delete_client(self) -> bool:
        df = pd.read_csv(self.CLIENT_FILE)
        if self.__client >= df.shape[0]:
            return False
        df.drop(self.__client).to_csv(self.CLIENT_FILE, index=False)
        return True
    
    def delete_appointment(self) -> bool:
        df = pd.read_csv(self.APPOINTMENTS_FILE)
        if self.__appointment >= df.shape[0]:
            return False
        df.drop(self.__appointment).to_csv(self.APPOINTMENTS_FILE, index=False)
        return True
    
    def update_client(self,updated_data: dict) -> bool:
        df = pd.read_csv(self.CLIENT_FILE)
        for col, val in enumerate(updated_data.values()):
            if val:
                df.iloc[self.__client,col] = val
        df.to_csv(self.CLIENT_FILE, index=False)
        return True
    
    def update_appointment(self,updated_data: dict) -> bool:
        df = pd.read_csv(self.APPOINTMENTS_FILE)
        for col, val in enumerate(updated_data.values()):
            if val:
                df.iloc[self.__appointment,col] = val
        df.to_csv(self.APPOINTMENTS_FILE, index=False)
        return True
    
    @property
    def get_clients_json(self) -> str:
        return pd.read_csv(self.CLIENT_FILE).to_json(orient="index")
    
    @property
    def get_client_json(self) -> str:
        df = pd.read_csv(self.CLIENT_FILE)
        return df.iloc[self.__client,:].to_json(orient="index")
    
    @property
    def get_appointments_json(self) -> str:
        return pd.read_csv(self.APPOINTMENTS_FILE).to_json(orient="index")
    
    @property
    def get_appointment_json(self) -> str:
        df = pd.read_csv(self.APPOINTMENTS_FILE)
        return df.iloc[self.__appointment,:].to_json(orient="index")

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
    
    def set_client(self,id: int) -> None:
        self.__client = id
    
    @property
    def get_client(self) -> int:
        return self.__client
    
    def set_appointment(self,id: int) -> None:
        self.__appointment = id

    @property
    def get_appointment(self) -> int:
        return self.__appointment

if "__main__" == __name__:
    db = Database()
    #Unit Test