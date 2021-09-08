from enum import Enum


#Mali podprogram koi ce mi vracati koji je statiu prijatelja
class FriendRequestStatus(Enum):
	NO_REQUEST_SENT = -1
	THEM_SENT_TO_YOU = 0
	YOU_SENT_TO_THEM = 1

	'''
		-1 => nema requesta
		 0 => oni su poslali meni
		 1 => ja poslao njima
	'''