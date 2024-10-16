from app.dao.base import BaseDAO
from app.services.models import Services


class ServicesDAO(BaseDAO):
    model = Services
