#database_0
import pandas as pd
import cryptpandas as crp
import os

from typing import List
from datetime import datetime

class Database():
    
    USER_HEADERS: List[str] = ["Username", "Password", "Firstname", "Lastname", "Date_of_Birth"]
    CLIENT_HEADERS: List[str] = ["Nachname", "Vorname", "Geburtstag", "Telefonnummer", "Handynummer", "Adresse",
                    "Arzt", "Pfleger", "Versicherung", "Versicherungsnummer",
                    "Geschlecht", "Rezept Details", "Beschwerde"]
    APPOINTMENTS_HEADERS: List[str] = ["Therapeut","Datum","Uhrzeit","Patient","Ort"]
    
    __user: str = "" #current user
    __client: int = None
    __appointment: int = None
    __date: str = str(datetime.now()).split(' ')[0]
    __therapist: str = ""
    __key: str = ""  #to be replaced with secure key
    #__salt: bytes = crp.make_salt()
    __salt: bytes = b'm\xde\x84\xb2\x17\xa7\xeb\x16\xd4\x8a\x15\xad*\xb1Pt' #needed for cryptpandas
    
    def __init__(self,root_path: str):

        # File paths
        self.ROOT: str = root_path
        self.USER_FILE: str = self.ROOT + "users.crypt"
        self.CLIENT_FILE: str = self.ROOT + "client_database.crypt"
        self.APPOINTMENTS_FILE: str = self.ROOT + "appointments.crypt"

        # Initialize user and client and appointments database files if they don't exist
        if not os.path.exists(self.USER_FILE):
            crp.to_encrypted(pd.DataFrame(columns=self.USER_HEADERS),self.USER_FILE,self.__key,self.__salt)

        if not os.path.exists(self.CLIENT_FILE):
            crp.to_encrypted(pd.DataFrame(columns=self.CLIENT_HEADERS),self.CLIENT_FILE,self.__key,self.__salt)

        if not os.path.exists(self.APPOINTMENTS_FILE):
            crp.to_encrypted(pd.DataFrame(columns=self.APPOINTMENTS_HEADERS),self.APPOINTMENTS_FILE,self.__key,self.__salt)

        try:
            self.__therapist = crp.read_encrypted(self.APPOINTMENTS_FILE,self.__key,self.__salt)["Therapeut"].iloc[0]
        except IndexError:
            pass

    def verify_user(self,username: str, password: str) -> bool:
        users = crp.read_encrypted(self.USER_FILE,self.__key,self.__salt)
        if ((users['Username'] == username) & (users['Password'].map(str) == password)).any():
            self.__set_user(username)
            return True
        else: 
            return False
    
    @property
    def log_out(self) -> None:
        self.__set_user("")
    
    def create_new_user(self,user_data: dict) -> bool:
        users = crp.read_encrypted(self.USER_FILE,self.__key,self.__salt)
        if user_data["Username"] in users['Username'].values:
            return False
        else:
            users = pd.concat([users, pd.DataFrame([user_data])], ignore_index=True)
            crp.to_encrypted(users,self.USER_FILE,self.__key,self.__salt)
            return True
    
    def create_new_client(self,client_data: dict) -> bool:
        df = crp.read_encrypted(self.CLIENT_FILE,self.__key,self.__salt)
        df = pd.concat([df, pd.DataFrame([client_data])], ignore_index=True)
        crp.to_encrypted(df.sort_values("Nachname"),self.CLIENT_FILE,self.__key,self.__salt)
        return True
    
    def create_new_appointment(self,appointment_data: dict) -> bool:
        df = crp.read_encrypted(self.APPOINTMENTS_FILE,self.__key,self.__salt)
        df = pd.concat([df, pd.DataFrame([appointment_data])], ignore_index=True)
        crp.to_encrypted(df,self.APPOINTMENTS_FILE,self.__key,self.__salt)
        return True
    
    def delete_client(self) -> bool:
        df = crp.read_encrypted(self.CLIENT_FILE,self.__key,self.__salt)
        if self.__client >= df.shape[0]:
            return False
        crp.to_encrypted(df.drop(self.__client),self.CLIENT_FILE,self.__key,self.__salt)
        return True
    
    def delete_appointment(self) -> bool:
        df = crp.read_encrypted(self.APPOINTMENTS_FILE,self.__key,self.__salt)
        if self.__appointment >= df.shape[0]:
            return False
        crp.to_encrypted(df.drop(self.__appointment),self.APPOINTMENTS_FILE,self.__key,self.__salt)
        return True
    
    def update_client(self,updated_data: dict) -> bool:
        df = crp.read_encrypted(self.CLIENT_FILE,self.__key,self.__salt)
        for col, val in enumerate(updated_data.values()):
            if val:
                df.iloc[self.__client,col] = val
        crp.to_encrypted(df,self.CLIENT_FILE,self.__key,self.__salt)
        return True
    
    def update_appointment(self,updated_data: dict) -> bool:
        df = crp.read_encrypted(self.APPOINTMENTS_FILE,self.__key,self.__salt)
        for col, val in enumerate(updated_data.values()):
            if val:
                df.iloc[self.__appointment,col] = val
        crp.to_encrypted(df,self.APPOINTMENTS_FILE,self.__key,self.__salt)
        return True
    
    @property
    def get_clients_json(self) -> str:
        return crp.read_encrypted(self.CLIENT_FILE,self.__key,self.__salt).to_json(orient="index")
    
    @property
    def get_client_json(self) -> str:
        df = crp.read_encrypted(self.CLIENT_FILE,self.__key,self.__salt)
        return df.iloc[self.__client,:].to_json(orient="index")
    
    @property
    def get_all_appointments_json(self) -> str:
        return crp.read_encrypted(self.APPOINTMENTS_FILE,self.__key,self.__salt).to_json(orient="index")
    
    @property
    def get_appointments_json(self) -> str:
        df = crp.read_encrypted(self.APPOINTMENTS_FILE,self.__key,self.__salt)
        return df.loc[(df["Therapeut"] == self.__therapist) & (df["Datum"] == self.__date)].to_json(orient="index")
    
    @property
    def get_appointment_json(self) -> str:
        df = crp.read_encrypted(self.APPOINTMENTS_FILE,self.__key,self.__salt)
        return df.iloc[self.__appointment,:].to_json(orient="index")

    @property
    def get_all_clients(self) -> pd.DataFrame:
        return crp.read_encrypted(self.CLIENT_FILE,self.__key,self.__salt)
    
    @property
    def get_all_therapists(self) -> list:
        df = crp.read_encrypted(self.APPOINTMENTS_FILE,self.__key,self.__salt)
        return list(df["Therapeut"].unique())
    
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
    
    def set_date(self, date: str) -> None:
        self.__date = date

    @property
    def get_date(self) -> str:
        return self.__date
    
    def set_therapist(self,therapist: str) -> None:
        self.__therapist = therapist

    @property
    def get_therapist(self) -> str:
        return self.__therapist
    


if "__main__" == __name__:
    db = Database()
    #Unit Test