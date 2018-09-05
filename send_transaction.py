import iota
from datetime import datetime
from pprint import pprint

MySeed = b"HGW9HB9LJPYUGVHNGCPLFKKPNZAIIFHZBDHKSGMQKFMANUBASSMSV9TAJSSMPRZZU9SFZULXKJ9YLAIUA"
TargetAddress1 = b"BXOM9LUNLPSEXBRJV9UUNLHSUHABEOGHQOGNBNBUEYSGOFZOEPYKEYRSFTXBOEJLUODUQXXGQ9NWQBSGH"
TargetAddress2 = b"CYJV9DRIE9NCQJYLOYOJOGKQGOOELTWXVWUYGQSWCNODHJAHACADUAAHQ9ODUICCESOIVZABA9LTMM9RW"

NowIs = datetime.now() # get a actual date & time - just to have some meaningfull info

# preparing transactions
pt = iota.ProposedTransaction(address = iota.Address(TargetAddress1), # 81 trytes long address
                              message = iota.TryteString.from_unicode('Here comes a first message. Now is %s' % (NowIs)),
                              tag     = iota.Tag(b'HRIBEK999IOTA999TUTORIAL'), # Up to 27 trytes
                              value   = 0)

pt2 = iota.ProposedTransaction(address = iota.Address(TargetAddress2), # 81 trytes long address
                               message = iota.TryteString.from_unicode('Here comes a second message. Now is %s' % (NowIs)),
                               tag     = iota.Tag(b'HRIBEK999IOTA999TUTORIAL'), # Up to 27 trytes
                               value   = 0)
#besides the given attributes, library also adds a transaction timestamp


api = iota.Iota("https://field.deviota.com:443")

print("Preparing/Broadcasting... Wait please...")
# the whole process initiated in a single call
FinalBundle = api.send_transfer(depth=3,
                                transfers=[pt,pt2],
                                min_weight_magnitude=14)['bundle'] # it returns a dictionary with a bundle object
    
#bundle is broadcasted, let's print it
print("\nGenerated bundle hash: %s" % (FinalBundle.hash))
print("\nTail Transaction in the Bundle is a transaction #%s." % (FinalBundle.tail_transaction.current_index))
        
print("\nList of all transactions in the bundle:\n")
for txn in FinalBundle:
    pprint(vars(txn))
    print("")
