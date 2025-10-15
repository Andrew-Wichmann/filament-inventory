import pydantic


class Filament(pydantic.BaseModel):
    id: int = pydantic.Field(gt=0)
    color: str
    weight: int = pydantic.Field(ge=0)


class AddFilamentRequest(pydantic.BaseModel):
    color: str
    weight: int = pydantic.Field(ge=0)

    model_config = pydantic.ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "color": "red",
                    "weight": 1000,
                }
            ]
        }
    )


class ConsumeRequest(pydantic.BaseModel):
    filament_id: int
    grams: int = pydantic.Field(gt=0)

    model_config = pydantic.ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "filament_id": 1,
                    "grams": 100,
                }
            ]
        }
    )
