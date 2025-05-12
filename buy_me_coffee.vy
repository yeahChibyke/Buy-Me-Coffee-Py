# pragma version ^0.4.0
# @license MIT

interface AggregatorV3Interface:
    def decimals() -> uint8: view 
    def description() -> String[100]: view 
    def version() -> uint256: view 
    def latestAnswer() -> int256: view

owner: address
minimum_usd: uint256
price_feed: AggregatorV3Interface
buyers: public(DynArray[address, 100]) #limited to 100 buyers
totalBuyers: uint256

@deploy
def __init__(address_to_use: address):
    self.owner = msg.sender
    self.minimum_usd = as_wei_value(5, "ether")
    self.price_feed = AggregatorV3Interface(address_to_use)

@external 
@payable
def buy_coffee():
    usd_value_of_eth: uint256 = self._get_eth_to_usd_rate(msg.value)
    assert usd_value_of_eth >= self.minimum_usd
    self.buyers.append(msg.sender)
    self.totalBuyers = self.totalBuyers + 1

@external 
def withdraw():
    assert msg.sender == self.owner
    send(msg.sender, self.balance)
    self.buyers = [] # reset buyers array after every withdrawal
    self.totalBuyers = 0

@internal 
def _get_eth_to_usd_rate(eth_amount: uint256) -> uint256:
    price: int256 = staticcall self.price_feed.latestAnswer()
    eth_price: uint256 = convert(price, uint256) * (10 ** 10)
    eth_amount_in_usd: uint256 = (eth_amount * eth_price) // (1 * (10 ** 18))
    return eth_amount_in_usd

@external 
@view 
def getTotalBuyers() -> uint256: 
    return self.totalBuyers

