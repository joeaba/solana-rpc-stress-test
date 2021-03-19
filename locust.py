import time
import json
import random
from locust import HttpUser, task, between

# A user of wallets
class TrafficSimulator(HttpUser):
  wait_time = between(0.1,1)

  def get_req_json(self, method, params=[]):
    req =  {"jsonrpc":"2.0","id":1,"method":method}
    if len(params) > 0:
      req["params"] = params
    return json.dumps(req)

  def rpc(self, method, params=[]):
   self.client.post('/', data=self.get_req_json(method,params),  headers={'content-type': 'application/json'}, name=method)

  @task(42)
  def get_account_info(self):
    self.rpc("getAccountInfo", [self.account_key,{"encoding": "base58"}])

  @task(18)
  def get_token_accounts_by_owner(self):
    self.rpc("getTokenAccountsByOwner", [ self.token_owner, {"mint":self.mint}, {"encoding":"base64"} ])

  @task(10)
  def get_balance(self):
    self.rpc("getBalance", [self.pubkey])

  @task(7)    
  def get_confirmed_block(self):
    self.rpc("getConfirmedBlock", [ self.block, {"encoding":"base64"} ])

  @task(1)
  def get_confirmed_blocks(self):
    self.rpc("getConfirmedBlocks", [self.start_block, self.end_block])

  @task(1)
  def get_epoch_info(self):
    self.rpc("getEpochInfo")

  @task(1)
  def get_minimum_balance_for_rent_exemption(self):
    self.rpc("getMinimumBalanceForRentExemption", [50])
  
  @task(1)
  def get_recent_block_hash(self):
    self.rpc("getRecentBlockhash")

  @task(1)
  def get_confirmed_signatures_for_address2(self):
    self.rpc("getConfirmedSignaturesForAddress2", [self.account_address, 100])

  @task(1)
  def get_slot(self):
    self.rpc("getSlot")

  @task(1)
  def get_program_accounts(self):
    self.rpc("getProgramAccounts", [self.program_key])

  @task(1)
  def get_version(self):
    self.rpc("getVersion")

  @task(1)
  def get_vote_accounts(self):
    self.rpc("getVoteAccounts")

  @task(1)
  def get_confirmed_transaction(self):
    self.rpc("getConfirmedTransaction", [self.transaction_signature, "json"])

  @task(1)
  def get_stake_activation(self):
    self.rpc("getStakeActivation", [self.stake_account])

  @task(1)
  def get_transaction_count(self):
    self.rpc("getTransactionCount")

  @task(1)
  def get_identity(self):
    self.rpc("getIdentity")

  @task(1)
  def get_token_account_balance(self):
    self.rpc("getTokenAccountBalance", [self.token_account])

  @task(1)
  def get_multiple_accounts(self):
    self.rpc("getMultipleAccounts", [ [self.account_key,self.account_key2], {"dataSlice":{"offset":0,"length":0}} ])

  @task(1)
  def get_token_supply(self):
    self.rpc("getTokenSupply", [ self.mint ])

  @task(1)
  def get_block_time(self):
    
    self.rpc("getBlockTime", [ self.block ])

  @task(1)
  def get_cluster_nodes(self):
    self.rpc("getClusterNodes")

  @task(1)
  def get_fees(self):
    self.rpc("getFees")

  def on_start(self):
    # @TODO randomise the wallet pubkey
    self.pubkey = "83astBRguLMdt2h5U1Tpdq5tjFoJ6noeGwaY3mDLVcri"
    self.stake_account = "CYRJWqiSjLitBAcRxPvWpgX3s5TvmN2SuRY3eEYypFvT"
    self.account_key = "vines1vzrYbzLMRdu58ou5XTby4qAqVRLmqo36NKPTg"
    self.account_key2 = "4fYNw3dojWmQ4dXtSGE9epjRGy9pFSx62YypT7avPYvA"
    self.account_address = "6H94zdiaYfRfPfKjYLjyr2VFBg6JHXygy84r3qhc3NsC"
    self.token_owner = "4Qkev8aNZcqFNSRhQzwyLMFSsi94jHqE8WNVTJzTP99F"
    self.token_account = "7fUAJdStEuGbc3sM84cKRL6yYaaSstyLSU4ve5oovLS7"
    self.program_key = "4Nd1mBQtrMJVYVfKf2PJy9NZUZdTAsp7D4xWLs4gDB4T"
    self.transaction_signature = "2nBhEBYYvfaAe16UMNqRHre4YNSskvuYgx3M6E4JP1oDYvZEJHvoPzyUidNgNX5r9sTyN1J9UxtbCXy2rqYcuyuv"
    self.mint = "3wyAj7Rt1TWVPZVteFJPLa26JmLvdb1CAKEFZm3NY75E"
   
    with self.client.post('/', data=self.get_req_json("getEpochInfo"),  headers={'content-type': 'application/json'}, catch_response=True, name="setupBlocks") as response:
      json_data = response.json()
      absolute_slot = json_data["result"]["absoluteSlot"]
      slot_index = json_data["result"]["slotIndex"]
      block_height = json_data["result"]["blockHeight"]
      first_slot_in_epoch = absolute_slot - slot_index + 1

      self.block = block_height-random.randint(1,1000) # get a random block 1 to 1000 blocks back
      self.start_block = random.randint(first_slot_in_epoch, absolute_slot-1)
      self.end_block = random.randint(self.start_block+1, absolute_slot)
      if self.end_block < self.start_block:
        self.start_block = self.end_block-random.randint(0,10)
