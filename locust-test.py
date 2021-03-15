import time
from locust import HttpUser, task, between

get_slot = '{"jsonrpc":"2.0","id":1, "method":"getSlot"}'
get_slot_leader = '{"jsonrpc":"2.0","id":1, "method":"getSlotLeader"}'
get_balance = '{"jsonrpc":"2.0", "id":1, "method":"getBalance", "params":["83astBRguLMdt2h5U1Tpdq5tjFoJ6noeGwaY3mDLVcri"]}'
get_leader_schedule = '{"jsonrpc":"2.0","id":1, "method":"getLeaderSchedule"}'
get_vote_accounts = '{"jsonrpc":"2.0","id":1, "method":"getVoteAccounts"}'
get_stake_activation = '{"jsonrpc":"2.0","id":1, "method":"getStakeActivation", "params": ["CYRJWqiSjLitBAcRxPvWpgX3s5TvmN2SuRY3eEYypFvT"]}'

# A user of wallets
class WalletUser(HttpUser):
  weight = 10 # wallet user 10x
  wait_time = between(0.1,1)

  @task
  def get_balance(self):
    self.client.post('/', data=get_balance,  headers={'content-type': 'application/json'}, name='getBalance')

# A validator
class ValidatorUser(HttpUser):
  weight = 3
  wait_time = between(0.1,1)

  @task(10) #this is a really common task so give it higher weight
  def get_slot(self):
    self.client.post('/', data=get_slot,  headers={'content-type': 'application/json'}, name='getSlot')

  @task
  def get_vote_accounts(self):
    self.client.post('/', data=get_vote_accounts,  headers={'content-type': 'application/json'}, name='getVoteAccounts')

  @task
  def get_stake_activation(self):
    self.client.post('/', data=get_stake_activation,  headers={'content-type': 'application/json'}, name='getStakeActivation')


# An explorer a la solanabeach.io
class ExplorerUser(HttpUser):
  weight = 1
  wait_time = between(0.1,1)

  @task 
  def get_slot(self):
    self.client.post('/', data=get_slot,  headers={'content-type': 'application/json'}, name='getSlot')

  @task
  def get_slot_leader(self):
    self.client.post('/', data=get_slot_leader,  headers={'content-type': 'application/json'}, name='getSlotLeader')

  @task
  def get_leader_schedule(self):
    self.client.post('/', data=get_leader_schedule,  headers={'content-type': 'application/json'}, name='getLeaderSchedule')

