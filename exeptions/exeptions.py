from fastapi import HTTPException, status


ChooseAnotherTimeOrSpecilist = HTTPException(
    status_code=status.HTTP_406_NOT_ACCEPTABLE,
    detail="Выберите другое время либо другого специалиста"
)

SpecilistNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Специалист не найден"
)

SpecilistOrServiceNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Специалист или сервис не найден"
)




