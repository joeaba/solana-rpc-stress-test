import time
import json
import random
from locust import HttpUser, task, between
from locust.exception import StopUser

# used for: getBalance, getAccountInfo, getMultipleAccounts, 
wallets = ["83astBRguLMdt2h5U1Tpdq5tjFoJ6noeGwaY3mDLVcri", "vines1vzrYbzLMRdu58ou5XTby4qAqVRLmqo36NKPTg", "4fYNw3dojWmQ4dXtSGE9epjRGy9pFSx62YypT7avPYvA","6H94zdiaYfRfPfKjYLjyr2VFBg6JHXygy84r3qhc3NsC"]
# addresses that will have signatures getConfirmedSignaturesForAddress2
confirmed_signature_address = ["Vote111111111111111111111111111111111111111"]
# used for getStakeActivation
stake_accounts = ["AjuuY2XHwQoSufRW9ttiGGhnp6R5CxMKmhvEQpTWYjq3", "FTjFea288rGKhe9umFWou5NtcCHS8A3FSgJDGxEWKDhS"]
# used for getProgramAccounts
program_keys = ["Vote111111111111111111111111111111111111111"]
# used for getConfirmedTransaction
transaction_signatures = ["2nBhEBYYvfaAe16UMNqRHre4YNSskvuYgx3M6E4JP1oDYvZEJHvoPzyUidNgNX5r9sTyN1J9UxtbCXy2rqYcuyuv"]
# used for getTokenAccountBalance
token_accounts = ["7zio4a4zAQz5cBS2Ah4WsHVCexQ2bt76ByiEjL3h8m1p","HMWpaDN61sMnDBQSyBPhpRkvM2czox6CVcyt7ggCuciX","DLD2PWQJXWdi44MFCB2urGNVB7PEGWHrFCGTVv1RH8Ea"]
#used for: getTokenSupply
mints = ["4k3Dyjzvzp8eMZWUXbBCjEvwSkkk59S5iCNLY3QrkX6R"] #raydium
# used for: getTokenAccountsByOwner
token_owners = ["122FAHxVFQDQjzgSBSNUmLJXJxG4ooUwLdYvgf3ASs2K"] #token owner of raydium

# Base class for Solana 
class SolanaUser(HttpUser):
  wait_time = between(0.1,1)
  abstract = True

  def get_req_json(self, method, params=[]):
    req =  {"jsonrpc":"2.0","id":1,"method":method}
    if len(params) > 0:
      req["params"] = params
    return json.dumps(req)

  def rpc(self, method, params=[]):
   with self.client.post('/', data=self.get_req_json(method,params),  headers={'content-type': 'application/json'}, name=method, catch_response=True) as response:
      try: 
        json_data = response.json()
        if "error" in json_data:
          response.failure(json_data["error"]["message"])
      except json.decoder.JSONDecodeError as e:
        response.failure("Invalid json returned: "+response.text+" "+str(e))

  def on_start(self):
    # Randomly select values
    self.stake_account = random.choice(stake_accounts)
    self.wallet = random.choice(wallets)
    self.wallets = random.sample(wallets,2)
    self.confirmed_sigs = random.choice(confirmed_signature_address)
    self.token_owner = random.choice(token_owners)
    self.token_account = random.choice(token_accounts)
    self.program_key = random.choice(program_keys)
    self.transaction_signature = random.choice(transaction_signatures)
    self.mint = random.choice(mints)
   
    # Get minimum stored ledger slot
    with self.client.post('/', data=self.get_req_json("minimumLedgerSlot"),  headers={'content-type': 'application/json'}, catch_response=True, name="setupBlocks") as response:
      json_data = response.json()
      if "error" in json_data:
        print(json_data["error"])
        raise StopUser()
      self.minimum_slot = json_data["result"]

    # Fetch the epoch info to find slots/blocks for RCPcalls
    with self.client.post('/', data=self.get_req_json("getEpochInfo"),  headers={'content-type': 'application/json'}, catch_response=True, name="setupBlocks") as response:
      try:
        json_data = response.json()
        if "error" in json_data:
          print(json_data["error"])
          raise StopUser()
          
        # Get epoch info 
        absolute_slot = json_data["result"]["absoluteSlot"]
        slot_index = json_data["result"]["slotIndex"]
        block_height = json_data["result"]["blockHeight"]
        first_slot = absolute_slot - slot_index + 1
        if self.minimum_slot > first_slot:
          first_slot = self.minimum_slot

        #  Find a random valid block
        for i in range(100):
          self.block = random.randint(first_slot, absolute_slot-1)
          with self.client.post('/', data=self.get_req_json("getConfirmedBlock", [self.block]),  headers={'content-type': 'application/json'}, catch_response=True, name="setupBlocks") as response:
            try: 
              conf_block = response.json()
              if "result" in conf_block and not "error" in conf_block:
                break # wait until we find a valid block not slipped slot
              elif(i == 99): # couldn't find a valid block 
                raise StopUser()
            except json.decoder.JSONDecodeError as e:
              print(response.text)
              raise StopUser()

        # Pick a random block/slot range
        self.start_block = random.randint(first_slot, absolute_slot-1)
        self.end_block = random.randint(self.start_block+1, absolute_slot)
        if self.end_block < self.start_block:
          self.start_block = self.end_block-random.randint(0,10)    
      except json.decoder.JSONDecodeError as e:
        print(response.text)
        raise StopUser()

# A solana explorer type user
class ExplorerUser(SolanaUser):
  weight = 1

  @task
  def get_slot(self):
    self.rpc("getSlot")

  @task
  def get_slot_leader(self):
    self.rpc("getSlotLeader")

  @task
  def get_leader_schedule(self):
    self.rpc("getLeaderSchedule")

  @task
  def get_cluster_nodes(self):
    self.rpc("getClusterNodes")

  @task
  def get_epoch_schedule(self):
    self.rpc("getEpochSchedule")

  @task
  def get_largest_accounts(self):
    self.rpc("getLargestAccounts")

  @task
  def get_epoch_info(self):
    self.rpc("getEpochInfo")

  @task
  def minimum_ledger_slot(self):
    self.rpc("minimumLedgerSlot")


  # This triggers big table lookup
  @task
  def get_confirmed_blocks(self):
    self.rpc("getConfirmedBlocks", [5, 10])


# A generic traffic simulator user
class TrafficSimulatorUser(SolanaUser):
  weight = 10

  @task(52)
  def get_account_info(self):
    self.rpc("getAccountInfo", [self.wallet, {"encoding": "base58"}])

  @task(22)
  def get_token_accounts_by_owner(self):
    self.rpc("getTokenAccountsByOwner", [ self.token_owner, {"mint":self.mint}, {"encoding":"base64"} ])

  @task(13)
  def get_balance(self):
    self.rpc("getBalance", [self.wallet])

  @task(8)    
  def get_confirmed_block(self):
    self.rpc("getConfirmedBlock", [ self.block ])

  @task(2)
  def get_epoch_info(self):
    self.rpc("getEpochInfo")

  @task(1)
  def get_confirmed_blocks(self):
    self.rpc("getConfirmedBlocks", [self.start_block, self.end_block])

  @task(1)
  def get_minimum_balance_for_rent_exemption(self):
    self.rpc("getMinimumBalanceForRentExemption", [50])
  
  @task(1)
  def get_recent_block_hash(self):
    self.rpc("getRecentBlockhash")

  @task(1)
  def get_confirmed_signatures_for_address2(self):
    self.rpc("getConfirmedSignaturesForAddress2", [self.confirmed_sigs, { "limit": 100 }])

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
    self.rpc("getMultipleAccounts", [ self.wallets, {"dataSlice":{"offset":0,"length":0}} ])

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

