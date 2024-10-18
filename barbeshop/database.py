from barbeshop.schemas.experts import Expert
from barbeshop.schemas.orders import Order
from barbeshop.schemas.services import Service
from typing import Dict

list_experts: Dict[int, Expert] = {}
dict_experts = {"Experts": list_experts}

list_services: Dict[int,Service] = {}
dict_services = {"Services": list_services}

list_orders: Dict[int, Order] = {}
dict_orders = {"Orders": list_orders}

fake_db = [dict_experts, dict_services, dict_orders]