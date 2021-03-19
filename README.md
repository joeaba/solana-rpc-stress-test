# solana-rpc-stress-test

To run:

1. Install virtualenv through `easy_install virtualenv` or through `pip install virtualenv`
2. Create virtualenv `virtualenv ~/ansible2.8`
3. Activate virtualenv `source ~/ansible2.8/bin/activate`
4. Install ansible and locust `pip install -r requirements.txt`
2. `locust -f locust.py`
3. visit http://localhost:8089
4. enter endpoint e.g. http://sg1.solrpc.com:8080

## Launching worker nodes

Before launching worker nodes, make sure you have a master node ready to run (start with `locust -f locust.py --master`). It should have a public IP accessible.

To launch worker nodes you need a digital ocean API token - https://cloud.digitalocean.com/account/api/tokens

Then specify the environment variable `DO_API_TOKEN`,  e.g. `export DO_API_TOKEN=<token>`

Verify settings for your launch in `vars.yml`

Then run the launch command `ansible-playbook launch-workers.yml`

## Terminating worker nodes

When you are done running the test, run the command: `ansible-playbook terminate-workers.yml`

## Status of worker nodes

Run ./status.sh to get the systemctl status locust on all worker nodes.

## Restart locust on workers

Run ./restart-workers.sh to restart all worker nodes.
