import time
from locust import HttpUser, task, between

get_slot = '{"jsonrpc":"2.0","id":1, "method":"getSlot"}'
get_slot_leader = '{"jsonrpc":"2.0","id":1, "method":"getSlotLeader"}'

class SolanaUser(HttpUser):
  wait_time = between(0.1,1)

  @task 
  def get_slot(self):
    self.client.post('/', data=get_slot,  headers={'content-type': 'application/json'})

  @task
  def get_slot_leader(self):
    self.client.post('/', data=get_slot_leader,  headers={'content-type': 'application/json'})
