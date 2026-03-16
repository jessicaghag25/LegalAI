from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "CTax AI"
    database_url: str = "postgresql://ctax:ctax@localhost:5432/ctax"
    disclaimer: str = (
        "CTax is a preparation and diagnostic assistant and not a substitute for "
        "professional tax or legal advice."
    )


settings = Settings()
