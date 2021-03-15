import time
import json
from locust import HttpUser, task, between

get_slot = {"jsonrpc":"2.0","id":1, "method":"getSlot"}
get_slot_leader = {"jsonrpc":"2.0","id":1, "method":"getSlotLeader"}
get_balance = {"jsonrpc":"2.0", "id":1, "method":"getBalance", "params":[]}
get_leader_schedule = {"jsonrpc":"2.0","id":1, "method":"getLeaderSchedule"}
get_vote_accounts = {"jsonrpc":"2.0","id":1, "method":"getVoteAccounts"}
get_stake_activation = {"jsonrpc":"2.0","id":1, "method":"getStakeActivation", "params": []}
get_cluster_nodes = {"jsonrpc":"2.0", "id":1, "method":"getClusterNodes"}

# A user of wallets
class WalletUser(HttpUser):
  weight = 10 # wallet user 10x
  wait_time = between(0.1,1)

  @task(10)
  def get_balance(self):
    req = get_balance
    req["params"] = [self.pubkey]
    self.client.post('/', data=json.dumps(req),  headers={'content-type': 'application/json'}, name='getBalance')

  def on_start(self):
    # @TODO randomise the wallet pubkey
    self.pubkey = "83astBRguLMdt2h5U1Tpdq5tjFoJ6noeGwaY3mDLVcri"
    self.stake_account = "CYRJWqiSjLitBAcRxPvWpgX3s5TvmN2SuRY3eEYypFvT"

# A validator
class ValidatorUser(HttpUser):
  weight = 3
  wait_time = between(0.1,1)

  @task(10) #this is a really common task so give it higher weight
  def get_slot(self):
    req = get_slot
    self.client.post('/', data=json.dumps(req),  headers={'content-type': 'application/json'}, name='getSlot')

  @task
  def get_balance(self):
    req = get_balance
    req["params"] = [self.pubkey]
    self.client.post('/', data=json.dumps(req),  headers={'content-type': 'application/json'}, name='getBalance')

  @task
  def get_vote_accounts(self):
    req = get_vote_accounts
    self.client.post('/', data=json.dumps(req),  headers={'content-type': 'application/json'}, name='getVoteAccounts')

  @task
  def get_stake_activation(self):
    req = get_stake_activation
    req["params"] = self.stake_account
    self.client.post('/', data=json.dumps(req),  headers={'content-type': 'application/json'}, name='getStakeActivation')

  def on_start(self):
    # @TODO we should randomise these from a list of options
    self.pubkey = "7cVfgArCheMR6Cs4t6vz5rfnqd56vZq4ndaBrY5xkxXy"
    self.vote_account = "7cVfgArCheMR6Cs4t6vz5rfnqd56vZq4ndaBrY5xkxXy"
    self.stake_account = "CYRJWqiSjLitBAcRxPvWpgX3s5TvmN2SuRY3eEYypFvT"

# An explorer a la solanabeach.io
class ExplorerUser(HttpUser):
  weight = 1
  wait_time = between(0.1,1)

  @task 
  def get_slot(self):
    req = get_slot
    self.client.post('/', data=json.dumps(req),  headers={'content-type': 'application/json'}, name='getSlot')

  @task
  def get_slot_leader(self):
    req = get_slot_leader
    self.client.post('/', data=json.dumps(req),  headers={'content-type': 'application/json'}, name='getSlotLeader')

  @task
  def get_leader_schedule(self):
    req = get_leader_schedule
    self.client.post('/', data=json.dumps(req),  headers={'content-type': 'application/json'}, name='getLeaderSchedule')

  @task
  def get_cluster_nodes(self):
    req = get_cluster_nodes
    self.client.post('/', data=json.dumps(req),  headers={'content-type': 'application/json'}, name='getLeaderSchedule')
