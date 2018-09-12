import iota
from iota import TryteString

class IOTATransaction:
    def __init__(self, _MySeed):
        self.MySeed = str.encode(_MySeed)
        self.FinalBundle = "INIT"
        self.TransactionHashList = list()
        #self.api = iota.Iota("https://field.deviota.com:443")
        self.api = iota.Iota("http://140.116.247.117:14265")
    def MakePreparingTransaction(self, TargetAddress, StringMessage, tag='KEVIN999IS999HANDSOME'):
        TargetAddress = str.encode(TargetAddress)
        pt = iota.ProposedTransaction(address = iota.Address(TargetAddress),message = iota.TryteString.from_unicode(StringMessage),tag = iota.Tag(str.encode(tag)),value=0)
        return pt
    def SendTransaction(self, PTList, dep=3, mwm=14):
        FinalBundle = self.api.send_transfer(depth=dep,transfers=PTList,min_weight_magnitude=mwm)['bundle']
        self.FinalBundle = FinalBundle
        for txn in FinalBundle:
            Vtxn = vars(txn)
            if Vtxn['hash'] not in self.TransactionHashList:
                self.TransactionHashList.append(Vtxn['hash'])
        
    def GetTransactionFinalBundleHash(self):
        return self.FinalBundle.hash
    def GetTransactionFinalBundle(self):
        return self.FinalBundle
    def GetTransactionHash(self):
        return self.TransactionHashList
    def GetTransactionMessage(self, TID):
        bundle = self.api.get_bundles(TID)
        for x in bundle['bundles']:
            for txn in x:
                Vtxn = vars(txn)
                if Vtxn['hash'] != TID:
                    continue
                TryteStringMessage = str(Vtxn['signature_message_fragment'])
                return TryteString(str.encode(TryteStringMessage)).decode()
