from wit import Wit
import logging

#Hakktathon app's token
WIT_TOKEN = 'DWWL45QV2WPIT4AOPX6VVXWNEFGGFDDI'

#initialise the wit client
def init_wit():

    wc = Wit(WIT_TOKEN)
    assert wc != None
    print(wc)
    wc.logger.setLevel(logging.WARNING)
    return wc

