from iota import Address, ProposedBundle, ProposedTransaction
from iota.crypto.signing import KeyGenerator
import iota
import pearldiver
import json
import requests
from iota import Iota
from iota import TryteString
headers = {'X-IOTA-API-Version': '1'}
getTips = {"command": "getTips"}
def call_iota_api(f):
    r = requests.post("http://140.116.247.117:14265", data=json.dumps(f), headers=headers)
    return r.text


SEED = 'BXOM9LUNLPSEXBRJV9UUNLHSUHABEOGHQOGNBNBUEYSGOFZOEPYKEYRSFTXBOEJLUODUQXXGQ9NWQBSGH'
api = Iota('http://140.116.247.117:14265', b'BXOM9LUNLPSEXBRJV9UUNLHSUHABEOGHQOGNBNBUEYSGOFZOEPYKEYRSFTXBOEJLUODUQXXGQ9NWQBSGH')
gna_result = api.get_new_addresses(count=2)

bundle = ProposedBundle()

tag = iota.Tag('TESTINGPYTHON')
pt = iota.ProposedTransaction(
    address=iota.Address('9TPHVCFLAZTZSDUWFBLCJOZICJKKPVDMAASWJZNFFBKRDDTEOUJHR9JVGTJNI9IYNVISZVXARWJFKUZWC'),
    value=0,
    tag=tag,
    message=iota.TryteString('HELLO')
)

bundle.add_transaction(pt)

addy = gna_result["addresses"][0]
addy.balance = 0
addy.key_index = 0
bundle.add_inputs([
    addy
])

bundle.send_unspent_inputs_to(
    gna_result["addresses"][0]
)

bundle.finalize()
bundle.sign_inputs(KeyGenerator(b'BXOM9LUNLPSEXBRJV9UUNLHSUHABEOGHQOGNBNBUEYSGOFZOEPYKEYRSFTXBOEJLUODUQXXGQ9NWQBSGH'))

tips = json.loads(call_iota_api(getTips))
print("llsdldld")
for x in tips['hashes']:
    getTransactionsToApprove = {"command": "getTransactionsToApprove", "depth": 15, "reference": x}
    result = json.loads(call_iota_api(getTransactionsToApprove))
    if "exception" in result:
        print(result)
        continue
    elif "error" in result:
        print(result)
        continue
    else:
        print(result)
        trunk_hash = result['trunkTransaction']
        branch_hash = result['branchTransaction']
        break
#prev_tx = None
trytes = bundle.as_tryte_strings()
Tlist = list()
for x in trytes:
    Tlist.append(str(x))
attachToTangle = {"command": "attachToTangle", "trunkTransaction": trunk_hash, "branchTransaction": branch_hash, "minWeightMagnitude": 18, "trytes": Tlist}
#print(json.dumps(attachToTangle))
output = call_iota_api(attachToTangle)
fw = open('output.json','w')
fw.write(json.dumps(output))
fw.close()
