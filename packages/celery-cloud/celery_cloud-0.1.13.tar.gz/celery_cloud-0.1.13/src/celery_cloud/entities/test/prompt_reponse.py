from pydantic import BaseModel, Field


class PromptResponse(BaseModel):
    """Representation of a prompt response (for testing purposes)

    Args:
        BaseModel (_type_): _description_
    """

    id: str = Field(
        ...,
        max_length=150,
        json_schema_extra={
            "description": "Unique task id",
            "example": "4b8f27d1-cd8b-4b79-a1d5-937c5d3579d7",
        },
    )

    prompt: str = Field(
        default=None,
        json_schema_extra={
            "description": "Prompt",
            "example": "Gimme some answers",
        },
    )

    response: str = Field(
        default=None,
        json_schema_extra={
            "description": "Response",
            "example": "Here you have some answers",
        },
    )
